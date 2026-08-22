"""
Application configuration variables.
"""

# Import os module
import os

# Import dotenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS credentials
AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")

AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")

AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

# S3 bucket
S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "")

# Bedrock embedding model
BEDROCK_EMBED_MODEL: str = os.getenv("BEDROCK_EMBED_MODEL", "")

# Bedrock LLM model
BEDROCK_LLM_MODEL: str = os.getenv("BEDROCK_LLM_MODEL", "")

# OpenSearch collection
OPENSEARCH_COLLECTION_NAME: str = os.getenv(
    "OPENSEARCH_COLLECTION_NAME", "rag-serverless"
)

# OpenSearch index
OPENSEARCH_INDEX: str = os.getenv("OPENSEARCH_INDEX", "rag-index")
