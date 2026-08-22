import os

from dotenv import load_dotenv

load_dotenv()

MODEL_ID = os.getenv("BEDROCK_MODEL_ID")

# CrewAI-compatible Bedrock model string
llm = f"bedrock/{MODEL_ID}"
