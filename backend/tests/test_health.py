# tests/test_health.py

from app.main import app
from fastapi.testclient import TestClient  # type: ignore

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"200": "OK"}  # Exact format match
