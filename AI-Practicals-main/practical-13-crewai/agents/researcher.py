from crewai import Agent
from llm.bedrock_llm import llm

researcher = Agent(
    role="Researcher",
    goal="Gather detailed and accurate information about the given topic.",
    backstory="You are an expert research analyst who gathers structured information.",
    verbose=True,
    allow_delegation=True,
    llm=llm
)
