"""
Tests for chat functionality
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.chat import ChatRequest

client = TestClient(app)

@pytest.fixture
def auth_token():
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/auth/token", data=login_data)
    return response.json()["access_token"]

def test_send_message(auth_token):
    chat_request = {
        "message": "Hello, how are you?",
        "user_id": "test_user_id"
    }
    response = client.post(
        "/api/chat/message",
        json=chat_request,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "relevant_documents" in data

def test_get_chat_history(auth_token):
    response = client.get(
        "/api/chat/history?user_id=test_user_id&limit=10",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 