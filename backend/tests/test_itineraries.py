import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

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
    
    response = client.get("/api/itineraries/user/user_123")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["destination"] == "Goa"
    mock_get_itineraries.assert_called_once()
