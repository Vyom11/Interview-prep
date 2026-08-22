# Practical 13: CrewAI Multi-Agent Crew

## Objective

Build a 2-agent CrewAI workflow:
- Researcher Agent
- Writer Agent

The Researcher gathers information on a topic.
The Writer creates a structured markdown summary.

## Technologies Used

- CrewAI
- Amazon Bedrock Nova
- LangChain AWS
- Python

## Run Project

```bash
pip install -r requirements.txt
aws configure
python3 main.py
```

## Output

Markdown report generated at:

```text
outputs/final_report.md
```
