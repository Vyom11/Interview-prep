"""Create OpenSearch vector index."""

import os

import boto3

# Used to load environment variables from a .env file (e.g., region, endpoints)
from dotenv import load_dotenv

# OpenSearch's official Python client and a connection class to handle HTTP requests
from opensearchpy import OpenSearch, RequestsHttpConnection

# AWS4Auth handles the complex AWS Signature Version 4 (SigV4) signing process
from requests_aws4auth import AWS4Auth

# The name of the index (think of an "index" as a "table" in a relational database)
INDEX_NAME = "documents-index"

# Load the environment variables securely from the .env file
load_dotenv()


def create_client() -> OpenSearch:
    """Create authenticated OpenSearch client."""

    # Retrieve AWS Region and the specific Collection Endpoint created in the previous script
    region = os.getenv("AWS_REGION")
    host = os.getenv("OPENSEARCH_COLLECTION_ENDPOINT")

    # Initialize a boto3 session to fetch the active AWS credentials
    session = boto3.Session()
    credentials = session.get_credentials()
    # Create the AWS4Auth object.
    # This automatically signs our HTTP requests with AWS credentials.
    # Note: The service name 'aoss' stands for Amazon OpenSearch Serverless.
    auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        "aoss",  # Service identifier for OpenSearch Serverless
        session_token=credentials.token,  # Token is required if using temporary IAM roles
    )

    # Initialize and return the OpenSearch client
    return OpenSearch(
        # The host URL cannot include "https://", so we strip it out
        hosts=[{"host": host.replace("https://", ""), "port": 443}],
        # Inject the AWS SigV4 authentication object
        http_auth=auth,
        # Force secure connections
        use_ssl=True,
        verify_certs=True,
        # Use the Requests HTTP connection class so our auth object works correctly
        connection_class=RequestsHttpConnection,
    )


def main() -> None:
    """Create knn_vector index."""

    # Get the authenticated client
    client = create_client()

    # Define the configuration (Settings) and schema (Mappings) for our new index
    mapping = {
        "settings": {
            # This setting tells OpenSearch to enable the k-Nearest Neighbor (k-NN) plugin
            # which is required to perform vector similarity searches.
            "index.knn": True
        },
        "mappings": {
            # Define the fields (columns) that each document will contain
            "properties": {
                # A standard field to hold the raw text data
                "text": {"type": "text"},
                # A specialized field to hold the mathematical vector representation of the text
                "embedding": {
                    "type": "knn_vector",
                    # The dimension size MUST match the output of the embedding model you are using.
                    # 384 is a very common dimension size for lightweight, efficient models
                    # like 'all-MiniLM-L6-v2' from HuggingFace.
                    "dimension": 384,
                },
            }
        },
    }

    # Make the API call to OpenSearch to create the index
    response = client.indices.create(
        index=INDEX_NAME,
        body=mapping,
    )

    # Print the response from the server (usually a JSON confirming creation)
    print(response)


# Standard Python idiom ensuring the code runs only when executed as a script directly
if __name__ == "__main__":
    main()
