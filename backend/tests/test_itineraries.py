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

@patch("routers.itineraries.get_user_itineraries")
def test_fetch_user_itineraries(mock_get_itineraries):
    mock_get_itineraries.return_value = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174003",
            "destination": "Goa",
            "start_date": "2026-10-01",
            "end_date": "2026-10-05",
            "itinerary_json": {}
        }
    ]
    
    response = client.get("/api/itineraries/user/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 200
    mock_get_itineraries.assert_called_once()
