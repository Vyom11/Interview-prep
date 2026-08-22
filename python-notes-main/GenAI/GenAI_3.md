# PART 3: RAG, AGENTS, OBSERVABILITY & DEPLOYMENT

---

# Topic 11: RAG Pipeline — Retrieval → Augment → Generate

## 1. Executive Summary
- RAG = Retrieval-Augmented Generation: retrieve relevant context → inject into LLM prompt
- **Problem solved:** LLMs have stale knowledge, hallucinate, can't access private data
- Three phases: Index (offline), Retrieve (query time), Generate (LLM with context)
- Retrieval quality is the #1 determinant of RAG quality
- Chunking strategy profoundly impacts retrieval
- Naive RAG → Advanced RAG → Modular RAG (evolution)
- Advanced techniques: HyDE, multi-query, parent-child chunking, re-ranking
- RAG vs Fine-tuning: RAG for knowledge; fine-tuning for style/behavior
- Evaluation: faithfulness, relevance, answer quality (RAGAS framework)
- Production RAG is 80% engineering, 20% LLM

## 2. Mental Model
> "RAG is like an open-book exam. Without RAG, the LLM relies on memorized facts (closed-book, may hallucinate). With RAG, you hand the LLM the relevant textbook pages (retrieved context) before answering — answers are grounded in facts."

```
OFFLINE (Index Time):
Documents → Chunk → Embed → Store in Vector DB

ONLINE (Query Time):
User Query → Embed → Retrieve → Augment Prompt → LLM → Answer
```

## 3. Beginner Level

