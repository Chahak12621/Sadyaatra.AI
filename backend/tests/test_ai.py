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

@patch("core.embedding_client.generate_embedding")
@patch("core.supabase_client.search_knowledge_base")
@patch("main.chat_with_agent")
def test_chat_endpoint(mock_chat, mock_search, mock_embedding):
    mock_embedding.return_value = [0.1, 0.2, 0.3]
    mock_search.return_value = [{"title": "Test", "content": "Fact"}]
    mock_chat.return_value = "Hello! I am Sadyaatra."
    
    payload = {
        "messages": [{"role": "user", "content": "Hi"}],
        "current_context": "Testing"
    }
    
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    mock_chat.assert_called_once()
    mock_search.assert_called_once()

@patch("main.generate_itinerary")
@patch("main.save_itinerary")
def test_generate_itinerary(mock_save, mock_generate):
    mock_generate.return_value = {
        "destination": "Paris",
        "total_estimated_cost": 1500.0,
        "days": [],
        "ai_notes": "Have fun!"
    }
    
    payload = {
        "destination": "Paris",
        "duration_days": 3,
        "budget_level": "moderate",
        "user_id": "123e4567-e89b-12d3-a456-426614174000"
    }
    
    response = client.post("/api/itinerary", json=payload)
    assert response.status_code == 200
    mock_generate.assert_called_once()
    mock_save.assert_called_once()
