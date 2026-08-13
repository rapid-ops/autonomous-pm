import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/autonomous_pm/.env"))

sys.path.insert(0, os.path.expanduser("~/autonomous_pm"))

from crewai import Crew
from tasks.lead_tasks import create_qualification_task, create_response_task
from tasks.tenant_tasks import create_classification_task, create_response_task as create_tenant_response_task, create_escalation_task
from tasks.maintenance_tasks import create_job_order_task, create_priority_task, create_status_update_task
from tasks.finance_tasks import create_payment_tracking_task, create_collections_task, create_finance_report_task
from tasks.vacancy_tasks import create_listing_task, create_platform_strategy_task, create_vacancy_analysis_task
from tasks.lease_tasks import create_lease_monitoring_task, create_renewal_task, create_document_checklist_task
from tasks.ceo_tasks import create_business_analysis_task, create_strategy_task, create_executive_report_task
from tasks.marketing_tasks import create_ad_copy_task, create_campaign_strategy_task, create_performance_analysis_task
from tasks.decision_tasks import create_data_aggregation_task, create_decision_task, create_action_dispatch_task
from agents.lead_agent import lead_qualifier, response_drafter
from agents.tenant_agent import message_classifier, tenant_responder, escalation_agent
from agents.maintenance_agent import job_creator, priority_manager, status_updater
from agents.finance_agent import payment_tracker, collections_agent, finance_reporter
from agents.vacancy_agent import listing_writer, platform_strategist, vacancy_analyst
from agents.lease_agent import lease_monitor, renewal_agent, lease_document_agent
from agents.ceo_agent import business_analyst, strategy_agent, executive_reporter
from agents.marketing_agent import ad_copywriter, campaign_strategist, performance_analyst
from agents.decision_agent import data_aggregator, decision_maker, action_dispatcher
from utils.database import (save_lead, save_tenant_message, save_maintenance_job,
                             save_finance_record, save_ceo_report, init_db)
from utils.email_sender import (send_hot_lead_alert, send_warm_cold_lead_summary,
                                 send_maintenance_alert, send_daily_ceo_report)

MANAGER_EMAIL = os.environ.get("MANAGER_EMAIL", "")
PROPERTY_NAME = os.environ.get("PROPERTY_NAME", "My Property")

init_db()

def process_lead(lead: dict):
    print(f"\n--- Processing lead from {lead['name']} ---")
    crew = Crew(
        agents=[lead_qualifier, response_drafter],
        tasks=[create_qualification_task(lead), create_response_task(lead)],
        verbose=True
    )
    result = crew.kickoff()

    try:
        import json
        result_str = str(result)
        score = 50
        status = "WARM"
        reasoning = ""

        if "HOT" in result_str:
            status = "HOT"
            score = 90
        elif "COLD" in result_str:
            status = "COLD"
            score = 20

        save_lead(lead, score, status, reasoning, result_str)

        if status == "HOT" and MANAGER_EMAIL:
            send_hot_lead_alert(MANAGER_EMAIL, lead, score, result_str)
        elif MANAGER_EMAIL:
            send_warm_cold_lead_summary(MANAGER_EMAIL, lead, score, status)

    except Exception as e:
        print(f"[lead] Post processing error: {e}")

    print("\n=== LEAD PROCESSED ===")
    print(result)
    return result


def process_tenant_message(message: dict):
    print(f"\n--- Processing message from {message['name']} in unit {message['unit']} ---")
    crew = Crew(
        agents=[message_classifier, tenant_responder, escalation_agent],
        tasks=[create_classification_task(message), create_tenant_response_task(message), create_escalation_task(message)],
        verbose=True
    )
    result = crew.kickoff()

    try:
        result_str = str(result)
        save_tenant_message(message, "MAINTENANCE", "MEDIUM", "", "false", result_str, "")
    except Exception as e:
        print(f"[tenant] Post processing error: {e}")

    print("\n=== TENANT MESSAGE PROCESSED ===")
    print(result)
    return result


def process_maintenance_request(request: dict):
    print(f"\n--- Processing maintenance for {request['name']} in {request['unit']} ---")
    crew = Crew(
        agents=[job_creator, priority_manager, status_updater],
        tasks=[create_job_order_task(request), create_priority_task(request), create_status_update_task(request)],
        verbose=True
    )
    result = crew.kickoff()

    try:
        result_str = str(result)
        priority = "HIGH"
        if "EMERGENCY" in result_str:
            priority = "EMERGENCY"
        elif "MEDIUM" in result_str:
            priority = "MEDIUM"
        elif "LOW" in result_str:
            priority = "LOW"

        job_id = f"JOB-{request['unit'].replace(' ', '')}"
        save_maintenance_job(request, job_id, priority, "ASAP", "false")

        if MANAGER_EMAIL:
            send_maintenance_alert(MANAGER_EMAIL, request, priority, job_id)

    except Exception as e:
        print(f"[maintenance] Post processing error: {e}")

    print("\n=== MAINTENANCE REQUEST PROCESSED ===")
    print(result)
    return result


