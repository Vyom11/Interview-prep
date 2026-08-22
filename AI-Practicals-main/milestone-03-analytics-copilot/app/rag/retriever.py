"""
Retriever configuration (lazy — connects on first RAG query, not at import).
"""

from app.core.config import OPENSEARCH_INDEX
from app.core.opensearch_client import get_vector_store_kwargs
from app.ingestion.embeddings import embedding_model
from langchain_community.vectorstores import OpenSearchVectorSearch

_retriever = None


def get_retriever():
    global _retriever
    if _retriever is None:
        vector_store = OpenSearchVectorSearch(
            index_name=OPENSEARCH_INDEX,
            embedding_function=embedding_model,
            **get_vector_store_kwargs(),
        )
        _retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 15},
        )
    return _retriever


class _RetrieverProxy:
    def invoke(self, *args, **kwargs):
        return get_retriever().invoke(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(get_retriever(), name)


retriever = _RetrieverProxy()
