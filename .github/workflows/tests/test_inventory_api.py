import pytest
from fastapi.testclient import TestClient
from src.mock_wms_api import app

client = TestClient(app)

def test_get_inventory_schema_and_status():
    """Verify inventory endpoint returns 200 and a valid list structure."""
    response = client.get("/api/v1/inventory")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Contract validation for mandatory keys
    for item in data:
        assert "sku" in item
        assert "location" in item
        assert "quantity" in item
        assert isinstance(item["quantity"], int)

def test_get_specific_sku_success():
    """Verify fetching an existing warehouse stock unit."""
    response = client.get("/api/v1/inventory/SKU-ROBOT-001")
    assert response.status_code == 200
    assert response.json()["location"] == "Zone-A-Rack-1"

def test_get_sku_not_found():
    """Negative test case for non-existent inventory items."""
    response = client.get("/api/v1/inventory/INVALID-SKU-999")
    assert response.status_code == 404
    assert response.json()["detail"] == "SKU not found in warehouse grid"

def test_dispatch_robot_task():
    """Validate robotic dispatch endpoint accepts valid execution commands."""
    payload = {
        "task_id": "TSK-8832",
        "robot_id": "AMR-Unit-04",
        "target_location": "Zone-C-Station-2",
        "action": "pick"
    }
    response = client.post("/api/v1/robot/task", json=payload)
    assert response.status_code == 201
    res_data = response.json()
    assert res_data["status"] == "dispatched"
    assert res_data["assigned_task"]["robot_id"] == "AMR-Unit-04"

