import asyncio
from app.core.event_bus import consume, publish_response
from app.services.ai_service import generate_response

def start_ai_worker():
    asyncio.create_task(run())

async def run():
    while True:
        event = await consume()
        response = await generate_response(event)
        await publish_response(response)
