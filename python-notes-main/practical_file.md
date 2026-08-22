# AI-Practicals

## Overview

`AI-Practicals` is a portfolio repository for practical AI engineering exercises that span:
- classical NLP and machine learning,
- local and cloud-based embedding search,
- retrieval-augmented generation,
- tool-enabled LangChain agents,
- workflow orchestration with LangGraph,
- and cooperative agent workflows using CrewAI.

The repository is structured to show a natural progression from foundational models and text analytics to deployment-ready AI services and agent routing architectures.

## What this repository does

This codebase documents and implements:
- a FastAPI microservice for text classification and summarization using AWS Bedrock,
- a cloud RAG pipeline that ingests PDF documents into OpenSearch and answers questions,
- an agentic routing system that decides between SQL and RAG based on user intention,
- several standalone practicals exploring TF-IDF, Word2Vec, SBERT embeddings, FAISS, OpenSearch, prompt engineering, and multi-agent workflows.

It is designed as a learning portfolio for building real AI systems, integrating model APIs, vector databases, workflow graphs, and observability.

## Technologies & Implementation

### Core technologies
- Python 3.11+ (project-wide standard)
- FastAPI for REST API services
- Streamlit for lightweight interactive demos
- Pydantic/Pydantic Settings for schema and config validation
- Pytest for automated tests
- SQLAlchemy for PostgreSQL access in milestone 3
- boto3 for AWS service integration

### AI and vector tooling
- AWS Bedrock via `langchain_aws` and raw `boto3` for LLM and embedding calls
- LangChain to structure RAG retrieval and tool-using agent behavior
- LangGraph to define stateful, conditional workflows in milestone 3 and practical 11
- FAISS for local vector similarity experiments
- `sentence-transformers` for SBERT and Word2Vec embedding experiments
- OpenSearch Serverless for managed vector search and hybrid retrieval
- CrewAI for multi-agent sequential task orchestration

### Cloud and infrastructure
- Amazon Bedrock for text generation and embeddings
- OpenSearch Serverless as the vector search backend
- S3 for document storage and ingestion
- PostgreSQL for structured SQL data queries
- Langfuse for optional tracing and observability of agent decisions

## Architecture & Design Choices

### Project architecture
The repository is split into three milestone projects plus standalone practicals:
- `milestone-01-llm-microservice` focuses on an API wrapper around an LLM.
- `milestone-02-rag-application` builds a document ingestion and retrieval pipeline.
- `milestone-03-agentic-routing` adds intelligence to route queries between structured SQL access and unstructured RAG search.

Standalone practicals fill in the conceptual and implementation knowledge needed to support those systems.

### Why these technologies?
- **FastAPI** gives validated request/response models, clean dependency injection, and auto-generated docs.
- **AWS Bedrock** avoids local model hosting, enabling fast prototyping with managed LLMs.
- **OpenSearch Serverless** supports vector fields and hybrid search while minimizing devops.
- **LangChain / LangGraph** provide composition for retrieval + generation and conditional flow control.
- **Pydantic / schemas** keep external model outputs structured and safe.
- **Tooling layers** separate concerns: one module for model calls, one for retrieval, one for workflow orchestration.

### Alternatives considered
- Local LLMs like GPT4All or llama.cpp could replace Bedrock for offline work.
- Vector stores such as Pinecone, Milvus, or Weaviate could be used instead of OpenSearch.
- A full React frontend could replace Streamlit for production UI.
- Flask or Django could be substituted for FastAPI, but FastAPI is more suitable for modern async API services.

## Detailed Milestone Summaries

### Milestone 1 — LLM Microservice

Key implementation:
- `main.py` creates a FastAPI app and mounts `app.api.routes.router`
- `app.api.routes` exposes `/classify` and `/summarize`
- `app.services.bedrock_service.BedrockService` wraps the Bedrock runtime client
- Prompts are carefully constructed to return strict JSON for classification
- Responses are cleaned to remove Markdown fences and parsed into JSON
- Pydantic schemas validate inputs and outputs before sending responses

This milestone demonstrates:
- prompt engineering for reliable JSON output,
- LLM-based text classification and summarization,
- robust error handling around external API calls.

### Milestone 2 — RAG Application

