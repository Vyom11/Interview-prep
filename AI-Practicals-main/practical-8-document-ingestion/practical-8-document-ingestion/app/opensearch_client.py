"""
OpenSearch Serverless client.
"""

import json
import time

import boto3
from app.config import settings
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

COLLECTION_NAME = "practical8-collection"

INDEX_NAME = settings.opensearch_index


def create_security_policies(aoss_client) -> None:
    """
    Create encryption, network,
    and access policies.
    """

    try:

        encryption_policy = {
            "Rules": [
                {
                    "ResourceType": "collection",
                    "Resource": [f"collection/{COLLECTION_NAME}"],
                }
            ],
            "AWSOwnedKey": True,
        }

        aoss_client.create_security_policy(
            name="practical8-encryption-policy",
            policy=json.dumps(encryption_policy),
            type="encryption",
        )

        print("Encryption policy created.")

    except Exception:

        print("Encryption policy already exists.")

    try:

        network_policy = [
            {
                "Rules": [
                    {
                        "ResourceType": "collection",
                        "Resource": [f"collection/{COLLECTION_NAME}"],
                    },
                    {
                        "ResourceType": "dashboard",
                        "Resource": [f"collection/{COLLECTION_NAME}"],
                    },
                ],
                "AllowFromPublic": True,
            }
        ]

        aoss_client.create_security_policy(
            name="practical8-network-policy",
            policy=json.dumps(network_policy),
            type="network",
        )

        print("Network policy created.")

    except Exception:

        print("Network policy already exists.")

    try:

        access_policy = [
            {
                "Rules": [
                    {
                        "ResourceType": "index",
                        "Resource": [f"index/{COLLECTION_NAME}/*"],
                        "Permission": ["aoss:*"],
                    },
                    {
                        "ResourceType": "collection",
                        "Resource": [f"collection/{COLLECTION_NAME}"],
                        "Permission": ["aoss:*"],
                    },
                ],
                "Principal": [boto3.client("sts").get_caller_identity()["Arn"]],
            }
        ]

        aoss_client.create_access_policy(
            name="practical8-access-policy",
            policy=json.dumps(access_policy),
            type="data",
        )

        print("Access policy created.")

    except Exception:

        print("Access policy already exists.")


def create_collection() -> str:
    """
    Create OpenSearch collection.
    """

    aoss_client = boto3.client("opensearchserverless", region_name=settings.aws_region)

    create_security_policies(aoss_client)

    try:

        response = aoss_client.create_collection(
            name=COLLECTION_NAME, type="VECTORSEARCH"
        )

        collection_id = response["createCollectionDetail"]["id"]

        print("Collection creation started.")

    except Exception:

        print("Collection already exists.")

        collections = aoss_client.list_collections(
            collectionFilters={"name": COLLECTION_NAME}
        )

        collection_id = collections["collectionSummaries"][0]["id"]

    while True:

        details = aoss_client.batch_get_collection(ids=[collection_id])

        status = details["collectionDetails"][0]["status"]

        print(f"Collection status: {status}")

        if status == "ACTIVE":
            break

        time.sleep(30)

    endpoint = details["collectionDetails"][0]["collectionEndpoint"]

    print(f"Collection endpoint: {endpoint}")

    return endpoint


def get_opensearch_client() -> OpenSearch:
    """
    Create OpenSearch client.
    """

    credentials = boto3.Session().get_credentials()

    aws_auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        settings.aws_region,
        "aoss",
        session_token=credentials.token,
    )

    host = settings.opensearch_host

    if not host:
        host = create_collection()

    return OpenSearch(
        hosts=[{"host": host.replace("https://", ""), "port": 443}],
        http_auth=aws_auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=60,
        max_retries=5,
        retry_on_timeout=True,
    )


def create_index() -> None:
    """
    Create vector index.
    """

    client = get_opensearch_client()

    if client.indices.exists(index=INDEX_NAME):

        print("Vector index already exists.")

        return

    index_body = {
        "settings": {"index": {"knn": True}},
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "source": {"type": "keyword"},
                "chunk_id": {"type": "integer"},
                "embedding": {
                    "type": "knn_vector",
                    "dimension": (settings.embedding_dimension),
                },
            }
        },
    }

    client.indices.create(index=INDEX_NAME, body=index_body)

    print("Vector index created.")
