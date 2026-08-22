#!/usr/bin/env bash
# Milestone 2 — full RAG pipeline (OpenSearch setup → index → ingest → API)
# Run from project root: bash scripts/run_milestone2_pipeline.sh

set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="$(pwd)${PYTHONPATH:+:$PYTHONPATH}"

echo "=== Step 0: Load .env (ensure AWS + S3 + Bedrock vars are set) ==="
if [[ ! -f .env ]]; then
  echo "Missing .env — copy .env.example and fill in values."
  exit 1
fi

echo ""
echo "=== Step 1: OpenSearch Serverless (collection + policies) ==="
echo "This creates collection '${OPENSEARCH_COLLECTION_NAME:-rag-serverless}' in AWS (~2–5 min)."
python3 scripts/setup_opensearch.py

echo ""
echo "=== Step 2: Wait until collection is ACTIVE, then create vector index ==="
python3 -c "
from app.core.opensearch_client import get_host
print('Collection ready at:', get_host())
"
python3 scripts/create_index.py

echo ""
echo "=== Step 3: Ingest PDF from S3 → chunks → embeddings → OpenSearch ==="
echo "Ensure sample2.pdf exists in your S3 bucket (see app/ingestion/s3_loader / ingest_pipeline.py)."
python3 scripts/ingest_pipeline.py

echo ""
echo "=== Step 4: Start API (RAG + routing agent) ==="
echo "  uvicorn app.api.main:app --reload --port 8000"
echo "  streamlit run app/frontend/streamlit_app.py   # optional UI"
echo ""
echo "Test RAG-only:  curl -X POST http://localhost:8000/ask -H 'Content-Type: application/json' -d '{\"question\":\"your question\"}'"
echo "Test routing:   curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{\"question\":\"your question\",\"session_id\":\"demo\"}'"
