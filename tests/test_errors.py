from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_not_found():
    response = client.get("/invalid-endpoint")
    json_response = response.json()  

    assert response.status_code == 404
    assert json_response == {
        "error": "El endpoint al que intentas acceder no existe.",
        "status_code": 404,
        "timestamp": json_response["timestamp"],  
        "path": json_response["path"] 
    }
        