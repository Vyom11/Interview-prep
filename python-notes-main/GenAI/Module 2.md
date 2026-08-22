# TOPIC 5: Vector Databases & AWS OpenSearch

## 1. Executive Summary
- Vector DBs store and efficiently search high-dimensional dense vectors
- Solve the "semantic search at scale" problem — SQL can't do nearest-neighbor over billions of vectors
- The spine of every RAG and semantic search system
- AWS OpenSearch Service = enterprise choice (managed, hybrid search, rich filtering)
- Core operation: given a query vector, find k most similar vectors (ANN)
- Engineers care because: wrong index choice = poor recall or OOM at scale
- Metadata filtering is critical — vector search without filters returns garbage in many use cases

## 2. Mental Model
- **Analogy**: A library where books are shelved by content similarity (not alphabetically). You walk in and say "I want books like this one" and get directed to the nearest shelf.
- **Key insight**: Vector DB = ANN index + metadata store + CRUD + production features
- **Design tension**: Recall vs Latency vs Memory — pick two

```
Documents → Embed → Store[vector, metadata, id]
Query → Embed → ANN search → filter metadata → return top-k IDs + scores → fetch docs
```

## 3. Core Concepts

| Concept | Definition |
|---------|-----------|
| ANN | Approximate Nearest Neighbor — fast but slightly imprecise |
| HNSW | Graph-based ANN — best recall/latency for most use cases |
| IVF | Cluster-based ANN — better for very large indices |
| Flat Index | Brute force exact search — correct, slow |
| Metadata Filtering | Filter by category, date, source BEFORE or AFTER vector search |
| Pre-filtering | Apply metadata filter, then vector search (fast but may miss results) |
| Post-filtering | Vector search, then apply metadata filter (slower but accurate) |
| Hybrid Search | BM25 keyword + vector similarity combined |
| Score Fusion | How to combine BM25 and vector scores (RRF, linear) |
| Sharding | Distribute index across nodes |
| Replication | Copies for availability and read throughput |

## 4. Engineering Deep Dive

### HNSW Deep Dive

**Build time**: `O(n × m × log(n))`  
**Query time**: `O(log(n))`  
**Memory**: `O(n × m × dim × precision)`

**Key parameters:**
| Parameter | Effect | Typical Value |
|-----------|--------|--------------|
| `m` | Connections per node; recall vs memory | 16-64 |
| `ef_construction` | Build-time graph quality | 200-512 |
| `ef_search` | Query-time recall vs speed | 100-512 |
| `space_type` | Distance metric: cosine, l2, innerproduct | cosine |

### OpenSearch Vector Index Configuration
```json
{
  "settings": {
    "index.knn": true,
    "index.knn.space_type": "cosine"
  },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 1536,
        "method": {
          "name": "hnsw",
          "engine": "nmslib",
          "space_type": "cosinesimil",
          "parameters": {
            "m": 16,
            "ef_construction": 512
          }
        }
      },
      "content": {"type": "text"},
      "source": {"type": "keyword"},
      "timestamp": {"type": "date"}
    }
  }
}
```

### Hybrid Search in OpenSearch
```python
# Combine BM25 + k-NN with Reciprocal Rank Fusion (RRF)
query = {
  "query": {
    "hybrid": {
      "queries": [
        {"match": {"content": query_text}},           # BM25
        {"knn": {"embedding": {"vector": query_vec, "k": 10}}}  # Vector
      ]
    }
  }
}
```

### Metadata Filtering Pattern
```python
# Filtered k-NN query
{
  "query": {
    "knn": {
      "embedding": {
        "vector": query_vector,
        "k": 10,
        "filter": {
          "bool": {
            "must": [
              {"term": {"source": "annual_report"}},
              {"range": {"date": {"gte": "2023-01-01"}}}
            ]
          }
        }
      }
    }
  }
}
```

### Scoring Normalization for Hybrid
- BM25 scores: unbounded (typically 0-20)
- k-NN scores: bounded (0-1 for cosine)
- Must normalize before combining: min-max normalization or L2 norm
- OpenSearch Normalization Processor handles this automatically in search pipeline

### Performance Considerations
- HNSW index lives in JVM heap → primary memory pressure
- Faiss-based engine (not nmslib) supports GPU, off-heap → better for huge indices
- Increase JVM heap to 50% of node RAM
- Warm cache before production: force-merge segments

## 5. Architecture Perspective

### Vector DB Selection Guide

| Use Case | Recommendation |
|----------|---------------|
| AWS-native, compliance | OpenSearch Service |
| Pure vector, managed | Pinecone |
| Open source, self-hosted | Qdrant, Weaviate |
| Prototyping, local | FAISS, Chroma |
| Postgres-embedded | pgvector |
| Multi-modal | Weaviate |

