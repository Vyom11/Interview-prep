"""Run hybrid keyword + semantic search."""

# Import the library to convert our text query into a vector
from sentence_transformers import SentenceTransformer

# Import the authenticated client generator and the index name
from opensearch_aws.create_index import INDEX_NAME, create_client

# Use the same model as ingestion to ensure our vectors inhabit the same dimensional space
MODEL_NAME = "all-MiniLM-L6-v2"


def main() -> None:
    """Execute hybrid search query."""

    # Initialize the Machine Learning model
    model = SentenceTransformer(MODEL_NAME)

    # Initialize the secure, SigV4-authenticated OpenSearch client
    client = create_client()

    # Encode the full natural language query into a 384-dimensional vector.
    # We append [0] to extract the single vector from the batch output.
    query_embedding = model.encode(["AI healthcare systems"])[0]

    # Construct the Hybrid Search query using OpenSearch's Compound Query DSL
    query = {
        "size": 5,  # Return the top 5 results overall
        "query": {
            # 'bool' (Boolean) is a compound query that allows us to combine multiple queries together
            "bool": {
                # 'should' acts as a logical OR.
                # Documents that match ANY of the queries inside this list will be returned.
                # Documents that match BOTH queries will receive a massive score boost.
                "should": [
                    # --- QUERY 1: LEXICAL (KEYWORD) SEARCH ---
                    {
                        "match": {
                            # Look for the exact word "healthcare" in the raw text.
                            # This uses the BM25 algorithm (exact term frequency).
                            "text": "healthcare"
                        }
                    },
                    # --- QUERY 2: SEMANTIC (VECTOR) SEARCH ---
                    {
                        "knn": {
                            # Look for conceptual similarity based on the mathematical vector.
                            # This uses the HNSW graph algorithm (cosine/euclidean distance).
                            "embedding": {
                                "vector": query_embedding.tolist(),
                                "k": 5,
                            }
                        }
                    },
                ]
            }
        },
    }

    # Execute the hybrid search against the OpenSearch cluster
    response = client.search(
        index=INDEX_NAME,
        body=query,
    )

    # The documents in the 'hits' array are ranked based on a combined score of
    # both the BM25 text match AND the k-NN vector similarity.
    hits = response["hits"]["hits"]

    print("\nHybrid Search Results:\n")

    for rank, hit in enumerate(hits, start=1):
        sentence = hit["_source"]["text"]
        score = hit["_score"]

        print(f"{rank}. {sentence}")
        print(f"   Combined Relevance Score: {score:.4f}\n")


# Standard Python idiom ensuring the code runs only when executed as a script directly
if __name__ == "__main__":
    main()
