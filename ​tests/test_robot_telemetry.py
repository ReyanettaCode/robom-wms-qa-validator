import pytest
from fastapi.testclient import TestClient
from src.mock_wms_api import app

client = TestClient(app)

def test_dispatch_robot_success():
    
    payload = {
        "task_id": "TSK-AMR-901",
        "robot_id": "AMR-Unit-01",
        "target_location": "Zone-A-Rack-5",
        "action": "pick"
    }
    response = client.post("/api/v1/robot/task", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "dispatched"
    assert data["assigned_task"]["task_id"] == "TSK-AMR-901"
    assert data["assigned_task"]["action"] == "pick"

def test_dispatch_robot_missing_fields():
    
    invalid_payload = {
        "task_id": "",
        "robot_id": "",
        "target_location": "Zone-B",
        "action": "place"
    }
    response = client.post("/api/v1/robot/task", json=invalid_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid telemetry payload"

def test_robot_action_types():
    
    actions = ["pick", "place", "charge"]
    for idx, act in enumerate(actions):
        payload = {
            "task_id": f"TSK-TEST-00{idx}",
            "robot_id": "AMR-Unit-02",
            "target_location": "Charging-Bay-1",
            "action": act
        }
        response = client.post("/api/v1/robot/task", json=payload)
        assert response.status_code == 201
        assert response.json()["assigned_task"]["action"] == act
