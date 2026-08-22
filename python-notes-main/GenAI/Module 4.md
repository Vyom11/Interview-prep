# GenAI Big Picture Map

## The Technology Evolution Chain

```
HUMAN LANGUAGE UNDERSTANDING
         ↓
    NLP Fundamentals
    (tokenization, TF-IDF, n-grams, embeddings)
    Problem solved: How machines process language
         ↓
    Transformer Architecture (2017)
    (attention, positional encoding, BERT/GPT)
    Problem solved: Context-aware language understanding at scale
         ↓
    Large Language Models
    (GPT-3/4, Claude, LLaMA, Mistral)
    Problem solved: Generalist language intelligence via scale
         ↓
    Prompt Engineering
    (zero/few-shot, CoT, ReAct, structured output)
    Problem solved: How to reliably direct LLM behavior
         ↓
    PROBLEM: LLMs hallucinate, have stale knowledge, can't access private data
         ↓
    Sentence Embeddings
    (dense vectors, bi-encoders, sentence-transformers)
    Problem solved: Measuring semantic similarity between texts
         ↓
    Vector Databases
    (FAISS, OpenSearch, Pinecone, Qdrant)
    Problem solved: Storing and retrieving embeddings at scale
         ↓
    RAG Pipelines
    (retrieve → augment → generate)
    Problem solved: Grounded, fresh, private-data-aware LLM responses
         ↓
    PROBLEM: How do I know my RAG is working?
         ↓
    RAGAS Framework
    (faithfulness, context precision/recall, answer relevancy)
    Problem solved: Automated evaluation of RAG quality
         ↓
    PROBLEM: RAG only retrieves, can't take actions
         ↓
    AI Agents + Tool Calling
    (ReAct, function calling, tool use)
    Problem solved: LLMs that can interact with the world
         ↓
    PROBLEM: Complex agents need loops, branches, state — LangChain chains aren't enough
         ↓
    LangGraph
    (stateful graph workflows, human-in-loop, multi-agent)
    Problem solved: Production-grade agent orchestration
         ↓
    CrewAI (parallel path)
    (role-based multi-agent teams)
    Problem solved: Multi-agent collaboration abstraction
         ↓
    PROBLEM: How do I debug, monitor, improve LLM systems?
         ↓
    Observability: LangSmith + LangFuse
    (traces, costs, evals, prompt management)
    Problem solved: Full visibility into LLM application behavior
         ↓
    PROBLEM: How do I deploy and scale all of this reliably?
         ↓
    AWS Services (Bedrock, OpenSearch, SageMaker)
    (managed GenAI infrastructure)
    Problem solved: Production-grade, compliant, scalable GenAI infra
         ↓
    Docker + Container Orchestration
    (ECR, ECS, EKS)
    Problem solved: Consistent, portable, scalable deployment
         ↓
    Multi-Agent Systems at Scale
    (supervisor patterns, parallel agents, human-in-loop)
    Problem solved: Complex knowledge work automation
```

## How Each Topic Connects to the Next

| From | To | Connection |
|------|-----|-----------|
| NLP → Transformers | Understanding what tokens are, why context matters | Pre-training data is tokenized text |
| Transformers → LLMs | Scale transformers + RLHF alignment | Same architecture, vastly more parameters |
| LLMs → Prompt Engineering | Need to reliably extract behavior | Input controls output |
| LLMs → Embeddings | Repurpose encoder for semantic vectors | Embeddings = encoder output |
| Embeddings → Vector DBs | Need to store and search millions of vectors | Embeddings need ANN indexing |
| Vector DBs → RAG | Retrieval is the R in RAG | Vector search enables semantic retrieval |
| RAG → RAGAS | Need to measure RAG quality | Systematic evaluation framework |
| RAG → Agents | RAG can only retrieve; need to act | Agents extend RAG with tool use |
| Agents → LangGraph | Simple agents need state + control flow | Graph model enables complex workflows |
| Agents → CrewAI | Single agent has limits; teams are better | Role-based multi-agent abstraction |
| Everything → Observability | Production systems need monitoring | Tracing + evals across the entire stack |
| Everything → AWS | Need managed, scalable, compliant infra | AWS provides the substrate |
| AWS → Docker | Apps packaged for deployment | Containers run in ECS/EKS |

