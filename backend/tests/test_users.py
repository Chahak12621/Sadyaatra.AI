import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

@patch("routers.users.create_user_profile")
def test_create_user(mock_create_profile):
    # Mock the return value of Supabase insertion
    mock_create_profile.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "test@example.com",
        "full_name": "John Doe",
        "role": "user",
        "onboarding_preferences": {}
    }
    
    payload = {
        "email": "test@example.com",
        "password": "securepassword123",
        "full_name": "John Doe"
    }
    
    response = client.post("/api/users/", json=payload)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    mock_create_profile.assert_called_once()

@patch("routers.users.get_user_profile")
def test_get_user(mock_get_profile):
    mock_get_profile.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "test@example.com",
        "full_name": "John Doe",
        "role": "user",
        "onboarding_preferences": {}
    }
    
    response = client.get("/api/users/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 200
    assert response.json()["full_name"] == "John Doe"
    mock_get_profile.assert_called_once()
