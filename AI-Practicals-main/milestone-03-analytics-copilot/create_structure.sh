#!/usr/bin/env bash
set -e

# Create directories
mkdir -p app/api
mkdir -p app/core
mkdir -p app/ingestion
mkdir -p app/rag
mkdir -p app/frontend
mkdir -p scripts
mkdir -p data

# Create files
touch app/api/main.py
touch app/core/config.py
touch app/core/aws_clients.py
touch app/core/opensearch_client.py
touch app/ingestion/s3_loader.py
touch app/ingestion/pdf_extractor.py
touch app/ingestion/chunker.py
touch app/ingestion/embeddings.py
touch app/ingestion/opensearch_store.py
touch app/rag/retriever.py
touch app/rag/chain.py
touch app/frontend/streamlit_app.py

touch scripts/setup_opensearch.py
touch scripts/create_index.py
touch scripts/ingest_pipeline.py

touch data/sample.pdf
touch requirements.txt
touch .env
touch .gitignore
touch README.md

echo "Folder structure created successfully."
