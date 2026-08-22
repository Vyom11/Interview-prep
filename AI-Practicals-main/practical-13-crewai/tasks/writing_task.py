from crewai import Task
from agents.writer import writer

writing_task = Task(
    description="""
    Use the research findings to create a structured markdown report.

    Include:
    - title
    - introduction
    - key concepts
    - advantages
    - challenges
    - applications
    - conclusion
    """,
    expected_output="A well-structured markdown report.",
    agent=writer,
    output_file="outputs/final_report.md"
)
