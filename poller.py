import requests
import time
import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/autonomous_pm/.env"))
sys.path.insert(0, os.path.expanduser("~/autonomous_pm"))

RAILWAY_URL = "https://autonomous-pm-production-c789.up.railway.app"
POLL_INTERVAL = 60

def fetch_pending_leads():
    try:
        response = requests.get(f"{RAILWAY_URL}/leads/pending", timeout=10)
        if response.status_code == 200:
            return response.json().get("leads", [])
    except Exception as e:
        print(f"[poller] Failed to fetch leads: {e}")
    return []

def mark_lead_processed(lead_id: int):
    try:
        requests.post(f"{RAILWAY_URL}/leads/{lead_id}/processed", timeout=10)
    except Exception as e:
        print(f"[poller] Failed to mark lead {lead_id}: {e}")

def run():
    print("[poller] Starting — checking Railway every 60 seconds")
    from main import process_lead

    while True:
        print(f"[poller] Checking for new leads...")
        leads = fetch_pending_leads()

        if leads:
            print(f"[poller] Found {len(leads)} pending leads")
            for lead in leads:
                lead_data = {
                    "name": lead[1],
                    "email": lead[2],
                    "phone": lead[3],
                    "message": lead[4],
                    "property_interest": lead[5]
                }
                print(f"[poller] Processing lead from {lead_data['name']}")
                process_lead(lead_data)
                mark_lead_processed(lead[0])
        else:
            print("[poller] No pending leads")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    run()
