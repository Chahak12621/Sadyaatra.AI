import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

@patch("routers.groups.create_trip_group")
@patch("routers.groups.add_group_member")
def test_create_group(mock_add_member, mock_create_group):
    mock_create_group.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174002",
        "name": "Goa Trip 2026",
        "created_by": "123e4567-e89b-12d3-a456-426614174000",
        "destination": "Goa"
    }
    
    payload = {
        "name": "Goa Trip 2026",
        "created_by": "123e4567-e89b-12d3-a456-426614174000",
        "destination": "Goa"
    }
    
    response = client.post("/api/groups/", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Goa Trip 2026"
    mock_create_group.assert_called_once()
    mock_add_member.assert_called_once()

@patch("routers.groups.add_group_member")
def test_add_group_member(mock_add_member):
    mock_add_member.return_value = {
        "group_id": "123e4567-e89b-12d3-a456-426614174002",
        "user_id": "123e4567-e89b-12d3-a456-426614174003",
        "role": "member"
    }
    
    payload = {
        "user_id": "123e4567-e89b-12d3-a456-426614174003",
        "role": "member"
    }
    
    response = client.post("/api/groups/123e4567-e89b-12d3-a456-426614174002/members", json=payload)
    assert response.status_code == 200
    assert response.json()["user_id"] == "123e4567-e89b-12d3-a456-426614174003"
    mock_add_member.assert_called_once()

@patch("routers.groups.get_group_profiles")
def test_get_group_members(mock_get_profiles):
    mock_get_profiles.return_value = [
        {"id": "123e4567-e89b-12d3-a456-426614174003", "full_name": "Test User"}
    ]
    
    response = client.get("/api/groups/123e4567-e89b-12d3-a456-426614174002/members")
    assert response.status_code == 200
    assert len(response.json()) == 1
    mock_get_profiles.assert_called_once()
