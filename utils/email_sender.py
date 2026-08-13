import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_EMAIL = os.environ.get("SMTP_EMAIL", "your_gmail@gmail.com")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "your_app_password_here")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to: str, subject: str, body: str, html: bool = False):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_EMAIL
        msg["To"] = to
        content_type = "html" if html else "plain"
        msg.attach(MIMEText(body, content_type))
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to, msg.as_string())
        print(f"[email] Sent to {to}: {subject}")
        return True
    except Exception as e:
        print(f"[email] Failed: {e}")
        return False

def send_hot_lead_alert(manager_email: str, lead: dict, score: int, response: str):
    subject = f"HOT LEAD ALERT — Score {score}/100 — {lead['name']}"
    body = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: #0d1b2a; padding: 20px; border-radius: 8px 8px 0 0;">
            <h2 style="color: white; margin: 0;">HOT LEAD ALERT</h2>
            <p style="color: #94a3b8; margin: 5px 0 0 0;">Score: {score}/100</p>
        </div>
        <div style="padding: 24px; border: 1px solid #e5e7eb; border-radius: 0 0 8px 8px;">
            <h3 style="color: #0d1b2a;">Lead Details</h3>
            <p><strong>Name:</strong> {lead['name']}</p>
            <p><strong>Email:</strong> {lead['email']}</p>
            <p><strong>Phone:</strong> {lead['phone']}</p>
            <p><strong>Message:</strong> {lead['message']}</p>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
            <h3 style="color: #0d1b2a;">AI Response Sent</h3>
            <p style="color: #374151;">{response}</p>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
            <p style="color: #6b7280; font-size: 12px;">Rapid Ops — Property Operations, Automated.</p>
        </div>
    </body></html>
    """
    return send_email(manager_email, subject, body, html=True)

def send_warm_cold_lead_summary(manager_email: str, lead: dict, score: int, status: str):
    subject = f"{status} Lead — {lead['name']} — Score {score}/100"
    body = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: #374151; padding: 20px; border-radius: 8px 8px 0 0;">
            <h2 style="color: white; margin: 0;">{status} LEAD</h2>
            <p style="color: #d1d5db; margin: 5px 0 0 0;">Score: {score}/100 — Handled automatically</p>
        </div>
        <div style="padding: 24px; border: 1px solid #e5e7eb; border-radius: 0 0 8px 8px;">
            <p><strong>Name:</strong> {lead['name']}</p>
            <p><strong>Email:</strong> {lead['email']}</p>
            <p><strong>Phone:</strong> {lead['phone']}</p>
            <p><strong>Message:</strong> {lead['message']}</p>
            <p style="color: #6b7280; font-size: 12px; margin-top: 20px;">This lead was automatically followed up. No action needed.</p>
        </div>
    </body></html>
    """
    return send_email(manager_email, subject, body, html=True)

def send_maintenance_alert(manager_email: str, request: dict, priority: str, job_id: str):
    color = "#dc2626" if priority == "EMERGENCY" else "#d97706" if priority == "HIGH" else "#374151"
    subject = f"{priority} Maintenance — {request['unit']} — {request['issue'][:40]}"
    body = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: {color}; padding: 20px; border-radius: 8px 8px 0 0;">
            <h2 style="color: white; margin: 0;">{priority} MAINTENANCE REQUEST</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0;">Job ID: {job_id}</p>
        </div>
        <div style="padding: 24px; border: 1px solid #e5e7eb; border-radius: 0 0 8px 8px;">
            <p><strong>Tenant:</strong> {request['name']}</p>
            <p><strong>Unit:</strong> {request['unit']}</p>
            <p><strong>Issue:</strong> {request['issue']}</p>
            <p><strong>Reported:</strong> {request.get('reported_at', 'Now')}</p>
            <p style="color: #6b7280; font-size: 12px; margin-top: 20px;">Rapid Ops — Property Operations, Automated.</p>
        </div>
    </body></html>
    """
    return send_email(manager_email, subject, body, html=True)

def send_daily_ceo_report(manager_email: str, property_name: str, report: str):
    subject = f"Daily Report — {property_name}"
    body = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: #0d1b2a; padding: 20px; border-radius: 8px 8px 0 0;">
            <h2 style="color: white; margin: 0;">Daily Executive Report</h2>
            <p style="color: #94a3b8; margin: 5px 0 0 0;">{property_name}</p>
        </div>
        <div style="padding: 24px; border: 1px solid #e5e7eb; border-radius: 0 0 8px 8px;">
            <pre style="white-space: pre-wrap; font-family: Arial, sans-serif; color: #374151;">{report}</pre>
            <p style="color: #6b7280; font-size: 12px; margin-top: 20px;">Rapid Ops — Property Operations, Automated.</p>
        </div>
    </body></html>
    """
    return send_email(manager_email, subject, body, html=True)
