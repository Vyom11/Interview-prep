# RAG + SQL Routing Agent

An intelligent Q&A system that combines **Retrieval-Augmented Generation (RAG)** over PDF documents with **structured SQL queries** over PostgreSQL. A LangGraph agent automatically routes each question to the right path, including a **hybrid** mode for questions that need both sources, with conversation memory and LangFuse observability.

---

## Overview

| Capability | Description |
|------------|-------------|
| **Milestone 2 — RAG** | Ingest PDFs from S3 → chunk → Bedrock embeddings → OpenSearch → answer via grounded Bedrock LLM |
| **Milestone 3 — Routing agent** | LangGraph classifier routes to **SQL agent**, **RAG agent**, or **hybrid** |
| **SQL agent** | Introspects PostgreSQL schema, generates read-only `SELECT` queries, summarizes results |
| **Hybrid path** | Runs SQL + RAG together, then synthesizes a single combined answer |
| **Safety** | Tool whitelists, max agent steps, SQL keyword blocking, row limits |
| **Tracing** | LangFuse integration for LLM/graph spans |
| **Deployment** | Run locally (AWS Serverless) or via **Docker Compose** (local OpenSearch + Postgres) |

---

## Architecture

### RAG pipeline (Milestone 2)

```text
PDF (S3) → PyPDF extract → LangChain chunk → Bedrock embeddings → OpenSearch
                                                                      ↓
User → FastAPI /ask → Retriever → context + Bedrock LLM → answer
```

RAG answers are now more conservative:

- the retriever uses MMR with a broader candidate pool to reduce repetitive or off-target chunks,
- retrieved chunks keep their original source metadata when available,
- the answer prompt is grounded in retrieved passages only,
- a verifier step rejects answers that are not explicitly supported and falls back to a safe "not enough information" response.

### Routing agent (Milestone 3)

```text
User → FastAPI /chat → LangGraph
                          │
                    classifier node
                 /        |        \
          sql_agent   rag_agent   hybrid_agent
              │            │             │
        PostgreSQL    OpenSearch RAG   SQL + RAG
      (read-only SQL)   (Milestone 2)  synthesis
```

---

## Tech stack

- **AWS:** S3, Bedrock (embeddings + LLM), OpenSearch Serverless (or local OpenSearch in Docker)
- **PostgreSQL:** Structured data for the SQL agent
- **LangChain / LangGraph:** RAG, agent workflow, memory (`MemorySaver`)
- **FastAPI + Streamlit:** API and chat UI
- **LangFuse:** Tracing and observability
- **Docker Compose:** Optional local Postgres + OpenSearch + API

---

## Project structure

```text
milestone-02-rag-application/
├── app/
│   ├── api/
│   │   └── main.py              # FastAPI: /health, /ask, /chat
│   ├── agent/
│   │   ├── graph.py             # LangGraph workflow
│   │   ├── nodes.py             # Classifier, SQL, RAG nodes
│   │   ├── runner.py            # run_agent() entry point
│   │   ├── db.py                # Postgres schema + read-only queries
│   │   ├── state.py             # Agent state (messages, route, steps)
│   │   └── tracing.py           # LangFuse callbacks
│   ├── core/
│   │   ├── config.py            # Environment configuration
│   │   ├── opensearch_client.py # AWS Serverless or local OpenSearch
│   │   ├── aws_clients.py       # S3 + Bedrock clients
│   │   └── safety.py            # SQL validation, tool whitelists
│   ├── ingestion/
│   │   ├── s3_loader.py
│   │   ├── pdf_extractor.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   └── opensearch_store.py
│   ├── rag/
│   │   ├── retriever.py
│   │   └── chain.py
│   └── frontend/
│       └── streamlit_app.py
├── scripts/
│   ├── _bootstrap.py            # Adds project root to PYTHONPATH for scripts
│   ├── setup_opensearch.py      # AWS Serverless collection (once)
│   ├── create_index.py          # Vector index (knn; dimension from BEDROCK_EMBED_DIMENSION)
│   ├── ingest_pipeline.py       # Full ingestion
│   ├── seed_postgres.py         # Sample SQL agent data
│   ├── run_agent_cli.py         # CLI for /chat + LangFuse demos
│   └── run_milestone2_pipeline.sh
├── docker/
│   ├── entrypoint.sh
│   └── postgres/init.sql
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── .env.docker.example
```

---

## Prerequisites

