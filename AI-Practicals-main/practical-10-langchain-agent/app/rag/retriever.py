"""
Retriever configuration.
"""

# Import vector store
# Import config
from app.core.config import OPENSEARCH_INDEX

# Import auth and host
from app.core.opensearch_client import awsauth, host

# Import embeddings
from app.ingestion.embeddings import embedding_model
from langchain_community.vectorstores import OpenSearchVectorSearch

# Import connection
from opensearchpy import RequestsHttpConnection

# Create vector store
vector_store = OpenSearchVectorSearch(
    index_name=OPENSEARCH_INDEX,
    embedding_function=embedding_model,
    opensearch_url=f"https://{host}",
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
