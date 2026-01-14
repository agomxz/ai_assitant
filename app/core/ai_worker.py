import json
from app.core.event_bus import (
    subscribe,
    publish,
)
from app.logger import setup_logger
from app.config import settings

logger = setup_logger(__name__)


def start_ai_worker():

    logger.info("AI Worker starting....")
    pubsub = subscribe(settings.incoming_stream)
    logger.info("Connected to Redis Stream")

    for event in pubsub.listen():
        if event["type"] != "message":
            continue

        data = json.loads(event["data"])

        publish(settings.outgoing_stream, data)