Key implementation:
- `app.core.aws_clients` and `app.core.opensearch_client` initialize AWS Bedrock and OpenSearch connections
- `app.ingestion.pdf_extractor` uses `PyPDFLoader` to extract PDF text
- `app.ingestion.chunker` splits documents into 1,000-character chunks with overlap
- `app.ingestion.embeddings` creates a Bedrock embeddings adapter for LangChain
- `app.ingestion.opensearch_store` indexes vectorized chunks into `OpenSearchVectorSearch`
- `app.rag.retriever` configures a retriever that returns the top 3 semantically similar chunks
- `app.rag.chain.ask_question` composes retrieved context into a single prompt and generates an answer with `ChatBedrock`

Infrastructure scripts:
- `scripts/setup_opensearch.py` automates OpenSearch collection and policy creation
- `scripts/create_index.py` defines a kNN vector index with a 1024-dimensional field
- `scripts/ingest_pipeline.py` downloads a PDF from S3, extracts it, chunks it, and stores embeddings

This milestone shows:
- a complete ingestion-to-query RAG flow,
- integration of AWS-managed services with Python,
- the importance of retrieval quality when prompting LLMs.

### Milestone 3 — Agentic Routing

Key implementation:
- `app/main.py` exposes `/query`, health checks, and session management endpoints
- `app.graph.workflow.AgentWorkflow` composes `ClassifierAgent`, `SQLAgent`, `RAGAgent`, and `ConversationMemory`
- `ClassifierAgent` uses an LLM prompt to choose between SQL and RAG and includes a keyword fallback
- `SQLAgent` introspects PostgreSQL schema via `PostgresService`, generates only `SELECT` queries, and executes read-only SQL safely
- `RAGAgent` performs hybrid search using both keyword and vector results via `OpenSearchService`
- `ConversationMemory` retains up to 50 turns per session and supplies recent history to the classifier
- `app.utils.tracing` optionally sends Langfuse traces for each agent decision and workflow event

This milestone highlights:
- conditional routing between structured and unstructured knowledge,
- the value of schema introspection for safe SQL generation,
- hybrid search strategies combining text and embedding relevance,
- stateful agent workflows and traceable execution.

## Practical Summaries

### Practical 1 — TF-IDF Classifier

Code notes:
- `practical-01-tfidf-classifier/practical_1.py` loads `spam.csv` and preprocesses text
- Uses `TfidfVectorizer`, `LogisticRegression`, and `MultinomialNB`
- Experiments with stopword removal and n-gram features
- Evaluates with accuracy, precision, recall, F1, and confusion matrices

This practical is a foundation for understanding how text features and classical ML models compare to embedding-based approaches.

### Practical 2 — Word2Vec Exploration

Code notes:
- `practical-02-word2vec-exploration/practical_2.py` trains Word2Vec on the Brown corpus
- Demonstrates semantic similarity, analogy composition, and nearest-neighbor queries
- Includes PCA and t-SNE visualizations of word vectors

It illustrates distributional word semantics and how vector geometry encodes meaning.

### Practical 3 — Bedrock Hello World

This practical is mostly an onboarding guide for AWS Bedrock, covering:
- IAM user creation
- AWS CLI setup
- Bedrock model access configuration
- basic model invocation and parameter experimentation

It is a prerequisite for the cloud-based milestones.

### Practical 4 — Prompt Engineering

This practical documents prompt engineering guidance and the relationship between prompt design and model behavior. It emphasizes:
- clear instructions,
- structured output formats,
- model settings such as temperature and top-p.

### Practical 5 — Structured Output (Reviews)

Key implementation:
- `practical-05-structured-output/practical-05-structured-output-reviews/app.py` loads product reviews and calls `BedrockService` to extract structured fields
- Validates model output using `ReleaseReview` Pydantic schema
- Includes logging, retry logic, and result export

This shows how to enforce schema correctness on LLM outputs.

### Practical 5 — Interactive Tool Calling (Weather & Stocks)

Key implementation:
- `practical-05-structured-output/practical-05-structured-output-weather-stocks/app.py` uses `BedrockService.decide_tool` to select between `get_weather` and `get_stock_price`
- Executes the chosen tool locally and prints structured results

It demonstrates tool selection and controlled execution with a LLM-driven decision layer.

