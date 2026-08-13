import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import process_lead, process_tenant_message, process_maintenance_request, process_finance, process_vacancy, process_leases, run_ceo_report

def clear():
    os.system('clear')

def menu():
    clear()
    print("=" * 45)
    print("   AUTONOMOUS PROPERTY MANAGEMENT SYSTEM")
    print("=" * 45)
    print("1. Process New Lead")
    print("2. Handle Tenant Message")
    print("3. Log Maintenance Request")
    print("4. Run Finance Report")
    print("5. List Vacant Unit")
    print("6. Check Lease Status")
    print("7. Generate CEO Report")
    print("0. Exit")
    print("=" * 45)
    return input("Select option: ").strip()

def get_lead():
    clear()
    print("--- NEW LEAD ---")
    name = input("Prospect Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    message = input("Their Message: ")
    return {"name": name, "email": email, "phone": phone, "message": message}

def get_tenant_message():
    clear()
    print("--- TENANT MESSAGE ---")
    name = input("Tenant Name: ")
    unit = input("Unit: ")
    message = input("Message: ")
    return {"name": name, "unit": unit, "message": message}

def get_maintenance():
    clear()
    print("--- MAINTENANCE REQUEST ---")
    name = input("Tenant Name: ")
    unit = input("Unit: ")
    issue = input("Issue Description: ")
    return {"name": name, "unit": unit, "issue": issue, "reported_at": "Now", "escalation_level": "NONE"}

while True:
    choice = menu()
    if choice == "1":
        process_lead(get_lead())
    elif choice == "2":
        process_tenant_message(get_tenant_message())
    elif choice == "3":
        process_maintenance_request(get_maintenance())
    elif choice == "0":
        print("Exiting.")
        break
    else:
        print("Coming soon.")
    input("\nPress Enter to continue...")
