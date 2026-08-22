# Practical 8 - Document Ingestion Pipeline

### Project Structure

This repository implements a document ingestion pipeline for PDF files, with AWS-native storage and search components plus local extraction and chunking.

```
.
├── README.md
├── main.py
├── requirements.txt
├── app/
│   ├── chunking.py
│   ├── config.py
│   ├── embeddings.py
│   ├── evaluation.py
│   ├── indexing.py
│   ├── opensearch_client.py
│   ├── retrieval.py
│   ├── s3_upload.py
│   └── textract_service.py
├── data/
│   ├── pdfs/
│   └── extracted/
├── results/
│   └── evaluation_results.csv
└── tests/
    └── test_chunking.py
```

---

## How the Pipeline Works

### Core workflow
1. main.py starts the pipeline.
2. `app/s3_upload.py` uploads local PDFs from `data/pdfs/` to S3.
3. `app/textract_service.py` extracts text from the same PDFs locally and writes JSON files to `data/extracted/`.
4. `app/indexing.py` loads extracted JSON text, chunks it, generates embeddings, and indexes chunks into OpenSearch.
5. `app/retrieval.py` performs semantic search using the vector index.
6. `app/evaluation.py` evaluates retrieval quality for sample questions.

### Data flow
- `data/pdfs/*.pdf`: source PDF documents
- `data/extracted/*.json`: extracted text output
- `results/evaluation_results.csv`: retrieval evaluation results shown in csv

---

## File-by-File Details

### main.py
- Entry point for the pipeline.
- Parses `--chunk-size` (default `500`).
- Calls:
  - `upload_pdfs()`
  - `extract_documents()`
  - `run_indexing_pipeline(chunk_size=...)`

### requirements.txt
- Python dependencies including:
  - `boto3`, `langchain`, `langchain-aws`
  - `langchain-text-splitters`
  - `opensearch-py`, `requests-aws4auth`
  - `python-dotenv`, `pandas`, `matplotlib`

### `app/config.py`
- Loads environment variables using `dotenv`.
- Defines settings:
  - AWS region
  - S3 bucket name
  - OpenSearch host and index
  - Bedrock model ID
  - Embedding dimension

### `app/chunking.py`
- Defines `chunk_document(text, chunk_size)`.
- Uses `RecursiveCharacterTextSplitter` from LangChain.
- Splits text into chunks with 10% overlap.

### `app/embeddings.py`
- Defines `TitanEmbeddings` for AWS Bedrock embeddings.
- `embed_text(text)` calls `bedrock-runtime.invoke_model`.
- Parses returned JSON and returns the embedding vector.

### `app/opensearch_client.py`
- Manages OpenSearch Serverless collection and index.
- Creates security policies and collection if needed.
- Builds an authenticated `OpenSearch` client using AWS credentials.
- Creates index mappings for:
  - `text` as full text
  - `source` as keyword
  - `chunk_id` as integer
  - `embedding` as `knn_vector`

### `app/indexing.py`
- Implements the indexing pipeline.
- Loads `.json` files from `data/extracted`.
- Chunks text and generates embeddings.
- Validates vectors and indexes each chunk into OpenSearch with:
  - `text`
  - `source`
  - `chunk_id`
  - `embedding`

### `app/retrieval.py`
- Implements semantic search.
- Embeds query text.
- Issues a KNN search against the OpenSearch `embedding` field.
- Returns top results.

### `app/s3_upload.py`
- Uploads PDF files from `data/pdfs` to the configured S3 bucket.
- Uses `boto3.client("s3")`.

### `app/textract_service.py`
- Extracts PDF text locally via `PyPDFLoader` from LangChain community loaders.
- Writes text output as JSON to `data/extracted/<pdf_stem>.json`.
- Note: this module performs local extraction, not AWS Textract.

### `app/evaluation.py`
- Defines a set of evaluation questions.
- Runs semantic search for each question.
- Writes a CSV report to `results/evaluation_results.csv`.
- Prints summary information.

### `tests/test_chunking.py`
- Unit test for `chunk_document`.
- Verifies large text is split into multiple chunks.

---

## Detailed Flow Summary

1. User runs:
   ```bash
   python main.py --chunk-size 500
   ```
2. Pipeline uploads PDFs.
3. Pipeline extracts text locally into JSON.
4. Pipeline creates OpenSearch collection/index if needed.
5. Pipeline chunks text and generates vector embeddings using Bedrock.
6. Pipeline indexes chunks into OpenSearch Serverless.
7. Retrieval and evaluation can be run separately via `app/retrieval.py` and `app/evaluation.py`.

---

## Important Notes
- The project is designed to integrate AWS services, but the actual text extraction is performed locally.
- OpenSearch collection creation is automated if `OPENSEARCH_HOST` is not provided.
- Chunking size is configurable and affects retrieval granularity, storage, and performance.
