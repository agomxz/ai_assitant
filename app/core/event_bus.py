import asyncio

incoming_events = asyncio.Queue()
outgoing_events = asyncio.Queue()

async def publish(event):
    await incoming_events.put(event)

async def consume():
    return await incoming_events.get()

async def publish_response(event):
    await outgoing_events.put(event)
