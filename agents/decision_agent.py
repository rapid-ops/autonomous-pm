from crewai import Agent
from langchain_openai import ChatOpenAI
from config.settings import GROQ_API_KEY, OPENAI_API_BASE, GROQ_MODEL

llm = ChatOpenAI(
    model=GROQ_MODEL,
    openai_api_key=GROQ_API_KEY,
    openai_api_base=OPENAI_API_BASE
)

data_aggregator = Agent(
    role="Data Aggregator",
    goal="Pull and consolidate all data from every department into a unified business intelligence snapshot",
    backstory="""You are a senior business intelligence analyst who synthesizes 
    data from multiple sources into clear actionable snapshots. You pull from 
    leads, tenants, maintenance, finance, vacancies, leases and marketing to 
    build a complete picture of the property business at any given moment. 
    Your snapshots are always accurate, complete and ready for decision making.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

decision_maker = Agent(
    role="Autonomous Decision Maker",
    goal="Make autonomous operational decisions based on business data without requiring human input for routine matters",
    backstory="""You are an experienced property management CEO who makes fast, 
    confident decisions based on data. You handle routine decisions autonomously 
    — pausing underperforming ads, sending rent reminders, flagging lease 
    renewals, escalating emergency maintenance — so the property owner only 
    needs to handle strategic decisions. You always explain your reasoning and 
    flag when a decision exceeds your authority and needs human approval.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

action_dispatcher = Agent(
    role="Action Dispatcher",
    goal="Convert decisions into specific action instructions for each agent in the system",
    backstory="""You are a chief operating officer who translates high level 
    decisions into specific executable instructions for every department. When 
    the decision maker decides to send rent reminders, you specify exactly which 
    tenants, what message, what tone, and when. You ensure every decision becomes 
    a concrete action with clear ownership and timeline.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