### When NOT to Use a Vector DB
- < 10K documents → FAISS in-memory or even cosine over numpy is fine
- Pure keyword search → Elasticsearch without k-NN is faster/cheaper
- Structured data with no semantic search → relational DB

## 6. Failure Modes & Debugging

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Poor recall | ef_search too low | Recall@k metric drop | Increase ef_search |
| JVM OOM | HNSW index too large for heap | Heap > 85%, GC pressure | Add nodes, increase heap, switch to Faiss |
| Wrong results | Metadata filter too aggressive | Missing expected docs | Check filter logic, post-filter instead |
| Slow indexing | m/ef_construction too high | High write latency | Reduce ef_construction for bulk load |
| Stale results | Embedding model changed, not re-indexed | Unexplained quality drop | Full re-index on model change |
| Score inversion | Wrong distance metric | High scores for irrelevant docs | Verify space_type matches model normalization |

## 7. End-to-End Flow
```
Document Ingestion:
Raw Doc → Text Extraction → Chunking → Embedding → OpenSearch Index

Query Flow:
User Query
    ↓
Query Embedding (bi-encoder)
    ↓
OpenSearch Hybrid Query (BM25 + k-NN)
    ↓
Score Normalization + Fusion (RRF)
    ↓
Metadata Filtering
    ↓
Top-K Results + Source Metadata
    ↓
Cross-Encoder Reranker (optional)
    ↓
RAG Context Assembly
```

## 8. Terminology Cheat Sheet

| Term | Meaning | Why It Matters |
|------|---------|---------------|
| RRF | Reciprocal Rank Fusion — hybrid score combination | Standard hybrid scoring |
| ef_construction | Graph quality at build time | Recall vs index time |
| ef_search | Graph quality at query time | Recall vs query latency |
| nmslib | Default HNSW engine in OpenSearch | Lives in JVM heap |
| Faiss | Meta's vector library — off-heap option | Better for huge indices |
| lucene | Lucene-based k-NN (HNSW) — also an option | JVM native |
| Segment | Lucene index unit — immutable | Affects query performance |
| Force-merge | Reduces segments for faster reads | Pre-production step |

## 9. Comparison Tables

### Vector DB Comparison

| DB | Type | Hybrid Search | Filtering | Managed | Best For |
|----|------|--------------|-----------|---------|---------|
| OpenSearch | Full-text + Vector | Yes (native) | Rich (Lucene) | AWS managed | Enterprise AWS |
| Pinecone | Vector-only | Limited | Yes | Fully managed | Simplicity |
| Qdrant | Vector-focused | Yes | Yes | Self/managed | Open source quality |
| Weaviate | Vector + graph | Yes | GraphQL | Self/managed | Multi-modal |
| pgvector | Postgres extension | Via SQL | SQL | Self | Existing Postgres |
| FAISS | Library | No | No | No | Local/embedded |
| Chroma | Embedded | No | Yes | No | Dev/prototype |

## 10. Interview Revision

### Senior Questions

**Q1: How do you tune OpenSearch for high recall with low latency?**
- **Answer**: Increase `ef_search` (recall), benchmark Recall@10 vs p99 latency tradeoff curve. Use Faiss engine for off-heap memory. Pre-warm with bulk queries. Use replica shards for parallel reads. Cache frequent queries.

**Q2: Explain the metadata filtering challenge in vector search.**
- **Answer**: Pre-filter (apply filter first, then search): may have too few vectors to find k results. Post-filter (search all, then filter): may return < k results if many filtered out. Solution: over-fetch (k×10) then filter. OpenSearch's filtered k-NN is sophisticated pre-filter.

**Q3: How would you migrate from one embedding model to another with zero downtime?**
- **Answer**: Create new index with new model. Dual-write to both indices. Background job re-indexes all documents. Validate new index Recall@k. Atomic cutover (config flag). Keep old index 7 days for rollback.

## 12. One-Page Revision Sheet

### Must Know
- HNSW: graph ANN, lives in JVM heap in OpenSearch (nmslib)
- Hybrid search = BM25 + k-NN with RRF score fusion
- Metadata filtering: pre-filter vs post-filter tradeoffs
- ef_search controls recall vs latency

### Production Nuggets
- Monitor JVM heap percentage — primary failure mode
- Force-merge before production for read performance
- Over-fetch then filter for reliable top-k with metadata

---

# TOPIC 6: LangChain Fundamentals

## 1. Executive Summary
- LangChain: Python/JS framework for building LLM-powered applications
- Provides building blocks: LLMs, prompts, chains, retrievers, memory, agents, tools
- Solves: orchestrating complex LLM workflows without reinventing infrastructure
- Where it fits: application layer above LLMs and vector DBs
- Problem: LLM apps need prompt management, output parsing, memory, tool use — LangChain packages all this
- LCEL (LangChain Expression Language) is the modern compose-first API
- Strong ecosystem: 100+ integrations (OpenAI, Bedrock, OpenSearch, Pinecone, etc.)
- Trade-off: convenience vs complexity; LangChain adds a layer you need to debug

