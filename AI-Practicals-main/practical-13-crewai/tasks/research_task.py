from crewai import Task
from agents.researcher import researcher

research_task = Task(
    description="""
    Research the topic:
    '{topic}'

    Collect:
    - overview
    - important concepts
    - advantages
    - challenges
    - real-world applications

    Return detailed notes.
    """,
    expected_output="Detailed research notes about the topic.",
    agent=researcher
)
