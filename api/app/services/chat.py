import json
import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any

from app.providers.base import ProviderError
from app.providers.registry import ProviderRegistry
from app.schemas import ChatMessage, ChatRequest
from app.services.skills import registry as skill_registry

logger = logging.getLogger(__name__)

@dataclass
class ChatEvent:
    type: str  # "meta" | "delta" | "error" | "tool_call" | "tool_result" | "done"
    data: dict[str, Any] = field(default_factory=dict)

    def to_sse(self) -> str:
        payload = json.dumps(self.data, ensure_ascii=False)
        if self.type == "delta":
            return f"data: {payload}\n\n"
        return f"event: {self.type}\ndata: {payload}\n\n"

NO_MODELS_MESSAGE = (
    "No AI model is available. Install a local model with `ollama pull llama3.2`, "
    "or add a cloud API key (Anthropic, OpenAI, Gemini, Grok or Meta) to the API's .env file."
)

class ChatService:
    def __init__(self, registry: ProviderRegistry, system_prompt: str, allow_fallback: bool):
        self._registry = registry
        self._system_prompt = system_prompt
        self._allow_fallback = allow_fallback

    def _with_system(self, messages: list[ChatMessage]) -> list[ChatMessage]:
        if not self._system_prompt or any(m.role == "system" for m in messages):
            return messages
        return [ChatMessage(role="system", content=self._system_prompt), *messages]

    async def stream(self, request: ChatRequest) -> AsyncIterator[ChatEvent]:
        try:
            candidates = await self._registry.candidates(
                request.provider, request.model, self._allow_fallback
            )
        except ProviderError as exc:
            yield ChatEvent("error", {"message": str(exc)})
            return

        if not candidates:
            yield ChatEvent("error", {"message": NO_MODELS_MESSAGE})
            return

        messages = self._with_system(request.messages)
        failures: list[str] = []

        for candidate in candidates:
            provider, model = candidate.provider, candidate.model
            started = False

            # Tool loop state
            iterations = 0
            max_iterations = 10

            while iterations < max_iterations:
                iterations += 1
                current_turn_started = False

                try:
                    # 1. Stream the chat completion
                    async for delta in provider.stream_chat(model, messages, request.temperature):
                        if not started:
                            started = True
                            yield ChatEvent(
                                "meta",
                                {
                                    "provider": provider.id,
                                    "provider_label": provider.label,
                                    "model": model,
                                    "local": provider.local,
                                    "fallback": bool(failures),
                                    "notice": "; ".join(failures) or None,
                                },
                            )

                        if isinstance(delta, dict) and delta.get("type") == "tool_call":
                            # Found a tool call!
                            tool_name = delta["name"]
                            tool_args = delta["arguments"]

                            yield ChatEvent("tool_call", {"name": tool_name, "args": tool_args})

                            # Execute the skill
                            result = skill_registry.execute(tool_name, tool_args)

                            yield ChatEvent("tool_result", {"name": tool_name, "result": result})

                            # Add the assistant's tool call and the tool's result to history for the next turn
                            messages.append(ChatMessage(role="assistant", content=f"Call tool {tool_name} with {tool_args}"))
                            messages.append(ChatMessage(role="tool", content=result))

                            # Break the inner stream to restart the loop with new history
                            current_turn_started = True
                            # We must break the async generator to stop the current provider.stream_chat call
                            # But the loop will continue
                            break
                        else:
                            # Regular text delta
                            yield ChatEvent("delta", {"delta": delta})

                    # If we didn't break due to a tool call, the LLM is done for this turn.
                    if not current_turn_started:
                        break

                except ProviderError as exc:
                    logger.warning("Provider %s/%s failed: %s", provider.id, model, exc)
                    if started:
                        yield ChatEvent("error", {"message": str(exc)})
                        return
                    failures.append(str(exc))
                    self._registry.invalidate()
                    continue

            if not started:
                yield ChatEvent(
                    "meta",
                    {
                        "provider": provider.id,
                        "provider_label": provider.label,
                        "model": model,
                        "local": provider.local,
                        "fallback": bool(failures),
                        "notice": "; ".join(failures) or None,
                    },
                )
            yield ChatEvent("done", {})
            return

        yield ChatEvent("error", {"message": " · ".join(failures) or NO_MODELS_MESSAGE})
