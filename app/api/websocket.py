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
        print("WebSocket connected for session:", session_id)
        await websocket.send_json({"status": "connected"})

        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)

            if message:
                print("Received from Redis:", message)
                level1 = json.loads(message["data"])

                level2 = json.loads(level1["data"])

                data = json.loads(level2["data"])

                #data = json.loads(message["data"]["data"])

                # Only send messages for this session
                if data["session_id"] == session_id:
                    print("Sending to WebSocket:", data)
                    await websocket.send_json({"content": data['content']})

            await asyncio.sleep(0.01)

    except Exception:
        pass
    finally:
        pubsub.close()
