"""
Tests for authentication functionality
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import UserCreate

client = TestClient(app)

def test_register_user():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "hashed_password" not in data

def test_login_user():
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/auth/token", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user():
    # First login to get token
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    login_response = client.post("/api/auth/token", data=login_data)
    token = login_response.json()["access_token"]
    
    # Then try to get current user
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == login_data["username"] 