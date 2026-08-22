# Practical 10: LangChain Agent Project Overview

## Project Purpose
This project builds a simple LangChain-based agent application with:
- a FastAPI backend,
- a Streamlit frontend,
- RAG retrieval from OpenSearch,
- AWS Bedrock model integration,
- tool usage including calculator, web search, and document retrieval,
- and conversation memory.

The main goal is to demonstrate an end-to-end agent workflow with safe tool use and retrieval-augmented generation.

---

## High-Level Structure

```text
practical-10-langchain-agent/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── PROJECT_OVERVIEW.md
├── app/
│   ├── api/
│   │   └── main.py
│   ├── agent/
│   │   ├── agent.py
│   │   ├── memory.py
│   │   └── tools.py
│   ├── core/
│   │   ├── aws_clients.py
│   │   ├── config.py
│   │   └── opensearch_client.py
│   ├── frontend/
│   │   └── streamlit_app.py
│   ├── ingestion/
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── opensearch_store.py
│   │   ├── pdf_extractor.py
│   │   └── s3_loader.py
│   └── rag/
│       ├── chain.py
│       └── retriever.py
├── scripts/
│   ├── create_index.py
│   ├── ingest_pipeline.py
│   └── setup_opensearch.py
└── venv/
```

---

## Key Files and Their Roles

### `app/api/main.py`
- Defines the FastAPI app.
- Exposes two endpoints:
  - `POST /ask` for legacy RAG-only question answering.
  - `POST /agent` for the LangChain tool-using agent.
- Uses the `ask_agent()` function from `app.agent.agent`.
- Handles optional `conversation_id` and `max_iterations` parameters.

### `app/agent/agent.py`
- Builds the LangChain agent using `create_agent()`.
- Uses AWS Bedrock for the LLM via `ChatBedrock`.
- Registers three tools:
  - `CalculatorTool`
  - `WebSearchTool`
  - `RAGRetrieverTool`
- Uses `ToolCallLimitMiddleware` to cap tool loop iterations.
- Maintains conversation history using `ConversationMemory`.
- Converts the graph-style agent response into a final assistant answer.

### `app/agent/tools.py`
Defines the three tools used by the agent:
- `CalculatorTool`
  - Implements safe arithmetic evaluation using Python AST.
  - Supports `+`, `-`, `*`, `/`, `**`, `%`, and selected math functions.
- `WebSearchTool`
  - Provides a mocked web search response.
  - No real external search calls are made.
- `RAGRetrieverTool`
  - Uses the RAG retriever to query the OpenSearch-backed vector store.
  - Returns relevant document passages as text.

### `app/agent/memory.py`
- Implements in-memory conversation history.
- Stores messages by `conversation_id`.
- Exposes:
  - `add_message()` to save a turn,
  - `get_history()` to retrieve raw history,
  - `get_context()` to produce a compact text summary for prompts.
- Helps the agent continue follow-up conversations.