## 2. Mental Model
- **Analogy**: LangChain is to LLM apps what Express.js is to web apps — provides structure, not magic
- **LCEL pipelines**: Unix pipes for LLM components: `prompt | llm | parser`
- **Key insight**: Everything in LangChain is a Runnable — composable, streamable, traceable

```
prompt_template | chat_model | output_parser
     ↓                ↓              ↓
   Runnable       Runnable       Runnable
     └───────────────────────────────┘
              RunnableSequence (chain)
```

## 3. Core Concepts

| Concept | Definition | Role |
|---------|-----------|------|
| Runnable | Base interface — has invoke/stream/batch | Everything is a Runnable |
| PromptTemplate | Parameterized prompt factory | Input formatting |
| ChatModel | LLM wrapper (OpenAI, Bedrock, etc.) | Text generation |
| OutputParser | Transforms raw LLM output | Structured output |
| Chain | Sequence of Runnables | Workflow |
| Retriever | Returns documents given a query | RAG component |
| VectorStore | Stores and searches embeddings | RAG component |
| Memory | Stores conversation history | Multi-turn context |
| Tool | Function the agent can call | Agent capability |
| Agent | LLM that decides which tools to call | Orchestration |
| LCEL | `|` operator for composing Runnables | Modern API |
| RunnableParallel | Run multiple chains in parallel | Performance |
| RunnablePassthrough | Pass input unchanged | Routing patterns |

## 4. Engineering Deep Dive

### LCEL Chains
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Answer: {question}")
model = ChatOpenAI(model="gpt-4o", temperature=0)
parser = StrOutputParser()

chain = prompt | model | parser

# Invoke
result = chain.invoke({"question": "What is RAG?"})

# Stream
for chunk in chain.stream({"question": "What is RAG?"}):
    print(chunk, end="")

# Batch (parallel)
results = chain.batch([{"question": "Q1"}, {"question": "Q2"}])
```

### RAG Chain with LCEL
```python
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import OpenSearchVectorSearch

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt  # "Context: {context}\nQuestion: {question}"
    | model
    | parser
)

answer = rag_chain.invoke("What is the capital of France?")
```

### Memory
```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
chain = ConversationChain(llm=model, memory=memory)

chain.predict(input="My name is Alice")
chain.predict(input="What is my name?")  # Remembers "Alice"
```

### Document Loaders + Text Splitters
```python
from langchain_community.document_loaders import S3FileLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load
loader = PyPDFLoader("document.pdf")
docs = loader.load()

# Split
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_documents(docs)
```

### Output Parsers
```python
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class Sentiment(BaseModel):
    label: str
    confidence: float

