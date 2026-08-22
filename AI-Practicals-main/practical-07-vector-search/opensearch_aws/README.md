# Practical 7 — Vector Search: FAISS to OpenSearch

# Overview

This practical demonstrates how modern AI search systems work using:

1. FAISS (Local Vector Search)
2. Amazon OpenSearch Serverless (Cloud Vector Database/Search Engine)

The practical is divided into two major parts:

| Part | Goal |
|---|---|
| FAISS Local | Understand embeddings and vector similarity locally |
| OpenSearch AWS | Build a scalable cloud-based semantic search system |

The project teaches:
- embeddings
- semantic search
- vector databases
- keyword search
- hybrid search
- OpenSearch Serverless
- AWS IAM permissions
- indexing pipelines
- vector similarity ranking

---

# What Problem Are We Solving?

Traditional search engines rely on:
- exact keyword matches
- lexical similarity
- token overlap

Example query:

AI in healthcare

Traditional keyword search may fail to retrieve semantically similar sentences because the wording differs.

Semantic search solves this problem using embeddings and vector similarity.

---

# What Are Embeddings?

Embeddings are numerical vector representations of text.

Example:

"Artificial intelligence helps doctors."

becomes a numerical vector.

Semantically similar sentences produce vectors close together in vector space.

---

# Technologies Used

| Technology | Purpose |
|---|---|
| FAISS | Local vector similarity search |
| Sentence Transformers | Generate embeddings |
| OpenSearch Serverless | Cloud vector database/search engine |
| boto3 | AWS SDK for Python |
| OpenSearch Python Client | Communicate with OpenSearch |
| AWS IAM | Authentication and authorization |

---

# What Is FAISS?

FAISS stands for Facebook AI Similarity Search.

It is a high-performance vector similarity library developed by Meta.

Used for:
- semantic search
- recommendation systems
- retrieval systems
- nearest neighbor search

Advantages:
- very fast
- lightweight
- excellent for experimentation

Disadvantages:
- local-only
- not cloud-native
- limited scalability

---

# What Is OpenSearch?

Amazon OpenSearch is a search and analytics engine.

It supports:
- keyword search
- vector search
- semantic retrieval
- hybrid search
- analytics

OpenSearch Serverless is a managed AWS version where AWS handles:
- infrastructure
- scaling
- availability
- provisioning

---

# What Is a Collection?

A collection is the top-level OpenSearch Serverless resource.

Think of it as:
- a search workspace
- an isolated search environment
- a managed search cluster

Collections contain:
- indexes
- vector data
- documents

Without a collection:
- indexes cannot exist
- vector search cannot operate

---

# What Is an Index?

An index is similar to a SQL table.

It stores:
- documents
- text fields
- embeddings
- metadata

Example document:

{
  "text": "AI improves healthcare diagnosis",
  "embedding": [0.12, 0.88, ...]
}

---

# What Is knn_vector?

OpenSearch uses a special field type called:

knn_vector

This stores embeddings.

Example:

"embedding": {
  "type": "knn_vector",
  "dimension": 384
}

The dimension must match the embedding model output.

---

# Project Structure

practical-7-vector-search/
│
├── README.md
├── requirements.txt
├── .env
├── .gitignore
│
├── data/
│   └── sentences.py
│
├── faiss_local/
│   ├── generate_embeddings.py
│   ├── build_index.py
│   └── search.py
│
└── opensearch_aws/
    ├── create_collection.py
    ├── create_index.py
    ├── index_documents.py
    ├── keyword_search.py
    ├── semantic_search.py
    ├── hybrid_search.py
    └── utils.py

---

# File-by-File Explanation

# README.md

Contains:
- project explanation
- setup instructions
- execution flow

Purpose:
- documentation
- reproducibility

---

# requirements.txt

Contains project dependencies.

Example:
- sentence-transformers
- faiss-cpu
- boto3
- opensearch-py
- python-dotenv

Used with:

pip install -r requirements.txt

---

# .env

Stores environment variables securely.

Example:

AWS_REGION=us-east-1
OPENSEARCH_COLLECTION_ENDPOINT=xxxxx.us-east-1.aoss.amazonaws.com

Purpose:
- avoid hardcoding secrets
- environment portability

---

# .gitignore

Prevents sensitive files from being committed.

Example:
- .env
- __pycache__/

---

# data/sentences.py

Contains dataset sentences used for:
- embeddings
- indexing
- vector search

The dataset intentionally contains multiple domains to better demonstrate semantic similarity.

---

# FAISS LOCAL SECTION

# generate_embeddings.py

Purpose:
- load embedding model
- generate sentence embeddings

Flow:

Sentence
→ Embedding Model
→ Vector

---

# build_index.py

Purpose:
- create FAISS vector index
- store embeddings

Flow:

Embeddings
→ FAISS Index
→ Similarity Search

---

# search.py

Purpose:
- generate query embedding
- search nearest vectors
- retrieve similar sentences

Flow:

User Query
→ Embedding
→ FAISS Search
→ Similar Results

---

# AWS SECTION

# Why Move to AWS?

FAISS is local-only.

