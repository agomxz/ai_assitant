from fastapi import APIRouter
from uuid import uuid4
from app.core.event_bus import publish, save_message
from app.logger import setup_logger
from app.config import settings

router = APIRouter(prefix="/chat")

logger = setup_logger(__name__)

@router.post("/send")
def send_message(content: str, session_id: str | None = None):
    """
    This endpoint is to publish a message to the redis stream
    """
    try:
    
        logger.info(f"Sending endpoint session_id [{session_id}] and content [{content}]")
        
        event = {
            "session_id": session_id or str(uuid4()),
            "message_id": str(uuid4()),
            "sender": "user",
            "content": content,
        }

        publish(settings.incoming_stream, event)
        save_message(event["session_id"], event)

        return {
            "status": "published",
            "session_id": event["session_id"],
        }

    except Exception as e:
        logger.error("Failed to publish message:", e)
        return {
            "status": "failed",
            "detail": "Failed to publish message to redis",
        }