parser = PydanticOutputParser(pydantic_object=Sentiment)
prompt = PromptTemplate(
    template="Analyze sentiment.\n{format_instructions}\nText: {text}",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
chain = prompt | model | parser
result: Sentiment = chain.invoke({"text": "I love this!"})
```

### Key Integrations
| Integration | Class | Use |
|-------------|-------|-----|
| OpenAI | `ChatOpenAI` | LLM |
| Bedrock | `BedrockChat` / `ChatBedrock` | AWS LLM |
| OpenSearch | `OpenSearchVectorSearch` | Vector DB |
| Pinecone | `Pinecone` | Vector DB |
| S3 | `S3FileLoader` | Document loading |
| Redis | `RedisCache` | LLM caching |
| LangSmith | `LANGSMITH_API_KEY` env | Tracing |

## 5. Architecture Perspective

### When to Use LangChain
- Building RAG applications with standard patterns
- Need multiple LLM integrations with same code
- Rapid prototyping
- Team familiar with LangChain ecosystem

### When NOT to Use LangChain
- Simple single-LLM call → direct SDK is simpler
- Need full control over every step → build custom
- Debugging LangChain abstraction layers is painful
- LangGraph or raw Anthropic/OpenAI SDK may be cleaner for agents

### LangChain vs Raw SDK

| Aspect | LangChain | Raw SDK |
|--------|-----------|---------|
| Speed to build | Fast | Slower |
| Debugging | Hard (many layers) | Easy |
| Flexibility | Medium | Full |
| Integrations | 100+ out of box | Manual |
| Dependency weight | Heavy | Light |
| Version stability | Rapidly changing | Stable |

## 6. Failure Modes & Debugging

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Output parser failure | LLM didn't follow format | OutputParserException | Add retry with error feedback |
| Chain breaks on empty retrieval | No docs found, format_docs returns "" | Empty context | Add fallback for empty retrieval |
| Memory overflow | Unbounded conversation history | High token count | Use ConversationSummaryMemory |
| LCEL type mismatch | Wrong input/output schema between Runnables | Runtime error | Use RunnableLambda to transform |
| Dependency conflicts | LangChain package versions | Import errors | Pin versions, use virtual envs |
| Tracing overhead | LangSmith enabled in prod | Latency increase | Sample tracing in production |

## 7. End-to-End Flow
```
User Query (str)
    ↓
RunnablePassthrough (passes query through)
    ↓
Retriever (OpenSearch/Pinecone) → List[Document]
    ↓
format_docs function → str (context)
    ↓
PromptTemplate (context + question → ChatMessages)
    ↓
ChatModel (Bedrock/OpenAI) → AIMessage
    ↓
StrOutputParser / PydanticOutputParser → Final Answer
```

## 8. Terminology Cheat Sheet

| Term | Meaning | Why It Matters |
|------|---------|---------------|
| LCEL | LangChain Expression Language | Modern composition API |
| Runnable | Base interface for all components | Universal interface |
| RunnableSequence | Chained Runnables | LCEL chain result |
| RunnableParallel | Parallel execution | Performance optimization |
| RunnableLambda | Wrap any function as Runnable | Custom steps |
| invoke/stream/batch | Three execution modes | Sync, streaming, parallel |
| ConversationBufferMemory | Full history in memory | Simple chat |
| ConversationSummaryMemory | Summarized history | Long conversations |
| BaseRetriever | Interface for all retrievers | Swap retrieval backends |
| Document | LangChain doc unit (page_content + metadata) | Core data type |

## 9. Comparison Tables

### LangChain vs LangGraph

| Aspect | LangChain | LangGraph |
|--------|-----------|-----------|
| Paradigm | Linear chain composition | Graph/workflow with state |
| Control flow | Sequential, parallel | Conditional, loops, branching |
| State management | Limited (memory) | First-class (State object) |
| Agents | Basic AgentExecutor | Full stateful agent workflows |
| Debugging | Harder | Easier (explicit state) |
| Use case | Simple RAG chains | Complex multi-step agents |

## 10. Interview Revision

### Senior Questions

**Q1: What is LCEL and why was it introduced?**
- **Answer**: LangChain Expression Language — composing Runnables with `|` operator. Introduced to unify interface (invoke/stream/batch), enable automatic parallelism, and integrate with LangSmith tracing. Old `LLMChain` API was verbose and inconsistent.

**Q2: How do you handle output parser failures in production?**
- **Answer**: Wrap parser in `RetryWithErrorOutputParser`. On failure, send error message back to LLM with format instructions. After N retries, fallback to default. Log failures for prompt iteration.

**Q3: How do you implement memory that doesn't overflow context?**
- **Answer**: `ConversationSummaryMemory` — after N turns, summarize history. Or `ConversationBufferWindowMemory(k=10)` — keep last k turns. Or external memory store (Redis) with semantic retrieval of relevant history.

## 12. One-Page Revision Sheet

### Must Know
- LCEL: `prompt | model | parser` — everything is a Runnable
- invoke (sync), stream (streaming), batch (parallel)
- RecursiveCharacterTextSplitter for chunking
- ConversationBufferMemory vs ConversationSummaryMemory

### Production Nuggets
- Pin LangChain versions — breaks frequently
- Use LangSmith tracing with sampling in production
- Always handle OutputParserException

### Common Traps
- Building complex nested chains — hard to debug
- Forgetting to handle empty retrieval results
- Memory growing unbounded → context overflow

---

# TOPIC 7: RAG Pipeline Fundamentals

## 1. Executive Summary
- RAG = Retrieval-Augmented Generation: retrieve relevant documents, inject into LLM context
- Solves: LLM hallucination, stale knowledge, lack of proprietary data
- Components: ingestion pipeline + retrieval pipeline + generation
- Why it exists: fine-tuning is expensive; RAG is cheaper and supports fresh data
- Production RAG ≠ simple RAG — requires chunking strategy, retrieval quality, context assembly, eval
- RAG is now the default architecture for knowledge-intensive LLM applications
- Main quality levers: chunking, embedding model, retriever, context assembly, prompt

## 2. Mental Model
- **Analogy**: Open-book exam vs closed-book. RAG = open-book. LLM with no RAG = closed-book.
- **Core flow**: "Find relevant pages, show them to the model, ask the question"
- **Key insight**: Retrieval quality determines generation quality. Garbage in (wrong context) → garbage out (hallucinated answer)

```
INGESTION:
Documents → Clean → Chunk → Embed → Index

RETRIEVAL:
Query → Embed → Search Index → Top-K Chunks → Assemble Context

GENERATION:
System Prompt + Context + Query → LLM → Answer + Citations
```

## 3. Core Concepts

| Concept | Definition |
|---------|-----------|
| Ingestion Pipeline | Process of converting raw docs to indexed vectors |
| Retrieval Pipeline | Finding relevant chunks for a query |
| Context Window | LLM's maximum input size — limits how much context we can inject |
| Chunking | Splitting documents into index-able units |
| Chunk Overlap | Repeated content at chunk boundaries to avoid info loss |
| Top-K | Number of chunks to retrieve |
| Context Assembly | How retrieved chunks are formatted for the prompt |
| Faithfulness | Answer only uses provided context (RAGAS metric) |
| Answer Relevancy | Answer actually addresses the question (RAGAS metric) |
| Context Precision | Retrieved context is relevant (RAGAS metric) |
| Context Recall | All needed context was retrieved (RAGAS metric) |
| Grounding | Answer traceable to source documents |
| Citation | Source reference for each answer claim |

## 4. Engineering Deep Dive

### Chunking Strategies

| Strategy | Method | Best For |
|----------|--------|---------|
| Fixed-size | `chunk_size=512, overlap=50` | General purpose |
| Recursive Character | Split on `\n\n`, `\n`, `.`, ` ` | Structured text |
| Semantic | Split on topic changes (NLP) | Dense documents |
| Sentence Window | 1 sentence as unit, ±N context | Precision retrieval |
| Parent-Child | Small child chunks, retrieve parent | Balance precision/context |
| Late Chunking | Embed full doc, then slice embeddings | Preserves full context |

### Parent-Child Retrieval (Advanced)
```python
# Index: small chunks (256 tokens) → point to parent doc ID
# At retrieval: find small chunk (precise), return parent (context)
# Result: precision of small chunks + context of large docs
```

### HyDE (Hypothetical Document Embedding)
```python
# Instead of embedding query directly:
# 1. Ask LLM to generate a hypothetical answer
# 2. Embed that hypothetical answer
# 3. Use that embedding to search (documents look like documents)
```

### Multi-Query Retrieval
```python
# Generate 3-5 variant queries using LLM
# Retrieve for each, deduplicate, union results
# Better recall for complex or ambiguous queries
```

### Context Assembly Best Practices
```
[SYSTEM]: You are a helpful assistant. Answer based ONLY on the provided context.
If the answer is not in the context, say "I don't have information about this."

[CONTEXT]:
Source 1: {chunk_1}
Source 2: {chunk_2}
Source 3: {chunk_3}

[QUESTION]: {user_query}

[ANSWER]:
```

**Citation pattern**: Include source metadata per chunk → LLM can generate citations.

### Reranking Pipeline
```
Initial Retrieval: Top 20 with bi-encoder (fast)
    ↓
Reranker: Cross-encoder scores all 20 (slow but accurate)
    ↓
Return: Top 5 reranked results
```

### Advanced RAG Patterns

| Pattern | Description | Use Case |
|---------|-------------|---------|
| HyDE | Embed hypothetical answer instead of query | Queries that don't look like documents |
| Multi-Query | Generate query variants, union results | Complex queries |
| Step-Back | Rephrase query at higher abstraction level | Specific queries need general context |
| FLARE | Retrieve only when model is uncertain | Dynamic retrieval |
| Corrective RAG | Evaluate retrieved docs, re-retrieve if poor | Quality assurance |
| Self-RAG | Model decides when to retrieve | Adaptive |

## 5. Architecture Perspective

### RAG vs Fine-Tuning vs Prompt-Only

| Aspect | Prompt Only | RAG | Fine-Tuning |
|--------|-------------|-----|-------------|
| Knowledge freshness | Base model (stale) | Real-time | Training time (stale) |
| Hallucination | High | Low (with grounding) | Medium |
| Cost | Low | Medium | High upfront |
| Latency | Low | Medium (+retrieval) | Low |
| Explainability | Low | High (citations) | Low |
| Data requirement | None | Document corpus | Labeled Q&A pairs |

**Best practice**: RAG + Fine-Tuning combined — fine-tune for style, RAG for knowledge.

### Production RAG Architecture
```
[Ingestion Service]
S3 (new file event) → Lambda → Textract → Chunker → Embedder (Bedrock/SageMaker)
    → OpenSearch (write)

[Query Service]
API Gateway → Lambda/ECS
    → Query Expansion (optional: HyDE, multi-query)
    → OpenSearch (hybrid search k-NN + BM25)
    → Reranker (cross-encoder, optional)
    → Context Assembly
    → Bedrock (generation)
    → Response + Citations
```

## 6. Failure Modes & Debugging

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Low faithfulness | Model ignores context | RAGAS faithfulness < 0.7 | Strengthen grounding instructions |
| Missing context | Poor retrieval | Low context recall | Hybrid search, increase top-k |
| Irrelevant context | Bad chunking or embedding | Low context precision | Better chunking, reranking |
| Context overflow | Too many/large chunks | LLM truncation | Reduce chunk size or top-k |
| Hallucination despite RAG | Model blends context with training data | Manual review | "Answer ONLY from context" instruction |
| Stale results | Index not updated | Users report outdated info | Event-driven ingestion on doc update |
| Slow retrieval | Large index, no warm cache | High p99 latency | Pre-warm, index optimization |
| Citation fabrication | LLM generates fake source | Verify citations | Return actual source with chunk |

## 7. End-to-End Flow
```
OFFLINE (Ingestion):
New Document (S3)
    ↓
Text Extraction (Textract)
    ↓
Text Cleaning (normalize, deduplicate)
    ↓
Chunking (RecursiveCharacterTextSplitter, 512 tokens, 50 overlap)
    ↓
Embedding (Bedrock Titan / OpenAI)
    ↓
Index (OpenSearch: knn_vector + metadata)

ONLINE (Query):
User: "What are the Q3 revenue figures?"
    ↓
Query Preprocessing (optional: HyDE, expansion)
    ↓
Hybrid Retrieval (BM25 + k-NN, top-20)
    ↓
Reranking (cross-encoder, top-5)
    ↓
Context Assembly (format chunks + metadata)
    ↓
Prompt Construction (system + context + query)
    ↓
LLM (Bedrock Claude/GPT-4)
    ↓
Output Validation (grounding check)
    ↓
Response + Citations
```

## 8. Terminology Cheat Sheet

| Term | Meaning | Why It Matters |
|------|---------|---------------|
| Naive RAG | Simple: retrieve top-k, prompt | Baseline |
| Advanced RAG | HyDE, multi-query, reranking | Production quality |
| Modular RAG | Components swappable (plug-in architecture) | Extensible design |
| Hallucination | Model invents info not in context | #1 risk |
| Lost in the Middle | LLM ignores middle-of-context chunks | Ordering matters |
| Context Poisoning | Malicious content in retrieved docs | Security risk |
| Grounding | Answer traceable to source | Trustworthiness |
| Top-K | Number of chunks to retrieve (typically 3-20) | Quality vs cost |
| Chunk Overlap | Repeated tokens at chunk boundaries | Boundary information loss prevention |

## 9. Comparison Tables

### RAG Architectures

| Architecture | Complexity | Quality | Use Case |
|-------------|-----------|---------|---------|
| Naive RAG | Low | Baseline | Prototype |
| Hybrid Retrieval | Medium | Good | Most production |
| Reranked RAG | Medium-High | Better | High-quality needs |
| Multi-Query RAG | High | Better | Complex queries |
| Corrective RAG | High | Best | Critical accuracy |
| Agentic RAG | Very High | Best | Multi-hop reasoning |

## 10. Interview Revision

### Top 10 Senior Questions

**Q1: How do you improve RAG recall without increasing false positives?**
- **Answer**: Hybrid search (BM25 + k-NN). Multi-query expansion for complex queries. Larger k in retrieval, then rerank to reduce false positives. Better embedding model. Semantic chunking to keep related info together.

**Q2: Explain "lost in the middle" problem.**
- **Answer**: LLMs are better at using information at the beginning and end of context. Middle content is underutilized. Mitigation: place most relevant chunks first/last. Use reranking. Don't over-retrieve (fewer, more relevant chunks).

**Q3: How do you handle multi-hop questions in RAG?**
- **Answer**: Decompose query into sub-queries. Answer sub-queries iteratively (each answer informs next retrieval). Use Corrective RAG or Agentic RAG. LangGraph is ideal for this workflow.

**Q4: How do you evaluate RAG quality in production without labeled data?**
- **Answer**: RAGAS faithfulness (LLM-as-judge: is answer supported by context?). Answer relevancy (LLM-as-judge: does answer address question?). Track retrieval metrics (hit rate, MRR). User feedback (thumbs up/down). A/B test retrieval strategies.

**Q5: Design a RAG system for a legal document corpus.**
- **Answer**: Hierarchical chunking (clause → section → document). Preserve document structure metadata. Hybrid search. Cross-encoder reranker (legal domain fine-tuned). Faithfulness guardrail. Citation with paragraph reference. Strict "don't hallucinate" system prompt. RAGAS monitoring.

## 11. Senior Engineer Notes

| Junior Focus | Senior Focus |
|-------------|-------------|
| "Does it retrieve correctly?" | "What's the p50/p99 latency? What's the recall@5 on eval set?" |
| Fixed-size chunking | Semantic chunking, parent-child, task-specific strategy |
| Single retriever | Hybrid search + reranking |
| "It works" | RAGAS metrics + regression test on prompt changes |
| Top-K = 5 | Optimal K for cost vs quality, token budget analysis |

## 12. One-Page Revision Sheet

### Must Know
- RAG = retrieve → assemble context → generate
- Chunking is critical: 256-512 tokens, 10-20% overlap
- Hybrid search (BM25 + k-NN) > single method
- Reranking (cross-encoder) improves precision
- RAGAS: faithfulness + answer relevancy + context precision + recall

### Good To Know
- HyDE for queries that don't look like documents
- Multi-query for complex/ambiguous queries
- Parent-child for precision with context

### Expert Knowledge
- Corrective RAG: evaluate retrieved docs, re-retrieve if insufficient
- FLARE: dynamic retrieval based on model uncertainty
- Late chunking: embed full doc first

### Interview Nuggets
- "Lost in the middle" → ordering matters in context assembly
- Always mention RAGAS evaluation when discussing RAG
- Hybrid search + reranking = production standard

### Production Nuggets
- Event-driven ingestion on document update
- Monitor hallucination rate (RAGAS faithfulness)
- Token budget: top-k × chunk_size must fit in context window

### Common Traps
- Not monitoring retrieval quality independently from generation quality
- Over-fetching (large k) and overwhelming context
- Not handling empty retrieval results

---

# TOPIC 8: RAGAS Framework

## 1. Executive Summary
- RAGAS = Retrieval Augmented Generation Assessment
- Automated evaluation framework for RAG pipelines
- Solves: "How do I know my RAG is working well?" — without expensive human annotation
- Provides reference-free metrics using LLM-as-judge
- Key metrics: faithfulness, answer_relevancy, context_precision, context_recall
- Where it fits: CI/CD for RAG — test before deploying
- Why engineers care: RAG quality without RAGAS eval = flying blind
- Industry standard for RAG evaluation

## 2. Mental Model
- **Analogy**: Unit tests for RAG pipelines. Each metric is a test case.
- **LLM-as-judge**: Use a capable LLM (GPT-4) to evaluate outputs at scale — no human labels needed
- **Quality triangle**: Retrieval Quality × Context Relevance × Generation Faithfulness

```
RAG System Output:
  Question (Q) + Context (C) + Answer (A) + Ground Truth (GT, optional)
         ↓
    RAGAS Metrics
         ↓
  faithfulness | answer_relevancy | context_precision | context_recall
```

## 3. Core Concepts

| Metric | What It Measures | Formula Intuition | Requires GT? |
|--------|----------------|------------------|-------------|
| **Faithfulness** | Is the answer supported by the context? | Claims in answer traceable to context | No |
| **Answer Relevancy** | Does the answer address the question? | How well does answer fit question | No |
| **Context Precision** | Are retrieved chunks relevant? | Relevant chunks / total retrieved chunks | Yes |
| **Context Recall** | Did we retrieve all needed info? | Needed info covered by context | Yes |
| **Answer Correctness** | Is the answer factually correct? | Answer vs ground truth | Yes |
| **Context Entity Recall** | Key entities from GT present in context | Entity coverage | Yes |

**Reference-free** (no GT needed): faithfulness, answer_relevancy  
**Reference-based** (GT needed): context_precision, context_recall, answer_correctness

## 4. Engineering Deep Dive

### Using RAGAS
```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset

# Build evaluation dataset
data = {
    "question": ["What is RAG?", "..."],
    "answer": ["RAG is...", "..."],          # LLM's generated answer
    "contexts": [["chunk1", "chunk2"], ...], # Retrieved context
    "ground_truth": ["Expected answer", "..."]  # Optional
}
dataset = Dataset.from_dict(data)

result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm=ChatOpenAI(model="gpt-4o")  # Judge LLM
)
print(result)  # {'faithfulness': 0.85, 'answer_relevancy': 0.92, ...}
```

### Interpreting Metrics

| Metric | Good | Problem Signal |
|--------|------|---------------|
| faithfulness | > 0.85 | Low → model hallucinating beyond context |
| answer_relevancy | > 0.85 | Low → answer off-topic or evasive |
| context_precision | > 0.80 | Low → too much irrelevant context retrieved |
| context_recall | > 0.80 | Low → relevant info not retrieved |

### Diagnostic Logic
```
Low faithfulness + High context_precision → Model ignoring context → Fix: stronger grounding prompt
Low context_recall → Missing relevant docs → Fix: better chunking/embedding, increase k
Low context_precision → Too much noise retrieved → Fix: reranking, tighter filters
Low answer_relevancy → Model dodging question → Fix: more direct instruction
```

### Building Eval Dataset Without GT
```python
# Testset generation with RAGAS
from ragas.testset import TestsetGenerator

