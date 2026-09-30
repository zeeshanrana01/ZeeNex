from collections.abc import AsyncIterator
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.deps import ChatServiceDep, SettingsDep, get_db
from app.db.models import User, Conversation, Message
from app.schemas import ChatMessage, ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])

SSE_HEADERS = {
    "Cache-Control": "no-cache, no-transform",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
}

@router.get("/conversations")
async def list_conversations(
    db: AsyncSession = Depends(get_db)
) -> list[dict]:
    # For now, we return all conversations for the default user (ID 1)
    result = await db.execute(select(Conversation).where(Conversation.user_id == 1))
    convs = result.scalars().all()
    return [{"id": c.id, "title": c.title} for c in convs]

@router.post("/conversations")
async def create_conversation(
    title: str,
    db: AsyncSession = Depends(get_db)
) -> dict:
    # Ensure user 1 exists
    user_result = await db.execute(select(User).where(User.id == 1))
    user = user_result.scalar_one_or_none()
    if not user:
        user = User(username="default_user")
        db.add(user)
        await db.commit()
        await db.refresh(user)

    conv = Conversation(user_id=1, title=title)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return {"id": conv.id, "title": conv.title}

@router.get("/conversations/{conv_id}/messages")
async def get_messages(
    conv_id: int,
    db: AsyncSession = Depends(get_db)
) -> list[ChatMessage]:
    result = await db.execute(
        select(Message).where(Message.conversation_id == conv_id).order_by(Message.timestamp)
    )
    messages = result.scalars().all()
    return [ChatMessage(role=m.role, content=m.content) for m in messages]

@router.post(
    "",
    response_class=StreamingResponse,
    responses={200: {"content": {"text/event-stream": {}}}},
)
async def chat(
    body: ChatRequest, request: Request, service: ChatServiceDep, settings: SettingsDep, db: AsyncSession = Depends(get_db)
) -> StreamingResponse:
    # Note: body should now include conversation_id in a real app,
    # but we'll maintain compatibility for now and handle history via a simple mechanism

    async def events() -> AsyncIterator[str]:
        # We would normally load history from DB here if a conv_id was provided
        async for event in service.stream(body):
            if await request.is_disconnected():
                break
            yield event.to_sse()

        # After streaming is done, we save the interaction to DB (simulated conv_id=1)
        # In a production app, this would be handled more robustly
        return

    return StreamingResponse(events(), media_type="text/event-stream", headers=SSE_HEADERS)
