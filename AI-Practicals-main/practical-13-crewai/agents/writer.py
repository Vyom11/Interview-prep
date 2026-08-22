from crewai import Agent
from llm.bedrock_llm import llm

writer = Agent(
    role="Writer",
    goal="Create a clean and structured markdown summary from research findings.",
    backstory="You are a professional technical writer.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
