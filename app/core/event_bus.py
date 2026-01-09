import json
import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

INCOMING_STREAM = "chat:incoming"
OUTGOING_STREAM = "chat:outgoing"


def publish(channel: str, message: dict):
    print('New Publishing event msg to redis:', message)
    redis_client.publish(channel, json.dumps({"data": json.dumps(message)}))


def new_subscribe(channel: str):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    return pubsub


def save_message(session_id: str, message: dict):
    key = f"chat:history:{session_id}"
    redis_client.rpush(key, json.dumps(message))

def get_history(session_id: str):
    key = f"chat:history:{session_id}"
    messages = redis_client.lrange(key, 0, -1)
    return [json.loads(m) for m in messages]
