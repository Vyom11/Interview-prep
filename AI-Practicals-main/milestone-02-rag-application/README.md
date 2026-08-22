# 📘 RAG Application Report (Milestone 02)

## 📌 Overview
This project implements a **Retrieval-Augmented Generation (RAG) pipeline** using AWS services and modern LLM tooling. The system allows users to ask questions about documents (PDFs), and it retrieves relevant content before generating accurate answers using a large language model.

---

## 🎯 Objective
The goal of this project is to:
- Build an **end-to-end RAG system**
- Enable **document-based question answering**
- Use **cloud-native AWS services**
- Understand **vector databases and embeddings**
- Integrate **backend + frontend systems**

---

## 🧠 What the Project Does

### Workflow:
1. PDF is stored in **S3**
2. Extract text using **PyPDFLoader**
3. Split text into chunks using **LangChain**
4. Convert chunks into vectors using **Bedrock Embeddings**
5. Store vectors in **OpenSearch Serverless**
6. User asks a question
7. System retrieves relevant chunks
8. LLM generates answer using context
9. Response shown via API / Streamlit

---

## 🏗️ Architecture

```text
User → FastAPI → Retriever → OpenSearch
                                 ↑
                        Embeddings (Bedrock)
                                 ↑
                   Chunked Documents (LangChain)
                                 ↑
                        PDF Loader (PyPDF)
                                 ↑
                                S3
```

---

## 🧰 Technologies Used

### 1. **Amazon S3**
- **What it is:** A scalable object storage service used to store files.
- **Why used:** Stores PDF documents, acts as the input data source, and is highly durable and scalable.

### 2. **PyPDFLoader (Local Extraction)**
- **What it is:** A document loader from LangChain that extracts text from PDFs.
- **Why used:** Simpler than Textract, has no AWS dependency, and is faster for local development.

### 3. **LangChain**
- **What it is:** A framework for building applications with LLMs.
- **Why used:** Handles chunking of documents, provides retriever abstraction, and integrates seamlessly with vector stores and LLMs.

### 4. **AWS Bedrock (Embeddings + LLM)**
- **What it is:** A fully managed service providing access to foundation models like Titan, Claude, and Nova.
- **Why used:** 
  - *Embeddings:* Converts text into vector representations to enable similarity search.
  - *LLM:* Generates accurate answers using the retrieved context.

### 5. **OpenSearch Serverless**
- **What it is:** A managed search and analytics engine with vector search support.
- **Why used:** Stores embeddings (acting as a Vector DB), performs similarity searches, and is serverless (requiring no infra management).

### 6. **FastAPI**
- **What it is:** A high-performance Python web framework.
- **Why used:** Provides the `/ask` endpoint, handles user queries, and connects the frontend with the backend.

### 7. **Streamlit**
- **What it is:** A Python framework for building web apps.
- **Why used:** Provides a simple chat UI, enables a quick frontend for testing, and allows for real-time user interaction.

---

## 📂 Folder Structure

```text
milestone-02-rag-application/
│
├── app/
│   ├── api/
│   │   └── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── opensearch_client.py
│   │   └── bedrock.py
│   │
│   ├── rag/
│   │   ├── chain.py
│   │   ├── ingest.py
│   │   └── retriever.py
│   │
│   └── frontend/
│       └── streamlit_app.py
│
├── scripts/
│   ├── setup_opensearch.py
│   ├── create_index.py
│   └── ingest_pipeline.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## 📄 File-Level Explanation

### `app/api/main.py`
- Entry point of FastAPI.
- Defines the `/ask` endpoint.
- Accepts the user's question and calls the RAG pipeline.

### `app/core/config.py`
- Loads environment variables.
- Central config for AWS credentials, Model IDs, and Index names.

### `app/core/opensearch_client.py`
- Initializes the OpenSearch client.
- Connects to the serverless collection and handles authentication.

### `app/core/bedrock.py`
- Initializes Bedrock clients for both the Embedding model and the LLM model.

### `app/rag/chain.py`
- Contains core RAG logic.
- Steps include retrieving documents, building context, and sending the prompt to the LLM to return the final answer.

### `app/rag/ingest.py`
- Handles document ingestion.
- Loads PDFs, splits text into chunks, generates embeddings, and pushes them to OpenSearch.

### `app/rag/retriever.py`
- Wraps the vector store.
- Performs similarity searches and returns relevant chunks.

### `app/frontend/streamlit_app.py`
- The chat interface.
- Sends user queries to the API and displays the responses.

### `scripts/setup_opensearch.py`
- Uses `boto3` to create the OpenSearch collection and required security policies.

### `scripts/create_index.py`
- Creates the vector index.
- Defines the embedding dimensions and the vector field.

### `scripts/ingest_pipeline.py`
- Runs the full ingestion pipeline, connecting all components together.

### `.env`
- Stores sensitive configuration details (e.g., AWS keys, Model IDs, Index name).

### `requirements.txt`
- Lists all Python dependencies to ensure reproducibility.

### `README.md`
- Explains the setup steps, architecture, and instructions on how to run the project.

---

## 🔄 End-to-End Flow
**PDF** ➔ **Chunking** ➔ **Embedding** ➔ **Storage** ➔ **Retrieval** ➔ **LLM** ➔ **Answer**

---

## 🧠 Key Learnings
- Vector databases require strict dimension matching.
- Embeddings power semantic search.
- RAG drastically improves LLM accuracy and reduces hallucinations.
- AWS Bedrock simplifies API access to state-of-the-art models.
- OpenSearch Serverless enables highly scalable retrieval without overhead.

---

## 🚀 Conclusion
This project demonstrates a production-style RAG pipeline using modern tools. It seamlessly integrates cloud services, vector databases, and LLMs to create an intelligent document Q&A system. It reflects real-world engineering challenges—such as handling embedding mismatches, adapting to API changes, and configuring infrastructure—and showcases how to solve them effectively.

---