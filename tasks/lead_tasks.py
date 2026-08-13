from crewai import Task
from agents.lead_agent import lead_qualifier, response_drafter

def create_qualification_task(lead: dict) -> Task:
    return Task(
        description=f"""
        Analyze this property inquiry and score it:
        
        Name: {lead['name']}
        Email: {lead['email']}
        Phone: {lead['phone']}
        Message: {lead['message']}
        
        Return a JSON with:
        - score (0-100)
        - status (HOT/WARM/COLD)
        - reasoning (one sentence)
        - key_signals (list of what made you score it this way)
        """,
        expected_output="A JSON object with score, status, reasoning and key_signals",
        agent=lead_qualifier
    )

def create_response_task(lead: dict) -> Task:
    return Task(
        description=f"""
        Draft a response to this property inquiry.
        Use the qualification result from the previous task to determine tone and depth.
        
        Name: {lead['name']}
        Message: {lead['message']}
        
        HOT lead: warm, urgent, book a viewing immediately
        WARM lead: informative, answer their questions, invite next step
        COLD lead: brief, polite, leave door open
        
        Return only the response message, no subject line.
        """,
        expected_output="A professional response message to the prospect",
        agent=response_drafter
    )
