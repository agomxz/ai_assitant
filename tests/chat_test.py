from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_send_message_success():
    """
    Test successful message publishing
    """

    payload = {"content": "Hello world", "session_id": "test-session-123"}
    response = client.post("/chat/send", params=payload)
    assert response.status_code == 201


def test_websocket_connect_success():
    """
    Test connection with websocket
    """
    session_id = "test-session-123"

    with client.websocket_connect(f"/ws/{session_id}") as websocket:
        assert websocket is not None