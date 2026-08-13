from crewai import Task
from agents.marketing_agent import ad_copywriter, campaign_strategist, performance_analyst

def create_ad_copy_task(campaign: dict) -> Task:
    return Task(
        description=f"""
        Write high converting ad copy for this rental property campaign:
        
        Property: {campaign['property_name']}
        Unit Type: {campaign['unit_type']}
        Rent: {campaign['rent']}
        Location: {campaign['location']}
        Key Features: {campaign['features']}
        Target Tenant: {campaign['target_tenant']}
        Campaign Goal: {campaign['goal']}
        
        Return a JSON with:
        - primary_headline (under 10 words, attention grabbing)
        - subheadline (one sentence expanding on headline)
        - body_copy (3 to 4 sentences, speaks to pain and solution)
        - call_to_action (action phrase for the button)
        - facebook_post_copy (complete post for organic sharing)
        - instagram_caption (with relevant hashtags)
        - hook_variations (3 alternative headlines to test)
        """,
        expected_output="A JSON with complete ad copy for all placements",
        agent=ad_copywriter
    )

def create_campaign_strategy_task(campaign: dict) -> Task:
    return Task(
        description=f"""
        Design a complete Facebook and Instagram ad campaign strategy using 
        the ad copy from the previous task:
        
        Property: {campaign['property_name']}
        Unit Type: {campaign['unit_type']}
        Rent: {campaign['rent']}
        Location: {campaign['location']}
        Monthly Ad Budget: {campaign['monthly_budget']}
        Target Tenant: {campaign['target_tenant']}
        Campaign Goal: {campaign['goal']}
        
        Return a JSON with:
        - campaign_objective (awareness/traffic/leads)
        - target_audience (age, interests, behaviors, location radius)
        - ad_placements (where to run — feed, stories, reels, messenger)
        - budget_breakdown (how to split budget across placements)
        - daily_budget (recommended daily spend)
        - campaign_duration (how many days to run)
        - expected_results (estimated leads, cost per lead, impressions)
        - ab_test_plan (what to test first)
        - optimization_schedule (when to review and adjust)
        """,
        expected_output="A complete campaign strategy JSON",
        agent=campaign_strategist
    )

def create_performance_analysis_task(campaign: dict) -> Task:
    return Task(
        description=f"""
        Analyze this ad campaign performance and provide optimization recommendations:
        
        Property: {campaign['property_name']}
        Campaign Duration: {campaign.get('days_running', 0)} days
        Budget Spent: {campaign.get('budget_spent', 0)}
        Impressions: {campaign.get('impressions', 0)}
        Clicks: {campaign.get('clicks', 0)}
        Leads Generated: {campaign.get('leads', 0)}
        Cost Per Lead: {campaign.get('cost_per_lead', 0)}
        Lead Quality: {campaign.get('lead_quality', 'Unknown')}
        Vacancies Filled: {campaign.get('vacancies_filled', 0)}
        
        Return a JSON with:
        - overall_rating (EXCELLENT/GOOD/FAIR/POOR)
        - key_metrics_analysis (what each metric means for this campaign)
        - what_is_working (list of positives)
        - what_needs_fixing (list of issues with severity)
        - immediate_actions (changes to make today)
        - budget_recommendation (increase, decrease, or maintain)
        - projected_improvement (expected results after optimization)
        - pause_recommendation (true/false — should campaign be paused)
        """,
        expected_output="A performance analysis and optimization JSON",
        agent=performance_analyst
    )