---

# ULTIMATE 30-MINUTE REVISION SHEET

> Read this section immediately before your interview. It covers everything essential.

---

## Most Important Concepts

### NLP & Tokenization
- Token ≠ word. ~1.3 tokens/word for English. Priced per token in all LLM APIs.
- BPE (GPT) vs WordPiece (BERT) — both subword; BPE merges by frequency
- Attention: Q (query), K (key), V (value). Scores = softmax(QK^T/√d_k) × V
- Context window = hard limit. Beyond it = truncation/loss.
- Cosine similarity over Euclidean for high-dim vectors

### LLMs & Prompting
- Temperature=0 → deterministic; 0.7 → balanced; 1+ → creative
- CoT: "Think step by step" → dramatically improves reasoning
- Hallucination: model invents plausible-sounding false info → mitigate with RAG
- Function calling: structured JSON tool invocation. finish_reason = "tool_calls"
- KV Cache: stores previous token computations → prefix caching for cost reduction

### Embeddings
- Bi-encoder (fast, pre-compute docs) vs Cross-encoder (accurate, query+doc together)
- Same embedding model for query and document — ALWAYS
- HNSW: graph ANN; ef_search controls recall vs latency
- Recall@k is the primary retrieval metric
- OpenAI 3-small: 1536-dim. BGE-large: 1024-dim. MiniLM: 384-dim

### Vector Databases
- HNSW lives in JVM heap → primary OpenSearch scaling concern
- Hybrid search: BM25 + k-NN + RRF score fusion → production standard
- Metadata filtering: pre-filter vs post-filter tradeoff
- Model change → full re-index required

### RAG Pipeline
- Chunking: 256-512 tokens, 10-20% overlap
- Top-K typical: 5-20 chunks
- Retrieval → Reranking (cross-encoder) → Context Assembly → Generation
- "Lost in the middle": LLMs use beginning/end better → order context carefully
- HyDE: generate hypothetical answer, embed it, search with that embedding

### RAGAS
- Faithfulness: answer grounded in context? (no GT needed)
- Answer Relevancy: answer addresses question? (no GT needed)
- Context Precision: retrieved chunks relevant? (needs GT)
- Context Recall: all needed info retrieved? (needs GT)
- Use in CI/CD as quality gate; sample 1-5% in production

### Agents
- ReAct: Reason → Act → Observe → loop
- max_iterations: always set to prevent infinite loops
- Tool description quality = tool selection quality
- Cost per agent run: 10-50× simple LLM call
- Parallel tool calling: multiple tools in one step (GPT-4o, Claude 3.5 support)

### LangGraph
- StateGraph: nodes + conditional edges + shared TypedDict state
- State reducers: `Annotated[list, operator.add]` for append mode
- Checkpointer: persist state (SQLite dev, Postgres prod), thread_id = session
- Interrupt: pause for human review before/after any node
- Supervisor pattern = standard multi-agent architecture

### AWS
- Bedrock: managed multi-model LLM API. Provisioned Throughput for prod SLAs.
- OpenSearch: HNSW (nmslib) in JVM heap. Faiss for large offline indices.
- Textract: async for > 5 pages. FeatureTypes: TABLES, FORMS.
- S3 Events → Lambda → ingestion pipeline standard pattern
- VPC Endpoints: Bedrock, S3, OpenSearch → data stays in your VPC

### Docker
- Dockerfile → Image → Container
- Multi-stage build: smaller, more secure
- Layer cache: copy requirements before application code
- `--platform linux/amd64` for M1 Mac building for AWS
- Non-root user in production always

---

## Most Important Architectures

### Production RAG Architecture
```
[Ingestion]                           [Query]
S3 (upload)                           User Query
  ↓ Event                               ↓
Lambda                               API Gateway → Lambda/ECS
  ↓                                      ↓
Textract (OCR)                       Embed Query (Bedrock Titan)
  ↓                                      ↓
Chunker (512t, 50 overlap)           OpenSearch Hybrid (BM25 + k-NN)
  ↓                                      ↓
Bedrock Embed (Titan)                Cross-encoder Reranker (Top-5)
  ↓                                      ↓
OpenSearch Index (knn_vector)        Context Assembly (+ metadata)
                                         ↓
                                     Bedrock Claude (generation)
                                         ↓
                                     Output Validation
                                         ↓
                                     Response + Citations
```

