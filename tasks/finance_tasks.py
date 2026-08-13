from crewai import Task
from agents.finance_agent import payment_tracker, collections_agent, finance_reporter

def create_payment_tracking_task(portfolio: dict) -> Task:
    return Task(
        description=f"""
        Analyze the payment status for this property portfolio:
        
        Property: {portfolio['property_name']}
        Period: {portfolio['period']}
        Units: {portfolio['units']}
        
        For each unit evaluate:
        - Is rent paid, partial, or overdue
        - How many days overdue if applicable
        - Total expected vs total received
        
        Return a JSON with:
        - total_units (int)
        - paid_units (int)
        - overdue_units (int)
        - partial_units (int)
        - total_expected (float)
        - total_collected (float)
        - outstanding_balance (float)
        - overdue_accounts (list of unit, tenant, days_overdue, amount_owed)
        - collection_rate (percentage)
        """,
        expected_output="A detailed JSON payment status report",
        agent=payment_tracker
    )

def create_collections_task(portfolio: dict) -> Task:
    return Task(
        description=f"""
        Using the payment tracking results from the previous task, generate 
        appropriate collections notices for all overdue accounts in:
        
        Property: {portfolio['property_name']}
        Period: {portfolio['period']}
        
        Notice levels based on days overdue:
        1 to 5 days: friendly reminder
        6 to 15 days: formal notice with late fee warning
        16 to 30 days: final notice with legal action warning
        30+ days: legal escalation alert for property manager
        
        Return a JSON list where each item has:
        - unit
        - tenant_name
        - days_overdue
        - notice_level
        - message (the actual notice to send)
        - late_fee_applicable (true/false)
        """,
        expected_output="A JSON list of collections notices for each overdue account",
        agent=collections_agent
    )

def create_finance_report_task(portfolio: dict) -> Task:
    return Task(
        description=f"""
        Generate a comprehensive financial report for this period using 
        the payment tracking and collections data from previous tasks:
        
        Property: {portfolio['property_name']}
        Period: {portfolio['period']}
        Expected Monthly Income: {portfolio['expected_monthly_income']}
        
        The report should include:
        - Executive summary (2 sentences)
        - Income summary (expected vs collected vs outstanding)
        - Collection rate and trend
        - Overdue accounts summary
        - Cash flow status
        - Recommended actions for property manager
        
        Return the full report as formatted text.
        """,
        expected_output="A comprehensive financial report in formatted text",
        agent=finance_reporter
    )
