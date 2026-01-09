import json
from app.core.event_bus import (
    new_subscribe,
    publish,
)
from app.services.ai_service import generate_response


def start_ai_worker():

    print('AI WORKER STARTED')
    pubsub = new_subscribe("chat:incoming")

    print("AI worker started, listening for messages...")

    for event in pubsub.listen():
        if event["type"] != "message":
            continue

        data = json.loads(event["data"])

        print("Received from Redis:", data)
        publish("chat:ai_out", data)