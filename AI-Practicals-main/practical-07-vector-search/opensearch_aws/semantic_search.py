"""Run semantic vector search in OpenSearch."""

# Import the SentenceTransformer library to convert our text query into a vector
from sentence_transformers import SentenceTransformer

# Import the authenticated client generator and the index name
from opensearch_aws.create_index import INDEX_NAME, create_client

# We MUST use the exact same model we used to index the data.
# If we used a different model, the vector dimensions and semantic meaning
# wouldn't align, resulting in gibberish search results.
MODEL_NAME = "all-MiniLM-L6-v2"


def main() -> None:
    """Execute semantic vector similarity search."""

    # Initialize the ML model. (Since we ran this previously, the weights
    # are likely cached locally, so this will load very quickly).
    model = SentenceTransformer(MODEL_NAME)

    # Initialize the secure, SigV4-authenticated OpenSearch client
    client = create_client()

    # Define the search string and encode it into a vector.
    # Note: model.encode() takes a list of strings and returns a list of vectors.
    # Because we are only passing one query ["AI in hospitals"], we append [0]
    # to extract just that first, single vector from the resulting batch.
    query_embedding = model.encode(["AI in hospitals"])[0]

    # Construct the Vector Search query using OpenSearch's k-NN Query DSL
    query = {
        # 'size' determines the maximum number of final results OpenSearch will return to us
        "size": 5,
        "query": {
            # We use the specialized 'knn' query type instead of the traditional 'match' query
            "knn": {
                # Target the specific field where we stored our vectors during ingestion
                "embedding": {
                    # Pass in the query vector. We must use .tolist() to convert it
                    # from a NumPy array to a standard JSON-serializable Python list of floats.
                    "vector": query_embedding.tolist(),
                    # 'k' is the number of "nearest neighbors" the algorithm should
                    # calculate and retrieve from the underlying vector graph (HNSW).
                    "k": 5,
                }
            }
        },
    }

    # Execute the semantic search against the OpenSearch cluster
    response = client.search(
        index=INDEX_NAME,  # Limit the search to our specific vector index
        body=query,  # Pass in the k-NN Query DSL defined above
    )

    # The 'hits' array will contain the top 5 most semantically similar documents,
    # scored by how close their vectors are to our query vector.
    hits = response["hits"]["hits"]

    print("\nSemantic Search Results:\n")

    for rank, hit in enumerate(hits, start=1):
        text = hit["_source"]["text"]
        score = hit["_score"]

        print(f"{rank}. {text}")
        print(f"   Score: {score:.4f}\n")


# Standard Python idiom ensuring the code runs only when executed as a script directly
if __name__ == "__main__":
    main()
