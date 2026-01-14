import json
import redis
from app.config import settings
from app.logger import setup_logger

logger = setup_logger(__name__)

redis_client = redis.Redis(
    host=settings.redis_host, port=settings.redis_port, decode_responses=True
)


def publish(channel: str, message: dict):
    """
    Method to create output message to websocket
    """
    logger.info("New message publishing to redis stream:")
    redis_client.publish(channel, json.dumps({"data": json.dumps(message)}))


def subscribe(channel: str):
    """
    Method to subscribe to incoming messages from redis
    """
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    return pubsub


def save_message(session_id: str, message: dict):
    "Store message in redis"
    key = f"chat:history:{session_id}"
    redis_client.rpush(key, json.dumps(message))


def get_history(session_id: str):
    """
    Method to get history from redis
    """
    key = f"chat:history:{session_id}"
    messages = redis_client.lrange(key, 0, -1)
    return [json.loads(m) for m in messages]