def process_finance(portfolio: dict):
    print(f"\n--- Processing finances for {portfolio['property_name']} ---")
    crew = Crew(
        agents=[payment_tracker, collections_agent, finance_reporter],
        tasks=[create_payment_tracking_task(portfolio), create_collections_task(portfolio), create_finance_report_task(portfolio)],
        verbose=True
    )
    result = crew.kickoff()
    print("\n=== FINANCE REPORT GENERATED ===")
    print(result)
    return result


def process_vacancy(vacancy: dict):
    print(f"\n--- Processing vacancy for {vacancy['unit']} at {vacancy['property_name']} ---")
    crew = Crew(
        agents=[listing_writer, platform_strategist, vacancy_analyst],
        tasks=[create_listing_task(vacancy), create_platform_strategy_task(vacancy), create_vacancy_analysis_task(vacancy)],
        verbose=True
    )
    result = crew.kickoff()
    print("\n=== VACANCY PROCESSED ===")
    print(result)
    return result


def process_leases(portfolio: dict):
    print(f"\n--- Processing leases for {portfolio['property_name']} ---")
    crew = Crew(
        agents=[lease_monitor, renewal_agent, lease_document_agent],
        tasks=[create_lease_monitoring_task(portfolio), create_renewal_task(portfolio['renewal_tenant']), create_document_checklist_task(portfolio['renewal_tenant'])],
        verbose=True
    )
    result = crew.kickoff()
    print("\n=== LEASE REPORT GENERATED ===")
    print(result)
    return result


def run_ceo_report(business_data: dict):
    print(f"\n--- Generating CEO report for {business_data['property_name']} ---")
    crew = Crew(
        agents=[business_analyst, strategy_agent, executive_reporter],
        tasks=[create_business_analysis_task(business_data), create_strategy_task(business_data), create_executive_report_task(business_data)],
        verbose=True
    )
    result = crew.kickoff()

    try:
        result_str = str(result)
        save_ceo_report(business_data['property_name'], business_data['period'], 75, "GOOD", result_str)
        if MANAGER_EMAIL:
            send_daily_ceo_report(MANAGER_EMAIL, business_data['property_name'], result_str)
    except Exception as e:
        print(f"[ceo] Post processing error: {e}")

    print("\n=== EXECUTIVE REPORT GENERATED ===")
    print(result)
    return result


def run_marketing_campaign(campaign: dict):
    print(f"\n--- Running marketing campaign for {campaign['property_name']} ---")
    crew = Crew(
        agents=[ad_copywriter, campaign_strategist, performance_analyst],
        tasks=[create_ad_copy_task(campaign), create_campaign_strategy_task(campaign), create_performance_analysis_task(campaign)],
        verbose=True
    )
    result = crew.kickoff()
    print("\n=== MARKETING CAMPAIGN READY ===")
    print(result)
    return result


def run_decision_engine(snapshot: dict):
    print(f"\n--- Running decision engine for {snapshot['property_name']} ---")
    crew = Crew(
        agents=[data_aggregator, decision_maker, action_dispatcher],
        tasks=[create_data_aggregation_task(snapshot), create_decision_task(snapshot), create_action_dispatch_task(snapshot)],
        verbose=True
    )
    result = crew.kickoff()
    print("\n=== DECISIONS MADE ===")
    print(result)
    return result


