from fastapi import APIRouter
from uuid import uuid4
from app.core.event_bus import publish

router = APIRouter(prefix="/chat")

@router.post("/send")
async def send_message(content: str, conversation_id: str | None = None):
    event = {
        "conversation_id": conversation_id or str(uuid4()),
        "message_id": str(uuid4()),
        "sender": "user",
        "content": content
    }
    await publish(event)
    return {"status": "sent", "conversation_id": event["conversation_id"]}
