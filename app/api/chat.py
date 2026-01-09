from fastapi import APIRouter
from uuid import uuid4
from app.core.event_bus import publish, save_message

router = APIRouter(prefix="/chat")

@router.post("/send")
def send_message(content: str, conversation_id: str | None = None):
    
    print("Sending message:", content)
    
    event = {
        "conversation_id": conversation_id or str(uuid4()),
        "session_id": conversation_id or str(uuid4()),
        "message_id": str(uuid4()),
        "sender": "user",
        "content": content,
    }

    publish("chat:incoming", event)
    save_message(event["session_id"], event)

    return {
        "status": "published",
        "conversation_id": event["conversation_id"],
    }