### Multi-Agent Architecture (LangGraph Supervisor)
```
User Request
    ↓
Supervisor Agent (GPT-4o, temperature=0)
"Next worker? researcher|analyst|writer|FINISH"
    ↓ (conditional edge)
┌───────────────────────────────────────┐
│ Researcher  │  Analyst  │  Writer     │
│ (web search │ (data     │ (no tools)  │
│  tools)     │  tools)   │             │
└───────────────────────────────────────┘
    ↓ (all report back to supervisor)
Supervisor decides next → ... → FINISH
    ↓
Final Answer
```

### Corrective RAG (CRAG) with LangGraph
```
Query → Retrieve → Grade Docs
                       ↓
            (if score < threshold)
                       ↓
             Re-retrieve with refined query
                       ↓
            (if score ≥ threshold)  
                       ↓
              Generate → Validate → END
```

### Observability Stack
```
Every Request → LangSmith/LangFuse Trace
                    ├── Retrieval Span (latency, num_docs, query)
                    ├── LLM Span (prompt, output, tokens, cost, latency)
                    └── Score (faithfulness, user_feedback)
                         ↓
                    Dashboard + Alerts
                         ↓
                 Low faithfulness → alert → investigate → fix
```

---

## Most Important Trade-offs

| Decision | Option A | Option B | Guidance |
|----------|----------|----------|---------|
| Retrieval | BM25 (keyword) | Dense (semantic) | Use hybrid; don't pick one |
| Retrieval quality | Higher k | Reranker | Reranker better than just k++ |
| Embedding model | Proprietary (OpenAI) | Open-source (BGE) | OSS if budget/latency sensitive |
| Embedding dim | High (3072) | Low (384) | High quality vs speed; Matryoshka for flexibility |
| Agent vs Workflow | Agent (flexible) | LangGraph workflow | Workflow if deterministic; Agent if not |
| CrewAI vs LangGraph | CrewAI (easy) | LangGraph (control) | Prototype CrewAI → productionize LangGraph |
| RAG vs Fine-tune | RAG (fresh data) | Fine-tune (style) | Combine both |
| Self-host vs Managed | Self-host (control) | Managed (AWS) | Managed unless compliance forces self-host |
| LangSmith vs LangFuse | LangSmith (easy) | LangFuse (data sovereignty) | LangFuse for compliance |
| Chunking | Fixed-size (simple) | Semantic (quality) | Semantic for production |
| HNSW vs IVF | HNSW (quality) | IVF (scale) | HNSW < 10M docs; IVF for 100M+ |

---

## Most Common Failure Modes

| Failure | System | Root Cause | Fix |
|---------|--------|-----------|-----|
| Hallucination | LLM/RAG | No grounding / weak retrieval | RAG + "ONLY from context" instruction |
| Low faithfulness | RAG | Retrieved wrong context | Hybrid search + reranking |
| Context overflow | RAG | Too many/large chunks | Reduce k or chunk_size |
| Agent infinite loop | Agents | No termination condition | max_iterations, explicit DONE signal |
| JVM OOM | OpenSearch | HNSW index too large | Scale cluster, use Faiss engine |
| Prompt injection | LLM | User input overrides system prompt | Input sanitization, output filtering |
| Stale embeddings | Vector DB | Doc updated, embedding not | Event-driven re-embedding on update |
| Token cost explosion | LLM | No max_tokens + no caching | Set max_tokens, implement caching |
| Chunking boundary loss | RAG | Chunk splits mid-sentence | Add 10-20% overlap, use recursive splitter |
| Bedrock throttling | AWS | On-demand rate limits | Provisioned Throughput + backoff |
| Output parser failure | LangChain | LLM doesn't follow format | Retry with error, use JSON mode |
| Platform mismatch | Docker | M1 Mac built for ARM | `--platform linux/amd64` |

---

## Most Important Metrics

