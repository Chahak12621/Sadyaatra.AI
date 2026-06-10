import pytest
import json
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

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Sadyaatra API is running!"}
