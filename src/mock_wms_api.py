from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="RobOm WMS Mock API", version="1.0.0")

class Item(BaseModel):
    sku: str
    location: str
    quantity: int
    status: str  # e.g., 'stored', 'in_transit', 'picked'

class RobotTask(BaseModel):
    task_id: str
    robot_id: str
    target_location: str
    action: str  # 'pick', 'place', 'charge'

# In-memory mock database
inventory_db = [
    {"sku": "SKU-ROBOT-001", "location": "Zone-A-Rack-1", "quantity": 150, "status": "stored"},
    {"sku": "SKU-ROBOT-002", "location": "Zone-B-Rack-4", "quantity": 80, "status": "stored"}
]

active_tasks = []

@app.get("/api/v1/inventory", response_model=List[Item])
def get_inventory():
    return inventory_db

@app.get("/api/v1/inventory/{sku}", response_model=Item)
def get_item(sku: str):
    for item in inventory_db:
        if item["sku"] == sku:
            return item
    raise HTTPException(status_code=404, detail="SKU not found in warehouse grid")

@app.post("/api/v1/robot/task", status_code=201)
def dispatch_robot(task: RobotTask):
    if not task.task_id or not task.robot_id:
        raise HTTPException(status_code=400, detail="Invalid telemetry payload")
    active_tasks.append(task.dict())
    return {"status": "dispatched", "assigned_task": task.dict()}
