"""
Setup OpenSearch Serverless infrastructure.
"""

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / "_bootstrap.py"))

# Import json
import json

# Import time
import time

# Import boto3
import boto3

# Import config
from app.core.config import AWS_REGION, OPENSEARCH_COLLECTION_NAME

# Import exceptions
from botocore.exceptions import ClientError

# Create OpenSearch Serverless client
client = boto3.client("opensearchserverless", region_name=AWS_REGION)

# Collection name
collection_name = OPENSEARCH_COLLECTION_NAME


def create_encryption_policy():
    """
    Create encryption policy.
    """

    try:

        print("Creating encryption policy...")

        client.create_security_policy(
            name="rag-encryption-policy",
            type="encryption",
            policy=json.dumps(
                {
                    "Rules": [
                        {
                            "Resource": [f"collection/{collection_name}"],
                            "ResourceType": "collection",
                        }
                    ],
                    "AWSOwnedKey": True,
                }
            ),
        )

        print("Encryption policy created!")

    except ClientError as error:

        # Ignore already exists error
        if error.response["Error"]["Code"] == "ConflictException":

            print("Encryption policy already exists.")

        else:
            raise error


def create_network_policy():
    """
    Create network policy.
    """

    try:

        print("Creating network policy...")

        client.create_security_policy(
            name="rag-network-policy",
            type="network",
            policy=json.dumps(
                [
                    {
                        "Rules": [
                            {
                                "ResourceType": "collection",
                                "Resource": [f"collection/{collection_name}"],
                            },
                            {
                                "ResourceType": "dashboard",
                                "Resource": [f"collection/{collection_name}"],
                            },
                        ],
                        "AllowFromPublic": True,
                    }
                ]
            ),
        )

        print("Network policy created!")

    except ClientError as error:

        if error.response["Error"]["Code"] == "ConflictException":

            print("Network policy already exists.")

        else:
            raise error


def create_collection():
    """
    Create OpenSearch collection.
    """

    try:

        print("Creating collection...")

        response = client.create_collection(name=collection_name, type="VECTORSEARCH")

        collection_id = response["createCollectionDetail"]["id"]

        print(f"Collection ID: {collection_id}")

        print("Waiting for collection creation...")

        time.sleep(120)

        print("Collection created!")

    except ClientError as error:

        if error.response["Error"]["Code"] == "ConflictException":

            print("Collection already exists.")

        else:
            raise error


def create_access_policy():
    """
    Create access policy.
    """

    try:

        print("Creating access policy...")

        # Create STS client
        sts = boto3.client("sts")

        # Get IAM identity
        identity = sts.get_caller_identity()

        iam_arn = identity["Arn"]

        # Create access policy
        client.create_access_policy(
            name="rag-access-policy",
            type="data",
            policy=json.dumps(
                [
                    {
                        "Rules": [
                            {
                                "ResourceType": "collection",
                                "Resource": [f"collection/{collection_name}"],
                                "Permission": ["aoss:*"],
                            },
                            {
                                "ResourceType": "index",
                                "Resource": [f"index/{collection_name}/*"],
                                "Permission": ["aoss:*"],
                            },
                        ],
                        "Principal": [iam_arn],
                    }
                ]
            ),
        )

        print("Access policy created!")

    except ClientError as error:

        if error.response["Error"]["Code"] == "ConflictException":

            print("Access policy already exists.")

        else:
            raise error


if __name__ == "__main__":

    # Create encryption policy
    create_encryption_policy()

    # Create network policy
    create_network_policy()

    # Create collection
    create_collection()

    # Create access policy
    create_access_policy()

    print("\nOpenSearch setup completed!")