| Metric | What It Measures | Good Value | Tool |
|--------|----------------|-----------|------|
| **Recall@k** | Top-k retrieval coverage | > 0.8 | Custom eval |
| **Faithfulness** | Answer grounded in context | > 0.85 | RAGAS |
| **Answer Relevancy** | Answer addresses question | > 0.85 | RAGAS |
| **Context Precision** | Retrieved chunks relevant | > 0.80 | RAGAS |
| **Context Recall** | All needed context retrieved | > 0.80 | RAGAS |
| **p50/p99 latency** | Response time | p99 < 3s typical | CloudWatch |
| **Token cost per request** | Spend per query | Budget-dependent | LangSmith/LangFuse |
| **RAGAS score** | Aggregate RAG quality | > 0.80 | RAGAS |
| **Error rate** | % failed requests | < 1% | CloudWatch |
| **Hallucination rate** | % answers not grounded | < 5% | RAGAS + manual |
| **MRR** | Mean Reciprocal Rank | > 0.8 | Custom eval |
| **Agent success rate** | % agent tasks completed | > 90% | Custom |

---

## Most Important Interview Topics

### Must-Answer Topics (High Frequency)
1. **"Design a RAG system"** → Ingestion pipeline + hybrid retrieval + reranking + RAGAS evaluation
2. **"How do you prevent hallucination?"** → RAG + grounding prompt + faithfulness monitoring
3. **"Explain chunking strategy"** → Size/overlap, recursive vs semantic, impact on retrieval
4. **"When would you use agents vs workflows?"** → Non-deterministic decisions → agents; known steps → workflow
5. **"How do you evaluate LLM apps?"** → RAGAS + LangSmith/LangFuse + user feedback
6. **"Explain hybrid search"** → BM25 + k-NN + RRF fusion in OpenSearch
7. **"How do you scale a RAG system?"** → OpenSearch cluster, async ingestion, caching, batching
8. **"RAG vs Fine-tuning?"** → RAG = fresh data + explainable; Fine-tune = style/behavior + lower latency

### System Design Anchors
- Always start with: ingestion, retrieval, generation, evaluation
- Always mention: latency SLA, cost budget, monitoring
- Always include: failure modes, retry logic, graceful degradation
- Differentiate yourself: mention RAGAS, hybrid search, reranking, LangGraph for complex flows

### Common Candidate Mistakes
- Saying "just use RAG" without explaining chunking, hybrid search, evaluation
- Not mentioning hallucination mitigation
- Describing agents without max_iterations, cost controls
- Forgetting observability (LangSmith/LangFuse)
- Treating embedding model choice as an afterthought

---

## Most Important Production Lessons

### The 10 Laws of Production GenAI

1. **Evaluate before you deploy**: RAGAS on every prompt change — no exceptions
2. **Hybrid search always beats single method**: BM25 + k-NN + reranker = production standard
3. **Token budgets are financial controls**: Set max_tokens, monitor cost per request
4. **Agents need guardrails**: max_iterations + cost_limit + tool validation = mandatory
5. **Observability is not optional**: Every LLM call must be traced (LangSmith/LangFuse)
6. **Chunking strategy matters more than embedding model**: Test empirically with RAGAS
7. **Event-driven ingestion**: Documents update → pipeline must re-embed
8. **Version everything**: Prompts, embeddings, indices — treat like code
9. **Cache aggressively**: LLM responses for deterministic inputs, embedding vectors
10. **Degrade gracefully**: If retrieval fails → say "I don't have info"; never hallucinate

### Operational Runbook

```
Retrieval quality degrades:
  1. Check embedding model (version change?)
  2. Check index health (OpenSearch cluster status)
  3. Check RAGAS context_recall / context_precision
  4. Check if new documents were added (distribution shift)
  5. A/B test chunking strategy changes

Hallucination increase:
  1. Check RAGAS faithfulness metric
  2. Check if system prompt was changed
  3. Inspect failing traces in LangSmith
  4. Verify retrieval is returning relevant context
  5. Strengthen "ONLY from context" instruction

Cost spike:
  1. Check max_tokens settings
  2. Check for agent loops (high iteration counts)
  3. Check prompt caching hit rate
  4. Review model routing (are simple queries hitting expensive model?)
  5. Check batch vs real-time processing split

Latency spike:
  1. Check p99 per stage (retrieval vs generation vs reranking)
  2. Check OpenSearch JVM heap
  3. Check LLM API status
  4. Check if new large documents breaking chunking
  5. Review cache hit rate
```

