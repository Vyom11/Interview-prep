import os

from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse

load_dotenv()

MODEL_ID = os.getenv("BEDROCK_MODEL_ID")
AWS_REGION = os.getenv("AWS_REGION")

llm = ChatBedrockConverse(model=MODEL_ID, region_name=AWS_REGION, temperature=0)