### Basic RAG Implementation
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Assumes vectorstore and retriever already created (see Topic 10)

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Answer using ONLY the provided context. 
If the answer isn't in the context, say "I don't know."
Context: {context}"""),
    ("user", "{question}")
])

llm = ChatAnthropic(model="claude-sonnet-4-5")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | RAG_PROMPT
    | llm
    | StrOutputParser()
)

response = rag_chain.invoke("What is the return policy?")
```

### Chunking Strategies
| Strategy | Chunk Size | Overlap | Best For |
|----------|-----------|---------|---------|
| Fixed-size | 500-1000 chars | 100-200 | General use |
| Recursive character | 1000 chars | 200 | Most documents |
| Sentence | 1-3 sentences | 0-1 | Q&A, facts |
| Semantic | Variable | Minimal | Long-form documents |
| Parent-child | Large/small | 0 | Rich context + precise retrieval |

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""],  # Try from most semantic to least
    length_function=len
)
```

## 4. Practitioner Level

### Advanced RAG Techniques

**HyDE (Hypothetical Document Embedding):**
```python
# Problem: Query "What causes inflation?" ↔ Document "Monetary policy drives price increases"
# They're semantically similar but phrased differently
# Solution: Generate a hypothetical answer first, then retrieve using that

hyde_prompt = "Write a brief passage that would answer: {question}"
hypothetical_doc = llm.invoke(hyde_prompt.format(question=user_question))
# Now retrieve using the hypothetical document (better semantic match)
docs = retriever.invoke(hypothetical_doc)
```

**Multi-Query Retrieval:**
```python
# One query may not capture all angles
# Generate 3-5 variations → retrieve for each → deduplicate

from langchain.retrievers.multi_query import MultiQueryRetriever

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm  # LLM generates query variations
)
# Query: "Python performance tips"
# Generated variations:
# - "How to optimize Python code speed"
# - "Python profiling and bottleneck identification"
# - "Best practices for fast Python applications"
```

**Parent-Child Chunking:**
```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

# Small chunks for precise retrieval, parent chunks for rich context
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

store = InMemoryStore()  # Stores parent docs
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)
# Retrieves small chunk (precise match) → returns parent (rich context)
```

### RAG Quality Optimization
```python
# STEP 1: Improve retrieval (most impactful)
# - Better embedding model (BGE > MiniLM)
# - Hybrid search (vector + BM25)
# - Re-ranking (cross-encoder)
# - Better chunking strategy

# STEP 2: Improve context (second most impactful)
# - Parent-child chunks
# - Contextual compression (LLM extracts relevant part)
# - Metadata filtering

# STEP 3: Improve generation (least impactful if retrieval is good)
# - Better prompting
# - Citation enforcement
# - Answer format specification
```

## 5. Advanced GenAI Engineering

### Agentic RAG with LangGraph
```python
# Corrective RAG: Grade retrieved docs, rewrite if poor quality
# Self-RAG: Generate with citations, check if citations support answer
# Adaptive RAG: Route to web search if knowledge base insufficient

class CorrectiveRAGState(TypedDict):
    question: str
    documents: list
    filtered_docs: list
    generation: str
    web_search_needed: bool

def grade_documents(state):
    graded = []
    web_needed = False
    for doc in state["documents"]:
        score = grader.invoke({"doc": doc, "question": state["question"]})
        if score.binary_score == "yes":
            graded.append(doc)
        else:
            web_needed = True
    return {"filtered_docs": graded, "web_search_needed": web_needed}
```

### Context Window Management
```python
# Never exceed context window — LLMs degrade with too much context
# "Lost in the middle" problem: LLMs focus on beginning and end

MAX_CONTEXT_TOKENS = 8000
MAX_DOCS = 5

def build_context(docs: list, max_tokens: int = MAX_CONTEXT_TOKENS) -> str:
    context_parts = []
    total_tokens = 0
    
    for doc in docs[:MAX_DOCS]:
        doc_tokens = count_tokens(doc.page_content)
        if total_tokens + doc_tokens > max_tokens:
            break
        context_parts.append(doc.page_content)
        total_tokens += doc_tokens
    
    return "\n\n---\n\n".join(context_parts)
```

## 6. Senior Engineer Perspective

### RAG vs Fine-tuning Decision

| Scenario | RAG | Fine-tuning |
|---------|-----|------------|
| Private/proprietary knowledge | ✅ | ⚠️ (leaks in weights) |
| Frequently updated knowledge | ✅ | ❌ (requires retraining) |
| Specialized style/format | ❌ | ✅ |
| Low-latency requirement | ⚠️ (adds latency) | ✅ |
| Limited labeled data | ✅ | ❌ |
| Regulatory audit trail | ✅ (citations) | ❌ |
| Cost-sensitive | ✅ (no training cost) | ⚠️ |

**In practice: RAG + Fine-tuning is often best for enterprise.**

### Production RAG Architecture
```
┌─────────────────────────────────────────────────┐
│  INDEXING PIPELINE (Offline)                     │
│  S3/DB → Loader → Splitter → Embedder → VectorDB│
│  + Metadata extraction + Document versioning     │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│  QUERY PIPELINE (Online, <500ms)                 │
│  Query → [Query Transform] → Embed               │
│       → [Hybrid Retrieve] → [Re-rank]            │
│       → [Context Build] → [LLM] → [Validate]    │
│       → Response + Citations                     │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│  EVALUATION (Continuous)                         │
│  RAGAS: Faithfulness, Relevancy, Recall          │
│  LangSmith traces, User feedback                 │
└─────────────────────────────────────────────────┘
```

## 7. Production Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|-----------|
| Hallucination | Irrelevant docs retrieved | Faithfulness score | Better retrieval, faithfulness guard |
| Irrelevant retrieval | Poor embeddings or chunking | Retrieval recall metrics | Better embedding model, tuning |
| Stale knowledge | Documents not re-indexed | Freshness checks | Incremental indexing pipeline |
| Context overflow | Too many/large chunks | Token count monitoring | Contextual compression, limits |
| Slow latency | Synchronous retrieval + generation | P95 latency | Async, caching, pre-fetching |
| Missing citations | No citation enforcement | Output monitoring | Citation-enforced prompts |
| Chunk boundary issues | Splits mid-sentence/concept | Human evaluation | Semantic chunking, larger overlap |

## 8. Interview Preparation

**Beginner:**
1. What is RAG? → Retrieve relevant docs → augment LLM prompt → generate grounded answer
2. Why RAG over just LLM? → Private data, current knowledge, reduces hallucination, citations
3. What is chunking? → Splitting documents into retrieval-sized pieces
4. What is a retriever? → Component that fetches relevant chunks from vector store
5. Naive vs Advanced RAG? → Naive: basic vector search; Advanced: reranking, query rewriting, etc.

**Senior:**
1. Design a RAG system for a 10M document legal knowledge base with <500ms SLA
2. How do you debug "the LLM ignores retrieved context" in production?
3. RAG vs fine-tuning for a customer support bot with weekly product updates
4. How do you handle multi-hop questions in RAG (answer requires 2+ documents)?

## 9. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | Index/retrieve/generate phases, chunking strategies, hybrid search, context injection |
| **Good To Know** | HyDE, multi-query, parent-child chunks, contextual compression |
| **Expert Knowledge** | Corrective RAG, Self-RAG, Adaptive RAG, RAGAS evaluation |
| **Architecture Nuggets** | Retrieval quality > generation quality; hybrid search always; re-rank top-k |
| **Interview Nuggets** | "RAG = open-book exam" — "Chunk boundaries break semantic units" |
| **Red Flags** | No re-ranking; ignoring chunk overlap; LLM answer without citation validation |
| **Production Lessons** | Monitor retrieval recall weekly; incremental indexing; 80% of RAG bugs are retrieval bugs |

---

# Topic 12: RAG Evaluation, Failure Modes & Debugging

## 1. Executive Summary
- RAG systems are complex; without evaluation you're flying blind
- **RAGAS**: Standard RAG evaluation framework (faithfulness, answer relevancy, context recall, precision)
- **Problem solved:** Quantify RAG quality, catch regressions, debug failures
- Three levels: retrieval quality, augmentation quality, generation quality
- Faithfulness = did the LLM answer only use provided context? (hallucination detection)
- Answer Relevancy = is the answer relevant to the question?
- Context Recall = did retrieval fetch all necessary context?
- Context Precision = were retrieved docs actually relevant (not noise)?
- LLM-as-judge: use LLM to evaluate other LLM outputs at scale
- Always maintain a golden test set; evaluate before deploying changes

## 2. Mental Model
> "RAG evaluation is like quality control in a factory. Each station (retrieve, augment, generate) can introduce defects. Measure each station independently, then measure the end-to-end output."

```
Input Question
      ↓
[Retrieval] → Measure: Recall@K, Precision@K, NDCG
      ↓
[Context Window] → Measure: Context Relevance, Context Precision
      ↓
[LLM Generation] → Measure: Faithfulness, Answer Relevancy, Accuracy
      ↓
Output Answer → Measure: End-to-end correctness, User satisfaction
```

## 3. RAGAS Framework

### Core Metrics
```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision
)
from datasets import Dataset

# Prepare evaluation dataset
data = {
    "question": ["What is RAG?", "How does HNSW work?"],
    "answer": ["RAG is retrieval augmented generation...", "HNSW is a graph..."],
    "contexts": [["doc1 content", "doc2 content"], ["doc3 content"]],
    "ground_truth": ["RAG combines retrieval with generation", "HNSW uses hierarchical graphs"]
}
dataset = Dataset.from_dict(data)

results = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_recall, context_precision]
)
print(results)
# {'faithfulness': 0.87, 'answer_relevancy': 0.91, 'context_recall': 0.78, 'context_precision': 0.83}
```

### Metrics Explained
| Metric | Measures | Score Interpretation |
|--------|---------|---------------------|
| **Faithfulness** | % of answer claims supported by context | Low → hallucination |
| **Answer Relevancy** | How relevant is answer to question | Low → off-topic answer |
| **Context Recall** | Was necessary context retrieved | Low → retrieval misses |
| **Context Precision** | Were retrieved docs actually useful | Low → noisy retrieval |

## 4. Debugging RAG Failures

### Failure Taxonomy
```
FAILURE TYPE 1: Retrieval Failure
Symptom: Context doesn't contain answer
Debug:   - Check if answer is in index at all
         - Evaluate embedding similarity scores
         - Try HyDE or multi-query
         - Check chunk boundaries (split mid-concept)

FAILURE TYPE 2: Context Injection Failure
Symptom: Context contains answer but LLM ignores it
Debug:   - Check context position in prompt (avoid "lost in the middle")
         - Reduce context (too much context = diluted signal)
         - Increase context relevance (re-ranking)
         - Check if context is properly formatted

FAILURE TYPE 3: Generation Failure
Symptom: Context has answer, LLM produces wrong answer
Debug:   - Check for confusing/contradictory context
         - Temperature too high (add randomness)
         - Prompt is ambiguous
         - Model capability issue
```

### LangSmith Debugging Workflow
```python
from langsmith import Client

# View traces for failed queries
client = Client()
runs = client.list_runs(
    project_name="rag-production",
    filter="and(has('error'), gte(start_time, '2024-01-01'))"
)

# Analyze which step failed
for run in runs:
    print(f"Step: {run.name}")
    print(f"Inputs: {run.inputs}")
    print(f"Outputs: {run.outputs}")
    print(f"Error: {run.error}")
```

## 5. Production Evaluation System

```python
# Golden test set evaluation (run before every deployment)
class RAGEvaluator:
    def __init__(self, golden_dataset_path: str):
        self.golden = load_golden_dataset(golden_dataset_path)
    
    def evaluate_deployment(self, rag_pipeline) -> dict:
        results = []
        for item in self.golden:
            answer, docs = rag_pipeline.invoke(item["question"])
            results.append({
                "question": item["question"],
                "answer": answer,
                "expected": item["expected_answer"],
                "retrieved_docs": docs,
                "contexts": [d.page_content for d in docs]
            })
        
        # RAGAS evaluation
        scores = evaluate(Dataset.from_list(results))
        
        # Regression check
        if scores["faithfulness"] < self.thresholds["faithfulness"]:
            raise EvaluationError(f"Faithfulness below threshold: {scores['faithfulness']}")
        
        return scores
```

## 6. Interview Preparation

**Beginner:**
1. What is faithfulness in RAG? → Are all answer claims supported by retrieved context?
2. What is RAGAS? → Framework for evaluating RAG systems across multiple metrics
3. What does context recall measure? → Was necessary context actually retrieved?
4. How do you detect retrieval failures? → Low context recall score; answer not in context

**Senior:**
1. Build a continuous evaluation pipeline for production RAG
2. How do you handle contradictory information in retrieved documents?
3. Design an evaluation strategy for a multilingual RAG system

## 7. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | RAGAS metrics (faithfulness, relevancy, recall, precision), golden test set |
| **Good To Know** | LLM-as-judge, DeepEval, continuous evaluation pipeline |
| **Expert Knowledge** | Custom eval metrics, human preference learning, A/B testing RAG changes |
| **Architecture Nuggets** | Evaluate each component independently; regression gate before deployment |
| **Interview Nuggets** | "Faithfulness = no hallucination" — "Context recall = retrieval completeness" |
| **Red Flags** | No evaluation before deployment; no golden test set; ignoring faithfulness |
| **Production Lessons** | Run RAGAS after every embedding model or chunking strategy change |

---

# Topic 13: AWS S3, Textract & SageMaker

## 1. Executive Summary
- **S3**: Object storage — foundation of data lake; stores documents for RAG indexing
- **Textract**: AWS managed OCR — extracts text, tables, forms from PDFs/images
- **SageMaker**: Managed ML platform — training, fine-tuning, model hosting, inference
- **Problem solved:** Document ingestion pipeline, model training at scale, custom model hosting
- S3 + Textract + Lambda = serverless document processing pipeline
- SageMaker Endpoints: custom model serving with auto-scaling
- SageMaker Jumpstart: deploy pre-trained models (LLaMA, Falcon) in one click
- For GenAI: S3=data lake; Textract=doc ingestion; SageMaker=custom model hosting
- Alternative to Bedrock when you need full model control or open-source models
- Key cost consideration: SageMaker instances are hourly; Bedrock is per-token

## 2. Practitioner Level

### S3 + Textract Document Pipeline
```python
import boto3
import json

def process_document_pipeline(s3_bucket: str, s3_key: str) -> str:
    """Extract text from S3 document using Textract."""
    textract = boto3.client('textract', region_name='us-east-1')
    
    # For async (large docs > 5MB)
    response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}
        },
        NotificationChannel={
            'SNSTopicArn': 'arn:aws:sns:us-east-1:123:textract-done',
            'RoleArn': 'arn:aws:iam::123:role/TextractRole'
        }
    )
    job_id = response['JobId']
    return job_id

def get_textract_results(job_id: str) -> str:
    textract = boto3.client('textract')
    pages = []
    
    response = textract.get_document_text_detection(JobId=job_id)
    while True:
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                pages.append(block['Text'])
        
        if 'NextToken' not in response:
            break
        response = textract.get_document_text_detection(
            JobId=job_id, NextToken=response['NextToken']
        )
    
    return '\n'.join(pages)

# Advanced: Extract tables
def extract_tables(job_id: str) -> list[dict]:
    """Extract structured tables from Textract results."""
    textract = boto3.client('textract')
    response = textract.get_document_analysis(JobId=job_id)
    # Parse TABLE and CELL blocks...
```

### SageMaker: Deploy Custom Embedding Model
```python
import sagemaker
from sagemaker.huggingface import HuggingFaceModel

# Deploy HuggingFace model to SageMaker endpoint
huggingface_model = HuggingFaceModel(
    model_data="s3://my-bucket/model.tar.gz",  # Model artifacts
    role="arn:aws:iam::123:role/SageMakerRole",
    transformers_version="4.37",
    pytorch_version="2.1",
    py_version="py310",
    env={
        "HF_MODEL_ID": "BAAI/bge-large-en-v1.5",
        "HF_TASK": "feature-extraction"
    }
)

predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type="ml.g4dn.xlarge",  # GPU instance
    endpoint_name="bge-embedding-endpoint"
)

# Invoke embedding endpoint
result = predictor.predict({
    "inputs": ["Text to embed"],
    "parameters": {"normalize": True}
})
embedding = result[0][0]  # 1024-dim vector
```

### S3 Event-Driven RAG Indexing
```python
# Serverless auto-indexing when new docs uploaded to S3
# Lambda triggered by S3 PutObject event

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Only process PDFs
        if not key.endswith('.pdf'):
            return
        
        # 1. Extract text with Textract
        text = extract_text_textract(bucket, key)
        
        # 2. Chunk
        chunks = text_splitter.split_text(text)
        
        # 3. Embed
        embeddings = embedding_model.encode(chunks)
        
        # 4. Upsert to OpenSearch
        upsert_to_opensearch(chunks, embeddings, metadata={"source": key})
        
        print(f"Indexed {len(chunks)} chunks from {key}")
```

## 4. Senior Engineer Perspective

### Bedrock vs SageMaker Decision Matrix

| Scenario | Bedrock | SageMaker |
|---------|---------|-----------|
| Standard foundation models | ✅ | ❌ (overkill) |
| Custom/fine-tuned model | ❌ | ✅ |
| Open-source models (LLaMA) | ✅ (some) | ✅ (full control) |
| Predictable, constant traffic | ❌ (per-token expensive) | ✅ (reserved) |
| Variable/bursty traffic | ✅ (pay per call) | ❌ (idle instances) |
| Model customization | Limited | Full |
| Fastest deployment | ✅ | ❌ |

## 5. Production Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|-----------|
| Textract timeout | Large documents | Job status polling | Async + SNS notification |
| Textract poor OCR | Scanned low-quality docs | Sample manual review | Image preprocessing, confidence scores |
| SageMaker endpoint cold start | Auto-scaling to 0 | P99 latency spike | Minimum instances > 0 |
| S3 event missed | S3 notification failure | Document count mismatch | Dead-letter queue |
| Textract rate limits | High document volume | Throttling errors | SQS queue + retry |

## 6. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | S3 event triggers, Textract sync vs async, SageMaker endpoint types |
| **Good To Know** | Textract table extraction, SageMaker Jumpstart, auto-scaling policies |
| **Expert Knowledge** | SageMaker multi-model endpoints, inference pipelines, shadow mode |
| **Architecture Nuggets** | S3→SNS→Lambda→Textract→OpenSearch is the standard doc ingestion pattern |
| **Interview Nuggets** | "SageMaker for custom models; Bedrock for managed APIs" |
| **Red Flags** | Sync Textract for large docs; no dead-letter queue for S3 events |
| **Production Lessons** | Minimum 1 SageMaker instance to avoid cold starts; monitor Textract job failure rate |

---

# Topic 14: AI Agents & Tool-Calling (with LangChain)

## 1. Executive Summary
- **AI Agent**: LLM that takes actions in a loop — perceive → think → act → observe → repeat
- **Problem solved:** Complex tasks requiring multiple steps, tool use, and decision-making
- Tool calling enables: web search, code execution, database queries, API calls, file I/O
- ReAct (Reason + Act): standard agent reasoning pattern
- Agent types: zero-shot, conversational, structured chat, OpenAI tools
- **Agent loop risk**: infinite loops, tool abuse, cost explosion — critical to manage
- LangGraph is preferred over LangChain AgentExecutor for production agents
- Multi-agent systems: specialize agents for subtasks (researcher, writer, reviewer)
- Human-in-the-loop: pause for approval before irreversible actions
- Reliability gap vs deterministic code: agents are probabilistic — need guardrails

## 2. Mental Model
> "An AI agent is like a capable employee given a task and a toolbox. It reads the task, decides which tool to use, uses it, reads the result, decides the next step, and repeats until done. A bad agent is an employee who loops endlessly or uses tools inappropriately."

```
Task: "Research and summarize the latest AI news"

Agent Loop:
→ THINK: "I need to search for AI news"
→ ACT: search_web("latest AI news 2024")
→ OBSERVE: [search results]
→ THINK: "I have results, let me get details on top 3"
→ ACT: fetch_url("https://...")
→ OBSERVE: [article content]
→ THINK: "I have enough information, I can write the summary"
→ ACT: format_response(...)
→ END
```

## 3. Beginner Level

### LangChain Agent with Tools
```python
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression. Input should be a valid Python math expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {"abs": abs, "round": round})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

tools = [DuckDuckGoSearchRun(), calculate]

llm = ChatAnthropic(model="claude-sonnet-4-5")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when needed."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)

result = agent_executor.invoke({"input": "What is 15% of 847, and what was GPT-4's release date?"})
```

## 4. Practitioner Level

### LangGraph Agent (Production Pattern)
```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_anthropic import ChatAnthropic

# Define tools
tools = [search_tool, calculator_tool, database_tool]

# LLM with tools bound
llm_with_tools = ChatAnthropic(model="claude-sonnet-4-5").bind_tools(tools)

def call_model(state):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Build agent graph
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    tools_condition,  # If LLM called a tool → "tools", else → END
)
workflow.add_edge("tools", "agent")  # After tool execution → back to agent

app = workflow.compile(checkpointer=memory)
```

### Tool Safety Patterns
```python
# Always add safety guardrails for production tools
class SafeToolExecutor:
    def __init__(self, tool, max_calls_per_session: int = 10):
        self.tool = tool
        self.max_calls = max_calls_per_session
        self.call_count = 0
    
    def execute(self, *args, **kwargs):
        # Rate limiting
        if self.call_count >= self.max_calls:
            raise ToolAbusePrevention(f"Max {self.max_calls} calls exceeded")
        
        # Input validation
        self._validate_input(*args, **kwargs)
        
        # Execution with timeout
        with timeout(seconds=30):
            result = self.tool.run(*args, **kwargs)
        
        self.call_count += 1
        return result
    
    def _validate_input(self, *args, **kwargs):
        # Tool-specific validation
        pass
```

### Human-in-the-Loop Pattern
```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

app = workflow.compile(
    checkpointer=SqliteSaver.from_conn_string("checkpoints.db"),
    interrupt_before=["execute_database_write"]  # Pause before write ops
)

# Run until interrupt
config = {"configurable": {"thread_id": "session-1"}}
result = app.invoke({"messages": [HumanMessage(content="Delete all test records")]}, config)

# Show proposed action to human
print("Agent wants to execute:", result["pending_action"])
approval = input("Approve? (yes/no): ")

if approval == "yes":
    # Resume execution
    final_result = app.invoke(None, config)  # None = resume from checkpoint
```

## 5. Senior Engineer Perspective

### Agent vs Workflow Decision

| Scenario | Agent | Workflow (LangGraph) |
|---------|-------|---------------------|
| Dynamic tool selection | ✅ | ❌ (predefined paths) |
| Predictable execution | ❌ | ✅ |
| Auditable steps | ❌ | ✅ |
| Complex conditional logic | ✅ | ✅ |
| High reliability needed | ❌ | ✅ |
| Open-ended research tasks | ✅ | ❌ |

### Common Agent Failure Patterns
```
1. Infinite loops: Agent keeps calling same tool
   Fix: Max iterations, detect repeated actions

2. Tool hallucination: Invents tool parameters
   Fix: Strict input validation, typed tool signatures

3. Context drift: Loses original task after many tool calls
   Fix: Periodically re-inject original task, use checkpoints

4. Cost explosion: Thousands of LLM calls
   Fix: Token budget, iteration limit, cost monitoring

5. Cascading failures: Tool error → wrong reasoning → wrong action
   Fix: Tool error handling, confidence thresholds
```

## 6. Production Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|-----------|
| Infinite agent loop | No exit condition | Iteration counter | max_iterations=10-20 |
| Tool parameter hallucination | LLM guesses params | Input validation | Pydantic tool schemas |
| Agent ignores tool errors | Poor error handling | Error in tool result | Explicit error return format |
| Context window overflow | Long tool results | Token monitoring | Truncate tool results |
| Cost explosion | Unbound tool calls | Cost per session | Budget limits, kill switch |

## 7. Interview Preparation

**Beginner:**
1. What is an AI agent? → LLM that perceives, reasons, and takes actions in a loop
2. What is ReAct? → Reason + Act; interleave reasoning and tool use
3. What is tool calling? → LLM returns structured function call; app executes it
4. Why is max_iterations important? → Prevents infinite loops and cost explosion
5. Agent vs chain? → Agent: dynamic tool selection; chain: fixed sequential steps

**Senior:**
1. Design a production agent system for automated code review
2. How do you audit agent decisions for compliance?
3. When would you use a deterministic workflow over an agent?
4. Design a multi-agent system for market research with specialized sub-agents

## 8. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | Agent loop (perceive/think/act/observe), tool calling, max_iterations, ReAct |
| **Good To Know** | LangGraph agent, human-in-the-loop, tool safety patterns |
| **Expert Knowledge** | Multi-agent systems, agent evaluation, cost-bounded agents |
| **Architecture Nuggets** | Workflows for reliability; agents for flexibility; always HITL for destructive actions |
| **Interview Nuggets** | "Agents are probabilistic — add guardrails" — "max_iterations is your circuit breaker" |
| **Red Flags** | No max iterations; no tool input validation; no cost limits; agents with write access and no HITL |
| **Production Lessons** | LangSmith every agent run; validate all tool inputs; implement kill switch for runaway agents |

---

# Topic 15: LangSmith & LangFuse

## 1. Executive Summary
- **LangSmith**: Anthropic/LangChain's observability platform for LLM apps — tracing, evaluation, debugging
- **LangFuse**: Open-source LLM observability — traces, evals, prompt management
- **Problem solved:** LLM apps are black boxes; need visibility into what prompts/retrievals/outputs look like
- Both provide: trace capture, latency, token usage, cost, error logging
- LangSmith: tightly integrated with LangChain/LangGraph; best for LangChain stack
- LangFuse: open-source, self-hostable, framework-agnostic; better for compliance
- Critical for: debugging RAG failures, prompt versioning, evaluation datasets
- Production monitoring: track latency, cost, error rates, user feedback
- Evaluation: run evals against ground truth, A/B test prompts
- Without observability, GenAI apps are unmanageable in production

## 2. Mental Model
> "LangSmith/LangFuse are like flight data recorders for LLM apps. Every input, intermediate step, tool call, and output is captured so you can replay and debug any failure."

## 3. LangSmith Setup & Usage
```python
# Setup (environment variables)
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
os.environ["LANGCHAIN_PROJECT"] = "rag-production"

# Everything using LangChain is now automatically traced!
# Traces appear at smith.langchain.com

# Manual tracing for non-LangChain code
from langsmith import traceable

@traceable(name="custom-rag-pipeline", tags=["production", "v2"])
def my_rag_pipeline(question: str) -> str:
    # ... your code
    return answer

# Add user feedback
from langsmith import Client
client = Client()
client.create_feedback(
    run_id="...",
    key="user_rating",
    score=0.9,
    comment="Answer was accurate"
)
```

## 4. LangFuse Setup & Usage
```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com"  # Or self-hosted URL
)

# Manual instrumentation
trace = langfuse.trace(
    name="rag-query",
    user_id="user_123",
    session_id="session_456",
    input={"question": user_question}
)

span = trace.span(name="retrieval", input={"query": user_question})
docs = retriever.invoke(user_question)
span.end(output={"doc_count": len(docs)})

generation = trace.generation(
    name="llm-call",
    model="claude-sonnet-4-5",
    input=[{"role": "user", "content": augmented_prompt}],
    output=answer,
    usage={"input": 1200, "output": 350}
)

trace.update(output={"answer": answer})
```

## 5. LangSmith vs LangFuse

| Dimension | LangSmith | LangFuse |
|----------|-----------|---------|
| **Open source** | ❌ | ✅ |
| **Self-hostable** | ❌ (enterprise) | ✅ (free) |
| **LangChain integration** | Native (auto) | Manual |
| **Framework agnostic** | Mostly LangChain | ✅ Any |
| **Prompt management** | ✅ | ✅ |
| **Evaluation** | ✅ LLM-as-judge | ✅ |
| **Cost** | Paid (freemium) | Open-source |
| **Best for** | LangChain stack | Multi-framework, compliance |

## 6. Production Monitoring Dashboard

### Key Metrics to Track
| Metric | LangSmith | LangFuse | Alert Threshold |
|--------|-----------|---------|----------------|
| P95 latency | ✅ | ✅ | >5 seconds |
| Token cost/hour | ✅ | ✅ | >$50/hour |
| Error rate | ✅ | ✅ | >1% |
| Retrieval count | ✅ | ✅ | Avg <3 might indicate issue |
| User feedback score | ✅ | ✅ | <0.7 triggers review |

## 7. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | Tracing, spans, generations, latency/cost/error monitoring |
| **Good To Know** | LLM-as-judge evals, prompt management, dataset curation from traces |
| **Expert Knowledge** | Self-hosted LangFuse, custom eval metrics, production feedback loops |
| **Architecture Nuggets** | Add LangSmith from day 1; trace every LLM call; save examples to eval datasets |
| **Interview Nuggets** | "LangSmith = LangChain native; LangFuse = open-source, any framework" |
| **Red Flags** | No observability in production; no cost monitoring; no latency alerts |
| **Production Lessons** | Traces are your debugging lifeline; capture user feedback; build eval datasets from production |

---

# Topic 16: CrewAI

## 1. Executive Summary
- **CrewAI**: Multi-agent orchestration framework where specialized agents collaborate as a "crew"
- **Problem solved:** Complex tasks benefit from specialized agents (researcher, analyst, writer)
- Each agent has: role, goal, backstory, tools, LLM
- Agents hand off work through a structured process (sequential, hierarchical, or parallel)
- Built on top of LangChain; integrates with LangSmith
- Good for: content pipelines, research tasks, automated workflows with specialization
- Limitations: Less flexible than LangGraph; limited state management; debugging harder
- vs LangGraph: CrewAI = high-level, roles-based; LangGraph = low-level, graph-based control
- Production maturity: LangGraph > CrewAI for complex production use cases

## 2. Mental Model
> "CrewAI is like assembling a project team. You hire a Researcher, an Analyst, and a Writer. Each knows their job. The Researcher finds info, hands it to the Analyst who synthesizes it, who hands to the Writer who drafts the report."

## 3. Core Usage
```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Define agents
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI',
    backstory='Expert researcher with 10 years in AI/ML',
    tools=[SerperDevTool()],  # Web search
    llm='claude-sonnet-4-5',
    verbose=True
)

writer = Agent(
    role='Tech Content Writer',
    goal='Write clear, engaging content about AI',
    backstory='Expert writer specializing in AI/tech content',
    tools=[],
    llm='claude-sonnet-4-5'
)

# Define tasks
research_task = Task(
    description='Research the latest RAG techniques. Focus on papers from last 6 months.',
    agent=researcher,
    expected_output='A detailed report on latest RAG techniques with citations'
)

writing_task = Task(
    description='Write a blog post based on the research findings',
    agent=writer,
    expected_output='A 1000-word blog post on RAG techniques'
)

# Assemble crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,  # researcher → writer
    verbose=True
)

result = crew.kickoff()
```

## 4. CrewAI vs LangGraph

| Dimension | CrewAI | LangGraph |
|----------|--------|-----------|
| **Abstraction level** | High (roles/tasks) | Low (nodes/edges) |
| **Learning curve** | Easy | Medium |
| **Flexibility** | Limited | Full |
| **State management** | Basic | Rich |
| **Debugging** | Harder | Visual + traces |
| **Production maturity** | Medium | High |
| **Best for** | Content pipelines, simple orchestration | Complex agents, conditional logic |
| **Human-in-the-loop** | Limited | First-class |

## 5. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | Agent (role/goal/backstory), Task, Crew, Process types |
| **Good To Know** | Memory types (short/long), hierarchical process, inter-agent delegation |
| **Expert Knowledge** | Custom tools, crew output callbacks, production deployment |
| **Architecture Nuggets** | Use CrewAI for content/research; LangGraph for control-critical systems |
| **Interview Nuggets** | "CrewAI = team metaphor; each agent has role, goal, tools" |
| **Red Flags** | Using CrewAI for financial/medical decisions without HITL; no observability |
| **Production Lessons** | CrewAI is great for prototyping; migrate to LangGraph for reliability-critical production |

---

# Topic 17: Docker Fundamentals for GenAI

## 1. Executive Summary
- **Docker**: Container runtime — package app + dependencies into isolated, portable unit
- **Problem solved:** "Works on my machine" — consistent environments from dev to production
- Containers share host OS kernel (lightweight vs VMs)
- Critical for: deploying LLM inference servers, RAG pipelines, embeddings services
- Dockerfile = recipe for building container image
- Docker Compose = multi-container apps (app + vector DB + redis)
- ECS/Fargate/Kubernetes: run containers at scale on AWS
- GPU support: NVIDIA Container Toolkit for LLM inference containers
- Multi-stage builds: smaller production images
- Security: don't run as root; scan images; minimal base images

## 2. Practitioner Level

### FastAPI + RAG Pipeline in Docker
```dockerfile
# Dockerfile for RAG API Service
FROM python:3.11-slim

# Security: Don't run as root
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# Install dependencies first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Docker Compose for Local RAG Stack
```yaml
# docker-compose.yml
version: '3.8'

services:
  rag-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENSEARCH_URL=http://opensearch:9200
    depends_on:
      - opensearch
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    
  opensearch:
    image: opensearchproject/opensearch:2.11.0
    environment:
      - discovery.type=single-node
      - DISABLE_SECURITY_PLUGIN=true
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - opensearch-data:/usr/share/opensearch/data
    
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  opensearch-data:
```

### GPU-Enabled Container (LLM Inference)
```dockerfile
# For vLLM / Ollama inference server
FROM nvidia/cuda:12.1-devel-ubuntu22.04

RUN pip install vllm

CMD ["python", "-m", "vllm.entrypoints.openai.api_server", \
     "--model", "meta-llama/Llama-3.1-8B-Instruct", \
     "--port", "8080"]
```

```bash
# Run with GPU access
docker run --gpus all -p 8080:8080 llm-inference:latest
```

### AWS ECR + ECS Deployment
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker build -t rag-api .
docker tag rag-api:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/rag-api:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/rag-api:latest
```

## 3. Docker Security Checklist
```
✅ Non-root user (USER appuser)
✅ Read-only filesystem (--read-only where possible)
✅ No secrets in Dockerfile (use env vars or secrets manager)
✅ Minimal base image (python:3.11-slim > python:3.11)
✅ Multi-stage builds (separate build and runtime)
✅ Image scanning (Snyk, Trivy, ECR scan-on-push)
✅ Health checks defined
✅ Resource limits (--memory, --cpus)
✅ No privileged mode
✅ Signed images (Docker Content Trust)
```

## 4. Production Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|-----------|
| Container OOM | Model too large for memory limit | OOM kill events | Increase memory limit; quantization |
| Image size too large | No multi-stage build | CI/CD slow builds | Multi-stage, .dockerignore |
| Secrets in image | ENV in Dockerfile | Image scanning | AWS Secrets Manager |
| Cold start latency | Large image, slow pull | Startup time metrics | Warm pools, smaller image |
| GPU not available | Missing nvidia runtime | cuda errors | NVIDIA Container Toolkit |

## 5. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | Dockerfile syntax, Docker Compose, build/run/push, layer caching |
| **Good To Know** | Multi-stage builds, health checks, GPU support, ECR |
| **Expert Knowledge** | Container orchestration (ECS, K8s), image scanning, Docker BuildKit |
| **Architecture Nuggets** | Layer cache: deps first, code second; non-root always; health checks required |
| **Interview Nuggets** | "Containers = consistent environments; compose = local multi-service dev" |
| **Red Flags** | Secrets in Dockerfile; running as root; no health check; massive images |
| **Production Lessons** | Multi-stage builds save 60%+ image size; scan images in CI; always set memory limits |