- Python 3.10+
- AWS account with access to **S3**, **Bedrock**, and (for bare-metal RAG) **OpenSearch Serverless**
- PostgreSQL (local or Docker) for the SQL agent
- Optional: [LangFuse](https://langfuse.com) project keys for tracing
- Optional: Docker and Docker Compose for containerized stack

---

## Configuration

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

### Key variables

| Variable | Description |
|----------|-------------|
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` | AWS credentials |
| `S3_BUCKET_NAME` | Bucket containing ingestion PDFs |
| `BEDROCK_EMBED_MODEL` | e.g. `amazon.nova-2-multimodal-embeddings-v1:0` |
| `BEDROCK_EMBED_DIMENSION` | Nova embedding size: `256`, `384`, `1024`, or `3072` (must match OpenSearch index) |
| `BEDROCK_LLM_MODEL` | e.g. `us.amazon.nova-2-lite-v1:0` |
| `OPENSEARCH_MODE` | `aws` (Serverless, default) or `local` (Docker) |
| `OPENSEARCH_COLLECTION_NAME` | Serverless collection name (`aws` mode) |
| `OPENSEARCH_INDEX` | Vector index name (default: `rag-index`) |
| `DATABASE_URL` | PostgreSQL connection string for SQL agent |
| `LANGFUSE_*` | Tracing keys; set `LANGFUSE_ENABLED=false` to disable |
| `AGENT_MAX_STEPS` | Max graph steps per turn (default: 8) |
| `AGENT_MAX_SQL_ROWS` | Max rows returned from SQL (default: 100) |

---

## Installation

```bash
cd milestone-02-rag-application
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="$(pwd)"
```

---

## Run locally (bare metal — AWS OpenSearch Serverless)

Use this flow when OpenSearch runs on **AWS Serverless** (Docker not required).

### Quick reference (full sequence)

```bash
export PYTHONPATH="$(pwd)"

python3 scripts/seed_postgres.py
python3 scripts/setup_opensearch.py      # one-time; wait ~2–5 min for ACTIVE
python3 scripts/create_index.py
aws s3 cp data/sample.pdf s3://YOUR_BUCKET/sample2.pdf
python3 scripts/ingest_pipeline.py

uvicorn app.api.main:app --reload --port 8000
# separate terminal:
streamlit run app/frontend/streamlit_app.py
```

### Step-by-step

**1. Seed PostgreSQL**

```bash
python3 scripts/seed_postgres.py
```

Creates `customers`, `products`, `orders`, `order_items` with sample data. Skips if data already exists.

**2. OpenSearch Serverless (one-time)**

```bash
python3 scripts/setup_opensearch.py
```

Wait until the collection is **ACTIVE** (~2–5 minutes).

**3. Create vector index**

```bash
python3 scripts/create_index.py
```

**4. Upload PDF and ingest**

```bash
aws s3 cp data/sample.pdf s3://YOUR_BUCKET/sample2.pdf
python3 scripts/ingest_pipeline.py
```

Ingest expects S3 key `sample2.pdf` (see `scripts/ingest_pipeline.py`).

**5. Start API and UI**

Terminal 1:

```bash
export PYTHONPATH="$(pwd)"
uvicorn app.api.main:app --reload --port 8000
```

Terminal 2:

```bash
streamlit run app/frontend/streamlit_app.py
```

- API docs: http://localhost:8000/docs
- Streamlit: http://localhost:8501

### One-shot pipeline script

```bash
bash scripts/run_milestone2_pipeline.sh
```

Then start uvicorn and Streamlit as above.

---

## Run with Docker Compose (optional)

Uses **local OpenSearch** and **PostgreSQL** in containers. Bedrock still requires AWS credentials in `.env`.

```bash
cp .env.docker.example .env   # or ensure .env has AWS Bedrock keys
docker compose up --build -d
curl http://localhost:8000/health
```

| Service | Port | Purpose |
|---------|------|---------|
| `api` | 8000 | FastAPI routing agent |
| `postgres` | 5432 | SQL agent DB (`milestone_3`) |
| `opensearch` | 9200 | Local vector store |

On startup the API container:

- Waits for Postgres and OpenSearch
- Seeds Postgres if empty
- Creates the `rag-index` vector index if missing

**Ingest into Docker OpenSearch (from host):**

```bash
export PYTHONPATH="$(pwd)"
export OPENSEARCH_MODE=local
export OPENSEARCH_HOST=localhost
export OPENSEARCH_PORT=9200
export OPENSEARCH_USE_SSL=false
python3 scripts/ingest_pipeline.py
```

**Useful commands:**

```bash
docker compose logs -f api
docker compose down
docker compose down -v   # reset volumes
```

> Do not run Docker API and local uvicorn on port 8000 at the same time.

---

## API reference

### `GET /health`

```bash
curl http://localhost:8000/health
```

### `POST /ask` — RAG only (Milestone 2)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main topics in the document?"}'
```

### `POST /chat` — Routing agent (Milestone 3)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How many customers are in the database?",
    "session_id": "user-123",
    "user_id": "optional-user-id"
  }'
