import pytest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

class LoggingTestClient(TestClient):
    def request(self, method, url, **kwargs):
        print(f"\n[API TEST] {method} {url}")
        if "json" in kwargs:
            print(f"Payload: {json.dumps(kwargs['json'], indent=2)}")
        response = super().request(method, url, **kwargs)
        try:
            print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
        except Exception:
            pass
        print("-" * 50)
        return response

client = LoggingTestClient(app)

@patch("routers.agents.create_agent_profile")
def test_create_agent(mock_create_profile):
    mock_create_profile.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "email": "agent@example.com",
        "full_name": "Agent Smith",
        "role": "agent",
        "status": "pending_review"
    }
    
    payload = {
        "email": "agent@example.com",
        "password": "password123",
        "full_name": "Agent Smith",
        "phone": "1234567890",
        "dob": "1990-01-01",
        "gender": "Male",
        "address": "123 Street",
        "city": "City",
        "state": "State",
        "pincode": "123456",
        "vehicle_type": "SUV",
        "vehicle_number": "AB12CD3456",
        "vehicle_model": "Model",
        "vehicle_year": "2020",
        "vehicle_color": "White",
        "seating_capacity": "4",
        "aadhar_number": "123412341234",
        "pan_number": "ABCDE1234F",
        "licence_number": "DL123456",
        "licence_expiry": "2030-01-01",
        "aadhar_front_url": "url",
        "aadhar_back_url": "url",
        "licence_image_url": "url",
        "vehicle_rc_url": "url",
        "vehicle_insurance_url": "url",
        "profile_photo_url": "url"
    }
    
    response = client.post("/api/agents/", json=payload)
    assert response.status_code == 200
    mock_create_profile.assert_called_once()

@patch("routers.agents.get_agent_profile")
def test_get_agent(mock_get_profile):
    mock_get_profile.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "email": "agent@example.com",
        "full_name": "Agent Smith",
        "role": "agent",
        "status": "approved"
    }
    
    response = client.get("/api/agents/123e4567-e89b-12d3-a456-426614174001")
    assert response.status_code == 200
    mock_get_profile.assert_called_once()
