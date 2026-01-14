import json
import asyncio
from fastapi import APIRouter, WebSocket
from app.core.event_bus import subscribe, save_message
from app.logger import setup_logger
from app.config import settings
from app.services.ai_service import generate_response

logger = setup_logger(__name__)

router = APIRouter()


@router.websocket("/ws/{session_id}")
async def chat_ws(websocket: WebSocket, session_id: str) -> None:
    """
    This endpoint is to consume messages from redis
    in order to push them to the client
    """
    try:
        logger.info(f"WebSocket connected for session_id [{session_id}]")
        await websocket.accept()
        pubsub = subscribe(settings.outgoing_stream)
        await websocket.send_json({"status": "connected"})

        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)

            if message:

                data_response = json.loads(message["data"])
                data_response = json.loads(data_response["data"])

                data = json.loads(data_response["data"])

                logger.info(f"Message session_id [{session_id}]: {data}")

                if data["session_id"] == session_id:

                    response = await generate_response(
                        data["session_id"], data["content"]
                    )

                    assistant_response = {
                        "session_id": session_id,
                        "sender": "assistant",
                        "content": response,
                    }

                    save_message(session_id, assistant_response)
                    await websocket.send_json({"content": response})
                    logger.info("Sended response ok")

            await asyncio.sleep(0.01)

    except Exception as e:
        logger.error("WebSocket connection closed", e)
    finally:
        pubsub.close()