```

**Response:**

```json
{
  "question": "...",
  "answer": "...",
  "route": "sql",
  "session_id": "user-123",
  "error": null
}
```

`route` is `sql`, `rag`, or `hybrid`. Conversation history is keyed by `session_id`.

### RAG grounding behavior

The RAG path is intentionally conservative:

- it prefers explicit facts from the retrieved passages,
- it cites chunk labels like `[1]` or `[2]` in the response when possible,
- it will refuse to guess the document topic if the retrieved chunks do not support it clearly.

---

## Example questions

| Type | Example |
|------|---------|
| SQL | "How many customers do we have?" |
| SQL | "What is total revenue per customer?" |
| SQL | "List all pending orders." |
| RAG | "Summarize the main topics in the uploaded document." |
| RAG | "What does the policy say about refunds?" |
| Hybrid | "How many customers are affected by the refund policy in the uploaded document?" |
| Hybrid | "Which product-related metrics from the database are mentioned in the policy PDF?" |

---

## CLI

```bash
export PYTHONPATH="$(pwd)"
python3 scripts/run_agent_cli.py --session demo "How many customers?"
python3 scripts/run_agent_cli.py --session demo "What does the document say about X?"
```

Run without a question argument for interactive mode.

---

## LangFuse tracing

1. Set `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_HOST` in `.env`.
2. Call `/chat` or use the CLI with a stable `session_id`.
3. Open your LangFuse project → **Traces** to view classifier, SQL/RAG, and LLM spans.

Run 3+ questions (mix SQL and document questions) with the same `session_id` for demo screenshots.

Disable tracing: `LANGFUSE_ENABLED=false`

---

## OpenSearch modes

| `OPENSEARCH_MODE` | When to use |
|-------------------|-------------|
| `aws` (default) | Local dev with AWS OpenSearch Serverless |
| `local` | Docker Compose or local OpenSearch on port 9200 |

---

## Safety

- **Tool whitelists:** SQL (`get_schema`, `run_readonly_query`); RAG (`search_documents`)
- **SQL:** Only `SELECT` / `WITH`; blocks DML/DDL; single statement; row cap via `AGENT_MAX_SQL_ROWS`
- **Agent:** `AGENT_MAX_STEPS` limits work per turn
- **Errors:** User-friendly messages returned in `/chat`; LangFuse init failures skip callbacks without crashing the API

---

## File reference

| File | Role |
|------|------|
| `app/api/main.py` | FastAPI endpoints |
| `app/agent/graph.py` | LangGraph: classifier → SQL, RAG, or hybrid |
| `app/agent/nodes.py` | Classifier, SQL, RAG, and hybrid node logic |
| `app/agent/db.py` | PostgreSQL introspection and read-only execution |
| `app/core/opensearch_client.py` | OpenSearch client (`aws` or `local` mode) |
| `app/rag/chain.py` | Grounded RAG retrieval, verification, and answer generation |
| `app/core/safety.py` | SQL validation and tool whitelists |
| `scripts/setup_opensearch.py` | Create AWS Serverless collection and policies |
| `scripts/ingest_pipeline.py` | S3 → PDF → chunks → embeddings → OpenSearch |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `No module named 'app'` | `export PYTHONPATH="$(pwd)"` from project root |
| Collection not found | Run `setup_opensearch.py`; wait for ACTIVE; retry `create_index.py` |
| RAG returns weak answers | Re-run ingest; confirm index exists and PDF is in S3; the grounded RAG path may now return "not enough information" instead of guessing |
| SQL errors | Check Postgres is running and `DATABASE_URL` is correct |
| `/chat` 500 (LangFuse) | Ensure LangFuse v4+ env vars; or `LANGFUSE_ENABLED=false` |
| Port 8000 in use | Stop Docker `api` service or change `API_PORT` |

---

## What works without full RAG setup

- **SQL `/chat` questions** — after `seed_postgres.py` + uvicorn (Postgres only).
- **RAG `/chat` or `/ask`** — after OpenSearch setup and `ingest_pipeline.py` complete.
