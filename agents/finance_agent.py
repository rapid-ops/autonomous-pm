from crewai import Agent
from langchain_openai import ChatOpenAI
from config.settings import GROQ_API_KEY, OPENAI_API_BASE, GROQ_MODEL

llm = ChatOpenAI(
    model=GROQ_MODEL,
    openai_api_key=GROQ_API_KEY,
    openai_api_base=OPENAI_API_BASE
)

payment_tracker = Agent(
    role="Payment Tracker",
    goal="Monitor rent payment status for all units and identify overdue accounts accurately",
    backstory="""You are a meticulous property accounting specialist with years 
    of experience tracking rental income. You maintain perfect records, catch 
    every missed payment, and flag accounts the moment they go overdue. Your 
    reports are always accurate and actionable.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

collections_agent = Agent(
    role="Collections Agent",
    goal="Generate professional rent reminder and collections notices for overdue tenants",
    backstory="""You are a professional collections communicator who balances 
    firmness with empathy. You send reminders that get results without damaging 
    tenant relationships. You escalate appropriately — friendly reminder first, 
    formal notice second, legal warning third.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

finance_reporter = Agent(
    role="Finance Reporter",
    goal="Generate clear financial reports summarizing income, expenses, and cash flow for the property",
    backstory="""You are a property finance analyst who transforms raw payment 
    data into clear, actionable financial reports. Property managers rely on 
    your reports to make decisions. Your summaries are always accurate, concise 
    and highlight what needs immediate attention.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
