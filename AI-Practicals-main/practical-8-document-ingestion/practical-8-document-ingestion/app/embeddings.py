"""
Titan embedding service using boto3.
"""

import json

import boto3
from app.config import settings


class TitanEmbeddings:
    """
    Generate Titan embeddings directly via boto3.
    """

    def __init__(self) -> None:

        self.client = boto3.client("bedrock-runtime", region_name=settings.aws_region)

    def embed_text(self, text: str) -> list[float]:
        """
        Generate embedding vector.
        """

        response = self.client.invoke_model(
            modelId=settings.bedrock_model_id,
            body=json.dumps({"inputText": text}),
            contentType="application/json",
            accept="application/json",
        )

        # -------------------------------------
        # Proper decoding/parsing
        # -------------------------------------

        response_body = json.loads(response["body"].read().decode("utf-8"))

        embedding = response_body.get("embedding")

        if embedding is None:
            raise ValueError(f"No embedding returned: {response_body}")

        return embedding


def get_embeddings_client() -> TitanEmbeddings:
    """
    Create embeddings client.
    """

    return TitanEmbeddings()
