from app.config import settings
from app.embeddings import get_embeddings_client
from app.opensearch_client import get_opensearch_client


def semantic_search(query: str, top_k: int = 3) -> dict:
    """Perform semantic search."""

    embeddings = get_embeddings_client()

    query_vector = embeddings.embed_text(query)

    search_body = {
        "size": top_k,
        "query": {"knn": {"embedding": {"vector": query_vector, "k": top_k}}},
    }

    client = get_opensearch_client()

    return client.search(index=settings.opensearch_index, body=search_body)
