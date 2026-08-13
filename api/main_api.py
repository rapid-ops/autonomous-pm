from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import sys
import os

sys.path.insert(0, os.path.expanduser("~/autonomous_pm"))

from scheduler.jobs import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()

app = FastAPI(title="Rapid Ops PM System", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=os.path.expanduser("~/autonomous_pm/static")), name="static")

class LeadForm(BaseModel):
    name: str
    email: str
    phone: str
    message: str
    property_interest: str = ""

class TenantMessage(BaseModel):
    name: str
    unit: str
    message: str

class MaintenanceRequest(BaseModel):
    name: str
    unit: str
    issue: str

class FinancePortfolio(BaseModel):
    property_name: str
    period: str
    expected_monthly_income: float
    units: list

class VacancyData(BaseModel):
    property_name: str
    unit: str
    rent: float
    bedrooms: int
    bathrooms: int
    size: str
    features: list
    available_from: str
    location: str
    days_vacant: int = 0
    previous_tenant_reason: str = ""
    monthly_budget: float = 300
    target_tenant: str = ""
    goal: str = "Fill vacancy within 30 days"

class CampaignData(BaseModel):
    property_name: str
    unit_type: str
    rent: float
    location: str
    features: list
    target_tenant: str
    goal: str
    monthly_budget: float
    days_running: int = 0
    budget_spent: float = 0
    impressions: int = 0
    clicks: int = 0
    leads: int = 0
    cost_per_lead: float = 0
    lead_quality: str = "Not yet running"
    vacancies_filled: int = 0

class DecisionSnapshot(BaseModel):
    property_name: str
    leads_data: str = ""
    tenant_data: str = ""
    maintenance_data: str = ""
    finance_data: str = ""
    vacancy_data: str = ""
    lease_data: str = ""
    marketing_data: str = ""

class BusinessData(BaseModel):
    property_name: str
    period: str
    owner_name: str = "Property Owner"
    owner_goals: str = ""
    finance_summary: str = ""
    maintenance_summary: str = ""
    vacancy_summary: str = ""
    lease_summary: str = ""
    lead_summary: str = ""

@app.get("/")
def root():
    return FileResponse(os.path.expanduser("~/autonomous_pm/static/index.html"))

@app.get("/health")
def health():
    return {"status": "Rapid Ops PM System Running", "scheduler": "active"}

@app.post("/lead")
def receive_lead(lead: LeadForm):
    from main import process_lead
    result = process_lead(lead.dict())
    return {"status": "processed", "result": str(result)}

@app.post("/tenant")
def receive_tenant_message(message: TenantMessage):
    from main import process_tenant_message
    result = process_tenant_message(message.dict())
    return {"status": "processed", "result": str(result)}

@app.post("/maintenance")
def receive_maintenance(request: MaintenanceRequest):
    from main import process_maintenance_request
    data = request.dict()
    data["reported_at"] = "Now"
    data["escalation_level"] = "NONE"
    result = process_maintenance_request(data)
    return {"status": "processed", "result": str(result)}

@app.post("/finance")
def receive_finance(portfolio: FinancePortfolio):
    from main import process_finance
    result = process_finance(portfolio.dict())
    return {"status": "processed", "result": str(result)}

@app.post("/vacancy")
def receive_vacancy(vacancy: VacancyData):
    from main import process_vacancy
    result = process_vacancy(vacancy.dict())
    return {"status": "processed", "result": str(result)}

@app.post("/marketing")
def receive_campaign(campaign: CampaignData):
    from main import run_marketing_campaign
    result = run_marketing_campaign(campaign.dict())
    return {"status": "processed", "result": str(result)}

@app.post("/decision")
def run_decisions(snapshot: DecisionSnapshot):
    from main import run_decision_engine
    result = run_decision_engine(snapshot.dict())
    return {"status": "processed", "result": str(result)}

@app.post("/ceo-report")
def run_ceo(data: BusinessData):
    from main import run_ceo_report
    result = run_ceo_report(data.dict())
    return {"status": "processed", "result": str(result)}
