from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict():
    payload = {
        "sleep_hours": 6.5,
        "stress_level": 7,
        "time_of_day": 9,
        "workload_level": 8
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "recommended_strength" in response.json()