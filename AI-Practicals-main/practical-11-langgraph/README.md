# Practical 11 - LangGraph Conditional Workflow

## Features

- LangGraph conditional routing
- SQL agent using PostgreSQL
- RAG agent using OpenSearch (Provisioned)
- Error handling node
- Mermaid graph visualization

## Setup

```bash
pip install -r requirements.txt
```

## Step 1: Create PostgreSQL DB

```sql
CREATE DATABASE langgraph_db;
```

## Step 2: Configure `.env`

Copy `.env.example` to `.env`

## Step 3: Create tables

```bash
python db/postgres_setup.py
```

## Step 4: Seed data

```bash
python db/seed_data.py
```

## Step 5: Create OpenSearch domain

```bash
python rag/opensearch_setup.py
```

Wait for endpoint generation and add it to `.env`

## Step 6: Ingest docs

```bash
python rag/ingest_docs.py
```

## Step 7: Run App

```bash
python app.py
```

## Mermaid Visualization

```python
print(graph.get_graph().draw_mermaid())
```