---

## Most Important Senior Engineer Insights

### The Three Shifts from Junior to Senior

**1. From "Does it work?" → "How do I know it works?"**
- Junior: tests manually, says "looks good"
- Senior: RAGAS eval dataset, regression tests on every change, production sampling

**2. From "Features" → "Operational Excellence"**
- Junior: builds the happy path
- Senior: designs for failure modes, retry logic, cost controls, rollback capability

**3. From "This approach" → "This approach with these tradeoffs"**
- Junior: "Let's use agents"
- Senior: "Agents give flexibility but add 10-50× cost and non-determinism. For this use case, a LangGraph workflow with one tool-calling step gives 80% of the benefit with 1/5 the cost and latency."

### Senior-Level Architecture Principles

| Principle | Application |
|-----------|-------------|
| **Separation of concerns** | Ingestion service ≠ query service ≠ evaluation service |
| **Fail fast, degrade gracefully** | Retrieval fails → fallback to direct answer, log alert |
| **Measure everything** | If you can't measure it, you can't improve it |
| **Immutable artifacts** | Container images, embedding model versions are immutable |
| **Event-driven over polling** | S3 events trigger ingestion; don't poll for new docs |
| **Cost visibility per request** | Track token spend at query level, not just aggregate |
| **Blue/green for ML changes** | New embedding model = new index, validate, then swap |

### Questions that Signal Seniority
- "What's our p99 latency budget and how does that constrain chunk count?"
- "How do we version the embedding index when we upgrade the embedding model?"
- "What's our RAGAS baseline before we make this change?"
- "If retrieval returns nothing, what does the user experience?"
- "How do we validate that the new chunking strategy improves real-user queries, not just the synthetic eval set?"
- "What's the cost per query breakdown: retrieval vs embedding vs generation vs reranking?"

---

## Quick Reference Card

### GenAI Stack Layers

| Layer | Technology | Key Decision |
|-------|-----------|-------------|
| Infrastructure | AWS (EC2, ECS, ECR, S3) | Managed vs self-host |
| Container | Docker, ECS/EKS | Image optimization |
| LLM | Bedrock, OpenAI, Anthropic | Model routing strategy |
| Embedding | Bedrock Titan, OpenAI, BGE | Quality vs cost |
| Vector DB | OpenSearch, Pinecone | Hybrid search |
| Retrieval | k-NN + BM25 + reranker | Precision vs recall |
| Orchestration | LangGraph, LangChain | Complexity of workflow |
| Multi-agent | CrewAI, LangGraph Supervisor | Collaboration needs |
| Evaluation | RAGAS, LangSmith | Continuous quality |
| Observability | LangSmith / LangFuse | Tracing + costs |

### Critical Numbers to Know

| Parameter | Typical Value | Why |
|-----------|---------------|-----|
| Chunk size | 256-512 tokens | Context quality vs cost |
| Chunk overlap | 10-20% | Boundary loss prevention |
| Top-K retrieval | 5-20 | Context budget |
| Temperature (production) | 0 (structured) / 0.7 (chat) | Determinism |
| Max iterations (agent) | 10-15 | Loop prevention |
| HNSW ef_search | 256-512 | Recall vs latency |
| HNSW m | 16-32 | Memory vs recall |
| Reranking candidate set | 20-100 → return 5 | Quality vs latency |
| LangFuse sampling | 5-10% in production | Cost vs observability |
| RAGAS faithfulness threshold | 0.8 | Quality gate |

### The GenAI Interview Framework

For any system design question, answer across these 5 dimensions:

```
1. DATA: How is data ingested, processed, stored, updated?
   → S3 → Textract → Chunk → Embed → OpenSearch

2. RETRIEVAL: How is relevant context found?
   → Hybrid (BM25 + k-NN) → Reranking

3. GENERATION: How is the final output produced?
   → Context assembly → Bedrock LLM → Output validation

4. EVALUATION: How do you know it's working?
   → RAGAS (faithfulness, context recall) → LangSmith traces

5. OPERATIONS: How do you run it at scale?
   → Docker → ECS → CloudWatch → Alerts → Incident runbook
```

---

*End of Revision Handbook. You are ready.*