### `app/core/config.py`
- Loads environment variables via `python-dotenv`.
- Exposes settings for:
  - AWS creds (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`)
  - S3 bucket name
  - Bedrock model IDs for embeddings and LLM
  - OpenSearch collection and index names

### `app/core/aws_clients.py`
- Creates boto3 clients for:
  - S3
  - Bedrock runtime
- These clients are reused across ingestion, retrieval, and inference.

### `app/core/opensearch_client.py`
- Initializes an OpenSearch Serverless client.
- Uses `boto3` to query collection status until the collection becomes active.
- Builds an authenticated `OpenSearch` client with AWS SigV4 credentials.
- This file is important because the retrieval stack depends on the OpenSearch endpoint being available.

### `app/rag/chain.py`
- Implements the core RAG question-answering flow.
- Retrieves documents from the vector retriever.
- Builds a prompt that includes the retrieved context.
- Calls Bedrock LLM via `ChatBedrock.invoke()`.
- Returns the final answer text.

### `app/rag/retriever.py`
- Configures `OpenSearchVectorSearch` from `langchain_community`.
- Connects to the OpenSearch Serverless index.
- Wraps the vector store in a LangChain retriever.
- The retriever is used by both the agent tool and the legacy RAG endpoint.

### `app/frontend/streamlit_app.py`
- Implements a chat UI using Streamlit.
- Stores session state for `conversation_id` and message history.
- Sends user questions to the backend `/agent` endpoint.
- Shows the assistant response in a chat interface.
- Includes a slider for `max_iterations`.

### `app/ingestion/*.py`
These files support document ingestion into the vector store.

#### `chunker.py`
- Uses `RecursiveCharacterTextSplitter` to break documents into chunks.
- Sets chunk size to 1000 characters with 200-character overlap.

#### `embeddings.py`
- Creates the Bedrock embedding model via `BedrockEmbeddings`.
- Used to convert text chunks into vectors.

#### `opensearch_store.py`
- Stores text chunks into OpenSearch as vectors.
- Uses `OpenSearchVectorSearch.from_documents()`.

#### `pdf_extractor.py`
- Loads PDFs using `PyPDFLoader`.
- Returns a list of LangChain `Document` objects.

#### `s3_loader.py`
- Downloads files from S3 using the shared S3 client.
- Allows ingestion to consume remote PDFs.

### `scripts/` folder
Contains utility scripts for infrastructure and ingestion.
- `setup_opensearch.py` - create OpenSearch collections / policies
- `create_index.py` - create the OpenSearch vector index
- `ingest_pipeline.py` - run ingestion from source documents into OpenSearch

---

## How Tools Are Implemented

### Calculator Tool
- Implemented in `app/agent/tools.py` as `CalculatorTool`.
- Inherits `BaseTool` from `langchain_core.tools`.
- Uses a restricted AST walker to avoid unsafe code execution.
- Only allowed expressions and selected math functions are supported.
- It returns a string result.

### Web Search Tool
- Implemented as `WebSearchTool`.
- Simulates a web search response with canned text.
- Detects keywords like `langchain`, `pdf`, and `document` to return topical mock answers.
- This avoids external network dependency.

### RAG Retriever Tool
- Implemented as `RAGRetrieverTool`.
- Uses `retriever.invoke(question)` from `app/rag/retriever.py`.
- Formats the top 3 retrieved document passages into a readable summary.
- This tool allows the agent to answer questions based on indexed documents.

---

## What `max_iterations` Means

- `max_iterations` is a safety limit for the agent’s internal tool-calling loop.
- It is enforced by `ToolCallLimitMiddleware` in `app/agent/agent.py`.
- If the agent requests tools too many times, the middleware raises `ToolCallLimitExceededError`.
- The backend catches this exception and returns a safe message instead of letting the agent run indefinitely.
- In practice, this prevents runaway behavior when the model keeps choosing tools or loops.
- The Streamlit UI exposes `max_iterations` as a slider so users can control the safety threshold.

### Why It's Important
- Without this guard, a tool-enabled agent could get stuck in repeated planning/tool execution loops.
- `max_iterations` is a practical safety mechanism for production-style agent workflows.

---

## How the Project Works End-to-End

1. **User asks a question in Streamlit**
2. **Streamlit sends** request to `POST /agent` with `question`, `conversation_id`, and `max_iterations`
3. **FastAPI receives** the request in `app/api/main.py`
4. **FastAPI calls** `ask_agent()` in `app/agent/agent.py`
5. **`ask_agent()`**
   - adds the user message to conversation memory
   - composes history into the system prompt
   - creates a LangChain agent with tools and middleware
   - invokes the agent with a user message payload
   - extracts the final assistant answer from the graph output
   - stores the assistant reply in memory
6. **The agent runs** the model and may call tools:
   - calculator for math
   - mock web search for general world knowledge
   - document retrieval for corpus-specific answers
7. **The response returns** to FastAPI, then to Streamlit
8. **Streamlit displays** the assistant answer and preserves the conversation ID for follow-ups

---

## Important Notes

- The project uses `langchain` and `langgraph` under the hood. The agent returns graph-style output that must be parsed before display.
- `ConversationMemory` is simple and in-memory only, so it will reset when the process restarts.
- The OpenSearch client initialization in `app/core/opensearch_client.py` blocks until the collection is ready, which avoids startup failures.
- The agent’s tool implementation is intentionally lightweight to keep the system stable and deterministic.

---

## Recommended Run Commands

```bash
cd practical-10-langchain-agent
source ../venv/bin/activate
uvicorn app.api.main:app --reload
streamlit run app/frontend/streamlit_app.py
```

---

## Summary
This practical project demonstrates a full LangChain agent app built around AWS Bedrock and OpenSearch Serverless. It combines:
- local tool execution,
- retrieval-augmented generation,
- safety middleware,
- conversational memory,
- and a simple chat frontend.

The project is a good example of how to structure an LLM application with modular tooling and a stable backend.
