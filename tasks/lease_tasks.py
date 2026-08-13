from crewai import Task
from agents.lease_agent import lease_monitor, renewal_agent, lease_document_agent

def create_lease_monitoring_task(portfolio: dict) -> Task:
    return Task(
        description=f"""
        Monitor and analyze all leases in this portfolio:
        
        Property: {portfolio['property_name']}
        Current Date: {portfolio['current_date']}
        Leases: {portfolio['leases']}
        
        For each lease evaluate:
        - Days until expiration
        - Renewal status
        - Action required
        
        Return a JSON with:
        - total_leases (int)
        - expiring_30_days (list of unit, tenant, expiry_date, days_remaining)
        - expiring_60_days (list of unit, tenant, expiry_date, days_remaining)
        - expiring_90_days (list of unit, tenant, expiry_date, days_remaining)
        - already_expired (list of unit, tenant, expiry_date, days_overdue)
        - renewals_in_progress (list)
        - action_required (prioritized list of what needs attention today)
        """,
        expected_output="A detailed JSON lease monitoring report",
        agent=lease_monitor
    )

def create_renewal_task(tenant: dict) -> Task:
    return Task(
        description=f"""
        Generate a personalized lease renewal offer for this tenant:
        
        Tenant Name: {tenant['name']}
        Unit: {tenant['unit']}
        Current Rent: {tenant['current_rent']}
        Proposed Rent: {tenant['proposed_rent']}
        Current Lease End: {tenant['lease_end']}
        Tenancy Duration: {tenant['tenancy_duration']}
        Payment History: {tenant['payment_history']}
        
        The renewal communication should:
        - Thank them for being a good tenant if payment history is good
        - Present the renewal offer clearly
        - Explain any rent increase fairly
        - Make next steps simple and clear
        - Create a sense of warmth and belonging
        
        Return a JSON with:
        - renewal_offer_letter (full personalized letter)
        - key_terms_summary (bullet points of what is changing)
        - next_steps (what tenant needs to do and by when)
        - incentive (suggest a retention incentive if rent increase is significant)
        """,
        expected_output="A JSON with complete renewal offer content",
        agent=renewal_agent
    )

def create_document_checklist_task(tenant: dict) -> Task:
    return Task(
        description=f"""
        Generate a lease document checklist and summary for this tenant transaction:
        
        Tenant Name: {tenant['name']}
        Unit: {tenant['unit']}
        Transaction Type: {tenant.get('transaction_type', 'RENEWAL')}
        Lease Start: {tenant.get('lease_start', 'TBD')}
        Lease End: {tenant.get('lease_end', 'TBD')}
        Monthly Rent: {tenant.get('proposed_rent', tenant.get('current_rent', 0))}
        
        Return a JSON with:
        - documents_required (list of every document needed)
        - documents_from_tenant (what tenant must provide)
        - documents_from_landlord (what property manager must provide)
        - lease_summary (plain English summary of key lease terms)
        - important_dates (list of critical dates and deadlines)
        - missing_information (anything needed to complete the transaction)
        """,
        expected_output="A complete document checklist and lease summary JSON",
        agent=lease_document_agent
    )
