from fastapi.testclient import TestClient
from event_platform.api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_publish_event():
    response = client.post("/v1/events", json={
        "event_id": "evt-test-1",
        "key": "customer-1",
        "event_type": "order.created",
        "payload": {"order_id": "o-1"},
    })
    assert response.status_code == 202
    assert response.json()["accepted"] is True
