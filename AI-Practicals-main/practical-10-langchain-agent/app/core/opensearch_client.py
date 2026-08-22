"""
Initialize OpenSearch Serverless client.
"""

# Import time
import time

# Import boto3
import boto3

# Import config
from app.core.config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    OPENSEARCH_COLLECTION_NAME,
)

# Import OpenSearch
from opensearchpy import OpenSearch, RequestsHttpConnection

# Import AWS4Auth
from requests_aws4auth import AWS4Auth

# Create OpenSearch Serverless boto client
serverless_client = boto3.client(
    service_name="opensearchserverless", region_name=AWS_REGION
)

print("Fetching OpenSearch collection details...")

# Maximum retries
MAX_RETRIES = 30

# Retry counter
retry_count = 0

# Initialize host
host = None

# Wait until collection becomes active
while retry_count < MAX_RETRIES:

    # Fetch collection details
    response = serverless_client.batch_get_collection(
        names=[OPENSEARCH_COLLECTION_NAME]
    )

    # Ensure collection exists
    if not response["collectionDetails"]:

        print("Collection not found.")

        time.sleep(10)

        retry_count += 1

        continue

    # Extract details
    collection_details = response["collectionDetails"][0]

    # Get status
    status = collection_details["status"]

    print(f"Collection status: {status}")

    # Check if active
    if status == "ACTIVE":

        # Safely get endpoint
        host = collection_details.get("collectionEndpoint")

        # Break if endpoint exists
        if host:

            break

    # Wait before retry
    time.sleep(10)

    retry_count += 1

# Raise error if endpoint missing
if not host:

    raise Exception("Collection endpoint not available.")

# Remove https://
host = host.replace("https://", "")

print(f"OpenSearch host: {host}")

# Create AWS auth
awsauth = AWS4Auth(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, "aoss")

# Create OpenSearch client
opensearch_client = OpenSearch(
    hosts=[{"host": host, "port": 443}],
    # AWS authentication
    http_auth=awsauth,
    # Enable SSL
    use_ssl=True,
    # Verify SSL certificates
    verify_certs=True,
    # Connection class
    connection_class=RequestsHttpConnection,
)

print("OpenSearch client initialized!")
