import json
import asyncio
from fastapi import APIRouter, WebSocket
from app.core.event_bus import new_subscribe

router = APIRouter()

@router.websocket("/ws/{session_id}")
async def chat_ws(websocket: WebSocket, session_id: str):
    await websocket.accept()

    pubsub = new_subscribe("chat:ai_out")

    try:
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                data = json.loads(message["data"])

                # Only send messages for this session
                if data["session_id"] == session_id:
                    await websocket.send_json(data)

            await asyncio.sleep(0.01)
    except Exception:
        pass
    finally:
        pubsub.close()
