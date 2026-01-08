import json
import time
from uuid import uuid4
from app.core.event_bus import (
    consume,
    new_subscribe,
    ack,
    publish_response
)
from app.services.ai_service import generate_response

GROUP = "ai-workers"
CONSUMER = "worker-1"

def start_ai_worker():

    print('AI WORKER STARTED')
    pubsub = new_subscribe("chat:incoming")

    print("🤖 AI worker started, listening for messages...")

    for event in pubsub.listen():
        if event["type"] != "message":
            continue

        data = json.loads(event["data"])

        print("📨 Received from Redis:", data)