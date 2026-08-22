"""
Application configuration variables.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# AWS credentials
AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

# S3 bucket
S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "")

# Bedrock embedding model (Nova multimodal: 256, 384, 1024, or 3072)
BEDROCK_EMBED_MODEL: str = os.getenv("BEDROCK_EMBED_MODEL", "")
BEDROCK_EMBED_DIMENSION: int = int(os.getenv("BEDROCK_EMBED_DIMENSION", "1024"))
BEDROCK_LLM_MODEL: str = os.getenv("BEDROCK_LLM_MODEL", "")

# OpenSearch: "aws" (Serverless) or "local" (Docker / self-hosted)
OPENSEARCH_MODE: str = os.getenv("OPENSEARCH_MODE", "aws").lower()
OPENSEARCH_COLLECTION_NAME: str = os.getenv(
    "OPENSEARCH_COLLECTION_NAME", "rag-serverless"
)
OPENSEARCH_INDEX: str = os.getenv("OPENSEARCH_INDEX", "rag-index")
OPENSEARCH_HOST: str = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT: int = int(os.getenv("OPENSEARCH_PORT", "9200"))
OPENSEARCH_USER: str = os.getenv("OPENSEARCH_USER", "")
OPENSEARCH_PASSWORD: str = os.getenv("OPENSEARCH_PASSWORD", "")
OPENSEARCH_USE_SSL: bool = os.getenv("OPENSEARCH_USE_SSL", "false").lower() == "true"

# PostgreSQL
POSTGRES_URL: str = os.getenv("DATABASE_URL", os.getenv("POSTGRES_URL", ""))
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "milestone_3")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "rag_user")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "rag_pass")

# Agent safety limits
AGENT_MAX_STEPS: int = int(os.getenv("AGENT_MAX_STEPS", "8"))
AGENT_MAX_SQL_ROWS: int = int(os.getenv("AGENT_MAX_SQL_ROWS", "100"))

# LangFuse tracing
LANGFUSE_PUBLIC_KEY: str = os.getenv("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY: str = os.getenv("LANGFUSE_SECRET_KEY", "")
LANGFUSE_HOST: str = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
LANGFUSE_ENABLED: bool = os.getenv("LANGFUSE_ENABLED", "true").lower() == "true"


def is_local_opensearch() -> bool:
    return OPENSEARCH_MODE == "local"


def postgres_dsn() -> str:
    """Build a PostgreSQL DSN from URL or discrete env vars."""
    if POSTGRES_URL:
        return POSTGRES_URL
    return (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
