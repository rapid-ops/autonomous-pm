from crewai import Agent
from langchain_openai import ChatOpenAI
from config.settings import GROQ_API_KEY, OPENAI_API_BASE, GROQ_MODEL

llm = ChatOpenAI(
    model=GROQ_MODEL,
    openai_api_key=GROQ_API_KEY,
    openai_api_base=OPENAI_API_BASE
)

lease_monitor = Agent(
    role="Lease Monitor",
    goal="Track all lease expiration dates and flag leases requiring immediate attention",
    backstory="""You are a meticulous lease administration specialist who never 
    lets a lease slip through the cracks. You monitor every lease in the portfolio, 
    flag upcoming expirations well in advance, and ensure property managers always 
    have time to act before a lease expires. Your tracking is always accurate.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

renewal_agent = Agent(
    role="Renewal Agent",
    goal="Generate personalized lease renewal offers and communications for tenants",
    backstory="""You are a tenant retention specialist who knows that keeping a 
    good tenant is always better than finding a new one. You craft renewal offers 
    that feel personal and fair. You highlight the value of staying, address 
    common objections, and make the renewal process as easy as possible for 
    the tenant.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

lease_document_agent = Agent(
    role="Lease Document Agent",
    goal="Generate accurate lease summaries and document checklists for new and renewing tenants",
    backstory="""You are a property legal documentation specialist who ensures 
    every lease transaction has the right paperwork. You generate clear lease 
    summaries that tenants actually understand, create document checklists, 
    and flag any missing information before it becomes a problem.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
