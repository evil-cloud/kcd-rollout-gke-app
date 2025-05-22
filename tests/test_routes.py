from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "gitops-api"
    }

def test_get_version():
    response = client.get("/api/v1/rollout/version")
    
    assert response.status_code == 200
    assert "version" in response.json()
    assert response.json()["version"] == "1.0.2"
