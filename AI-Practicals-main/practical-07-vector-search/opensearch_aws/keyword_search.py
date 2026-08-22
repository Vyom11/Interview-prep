"""Run keyword search in OpenSearch."""

# Import the authenticated client generator and the index name ("documents-index")
# This ensures we connect to the exact same Serverless collection securely.
from opensearch_aws.create_index import INDEX_NAME, create_client


def main() -> None:
    """Execute keyword search query."""

    # Initialize the secure, SigV4-authenticated OpenSearch client
    client = create_client()

    # Construct the search query using OpenSearch's Query DSL (Domain Specific Language).
    # This is standard JSON formatted specifically for OpenSearch/Elasticsearch.
    query = {
        "query": {
            # The 'match' query is the standard query for performing a full-text search.
            "match": {
                # We are telling the database to look inside the "text" field
                # (which we defined in our mapping previously) for the words "healthcare AI"
                "text": "healthcare AI"
            }
        }
    }

    # Execute the search against the OpenSearch cluster
    response = client.search(
        index=INDEX_NAME,  # Limit the search to our specific index
        body=query,  # Pass in the Query DSL defined above
    )

    # This response will contain a 'hits' array, which includes the matching
    # documents, their IDs, and a '_score' indicating how well they matched.
    hits = response["hits"]["hits"]

    print("\nKeyword Search Results:\n")

    for rank, hit in enumerate(hits, start=1):
        text = hit["_source"]["text"]
        score = hit["_score"]

        print(f"{rank}. {text}")
        print(f"   Score: {score:.4f}\n")


# Standard Python idiom ensuring the code runs only when executed as a script directly
if __name__ == "__main__":
    main()
