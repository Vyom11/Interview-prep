#!/bin/bash
set -euo pipefail

export PYTHONPATH=/app

echo "==> Waiting for PostgreSQL..."
until python - <<'PY'
import os, sys
import psycopg2
from app.core.config import postgres_dsn
try:
    psycopg2.connect(postgres_dsn()).close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
do
  sleep 2
done
echo "PostgreSQL is ready."

echo "==> Waiting for OpenSearch..."
OPENSEARCH_WAIT_URL="${OPENSEARCH_WAIT_URL:-http://opensearch:9200}"
until curl -fs "${OPENSEARCH_WAIT_URL}/_cluster/health" >/dev/null 2>&1; do
  sleep 2
done
echo "OpenSearch is ready."

echo "==> Seeding PostgreSQL (if empty)..."
python /app/scripts/seed_postgres.py || true

echo "==> Ensuring OpenSearch vector index..."
python /app/scripts/create_index.py || true

echo "==> Starting API..."
exec "$@"
