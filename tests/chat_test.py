import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


@patch("app.api.chat.save_message")
@patch("app.api.chat.publish")
def test_send_message_success(mock_publish, mock_save_message):
    """
    Test successful message publishing
    """

    payload = {
        "content": "Hello world",
        "session_id": "test-session-123"
    }

    response = client.post("/chat/send", params=payload)

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "published"
    assert body["session_id"] == "test-session-123"

    # Ensure side effects were called
    mock_publish.assert_called_once()
    mock_save_message.assert_called_once()


@patch("app.api.chat.publish", side_effect=Exception("Redis down"))
def test_send_message_failure(mock_publish):
    """
    Test failure when publish raises an exception
    """

    payload = {
        "content": "Hello world"
    }

    response = client.post("/chat/send", params=payload)

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "failed"
    assert body["detail"] == "Failed to publish message to redis"
