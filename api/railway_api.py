from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import os
import json
import requests
from datetime import datetime

app = FastAPI(title="Rapid Ops - Lead Gateway")

DB_PATH = "/tmp/rapid_ops.db"
PHONE_WEBHOOK = os.environ.get("PHONE_WEBHOOK_URL", "")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT, phone TEXT,
        message TEXT, property_interest TEXT,
        status TEXT DEFAULT 'PENDING',
        created_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tenant_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, unit TEXT, message TEXT,
        status TEXT DEFAULT 'PENDING',
        created_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS maintenance_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, unit TEXT, issue TEXT,
        status TEXT DEFAULT 'PENDING',
        created_at TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

def notify_phone(endpoint: str, data: dict):
    if PHONE_WEBHOOK:
        try:
            requests.post(f"{PHONE_WEBHOOK}{endpoint}", json=data, timeout=5)
        except Exception as e:
            print(f"[webhook] Could not reach phone: {e}")

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

@app.get("/")
def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "../static/index.html"))

@app.get("/health")
def health():
    return {"status": "Rapid Ops Gateway Running"}

@app.post("/lead")
def receive_lead(lead: LeadForm):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO leads (name, email, phone, message, property_interest, created_at)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (lead.name, lead.email, lead.phone, lead.message,
               lead.property_interest, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    notify_phone("/process-lead", lead.dict())
    return {"status": "received", "message": "Your inquiry has been received. We will respond within minutes."}

@app.post("/tenant")
def receive_tenant(msg: TenantMessage):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO tenant_messages (name, unit, message, created_at)
                 VALUES (?, ?, ?, ?)''',
              (msg.name, msg.unit, msg.message, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    notify_phone("/process-tenant", msg.dict())
    return {"status": "received"}

@app.post("/maintenance")
def receive_maintenance(req: MaintenanceRequest):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO maintenance_requests (name, unit, issue, created_at)
                 VALUES (?, ?, ?, ?)''',
              (req.name, req.unit, req.issue, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    notify_phone("/process-maintenance", req.dict())
    return {"status": "received"}

@app.get("/leads")
def get_leads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leads ORDER BY created_at DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return {"leads": rows}
