# AI-Practicals

## About the Project

`AI-Practicals` is a hands-on learning repository that collects a sequence of AI and machine learning exercises, from foundational NLP and classical model building to modern retrieval-augmented generation (RAG), agent workflows, and multi-agent coordination.

The repository is organized into:
- three milestone-level projects that build progressively more advanced AI systems using AWS Bedrock, OpenSearch, and agent orchestration,
- multiple practical exercises that explore text classification, embeddings, vector search, prompt engineering, document ingestion, and intelligent tool calling.

This work demonstrates how to design, implement, and evaluate practical AI systems with real-world architecture patterns, including API services, vector search, workflow routing, and AWS cloud integrations.

## Technologies & Implementation

### Core stack
- Python 3
- FastAPI for REST APIs and service endpoints
- Streamlit for lightweight application frontends
- `python-dotenv` / `.env` for configuration management
- Pydantic for structured data validation
- Pytest for automated tests

### AWS and cloud services
- AWS Bedrock for LLM inference and embeddings
- Amazon S3 for document storage and ingestion
- OpenSearch Serverless for vector search and semantic retrieval
- PostgreSQL for structured SQL data access in agent workflows

### AI and data tooling
- `scikit-learn` for TF-IDF, classifiers, and evaluation metrics
- `gensim` for Word2Vec model training and exploration
- `sentence-transformers` for SBERT embeddings
- FAISS for local vector similarity search
- LangChain for retrieval, prompt chaining, and tool-enabled agents
- LangGraph for conditional workflow routing and agent orchestration
- Langfuse for tracing and observability of agent execution
- CrewAI for multi-agent collaboration and sequential task execution
- LangChain community loaders for PDF ingestion and text chunking

## Architectural Choices

### Why AWS Bedrock?
AWS Bedrock provides managed access to high-quality foundation models such as Nova, Claude, and Titan. It was chosen to avoid local model maintenance while enabling prompt-driven classification, summarization, structured output extraction, and tool selection.

### Why OpenSearch Serverless?
OpenSearch Serverless is used for vector search because it supports KNN vectors, scales without manual cluster management, and integrates cleanly with AWS credentials and Bedrock embeddings. It is a pragmatic choice for RAG systems where latency and scalability matter.

### Why FastAPI and Streamlit?
FastAPI was selected for backend APIs due to its performance, automatic request validation, and OpenAPI documentation. Streamlit provides a rapid UI layer for interactive demos without requiring front-end engineering.

### Why LangChain, LangGraph, and CrewAI?
- LangChain enables modular retrieval and agent flows.
- LangGraph supports conditional routing, workflow state, and branching between SQL and RAG execution paths.
- CrewAI demonstrates multi-agent collaboration for research and writing workflows.

### Alternatives considered
Other architectures could use:
- local LLMs such as GPT-4all, llama.cpp, or Ollama for offline experimentation,
- vector stores like Pinecone, Milvus, or Weaviate instead of OpenSearch,
- Flask or Django rather than FastAPI,
- React/Vue instead of Streamlit for more advanced frontend UIs.

## Milestones

### Milestone 1 — LLM Microservice
- FastAPI microservice exposing `/classify` and `/summarize` endpoints.
- Uses Amazon Bedrock / Nova Lite for text classification and summarization.
- Implements structured JSON responses, Pydantic validation, Swagger docs, and error handling.
- Includes a test suite and AWS credentials configuration guidance.

### Milestone 2 — RAG Application
- End-to-end retrieval-augmented generation pipeline for document question answering.
- Uses PDF ingestion, text chunking, Bedrock embeddings, and OpenSearch semantic search.
- Serves user queries through FastAPI and includes a Streamlit chat frontend.
- Demonstrates cloud-native AWS integration for S3, Bedrock, and OpenSearch.

### Milestone 3 — Agentic Routing
- Builds an intelligent routing agent that chooses between SQL and RAG.
- Uses LangGraph workflow orchestration to route user queries based on intent.
- Implements a SQL agent with PostgreSQL schema introspection and read-only execution.
- Reuses the Milestone 2 RAG retrieval stack for document-based answers.
- Adds Langfuse tracing and conversation memory for observability and multi-turn context.

## Practicals

### Practical 1 — TF-IDF Classifier
- Builds a spam classifier using TF-IDF vectorization and logistic regression / Naive Bayes.
- Covers preprocessing, stopword removal, n-gram features, and model evaluation.
- Uses `pandas`, `scikit-learn`, `nltk`, and visualization with Matplotlib / Seaborn.

### Practical 2 — Word2Vec Exploration
- Trains a Word2Vec model on the Brown corpus.
- Explores semantic similarity, analogies, and vector arithmetic.
- Includes PCA and t-SNE visualization of learned word embeddings.

### Practical 3 — Bedrock Hello World
- Onboarding guide for AWS Bedrock access.
- Covers AWS CLI setup, IAM permissions, Bedrock model access, and basic Bedrock API usage.
- Demonstrates model listing, Converse API invocation, and experimentation with temperature and top-p.

