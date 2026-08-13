from crewai import Task
from agents.maintenance_agent import job_creator, priority_manager, status_updater

def create_job_order_task(request: dict) -> Task:
    return Task(
        description=f"""
        Create a detailed maintenance job order from this request:
        
        Tenant Name: {request['name']}
        Unit: {request['unit']}
        Issue: {request['issue']}
        Reported At: {request['reported_at']}
        Escalation Level: {request.get('escalation_level', 'NONE')}
        
        Return a JSON with:
        - job_id (format: JOB-YYYYMMDD-UNIT)
        - title (short description)
        - description (detailed what needs to be done)
        - location (unit and specific area)
        - materials_needed (list)
        - estimated_duration (in hours)
        - special_instructions (any safety or access notes)
        """,
        expected_output="A detailed JSON job order",
        agent=job_creator
    )

def create_priority_task(request: dict) -> Task:
    return Task(
        description=f"""
        Assess and assign priority to this maintenance request using the job order from the previous task:
        
        Tenant Name: {request['name']}
        Unit: {request['unit']}
        Issue: {request['issue']}
        Escalation Level: {request.get('escalation_level', 'NONE')}
        
        Priority levels:
        EMERGENCY: safety threat, flooding, fire risk, no heat in winter, gas leak
        HIGH: major inconvenience, appliance failure, hot water loss
        MEDIUM: standard repair, minor leak, broken fixture
        LOW: cosmetic, paint, minor wear
        
        Return a JSON with:
        - priority (EMERGENCY/HIGH/MEDIUM/LOW)
        - response_time (how soon technician should arrive)
        - reasoning (why this priority was assigned)
        - safety_risk (true/false)
        """,
        expected_output="A JSON with priority assessment",
        agent=priority_manager
    )

def create_status_update_task(request: dict) -> Task:
    return Task(
        description=f"""
        Generate a tenant status update for this maintenance request using the job order and priority from previous tasks:
        
        Tenant Name: {request['name']}
        Unit: {request['unit']}
        Issue: {request['issue']}
        
        The update should:
        - Confirm the request was received and logged
        - State the priority level in plain language
        - Give a realistic timeline for when someone will arrive
        - Tell them what to do or avoid in the meantime
        - Provide a job reference number
        
        Return only the message to send to the tenant.
        """,
        expected_output="A clear tenant status update message",
        agent=status_updater
    )
