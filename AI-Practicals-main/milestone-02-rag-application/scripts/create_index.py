"""
Create vector index.
"""

# Import client
# Import config
from app.core.config import OPENSEARCH_INDEX
from app.core.opensearch_client import opensearch_client

# Index body
index_body = {
    "settings": {"index": {"knn": True}},
    "mappings": {
        "properties": {"vector_field": {"type": "knn_vector", "dimension": 1024}}
    },
}

# Create index
response = opensearch_client.indices.create(index=OPENSEARCH_INDEX, body=index_body)

print(response)
