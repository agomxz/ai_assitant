from fastapi import APIRouter, HTTPException, status
from uuid import uuid4
from app.core.event_bus import publish, save_message
from app.logger import setup_logger
from app.config import settings
from app.schemas.messages import SendMessageResponse, ErrorResponse

router = APIRouter(prefix="/chat", tags=["chat"])
logger = setup_logger(__name__)


@router.post(
    "/send",
    response_model=SendMessageResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Message published successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def send_message(content: str, session_id: str | None = None):
    """
    Publish message to the Redis stream.
    """

    if not content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty",
        )

    try:
        resolved_session_id = session_id or str(uuid4())
        message_id = str(uuid4())

        event = {
            "session_id": resolved_session_id,
            "message_id": message_id,
            "sender": "user",
            "content": content,
        }

        logger.info(
            "Publishing message",
            extra={
                "session_id": resolved_session_id,
                "message_id": message_id,
            },
        )

        publish(settings.incoming_stream, event)
        save_message(resolved_session_id, event)

        return {
            "status": "published",
            "session_id": resolved_session_id,
            "message_id": message_id,
        }

    except ConnectionError:
        logger.exception("Redis connection error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Redis is unavailable",
        )

    except Exception:
        logger.exception("Unexpected error while publishing message")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish message",
        )
