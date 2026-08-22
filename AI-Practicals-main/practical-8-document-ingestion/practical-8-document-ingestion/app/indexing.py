"""
Document indexing pipeline.
"""

import json
from pathlib import Path

from app.chunking import chunk_document
from app.config import settings
from app.embeddings import get_embeddings_client
from app.opensearch_client import create_index, get_opensearch_client


def run_indexing_pipeline(chunk_size: int) -> None:
    """
    Run document indexing pipeline.
    """

    create_index()

    client = get_opensearch_client()

    embeddings = get_embeddings_client()

    extracted_directory = Path("data/extracted")

    for json_file in extracted_directory.glob("*.json"):

        with open(json_file, "r", encoding="utf-8") as file:

            data = json.load(file)

        chunks = chunk_document(data["text"], chunk_size=chunk_size)

        for index, chunk in enumerate(chunks):

            print(f"Embedding chunk {index} " f"from {json_file.name}")

            try:

                vector = embeddings.embed_text(chunk)

                # -----------------------------
                # Validation
                # -----------------------------

                if vector is None:
                    print(f"Null vector for chunk {index}")
                    continue

                if not isinstance(vector, list):
                    print(f"Invalid vector type " f"for chunk {index}")
                    continue

                if len(vector) == 0:
                    print(f"Empty vector for chunk {index}")
                    continue

                document = {
                    "text": chunk,
                    "source": json_file.name,
                    "chunk_id": index,
                    "embedding": vector,
                }

                client.index(index=settings.opensearch_index, body=document)

                print(f"Indexed chunk {index} " f"from {json_file.name}")

            except Exception as error:

                print(f"Failed chunk {index}: " f"{error}")
