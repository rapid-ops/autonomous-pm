from crewai import Agent
from langchain_openai import ChatOpenAI
from config.settings import GROQ_API_KEY, OPENAI_API_BASE, GROQ_MODEL

llm = ChatOpenAI(
    model=GROQ_MODEL,
    openai_api_key=GROQ_API_KEY,
    openai_api_base=OPENAI_API_BASE
)

lead_qualifier = Agent(
    role="Lead Qualifier",
    goal="Analyze incoming property inquiries and determine how serious the prospect is",
    backstory="""You are an expert property management analyst with years of experience 
    identifying serious tenants from time wasters. You analyze every inquiry carefully 
    and score it based on urgency, specificity, and intent.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

response_drafter = Agent(
    role="Response Drafter",
    goal="Draft professional and personalized responses to property inquiries based on their score",
    backstory="""You are a professional property manager communicator. You craft responses 
    that are warm for HOT leads, informative for WARM leads, and brief for COLD leads. 
    Every response moves the conversation forward.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
