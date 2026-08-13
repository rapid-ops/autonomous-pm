from crewai import Task
from agents.tenant_agent import message_classifier, tenant_responder, escalation_agent

def create_classification_task(message: dict) -> Task:
    return Task(
        description=f"""
        Classify this tenant message:
        
        Tenant Name: {message['name']}
        Unit: {message['unit']}
        Message: {message['message']}
        
        Return a JSON with:
        - category (MAINTENANCE/RENT/COMPLAINT/LEASE/GENERAL)
        - urgency (EMERGENCY/HIGH/MEDIUM/LOW)
        - summary (one sentence)
        - requires_escalation (true/false)
        """,
        expected_output="A JSON object with category, urgency, summary and requires_escalation",
        agent=message_classifier
    )

def create_response_task(message: dict) -> Task:
    return Task(
        description=f"""
        Draft a response to this tenant message using the classification from the previous task.
        
        Tenant Name: {message['name']}
        Unit: {message['unit']}
        Message: {message['message']}
        
        MAINTENANCE: reassuring, give timeline, log it
        RENT: clear, factual, reference payment details
        COMPLAINT: empathetic, solution focused, no blame
        LEASE: accurate, professional, invite follow up questions
        GENERAL: friendly, helpful, concise
        
        Return only the response message.
        """,
        expected_output="A professional response message to the tenant",
        agent=tenant_responder
    )

def create_escalation_task(message: dict) -> Task:
    return Task(
        description=f"""
        Review this tenant message and the classification from the previous tasks.
        
        Tenant Name: {message['name']}
        Unit: {message['unit']}
        Message: {message['message']}
        
        If requires_escalation is true, create an escalation alert for the property manager with:
        - alert_level (CRITICAL/HIGH)
        - reason (why this needs immediate attention)
        - recommended_action (what the property manager should do)
        - tenant_details (name and unit)
        
        If requires_escalation is false, return "NO_ESCALATION_NEEDED".
        """,
        expected_output="An escalation alert JSON or NO_ESCALATION_NEEDED",
        agent=escalation_agent
    )
