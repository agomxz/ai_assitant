from uuid import uuid4

async def generate_response(event):
    return {
        "conversation_id": event["conversation_id"],
        "message_id": str(uuid4()),
        "sender": "ai",
        "content": f"Mocked AI response to: {event['content']}"
    }
