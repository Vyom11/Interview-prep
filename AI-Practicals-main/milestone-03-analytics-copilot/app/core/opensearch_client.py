"""
OpenSearch client: AWS Serverless (default) or local Docker OpenSearch.
"""

from __future__ import annotations

import time
from typing import Any, Optional, Tuple, Union

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from app.core.config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    OPENSEARCH_COLLECTION_NAME,
    OPENSEARCH_HOST,
    OPENSEARCH_PASSWORD,
    OPENSEARCH_PORT,
    OPENSEARCH_USE_SSL,
    OPENSEARCH_USER,
    is_local_opensearch,
)

_host: str | None = None
_awsauth: AWS4Auth | None = None
_local_auth: Optional[Tuple[str, str]] = None
_opensearch_client: OpenSearch | None = None
_init_error: str | None = None

HttpAuth = Union[AWS4Auth, Tuple[str, str], None]


def _resolve_collection_host() -> str:
    serverless_client = boto3.client("opensearchserverless", region_name=AWS_REGION)
    max_retries = 30

    for attempt in range(1, max_retries + 1):
        response = serverless_client.batch_get_collection(
            names=[OPENSEARCH_COLLECTION_NAME]
        )

        if not response["collectionDetails"]:
            print(
                f"[{attempt}/{max_retries}] Collection '{OPENSEARCH_COLLECTION_NAME}' "
                "not found. Run: python scripts/setup_opensearch.py"
            )
            time.sleep(10)
            continue

        details = response["collectionDetails"][0]
        status = details["status"]
        print(f"[{attempt}/{max_retries}] Collection status: {status}")

        if status == "ACTIVE":
            endpoint = details.get("collectionEndpoint")
            if endpoint:
                return endpoint.replace("https://", "").replace("http://", "")

        time.sleep(10)

    raise RuntimeError(
        f"OpenSearch collection '{OPENSEARCH_COLLECTION_NAME}' is not available."
    )


def _local_base_url() -> str:
    scheme = "https" if OPENSEARCH_USE_SSL else "http"
    return f"{scheme}://{OPENSEARCH_HOST}:{OPENSEARCH_PORT}"


def _ensure_initialized() -> None:
    global _host, _awsauth, _local_auth, _opensearch_client, _init_error

    if _opensearch_client is not None:
        return
    if _init_error is not None:
        raise RuntimeError(_init_error)

    try:
        if is_local_opensearch():
            print(f"Connecting to local OpenSearch at {_local_base_url()}...")
            _host = f"{OPENSEARCH_HOST}:{OPENSEARCH_PORT}"
            if OPENSEARCH_USER and OPENSEARCH_PASSWORD:
                _local_auth = (OPENSEARCH_USER, OPENSEARCH_PASSWORD)
            else:
                _local_auth = None
            _opensearch_client = OpenSearch(
                hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
                http_auth=_local_auth,
                use_ssl=OPENSEARCH_USE_SSL,
                verify_certs=OPENSEARCH_USE_SSL,
                connection_class=RequestsHttpConnection,
            )
        else:
            print("Connecting to OpenSearch Serverless...")
            _host = _resolve_collection_host()
            print(f"OpenSearch host: {_host}")
            _awsauth = AWS4Auth(
                AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, "aoss"
            )
            _opensearch_client = OpenSearch(
                hosts=[{"host": _host, "port": 443}],
                http_auth=_awsauth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
            )
        print("OpenSearch client ready.")
    except Exception as exc:
        _init_error = str(exc)
        raise


def get_host() -> str:
    _ensure_initialized()
    assert _host is not None
    return _host


def get_opensearch_url() -> str:
    """Full base URL for LangChain OpenSearchVectorSearch."""
    if is_local_opensearch():
        return _local_base_url()
    _ensure_initialized()
    return f"https://{get_host()}"


def get_http_auth() -> HttpAuth:
    _ensure_initialized()
    if is_local_opensearch():
        return _local_auth
    assert _awsauth is not None
    return _awsauth


def get_awsauth() -> AWS4Auth:
    """AWS auth only (Serverless mode)."""
    if is_local_opensearch():
        raise RuntimeError("get_awsauth() is not available in local OpenSearch mode.")
    _ensure_initialized()
    assert _awsauth is not None
    return _awsauth


def get_vector_store_kwargs() -> dict[str, Any]:
    """Kwargs for langchain_community OpenSearchVectorSearch."""
    _ensure_initialized()
    return {
        "opensearch_url": get_opensearch_url(),
        "http_auth": get_http_auth(),
        "use_ssl": OPENSEARCH_USE_SSL if is_local_opensearch() else True,
        "verify_certs": OPENSEARCH_USE_SSL if is_local_opensearch() else True,
        "connection_class": RequestsHttpConnection,
    }


def get_opensearch_client() -> OpenSearch:
    _ensure_initialized()
    assert _opensearch_client is not None
    return _opensearch_client


class _LazyProxy:
    def __getattr__(self, name: str):
        return getattr(get_opensearch_client(), name)


opensearch_client = _LazyProxy()


def __getattr__(name: str):
    if name == "host":
        return get_host()
    if name == "awsauth":
        return get_http_auth()
    raise AttributeError(name)
