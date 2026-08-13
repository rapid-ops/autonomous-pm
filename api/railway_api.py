from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import requests
from datetime import datetime

app = FastAPI(title="Rapid Ops - Lead Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "/tmp/rapid_ops.db"

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
    return {"status": "Rapid Ops Gateway Running"}

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
    return {"status": "received"}

@app.get("/leads")
def get_leads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leads ORDER BY created_at DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return {"leads": rows}

@app.get("/leads/pending")
def get_pending_leads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leads WHERE status = 'PENDING' ORDER BY created_at ASC")
    rows = c.fetchall()
    conn.close()
    return {"leads": rows}

@app.post("/leads/{lead_id}/processed")
def mark_processed(lead_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE leads SET status = 'PROCESSED' WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()
    return {"status": "updated"}
