"""
Store embeddings in OpenSearch Serverless.
"""

# Import vector store
# Import config
from app.core.config import OPENSEARCH_INDEX

# Import OpenSearch auth
from app.core.opensearch_client import awsauth, host

# Import embeddings
from app.ingestion.embeddings import embedding_model
from langchain_community.vectorstores import OpenSearchVectorSearch

# Import connection
from opensearchpy import RequestsHttpConnection


def store_documents(chunks):
    """
    Store chunks in vector database.
    """

    # Create vector store
    vector_store = OpenSearchVectorSearch.from_documents(
        documents=chunks,
        embedding=embedding_model,
        opensearch_url=f"https://{host}",
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        index_name=OPENSEARCH_INDEX,
    )

    return vector_store
