"""
Initialize Bedrock embeddings.
"""

# Import embeddings
# Import Bedrock client
from app.core.aws_clients import bedrock_client

# Import config
from app.core.config import BEDROCK_EMBED_MODEL
from langchain_aws import BedrockEmbeddings

# Create embedding model
embedding_model = BedrockEmbeddings(client=bedrock_client, model_id=BEDROCK_EMBED_MODEL)
