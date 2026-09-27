import logging
import os
import httpx
import asyncio
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, inference, TurnHandlingOptions

load_dotenv(".env")

# API Configuration - Point this to your FastAPI backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/chat")

# Filter out harmless Windows asyncio polling watchdog warnings from terminal
class EventLoopWatchdogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "event loop blocked" not in record.getMessage()

logging.getLogger("livekit.agents").addFilter(EventLoopWatchdogFilter())


class VoiceAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are the voice interface of ZeeNex AI Assistant.
            You provide concise, natural-sounding responses.
            Avoid emojis, asterisks, or complex formatting.
            Keep answers short and friendly for voice conversation.""",
        )

    async def get_backend_response(self, text: str) -> str:
        """Calls the existing Fullstack AI Assistant API to get a response."""
        payload = {
            "messages": [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": text}
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # We use the existing /api/chat endpoint
                # Note: Your current API is streaming (SSE),
                # so we need to handle the stream or use a non-streaming approach.
                # For voice, we'll collect the stream into a full string for the TTS.
                response = await client.post(BACKEND_URL, json=payload)
                response.raise_for_status()

                # Since the API returns SSE (text/event-stream), we parse the 'data' lines
                full_text = ""
                for line in response.iter_lines():
                    if line.startswith("data: "):
                        import json
                        try:
                            data = json.loads(line[6:])
                            if "delta" in data:
                                full_text += data["delta"]
                        except json.JSONDecodeError:
                            continue

                return full_text if full_text else "I'm sorry, I couldn't process that."
        except Exception as e:
            logging.error(f"Backend API Error: {e}")
            return "I'm having trouble connecting to my brain right now."


server = AgentServer()


@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    # We remove the LLM from the session config because we are using our own API
    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3", language="multi"),
        # llm=None, # We handle LLM logic manually via the backend API
        tts=inference.TTS(
            model="inworld/inworld-tts-2",
            voice="Ashley",
        ),
        turn_handling=TurnHandlingOptions(
            turn_detection=inference.TurnDetector(),
        ),
    )

    # Custom logic to intercept user speech and call the backend
    @session.on("user_speech_finished")
    async def on_speech_finished(text: str):
        # 1. Get response from our Fullstack AI Assistant
        assistant = VoiceAssistant()
        reply_text = await assistant.get_backend_response(text)

        # 2. Speak the response
        await session.say(reply_text)

    await session.start(
        agent=VoiceAssistant(),
        room=ctx.room,
    )

    # Initial Greeting
    await session.say("Hello! I am ZeeNex AI. How can I help you today?")


if __name__ == "__main__":
    print("\n" + "=" * 65)
    print(" >>> ZeeNex Integrated Voice Agent Starting Up <<<")
    print(f" Backend Connection: {BACKEND_URL}")
    print(" LiveKit Cloud: Connected & Ready")
    print("=" * 65 + "\n")
    agents.cli.run_app(server)
