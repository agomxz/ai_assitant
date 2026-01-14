import json
from unittest.mock import patch, MagicMock

from app.core.event_bus import publish, subscribe, save_message, get_history


@patch("app.core.event_bus.redis_client")
def test_publish(mock_redis_client):
    channel = "test-channel"
    message = {"content": "hello"}

    publish(channel, message)

    mock_redis_client.publish.assert_called_once_with(
        channel,
        json.dumps({"data": json.dumps(message)})
    )


@patch("app.core.event_bus.redis_client")
def test_subscribe(mock_redis_client):
    mock_pubsub = MagicMock()
    mock_redis_client.pubsub.return_value = mock_pubsub

    channel = "test-channel"

    pubsub = subscribe(channel)

    mock_redis_client.pubsub.assert_called_once()
    mock_pubsub.subscribe.assert_called_once_with(channel)
    assert pubsub == mock_pubsub



@patch("app.core.event_bus.redis_client")
def test_save_message(mock_redis_client):
    session_id = "session-123"
    message = {"content": "hello"}

    save_message(session_id, message)

    mock_redis_client.rpush.assert_called_once_with(
        "chat:history:session-123",
        json.dumps(message)
    )


@patch("app.core.event_bus.redis_client")
def test_get_history(mock_redis_client):
    session_id = "session-123"

    mock_redis_client.lrange.return_value = [
        json.dumps({"content": "hello"}),
        json.dumps({"content": "world"}),
    ]

    result = get_history(session_id)

    mock_redis_client.lrange.assert_called_once_with(
        "chat:history:session-123",
        0,
        -1
    )

    assert result == [
        {"content": "hello"},
        {"content": "world"},
    ]
