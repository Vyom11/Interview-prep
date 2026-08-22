"""
Create vector index.
"""

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / "_bootstrap.py"))

# Import client
# Import config
from app.core.config import BEDROCK_EMBED_DIMENSION, OPENSEARCH_INDEX
from app.core.opensearch_client import opensearch_client

# Index body
index_body = {
    "settings": {"index": {"knn": True}},
    "mappings": {
        "properties": {
            "vector_field": {
                "type": "knn_vector",
                "dimension": BEDROCK_EMBED_DIMENSION,
            }
        }
    },
}

client = opensearch_client

if client.indices.exists(index=OPENSEARCH_INDEX):
    print(f"Index '{OPENSEARCH_INDEX}' already exists — skipping.")
else:
    response = client.indices.create(index=OPENSEARCH_INDEX, body=index_body)
    print(response)