### Practical 6 — Sentence Embeddings & SBERT

Key implementation:
- `Practical6_SBERT_Sentence_Embeddings.ipynb` generates sentence embeddings with `all-MiniLM-L6-v2`
- Computes pairwise cosine similarity and clusters sentences into semantic groups
- Visualizes relationships with t-SNE

This practical provides intuition for why sentence embeddings power semantic search.

### Practical 7 — Vector Search: FAISS to OpenSearch

Key implementation:
- `practical-07-vector-search/faiss_local/generate_embeddings.py` builds local sentence embeddings
- `build_index.py` constructs a FAISS `IndexFlatL2`
- `search.py` performs nearest-neighbor similarity queries
- `practical-07-vector-search/opensearch_aws/` implements AWS OpenSearch collection creation, vector index creation, semantic search, keyword search, and hybrid search

This practical compares local search and managed cloud vector search.

### Practical 8 — Document Ingestion Pipeline

Key implementation:
- `practical-8-document-ingestion/practical-8-document-ingestion/main.py` orchestrates upload, extraction, and indexing
- `app/textract_service.py` loads PDFs with `PyPDFLoader`
- `app/indexing.py` chunks text, embeds chunks with Titan embeddings, and indexes them in OpenSearch
- `app/opensearch_client.py` creates OpenSearch collections and vector indexes programmatically
- `app/evaluation.py` provides retrieval quality checks

This practical implements a reusable end-to-end ingestion pipeline.

### Practical 10 — LangChain Agent

Key implementation:
- `app/agent/agent.py` builds a LangChain agent with `CalculatorTool`, `WebSearchTool`, and `RAGRetrieverTool`
- `ToolCallLimitMiddleware` enforces a max tool-call budget
- `app/agent/memory.py` keeps conversation history per `conversation_id`
- `app/api/main.py` exposes legacy `/ask` and agent `/agent` endpoints
- `app/rag/retriever.py` uses `OpenSearchVectorSearch` to retrieve documents

It demonstrates safe agent orchestration and conversational retrieval.

### Practical 11 — LangGraph Conditional Workflow

Key implementation:
- `workflow/graph.py` defines a `StateGraph` with nodes for classifier, SQL, RAG, and error handling
- Uses a rule-based keyword classifier with an LLM fallback
- Routes queries to the appropriate tool and composes the final answer

This practical shows how to model agent logic as a graph with explicit control flow.

### Practical 13 — CrewAI Multi-Agent Crew

Key implementation:
- `practical-13-crewai/main.py` boots a CrewAI process with Researcher and Writer agents
- The researcher collects information and the writer generates a Markdown report
- Outputs are persisted to `outputs/final_report.md`

This practical explores agent collaboration and task division.

## Key Learnings

### Architecture & engineering
- Building robust ML systems requires clear separation of concerns: model calling, retrieval, data ingestion, and workflow orchestration.
- RAG works best when retrieval quality is high and prompts are constrained to the retrieved context.
- A hybrid SQL/RAG architecture bridges structured data and unstructured knowledge.
- Observability with Langfuse or logging is essential for debugging agent decisions.
- Schema validation is critical for LLM outputs, especially when models produce JSON-like responses.

### Technical tradeoffs
- Managed cloud services reduce infrastructure work but introduce dependency on credentials and network availability.
- Local FAISS is fast for experimentation, while OpenSearch offers managed scaling and search features.
- Rule-based fallbacks are useful safety nets for classification when LLM parsing fails.
- Tool-enabled agents need explicit loop guards to avoid runaway execution.

## How to use this repository

1. Choose the subproject or milestone you want to explore.
2. `cd` into that folder.
3. Create and activate a virtual environment.
4. Install dependencies: `pip install -r requirements.txt`.
5. Configure `.env` as needed for AWS, PostgreSQL, OpenSearch, and Langfuse.
6. Follow the subproject README for run commands.

## Notes

- `practical-09` is not present in the repository.
- Most cloud projects require AWS credentials and optionally Langfuse API keys.
- The repository favors AWS Bedrock / OpenSearch, but the architecture can be adapted to other providers.

---

If you want, I can also generate a per-milestone architecture diagram or a shorter executive summary for non-technical stakeholders.