generator = TestsetGenerator(llm=generator_llm, embeddings=embedding_model)
testset = generator.generate_with_langchain_docs(
    documents,
    test_size=100,
    distributions={simple: 0.5, reasoning: 0.3, multi_context: 0.2}
)
```

### Integration into CI/CD
```yaml
# GitHub Actions: run RAGAS on PR
- name: RAG Eval
  run: |
    python eval/run_ragas.py \
      --sample-size 50 \
      --min-faithfulness 0.8 \
      --min-context-recall 0.75
  # Fail PR if metrics below threshold
```

## 5. Architecture Perspective

### RAGAS in Production

| Stage | Action |
|-------|--------|
| Dev | Run full RAGAS on eval dataset before merging prompt changes |
| CI/CD | Automated RAGAS gate — block deploy if metrics drop |
| Production | Sample 1-5% of traffic, run async RAGAS, alert on degradation |
| A/B Test | Compare RAGAS scores between retrieval strategies |

### When NOT to Use RAGAS
- Simple factual QA where ground truth is easy to get → use exact match
- Very high cost sensitivity → sample aggressively
- Non-English text → validate judge LLM quality first

## 6. Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| High faithfulness, wrong answer | Model is faithful to wrong context | answer_correctness | Add GT-based metrics |
| RAGAS itself hallucinates | Judge LLM makes errors | Validate on known cases | Use stronger judge (GPT-4), sample-validate |
| Metric gaming | Prompt optimized for metric, not quality | Human spot check | Combine automated + manual eval |
| Eval set distribution mismatch | Eval queries ≠ production queries | Metric looks good, users unhappy | Build eval from real user queries |

## 7. End-to-End Flow
```
RAG System
    ↓ (sample questions)
    ↓ (retrieve + generate)
  Results: {question, answer, contexts, ground_truth}
    ↓
