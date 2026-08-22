from crewai import Crew, Process

from agents.researcher import researcher
from agents.writer import writer

from tasks.research_task import research_task
from tasks.writing_task import writing_task

topic = input("Enter a research topic: ")

research_task.description = (
    research_task.description.replace("{topic}", topic)
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()

print("\nFINAL OUTPUT:\n")
print(result)

print("\nMarkdown report saved to outputs/final_report.md")
