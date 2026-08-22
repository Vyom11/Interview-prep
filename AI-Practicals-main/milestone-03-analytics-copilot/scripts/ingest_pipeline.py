"""
Run ingestion pipeline.
"""

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / "_bootstrap.py"))

# Import modules
from app.ingestion.chunker import chunk_documents
from app.ingestion.opensearch_store import store_documents
from app.ingestion.pdf_extractor import extract_pdf_documents
from app.ingestion.s3_loader import download_file_from_s3


def run_pipeline():
    """
    Execute ingestion pipeline.
    """

    # S3 file key
    s3_key = "sample2.pdf"

    # Local file path
    local_path = "data/sample.pdf"

    # Download file
    file_path = download_file_from_s3(s3_key=s3_key, local_path=local_path)

    # Extract text
    documents = extract_pdf_documents(file_path)

    # Create chunks
    chunks = chunk_documents(documents)

    # Store embeddings
    store_documents(chunks)

    print("Ingestion completed successfully!")


if __name__ == "__main__":

    run_pipeline()
