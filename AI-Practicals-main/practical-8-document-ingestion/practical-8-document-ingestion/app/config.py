import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    bucket_name: str = os.getenv("S3_BUCKET_NAME", "")
    opensearch_host: str = os.getenv("OPENSEARCH_HOST", "")
    opensearch_index: str = os.getenv("OPENSEARCH_INDEX", "documents")
    bedrock_model_id: str = os.getenv(
        "BEDROCK_MODEL_ID",
        "amazon.titan-embed-text-v2:0"
    )
    embedding_dimension: int = int(
        os.getenv("EMBEDDING_DIMENSION", "512")
    )


settings = Settings()