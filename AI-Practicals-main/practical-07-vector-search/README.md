# Practical 7 — Vector Search: FAISS to OpenSearch

## Objective

This practical demonstrates semantic vector search using:

1. FAISS for local vector similarity search
2. AWS OpenSearch Serverless for scalable vector search

The project covers:
- Sentence embeddings
- Vector indexing
- Similarity search
- Keyword search
- Semantic search
- Hybrid search

---

# Project Structure

```text
practical-7-vector-search/
│
├── data/
├── faiss_local/
├── opensearch_aws/
├── requirements.txt
├── .env.example
└── README.md
```

---

# Setup

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Fill AWS credentials carefully.

Never commit `.env` files to GitHub.

---

# Part 1 — FAISS Local Search

## Run

```bash
python faiss_local/generate_embeddings.py
python faiss_local/build_index.py
python faiss_local/search.py
```

---

# Part 2 — OpenSearch AWS

## Steps

1. Create OpenSearch policies
2. Create collection
3. Create vector index
4. Index documents
5. Run queries

## Run

```bash
python opensearch_aws/create_collection.py
python opensearch_aws/create_index.py
python opensearch_aws/index_documents.py
python opensearch_aws/keyword_search.py
python opensearch_aws/semantic_search.py
python opensearch_aws/hybrid_search.py
```

---

# Expected Learning Outcomes

- Understand embeddings to its core
- Learn vector databases
- Compare keyword vs semantic search
- Use OpenSearch knn_vector
- Build hybrid search systems