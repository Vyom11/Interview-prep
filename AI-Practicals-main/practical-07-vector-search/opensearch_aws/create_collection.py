"""Create OpenSearch Serverless collection and policies."""

import time  # Required to pause the script (sleep) while waiting for AWS to provision resources

import boto3  # The official AWS SDK for Python used to interact with AWS services
from dotenv import (
    load_dotenv,  # Used to securely load environment variables from a .env file
)

# Define the name of our OpenSearch Serverless collection as a constant
COLLECTION_NAME = "vector-search-demo"

# Load environment variables (e.g., AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
# This prevents hardcoding sensitive credentials directly in the code.
load_dotenv()


def main() -> None:
    """Create OpenSearch Serverless collection."""

    # Initialize the boto3 client specifically for the 'opensearchserverless' service.
    # It will automatically use the credentials loaded by dotenv.
    client = boto3.client("opensearchserverless")

    # Define the Encryption Policy.
    # OpenSearch Serverless requires an encryption policy before creating a collection.
    # This policy tells AWS to encrypt the "vector-search-demo" collection using an AWS-owned KMS key.
    encryption_policy = {
        "Rules": [
            {
                "Resource": [f"collection/{COLLECTION_NAME}"],
                "ResourceType": "collection",
            }
        ],
        "AWSOwnedKey": True,  # Use default AWS key instead of a custom Customer Managed Key (CMK)
    }

    # Define the Network Policy.
    # This dictates from where the collection can be accessed.
    # Here, it is set to allow public access to the "vector-search-demo" collection.
    network_policy = [
        {
            "Rules": [
                {
                    "Resource": [f"collection/{COLLECTION_NAME}"],
                    "ResourceType": "collection",
                }
            ],
            "AllowFromPublic": True,  # Exposes the collection endpoint publicly
        }
    ]

    # --- POLICY CREATION (COMMENTED OUT) ---
    # In AWS OpenSearch Serverless, you MUST have matching network and encryption
    # policies in place BEFORE you create the collection.
    # These lines are commented out, which assumes either:
    # 1. You already ran this once and the policies exist in your AWS account.
    # 2. You created the policies manually via the AWS Console.

    # client.create_security_policy(
    #     name="vector-encryption-policy",
    #     type="encryption",
    #     policy=json.dumps(encryption_policy),
    # )

    # client.create_security_policy(
    #     name="vector-network-policy",
    #     type="network",
    #     policy=json.dumps(network_policy),
    # )

    # Initiate the creation of the OpenSearch Serverless collection.
    # The type is set to 'VECTORSEARCH', optimizing it for storing and querying
    # high-dimensional vector embeddings (used in AI/ML and RAG applications).
    response = client.create_collection(
        name=COLLECTION_NAME,
        type="VECTORSEARCH",
    )

    # The creation API is asynchronous. It returns a response immediately with the ID,
    # but the collection isn't ready to use yet. We extract the ID to monitor it.
    collection_id = response["createCollectionDetail"]["id"]

    print(f"Creating collection: {collection_id}")

    # --- POLLING LOOP ---
    # OpenSearch Serverless collections take several minutes to provision.
    # We use an infinite loop to check the status repeatedly.
    while True:
        # Fetch the current details of the newly created collection using its ID
        status_response = client.batch_get_collection(ids=[collection_id])

        # Extract the 'status' field from the response
        # Expected statuses include 'CREATING', 'DELETING', 'ACTIVE', or 'FAILED'
        status = status_response["collectionDetails"][0]["status"]

        print(f"Status: {status}")

        # If the provisioning is completely finished, break out of the infinite loop
        if status == "ACTIVE":
            break

        # If not active yet, pause the script for 30 seconds before pinging AWS again
        # This prevents us from spamming the AWS API and hitting rate limits (Throttling)
        time.sleep(30)

    # Once the loop breaks, the script confirms readiness
    print("Collection is ACTIVE")


# Standard Python idiom to ensure the main() function is only executed
# if this file is run directly (not if it is imported as a module in another script).
if __name__ == "__main__":
    main()