Production systems require:
- scalability
- persistence
- distributed search
- APIs
- security
- cloud access

OpenSearch solves these issues.

---

# AWS Services Used

| Service | Purpose |
|---|---|
| IAM | User permissions and authentication |
| OpenSearch Serverless | Managed vector search engine |
| boto3 | AWS SDK |
| AWS4Auth | Request signing |

---

# What Is IAM?

IAM controls:
- users
- permissions
- authentication
- authorization

Without IAM:
- AWS APIs cannot be securely accessed

---

# Why Permissions Matter

OpenSearch Serverless requires:
1. IAM permissions
2. Data access policies
3. Network policies

All three must work together.

---

# What Is boto3?

boto3 is AWS's Python SDK.

Used for:
- creating collections
- managing policies
- AWS API communication

---

# What Is AWS4Auth?

AWS APIs require signed requests.

AWS4Auth:
- signs requests
- authenticates requests
- enables secure OpenSearch communication

Without signing:
- requests fail with 403 errors

---

# create_collection.py

Purpose:
- create OpenSearch collection
- create security policies

Creates:
- encryption policy
- network policy
- collection resource

---

# Network Policy

Controls:
- who can access collection endpoints

Example:
"AllowFromPublic": true

Without this:
- requests are blocked

---

# Data Access Policy

Controls:
- who can read/write indexes

Uses IAM principal ARNs.

Example:

"Principal": [
  "arn:aws:iam::ACCOUNT:user/username"
]

---

# create_index.py

Purpose:
- create vector-enabled index

Defines:
- text field
- knn_vector field

Important setting:

"index.knn": true

This enables vector similarity search.

---

# index_documents.py

Purpose:
- generate embeddings
- upload documents into OpenSearch

Each document contains:
- text
- vector embedding

Flow:

Sentence
→ Embedding
→ OpenSearch Index

---

# keyword_search.py

Performs lexical search using BM25 ranking.

Strengths:
- exact term matching

Weaknesses:
- poor semantic understanding

---

# semantic_search.py

Performs vector similarity search.

Flow:

Query
→ Embedding
→ Vector Similarity Search

Strengths:
- understands meaning
- retrieves paraphrases

Weaknesses:
- computationally heavier

---

# hybrid_search.py

Combines:
- keyword search
- semantic search

Benefits:
- balances exact matches and semantic meaning

Widely used in production AI systems.

---

# Understanding Search Scores

# Semantic Search Scores

Usually between:
0 → 1

Because cosine similarity is often normalized.

Higher values indicate stronger semantic similarity.

---

# Keyword Search Scores

BM25 scores are unbounded.

They can exceed:
- 2
- 5
- 10

depending on:
- keyword frequency
- rarity
- document length

---

# Hybrid Scores

Hybrid scores combine:
- lexical relevance
- semantic similarity

Absolute values are less important than ranking order.

---

# Common Problems Encountered

# 403 Forbidden

Cause:
- missing permissions
- incorrect policies
- bad request signing

Fix:
- IAM permissions
- APIAccessAll
- valid region
- correct policies

---

# REGION=None

Cause:
- .env not loaded correctly

Effect:
- AWS signing fails

Fix:
- place .env in project root

---

# Duplicate Documents

Cause:
- reindexing without clearing index

Fix:
- delete/recreate index

---

# FAISS vs OpenSearch

| Feature | FAISS | OpenSearch |
|---|---|---|
| Local | Yes | No |
| Distributed | No | Yes |
| Cloud Native | No | Yes |
| Security | Minimal | Strong |
| Scalability | Limited | High |
| Hybrid Search | Manual | Built-in |

---

# Drawbacks of Vector Search

| Drawback | Explanation |
|---|---|
| Computationally expensive | High-dimensional math |
| Storage heavy | Embeddings consume space |
| Approximate retrieval | Results may not be perfect |
| Model dependent | Search quality depends on embedding model |

---

# Real-World Applications

Vector search powers:
- AI assistants
- semantic document search
- recommendation engines
- RAG pipelines
- enterprise knowledge systems

---

# Practical Learning Outcomes

After completing this practical, you understand:
- embeddings
- vector similarity
- semantic retrieval
- FAISS indexing
- OpenSearch Serverless
- AWS IAM
- hybrid search
- vector database architecture

---

# Execution Flow

# Local FAISS Flow

Sentences
→ Embeddings
→ FAISS Index
→ Similarity Search

---

# OpenSearch Flow

Sentences
→ Embeddings
→ OpenSearch Index
→ Keyword Search
→ Semantic Search
→ Hybrid Search

---

# Final Conclusion

This practical demonstrates the transition from:
- traditional keyword search
to:
- modern semantic AI retrieval systems

The project begins with FAISS to build intuition around:
- embeddings
- vector spaces
- nearest neighbor retrieval

It then scales into a production-style architecture using:
- OpenSearch Serverless
- AWS IAM
- cloud-based vector indexing

The practical also highlights the difference between:
- lexical relevance
- semantic similarity
- hybrid retrieval

These are foundational concepts behind:
- Retrieval-Augmented Generation (RAG)
- AI copilots
- semantic search systems
- intelligent assistants