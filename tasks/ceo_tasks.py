from crewai import Task
from agents.ceo_agent import business_analyst, strategy_agent, executive_reporter

def create_business_analysis_task(business_data: dict) -> Task:
    return Task(
        description=f"""
        Analyze the overall health of this property business using all department data:
        
        Property: {business_data['property_name']}
        Period: {business_data['period']}
        
        Finance Summary: {business_data.get('finance_summary', 'Not provided')}
        Maintenance Summary: {business_data.get('maintenance_summary', 'Not provided')}
        Vacancy Summary: {business_data.get('vacancy_summary', 'Not provided')}
        Lease Summary: {business_data.get('lease_summary', 'Not provided')}
        Lead Summary: {business_data.get('lead_summary', 'Not provided')}
        
        Return a JSON with:
        - overall_health_score (0-100)
        - health_rating (EXCELLENT/GOOD/FAIR/POOR/CRITICAL)
        - strongest_area (what is performing best)
        - weakest_area (what needs most attention)
        - critical_issues (list of things needing immediate action)
        - positive_indicators (list of what is going well)
        - risk_level (LOW/MEDIUM/HIGH/CRITICAL)
        - revenue_at_risk (estimated income at risk if issues not addressed)
        """,
        expected_output="A comprehensive business health analysis JSON",
        agent=business_analyst
    )

def create_strategy_task(business_data: dict) -> Task:
    return Task(
        description=f"""
        Using the business analysis from the previous task, develop strategic 
        recommendations for this property:
        
        Property: {business_data['property_name']}
        Period: {business_data['period']}
        Owner Goals: {business_data.get('owner_goals', 'Maximize returns and minimize vacancy')}
        
        Return a JSON with:
        - immediate_actions (must do this week, list with owner or agent responsible)
        - short_term_strategy (next 30 days, list of initiatives)
        - long_term_strategy (next 90 days, list of initiatives)
        - revenue_opportunities (ways to increase income)
        - cost_reduction_opportunities (ways to reduce expenses)
        - tenant_retention_priority (which tenants to focus on keeping)
        - projected_impact (estimated financial impact if recommendations followed)
        """,
        expected_output="A strategic recommendations JSON",
        agent=strategy_agent
    )

def create_executive_report_task(business_data: dict) -> Task:
    return Task(
        description=f"""
        Generate a concise executive report for the property owner using all 
        analysis and strategy from previous tasks:
        
        Property: {business_data['property_name']}
        Period: {business_data['period']}
        Owner Name: {business_data.get('owner_name', 'Property Owner')}
        
        The report must:
        - Open with a one paragraph overall summary
        - Show key metrics in a clear format
        - Flag critical issues requiring owner decision
        - Summarize what agents are handling automatically
        - End with top 3 recommended actions for the owner
        - Be readable in under 2 minutes
        
        Return the full executive report as formatted text.
        """,
        expected_output="A concise executive report in formatted text",
        agent=executive_reporter
    )