### Practical 4 — Prompt Engineering
- Focuses on prompt composition and structured output behaviors.
- Builds on Bedrock configuration from Practical 3.
- Documents prompt construction, model settings, and effective instruction design.

### Practical 5 — Structured Output (Reviews)
- Processes product reviews with an LLM to generate structured JSON output.
- Uses Bedrock to extract sentiment, key topics, and rating estimates.
- Validates output with Pydantic and supports retries, logging, and export.

### Practical 5 — Interactive Tool Calling (Weather & Stocks)
- Implements a Bedrock-powered tool selection flow.
- The model dynamically chooses between `get_weather` and `get_stock_price` tools.
- Validates tool decisions and saves results to structured output.
- Demonstrates safe tool calling, modular tool design, and interactive CLI behavior.

### Practical 6 — Sentence Embeddings & SBERT
- Demonstrates sentence embedding generation using SBERT (`all-MiniLM-L6-v2`).
- Computes cosine similarity for semantic sentence matching.
- Visualizes embeddings with t-SNE and explores clustering by topic.

### Practical 7 — Vector Search: FAISS to OpenSearch
- Builds a local FAISS vector search pipeline.
- Compares FAISS with AWS OpenSearch Serverless for scalable vector retrieval.
- Covers embedding generation, vector indexing, keyword search, semantic search, and hybrid search.

### Practical 8 — Document Ingestion Pipeline
- Implements a PDF ingestion pipeline with upload, extraction, chunking, embedding, indexing, and retrieval.
- Uses local PDF extraction, OpenSearch vector indexing, and evaluation support.
- Provides a reusable pipeline for document search and retrieval experiments.

### Practical 9 — Not Included
- `practical-09` is not present in this repository.
- Placeholder included for future extension or missing coursework.

### Practical 10 — LangChain Agent
- End-to-end LangChain agent with FastAPI backend and Streamlit frontend.
- Includes tool-enabled reasoning with calculator, web search, and RAG retrieval tools.
- Maintains conversation memory and uses Bedrock for both retrieval and generation.
- Structures retrieval with OpenSearch Serverless and custom agent middleware.

### Practical 11 — LangGraph Conditional Workflow
- Demonstrates LangGraph conditional routing for SQL vs. RAG execution.
- Includes PostgreSQL setup, schema-based SQL query generation, error handling node, and RAG retrieval.
- Uses Mermaid graph visualization to inspect workflow states.

### Practical 13 — CrewAI Multi-Agent Crew
- Builds a research-and-writing multi-agent workflow using CrewAI.
- Coordinates a Researcher agent to gather information and a Writer agent to produce a structured markdown report.
- Outputs a final summary report to `outputs/final_report.md`.

## Key Learnings

### Practical insights
- Basic NLP workflows can be built with TF-IDF and Word2Vec before moving to embeddings and retrieval.
- Structured output and prompt design are essential for reliable LLM integrations.
- Vector similarity search is the foundation for RAG and semantic retrieval.
- Multi-agent orchestration improves modularity and enables complex task decomposition.

### Engineering takeaways
- Use FastAPI for clean API boundaries and automatic validation.
- Keep tool-selection loops bounded to avoid runaway agent behavior.
- Choose managed vector stores when scaling retrieval-heavy applications.
- Observe agent decisions with tracing platforms to debug and improve workflows.
- Validate model outputs with schemas to catch parsing and format errors early.

### Architecture lessons
- Combining SQL and RAG in a single routing flow enables hybrid knowledge access.
- Conversation memory and contextual state are important for follow-up queries.
- AWS-managed services reduce operational overhead for Bedrock and OpenSearch.
- Local experimentation with FAISS and SBERT helps validate concepts before moving to cloud deployment.

## Repository Structure

- `milestone-01-llm-microservice/` — Bedrock-powered FastAPI microservice
- `milestone-02-rag-application/` — RAG pipeline with OpenSearch and Streamlit
- `milestone-03-agentic-routing/` — LangGraph-based SQL/RAG routing agent
- `practical-01-tfidf-classifier/` — TF-IDF spam classification
- `practical-02-word2vec-exploration/` — Word2Vec training and visualization
- `practical-03-bedrock-hello-world/` — AWS Bedrock onboarding and demo
- `practical-04-prompt-engineering/` — prompt engineering notes
- `practical-05-structured-output/` — structured review extraction + tool calling
- `practical-06-sentence-embeddings/` — SBERT sentence similarity notebook
- `practical-07-vector-search/` — FAISS and OpenSearch vector search
- `practical-8-document-ingestion/` — document ingestion and indexing pipeline
- `practical-10-langchain-agent/` — LangChain agent application
- `practical-11-langgraph/` — LangGraph conditional workflow demo
- `practical-13-crewai/` — CrewAI multi-agent workflow

## Getting Started

Each subproject includes its own setup instructions and requirements file. The typical workflow is:

1. `cd` into the chosen subdirectory
2. create and activate a Python virtual environment
3. install dependencies with `pip install -r requirements.txt`
4. copy or create `.env` from `.env.example` when needed
5. follow that subproject's README for run commands

---

If you want a specific path or subproject expanded into its own dedicated documentation, open the relevant folder and I can generate a more focused README or runbook.
