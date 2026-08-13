from crewai import Task
from agents.decision_agent import data_aggregator, decision_maker, action_dispatcher
from datetime import datetime

def create_data_aggregation_task(snapshot: dict) -> Task:
    return Task(
        description=f"""
        Aggregate and analyze all business data for this property:
        
        Property: {snapshot['property_name']}
        Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        
        Leads Data: {snapshot.get('leads_data', 'No data')}
        Tenant Messages: {snapshot.get('tenant_data', 'No data')}
        Maintenance Jobs: {snapshot.get('maintenance_data', 'No data')}
        Finance Data: {snapshot.get('finance_data', 'No data')}
        Vacancy Data: {snapshot.get('vacancy_data', 'No data')}
        Lease Data: {snapshot.get('lease_data', 'No data')}
        Marketing Data: {snapshot.get('marketing_data', 'No data')}
        
        Return a JSON with:
        - snapshot_time (current datetime)
        - business_health_score (0-100)
        - critical_alerts (list of things needing immediate attention)
        - revenue_status (on track/at risk/critical)
        - occupancy_rate (percentage)
        - active_issues_count (total open issues across all departments)
        - department_scores (score for each department 0-100)
        - trend (improving/stable/declining)
        """,
        expected_output="A unified business intelligence snapshot JSON",
        agent=data_aggregator
    )

def create_decision_task(snapshot: dict) -> Task:
    return Task(
        description=f"""
        Review the business intelligence snapshot from the previous task and 
        make autonomous decisions for this property:
        
        Property: {snapshot['property_name']}
        
        You have authority to autonomously decide:
        - Send rent reminders to overdue tenants
        - Pause or adjust underperforming ad campaigns
        - Trigger lease renewal outreach for expiring leases
        - Escalate emergency maintenance to property manager
        - Flag leads requiring immediate callback
        - Schedule routine maintenance checks
        
        You must escalate to human for:
        - Eviction proceedings
        - Legal matters
        - Budget increases above 20 percent
        - Tenant disputes requiring mediation
        - Major repairs above a set cost threshold
        
        Return a JSON with:
        - autonomous_decisions (list of decisions made with reasoning)
        - human_escalations (list of items requiring owner approval with urgency)
        - deferred_decisions (items to revisit tomorrow with reason)
        - decision_summary (one paragraph summary for the owner)
        - confidence_level (HIGH/MEDIUM/LOW for overall decision set)
        """,
        expected_output="A complete decision log JSON",
        agent=decision_maker
    )

def create_action_dispatch_task(snapshot: dict) -> Task:
    return Task(
        description=f"""
        Convert the decisions from the previous task into specific executable 
        action instructions for each department:
        
        Property: {snapshot['property_name']}
        Date: {datetime.now().strftime("%Y-%m-%d")}
        
        For each autonomous decision, create a specific action instruction that includes:
        - Which agent or system handles it
        - Exact parameters needed to execute
        - Priority and timing
        - Expected outcome
        - How to confirm it was completed
        
        Return a JSON with:
        - action_queue (list of actions ordered by priority)
        - email_actions (emails to send with recipient, subject, content)
        - agent_triggers (which agents to run with what data)
        - scheduled_actions (actions to run at specific times)
        - completed_actions (actions already handled in this cycle)
        - action_summary (brief summary of what will happen next)
        """,
        expected_output="A complete action dispatch plan JSON",
        agent=action_dispatcher
    )
