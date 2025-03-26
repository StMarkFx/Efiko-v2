"""
Tests for document management functionality
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.document import DocumentSearch

client = TestClient(app)

@pytest.fixture
def auth_token():
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/auth/token", data=login_data)
    return response.json()["access_token"]

def test_upload_document(auth_token):
    # Create a test file
    test_file = ("test.txt", "This is a test document content", "text/plain")
    files = {"file": test_file}
    
    response = client.post(
        "/api/documents/upload",
        files=files,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "test.txt"
    assert data["content"] == "This is a test document content"

def test_get_user_documents(auth_token):
    response = client.get(
        "/api/documents/?user_id=test_user_id",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_search_documents(auth_token):
    search_request = {
        "query": "test document",
        "limit": 5,
        "threshold": 0.7
    }
    response = client.post(
        "/api/documents/search",
        json=search_request,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 