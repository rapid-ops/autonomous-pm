from crewai import Agent
from langchain_openai import ChatOpenAI
from config.settings import GROQ_API_KEY, OPENAI_API_BASE, GROQ_MODEL

llm = ChatOpenAI(
    model=GROQ_MODEL,
    openai_api_key=GROQ_API_KEY,
    openai_api_base=OPENAI_API_BASE
)

message_classifier = Agent(
    role="Message Classifier",
    goal="Read tenant messages and classify them accurately into the correct category",
    backstory="""You are an expert property management coordinator who has handled 
    thousands of tenant communications. You instantly recognize whether a message 
    is a maintenance request, rent question, complaint, lease question, or general 
    inquiry. Your classification is always accurate.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

tenant_responder = Agent(
    role="Tenant Responder",
    goal="Draft professional, empathetic and helpful responses to tenant messages",
    backstory="""You are a seasoned property manager known for excellent tenant 
    relations. You respond to every message with professionalism and empathy. 
    For maintenance issues you are urgent and reassuring. For complaints you are 
    calm and solution focused. For questions you are clear and informative.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

escalation_agent = Agent(
    role="Escalation Manager",
    goal="Identify messages that require immediate property manager attention and create escalation alerts",
    backstory="""You are a senior property management supervisor. You identify 
    critical situations — emergency maintenance, legal threats, safety issues, 
    or hostile tenants — that cannot wait for standard response times and must 
    be escalated immediately to the property manager.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
