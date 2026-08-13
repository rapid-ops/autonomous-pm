from crewai import Task
from agents.vacancy_agent import listing_writer, platform_strategist, vacancy_analyst

def create_listing_task(vacancy: dict) -> Task:
    return Task(
        description=f"""
        Write a compelling rental listing for this vacant unit:
        
        Property: {vacancy['property_name']}
        Unit: {vacancy['unit']}
        Rent: {vacancy['rent']}
        Bedrooms: {vacancy['bedrooms']}
        Bathrooms: {vacancy['bathrooms']}
        Size: {vacancy['size']}
        Features: {vacancy['features']}
        Available From: {vacancy['available_from']}
        Location: {vacancy['location']}
        
        Return a JSON with:
        - headline (attention grabbing title under 10 words)
        - short_description (2 sentences for social media)
        - full_listing (complete listing with all details)
        - key_selling_points (list of top 5 features)
        - target_tenant (who this unit is ideal for)
        """,
        expected_output="A JSON with complete listing content",
        agent=listing_writer
    )

def create_platform_strategy_task(vacancy: dict) -> Task:
    return Task(
        description=f"""
        Using the listing from the previous task, create a platform distribution 
        strategy for this vacancy:
        
        Property: {vacancy['property_name']}
        Unit: {vacancy['unit']}
        Rent: {vacancy['rent']}
        Target Tenant: (use result from previous task)
        
        Consider these platforms:
        Zillow, Trulia, Apartments.com, Facebook Marketplace, Craigslist, 
        LinkedIn (for corporate tenants), Instagram (for young professionals)
        
        Return a JSON with:
        - recommended_platforms (list with reasoning for each)
        - posting_schedule (when to post on each)
        - budget_recommendation (free vs paid listings)
        - estimated_time_to_fill (in days)
        - tips (platform specific tips for this listing)
        """,
        expected_output="A JSON platform distribution strategy",
        agent=platform_strategist
    )

def create_vacancy_analysis_task(vacancy: dict) -> Task:
    return Task(
        description=f"""
        Analyze this vacancy situation and provide recommendations using 
        the listing and platform strategy from previous tasks:
        
        Property: {vacancy['property_name']}
        Unit: {vacancy['unit']}
        Rent: {vacancy['rent']}
        Days Vacant: {vacancy.get('days_vacant', 0)}
        Previous Tenant: {vacancy.get('previous_tenant_reason', 'New vacancy')}
        
        Return a JSON with:
        - vacancy_cost_per_day (daily income loss)
        - urgency_level (LOW/MEDIUM/HIGH/CRITICAL)
        - pricing_assessment (is rent competitive)
        - recommended_actions (prioritized list)
        - risk_factors (what could delay filling this unit)
        - success_probability (percentage chance of filling within 30 days)
        """,
        expected_output="A comprehensive vacancy analysis JSON",
        agent=vacancy_analyst
    )
