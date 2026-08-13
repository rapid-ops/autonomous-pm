from crewai import Agent
from langchain_openai import ChatOpenAI
from config.settings import GROQ_API_KEY, OPENAI_API_BASE, GROQ_MODEL

llm = ChatOpenAI(
    model=GROQ_MODEL,
    openai_api_key=GROQ_API_KEY,
    openai_api_base=OPENAI_API_BASE
)

listing_writer = Agent(
    role="Listing Writer",
    goal="Write compelling, accurate and platform optimized rental listings that attract high quality tenants",
    backstory="""You are an expert real estate copywriter who has written thousands 
    of rental listings. You know exactly what words attract serious tenants and 
    what details they care about. Your listings always highlight the best features, 
    set accurate expectations, and drive inquiries from qualified prospects.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

platform_strategist = Agent(
    role="Platform Strategist",
    goal="Determine the best platforms to post each vacancy on and create a distribution strategy",
    backstory="""You are a digital marketing specialist focused on rental properties. 
    You know which platforms attract which types of tenants, what posting schedules 
    work best, and how to maximize visibility for each listing. You create distribution 
    plans that fill vacancies fast.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

vacancy_analyst = Agent(
    role="Vacancy Analyst",
    goal="Analyze vacancy performance and provide recommendations to reduce time to fill",
    backstory="""You are a property performance analyst who tracks how quickly 
    vacancies are filled and why some take longer than others. You identify 
    pricing issues, listing quality problems, and platform gaps. Your recommendations 
    consistently reduce vacancy periods and increase rental income.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