RAGAS evaluate()
    ↓
Metrics per question + aggregate scores
    ↓
Dashboard / CI gate
    ↓
Alert if any metric < threshold
```

## 8. Terminology Cheat Sheet

| Term | Meaning |
|------|---------|
| Faithfulness | Answer supported by retrieved context |
| Answer Relevancy | Answer addresses the question |
| Context Precision | Proportion of retrieved context that's relevant |
| Context Recall | Proportion of needed context that was retrieved |
| LLM-as-judge | Using LLM to evaluate LLM output |
| Reference-free metric | No ground truth required |
| Testset generation | Auto-generating QA pairs from your corpus |
| RAGAS score | Aggregate of all metrics (harmonic mean or weighted) |

## 9. Comparison Tables

### Evaluation Approaches

| Approach | Cost | Scalability | Reliability |
|----------|------|-------------|------------|
| Human eval | High | Low | High |
| RAGAS (LLM-as-judge) | Medium | High | Medium-High |
| Exact match | Low | High | Low (misses paraphrasing) |
| ROUGE/BLEU | Low | High | Low (doesn't capture semantics) |
| Embedding similarity | Low | High | Medium |

## 10. Interview Revision

### Top Questions

**Q1: Explain faithfulness metric in RAGAS.**
- **Answer**: Measures if every claim in the answer is supported by the retrieved context. RAGAS extracts claims from the answer, then for each claim asks the judge LLM: "Is this supported by context?" Faithfulness = supported_claims / total_claims.

**Q2: How do you build a RAGAS eval dataset without ground truth?**
- **Answer**: RAGAS TestsetGenerator — uses LLM to generate diverse questions from your document corpus (simple, reasoning, multi-context). These become your eval set. Reference-free metrics (faithfulness, answer_relevancy) work without GT.

**Q3: How do you use RAGAS in production CI/CD?**
- **Answer**: Maintain eval dataset (100-500 QA pairs). Run RAGAS on every PR that touches retrieval or prompts. Set thresholds (e.g., faithfulness > 0.8). Block merge if metrics drop. Dashboard for trend monitoring.

## 12. One-Page Revision Sheet

### Must Know
- 4 core metrics: faithfulness, answer_relevancy, context_precision, context_recall
- Reference-free: faithfulness + answer_relevancy (no GT needed)
- LLM-as-judge pattern — uses capable LLM to evaluate at scale
- Use in CI/CD as a quality gate

### Interview Nuggets
- Faithfulness = "did model hallucinate beyond context?"
- Context recall = "did retrieval find what was needed?"
- "RAGAS is the pytest of RAG systems"

### Production Nuggets
- Sample 1-5% in production for continuous monitoring
- Build eval set from real user queries, not synthetic only
- Alert on faithfulness drops — early hallucination warning

### Common Traps
- Using RAGAS faithfulness to measure factual accuracy (it doesn't — measures if answer is grounded in context)
- Not validating RAGAS judge LLM accuracy on your domain
- Only running eval at dev time, not in production

---