if __name__ == "__main__":
    test_lead = {
        "name": "John Smith",
        "email": "john@gmail.com",
        "phone": "+1234567890",
        "message": "Hi, I am very interested in Apartment 3B. I need to move in by next week. Is it still available? I have all documents ready.",
        "property_interest": "Apartment 3B"
    }

    test_message = {
        "name": "Sarah Johnson",
        "unit": "Apt 5A",
        "message": "The pipe under my kitchen sink has been leaking since yesterday and water is now on the floor."
    }

    test_maintenance = {
        "name": "Sarah Johnson",
        "unit": "Apt 5A",
        "issue": "Pipe under kitchen sink leaking, water on floor",
        "reported_at": "2026-08-13 09:00",
        "escalation_level": "CRITICAL"
    }

    test_portfolio = {
        "property_name": "Sunset Apartments",
        "period": "August 2026",
        "expected_monthly_income": 25000,
        "units": [
            {"unit": "Apt 1A", "tenant": "Mike Brown", "rent": 1200, "paid": 1200, "payment_date": "2026-08-01"},
            {"unit": "Apt 2B", "tenant": "Lisa Chen", "rent": 1500, "paid": 0, "payment_date": None},
            {"unit": "Apt 3C", "tenant": "James Wilson", "rent": 1800, "paid": 900, "payment_date": "2026-08-05"},
            {"unit": "Apt 4D", "tenant": "Emma Davis", "rent": 2000, "paid": 0, "payment_date": None},
            {"unit": "Apt 5A", "tenant": "Sarah Johnson", "rent": 1500, "paid": 1500, "payment_date": "2026-08-02"},
        ]
    }

    test_vacancy = {
        "property_name": "Sunset Apartments",
        "unit": "Apt 6B",
        "rent": 1600,
        "bedrooms": 2,
        "bathrooms": 1,
        "size": "850 sqft",
        "features": ["Hardwood floors", "Modern kitchen", "In-unit laundry", "Parking included", "Pet friendly"],
        "available_from": "2026-09-01",
        "location": "Austin, Texas",
        "days_vacant": 12,
        "previous_tenant_reason": "Lease ended naturally",
        "monthly_budget": 500,
        "target_tenant": "Young professionals",
        "goal": "Fill vacancy within 30 days"
    }

    test_lease_portfolio = {
        "property_name": "Sunset Apartments",
        "current_date": "2026-08-13",
        "leases": [
            {"unit": "Apt 1A", "tenant": "Mike Brown", "lease_end": "2026-09-30", "rent": 1200},
            {"unit": "Apt 2B", "tenant": "Lisa Chen", "lease_end": "2026-10-31", "rent": 1500},
            {"unit": "Apt 3C", "tenant": "James Wilson", "lease_end": "2026-08-31", "rent": 1800},
            {"unit": "Apt 4D", "tenant": "Emma Davis", "lease_end": "2027-01-31", "rent": 2000},
            {"unit": "Apt 5A", "tenant": "Sarah Johnson", "lease_end": "2026-11-30", "rent": 1500},
        ],
        "renewal_tenant": {
            "name": "James Wilson",
            "unit": "Apt 3C",
            "current_rent": 1800,
            "proposed_rent": 1900,
            "lease_end": "2026-08-31",
            "lease_start": "2026-09-01",
            "tenancy_duration": "2 years",
            "payment_history": "Perfect — never missed a payment",
            "transaction_type": "RENEWAL"
        }
    }

    test_campaign = {
        "property_name": "Sunset Apartments",
        "unit_type": "2 bedroom apartment",
        "rent": 1600,
        "location": "Austin, Texas",
        "features": ["Hardwood floors", "Modern kitchen", "In-unit laundry", "Parking", "Pet friendly"],
        "target_tenant": "Young professionals aged 25-35",
        "goal": "Generate 20 qualified leads in 30 days",
        "monthly_budget": 500,
        "days_running": 0,
        "budget_spent": 0,
        "impressions": 0,
        "clicks": 0,
        "leads": 0,
        "cost_per_lead": 0,
        "lead_quality": "Not yet running",
        "vacancies_filled": 0
    }

    test_snapshot = {
        "property_name": "Sunset Apartments",
        "leads_data": "3 new leads this week, 1 HOT pending callback",
        "tenant_data": "2 open tenant messages, 1 maintenance escalation",
        "maintenance_data": "1 EMERGENCY job open, 2 MEDIUM jobs pending",
        "finance_data": "Collection rate 60 percent, 2 units fully overdue",
        "vacancy_data": "1 unit vacant 12 days, listing not posted yet",
        "lease_data": "2 leases expiring within 50 days",
        "marketing_data": "No active campaigns running"
    }

    test_business_data = {
        "property_name": "Sunset Apartments",
        "period": "August 2026",
        "owner_name": "Mr. Anderson",
        "owner_goals": "Maximize occupancy and increase NOI by 10 percent this quarter",
        "finance_summary": "Collection rate 60 percent, 2 units fully overdue, 1 partial payment",
        "maintenance_summary": "1 critical maintenance issue active, 3 routine requests pending",
        "vacancy_summary": "1 unit vacant for 12 days, listing not yet posted",
        "lease_summary": "2 leases expiring within 50 days, 1 renewal in progress",
        "lead_summary": "3 new inquiries this week, 1 HOT lead pending response"
    }

    print("\n========== LEAD PROCESSING ==========")
    process_lead(test_lead)

    print("\n========== TENANT COMMUNICATION ==========")
    process_tenant_message(test_message)

    print("\n========== MAINTENANCE PROCESSING ==========")
    process_maintenance_request(test_maintenance)

    print("\n========== FINANCE PROCESSING ==========")
    process_finance(test_portfolio)

    print("\n========== VACANCY PROCESSING ==========")
    process_vacancy(test_vacancy)

    print("\n========== LEASE PROCESSING ==========")
    process_leases(test_lease_portfolio)

    print("\n========== MARKETING CAMPAIGN ==========")
    run_marketing_campaign(test_campaign)

    print("\n========== DECISION ENGINE ==========")
    run_decision_engine(test_snapshot)

    print("\n========== CEO EXECUTIVE REPORT ==========")
    run_ceo_report(test_business_data)
