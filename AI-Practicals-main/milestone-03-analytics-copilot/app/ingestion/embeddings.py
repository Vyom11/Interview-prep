"""
Initialize Bedrock embeddings (Nova multimodal or Titan/Cohere via langchain-aws).
"""

import os

from app.core.aws_clients import bedrock_client
from app.core.config import (
    BEDROCK_EMBED_DIMENSION,
    BEDROCK_EMBED_MODEL,
)
from langchain_aws import BedrockEmbeddings


class NovaMultimodalBedrockEmbeddings(BedrockEmbeddings):
    """Nova multimodal embeddings with RAG-appropriate indexing vs query purposes."""

    def embed_query(self, text: str) -> list[float]:
        if not self._is_nova_embed:
            return super().embed_query(text)

        text = text.replace(os.linesep, " ")
        single_embedding_params: dict = {
            "embeddingPurpose": "TEXT_RETRIEVAL",
            "text": {"truncationMode": "END", "value": text},
        }
        if self.dimensions:
            single_embedding_params["embeddingDimension"] = self.dimensions

        response_body = self._invoke_model(
            input_body={
                "taskType": "SINGLE_EMBEDDING",
                "singleEmbeddingParams": single_embedding_params,
            }
        )
        embeddings = response_body.get("embeddings")
        if not embeddings or not embeddings[0].get("embedding"):
            raise ValueError("No embedding returned from model")

        embedding = embeddings[0]["embedding"]
        if self.normalize:
            return self._normalize_vector(embedding)
        return embedding


def _build_embedding_model() -> BedrockEmbeddings:
    kwargs: dict = {
        "client": bedrock_client,
        "model_id": BEDROCK_EMBED_MODEL,
    }
    if "nova" in BEDROCK_EMBED_MODEL and "embed" in BEDROCK_EMBED_MODEL:
        kwargs["dimensions"] = BEDROCK_EMBED_DIMENSION
        return NovaMultimodalBedrockEmbeddings(**kwargs)
    return BedrockEmbeddings(**kwargs)


embedding_model = _build_embedding_model()
