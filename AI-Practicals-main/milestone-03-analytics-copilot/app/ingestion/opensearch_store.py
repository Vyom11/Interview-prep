"""
Store embeddings in OpenSearch (Serverless or local).
"""

from app.core.config import OPENSEARCH_INDEX
from app.core.opensearch_client import get_vector_store_kwargs
from app.ingestion.embeddings import embedding_model
from langchain_community.vectorstores import OpenSearchVectorSearch


def store_documents(chunks):
    """Store chunks in vector database."""
    vector_store = OpenSearchVectorSearch.from_documents(
        documents=chunks,
        embedding=embedding_model,
        index_name=OPENSEARCH_INDEX,
        **get_vector_store_kwargs(),
    )
    return vector_store
