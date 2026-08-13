import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.expanduser("~/autonomous_pm/data/rapid_ops.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        message TEXT,
        property_interest TEXT,
        score INTEGER,
        status TEXT,
        reasoning TEXT,
        ai_response TEXT,
        created_at TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS tenant_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        unit TEXT,
        message TEXT,
        category TEXT,
        urgency TEXT,
        summary TEXT,
        requires_escalation TEXT,
        ai_response TEXT,
        escalation_alert TEXT,
        created_at TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS maintenance_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT,
        name TEXT,
        unit TEXT,
        issue TEXT,
        priority TEXT,
        response_time TEXT,
        safety_risk TEXT,
        status TEXT DEFAULT 'OPEN',
        reported_at TEXT,
        created_at TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS finance_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_name TEXT,
        period TEXT,
        total_expected REAL,
        total_collected REAL,
        outstanding_balance REAL,
        collection_rate TEXT,
        overdue_accounts TEXT,
        created_at TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS vacancies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_name TEXT,
        unit TEXT,
        rent REAL,
        days_vacant INTEGER,
        status TEXT DEFAULT 'VACANT',
        listing_headline TEXT,
        platform_strategy TEXT,
        created_at TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS leases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_name TEXT,
        unit TEXT,
        tenant_name TEXT,
        lease_end TEXT,
        current_rent REAL,
        status TEXT DEFAULT 'ACTIVE',
        renewal_sent TEXT DEFAULT 'NO',
        created_at TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS ceo_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_name TEXT,
        period TEXT,
        health_score INTEGER,
        health_rating TEXT,
        report_text TEXT,
        created_at TEXT
    )''')

    conn.commit()
    conn.close()
    print("[db] Database initialized")

def save_lead(lead: dict, score: int, status: str, reasoning: str, ai_response: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO leads 
        (name, email, phone, message, property_interest, score, status, reasoning, ai_response, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (lead['name'], lead['email'], lead['phone'], lead['message'],
         lead.get('property_interest', ''), score, status, reasoning, ai_response,
         datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_tenant_message(message: dict, category: str, urgency: str, summary: str,
                        requires_escalation: str, ai_response: str, escalation_alert: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO tenant_messages
        (name, unit, message, category, urgency, summary, requires_escalation, ai_response, escalation_alert, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (message['name'], message['unit'], message['message'], category, urgency,
         summary, requires_escalation, ai_response, escalation_alert, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_maintenance_job(request: dict, job_id: str, priority: str, response_time: str, safety_risk: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO maintenance_jobs
        (job_id, name, unit, issue, priority, response_time, safety_risk, reported_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (job_id, request['name'], request['unit'], request['issue'],
         priority, response_time, safety_risk,
         request.get('reported_at', 'Now'), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_finance_record(portfolio: dict, total_collected: float, outstanding: float,
                        collection_rate: str, overdue_accounts: list):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO finance_records
        (property_name, period, total_expected, total_collected, outstanding_balance, collection_rate, overdue_accounts, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (portfolio['property_name'], portfolio['period'],
         portfolio.get('expected_monthly_income', 0), total_collected,
         outstanding, collection_rate, json.dumps(overdue_accounts), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_ceo_report(property_name: str, period: str, health_score: int, health_rating: str, report_text: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO ceo_reports
        (property_name, period, health_score, health_rating, report_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (property_name, period, health_score, health_rating, report_text, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_leads(limit: int = 50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leads ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_open_maintenance_jobs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM maintenance_jobs WHERE status = 'OPEN' ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_overdue_leases(current_date: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leases WHERE lease_end <= ? AND status = 'ACTIVE'", (current_date,))
    rows = c.fetchall()
    conn.close()
    return rows

init_db()
