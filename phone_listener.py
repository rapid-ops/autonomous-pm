from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sys
import os

sys.path.insert(0, os.path.expanduser("~/autonomous_pm"))

app = FastAPI(title="Rapid Ops Phone Listener")

class LeadData(BaseModel):
    name: str
    email: str
    phone: str
    message: str
    property_interest: str = ""

class TenantData(BaseModel):
    name: str
    unit: str
    message: str

class MaintenanceData(BaseModel):
    name: str
    unit: str
    issue: str

@app.post("/process-lead")
def process_lead(lead: LeadData):
    from main import process_lead as run_lead
    run_lead(lead.dict())
    return {"status": "processed"}

@app.post("/process-tenant")
def process_tenant(msg: TenantData):
    from main import process_tenant_message
    process_tenant_message(msg.dict())
    return {"status": "processed"}

@app.post("/process-maintenance")
def process_maintenance(req: MaintenanceData):
    from main import process_maintenance_request
    data = req.dict()
    data["reported_at"] = "Now"
    data["escalation_level"] = "NONE"
    process_maintenance_request(data)
    return {"status": "processed"}

@app.get("/health")
def health():
    return {"status": "Phone listener running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
