from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.expanduser("~/autonomous_pm"))

scheduler = BackgroundScheduler(timezone="UTC")

def run_daily_ceo_report():
    print(f"[scheduler] Running daily CEO report at {datetime.now()}")
    try:
        from main import run_ceo_report
        from utils.email_sender import send_daily_ceo_report
        from dotenv import load_dotenv
        load_dotenv(os.path.expanduser("~/autonomous_pm/.env"))

        business_data = {
            "property_name": os.environ.get("PROPERTY_NAME", "My Property"),
            "period": datetime.now().strftime("%B %Y"),
            "owner_name": os.environ.get("OWNER_NAME", "Property Owner"),
            "owner_goals": "Maximize occupancy and reduce vacancy",
            "finance_summary": "Pulled from database",
            "maintenance_summary": "Pulled from database",
            "vacancy_summary": "Pulled from database",
            "lease_summary": "Pulled from database",
            "lead_summary": "Pulled from database"
        }

        result = run_ceo_report(business_data)
        manager_email = os.environ.get("MANAGER_EMAIL", "")
        property_name = os.environ.get("PROPERTY_NAME", "My Property")

        if manager_email:
            send_daily_ceo_report(manager_email, property_name, str(result))
            print("[scheduler] Daily CEO report sent")

    except Exception as e:
        print(f"[scheduler] CEO report failed: {e}")

def run_lease_check():
    print(f"[scheduler] Running lease check at {datetime.now()}")
    try:
        from utils.database import get_overdue_leases
        from utils.email_sender import send_email
        from dotenv import load_dotenv
        load_dotenv(os.path.expanduser("~/autonomous_pm/.env"))

        today = datetime.now().strftime("%Y-%m-%d")
        overdue = get_overdue_leases(today)

        if overdue:
            manager_email = os.environ.get("MANAGER_EMAIL", "")
            if manager_email:
                body = f"<p>{len(overdue)} lease(s) require attention today.</p>"
                for lease in overdue:
                    body += f"<p>Unit {lease[3]} — Tenant: {lease[4]} — Expired: {lease[5]}</p>"
                send_email(manager_email, f"Lease Alert — {len(overdue)} lease(s) need attention", body, html=True)
                print(f"[scheduler] Lease alert sent for {len(overdue)} leases")

    except Exception as e:
        print(f"[scheduler] Lease check failed: {e}")

def run_maintenance_check():
    print(f"[scheduler] Running maintenance check at {datetime.now()}")
    try:
        from utils.database import get_open_maintenance_jobs
        from utils.email_sender import send_email
        from dotenv import load_dotenv
        load_dotenv(os.path.expanduser("~/autonomous_pm/.env"))

        open_jobs = get_open_maintenance_jobs()

        if open_jobs:
            manager_email = os.environ.get("MANAGER_EMAIL", "")
            if manager_email:
                body = f"<p>{len(open_jobs)} open maintenance job(s) pending.</p>"
                for job in open_jobs:
                    body += f"<p>{job[1]} — Unit {job[3]} — Priority: {job[5]}</p>"
                send_email(manager_email, f"Maintenance Update — {len(open_jobs)} open job(s)", body, html=True)
                print(f"[scheduler] Maintenance alert sent for {len(open_jobs)} jobs")

    except Exception as e:
        print(f"[scheduler] Maintenance check failed: {e}")

def start_scheduler():
    scheduler.add_job(
        run_daily_ceo_report,
        CronTrigger(hour=7, minute=0),
        id="daily_ceo_report",
        replace_existing=True
    )
    scheduler.add_job(
        run_lease_check,
        CronTrigger(hour=8, minute=0),
        id="lease_check",
        replace_existing=True
    )
    scheduler.add_job(
        run_maintenance_check,
        CronTrigger(hour=8, minute=30),
        id="maintenance_check",
        replace_existing=True
    )
    scheduler.start()
    print("[scheduler] Scheduler started — daily report at 7AM, lease check at 8AM, maintenance at 8:30AM")

def stop_scheduler():
    scheduler.shutdown()
    print("[scheduler] Scheduler stopped")
