## 🗺️ Big Picture First — What Even Is RAG?

### The Core Idea

**RAG = Retrieval-Augmented Generation.**

Think of it this way: an LLM by itself is like a very well-read person who was locked in a library until a specific date, then let out. They know everything up to that date, but nothing after. And for topics specific to *your* company, your *own* documents, or your *internal* data — they know nothing at all.

RAG solves this by giving the LLM a "cheat sheet" at query time. Instead of answering purely from memory, the system first *goes and finds relevant documents*, hands those to the LLM, and says "answer the question using only these."

```
User Query
    │
    ▼
[Retriever] ──── searches a vector database ──── returns top-K chunks
    │
    ▼
[LLM Prompt] = system prompt + retrieved chunks + user query
    │
    ▼
[LLM] generates a final answer
```

### Why Does RAG Fail in Production?

Simple RAG works fine in demos. In production, it silently fails in very specific ways that are hard to spot without a structured evaluation framework. There are two fundamental failure points:

1. **Retrieval fails** — the wrong documents come back, or important ones are missed entirely.
2. **Generation fails** — the right documents came back, but the LLM still produced a wrong, hallucinated, or incomplete answer.

This guide teaches you to categorize these failures, measure them with proper metrics, trace them in production, and apply targeted engineering fixes.

---

## Module 1 — Production Failure Mode Taxonomy

### 🌐 Broad View

You cannot fix what you cannot name. This module is a precise vocabulary for the ways RAG breaks. Think of it as a field guide to failure — before you can debug a pipeline, you need to recognize *which kind* of failure you're looking at.

---

### Retrieval Faults

#### 1. Semantic Compression Mismatch

**Theory:**

When you store a document in a vector database, you first convert it into an *embedding* — a list of hundreds of floating-point numbers (e.g., 384 or 1536 numbers). This list is a compressed mathematical representation of the document's meaning. The process is called *dense retrieval* because all meaning is packed into a fixed-size dense vector.

The problem: compression is lossy. When you squash a paragraph into a vector, subtle linguistic signals get averaged out. The model learns that "format" and "not format" both live in the universe of "disk formatting topics" and places their vectors very close together. The negation — the most important part of the second query — barely moves the needle.

This is a fundamental property of how transformer-based embedding models work. They are trained to bring *semantically related* text close together. But "related" is not the same as "identical in meaning" or "logically equivalent." Negations, specific serial numbers, legal terms, and exact product codes all tend to collapse into the same neighborhood in vector space as their positive counterparts.

**Real-world impact:** A user asks "which medications should NOT be taken with aspirin?" The retriever returns chunks about aspirin interactions — including both compatible and incompatible drugs — because it cannot distinguish the negation. The LLM then gets noisy context and may miss the contraindications entirely.

```python
# Demonstrating the problem with a simple similarity check
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

# These two queries are OPPOSITE in meaning, but very similar in embedding space
query_a = "how to format a hard drive"
query_b = "how to NOT format a hard drive"

# Encode both queries into vectors (lists of 384 numbers each)
emb_a = model.encode(query_a)
emb_b = model.encode(query_b)

# Cosine similarity: 1.0 = identical direction, 0.0 = unrelated, -1.0 = opposite
similarity = util.cos_sim(emb_a, emb_b).item()

print(f"Similarity between opposite queries: {similarity:.4f}")
# Output will be very HIGH (e.g., 0.91) — the retriever treats them as nearly the same!
```

**Why this matters in practice:** If your product has a safety-critical knowledge base (medical, legal, financial), a retriever that cannot distinguish negations is a liability. It will silently retrieve the wrong context and the LLM will silently answer wrong.

**Fix:** Hybrid Search — covered in Module 6. You combine dense vector search with sparse keyword search (BM25), so exact words like "NOT" and serial numbers are matched literally.

---

#### 2. Context Fragmentation & Boundary Violations

**Theory:**

Before documents are stored in a vector database, they must be chopped into smaller pieces called *chunks*. This is unavoidable because: (a) embedding models have a maximum input length, and (b) you want fine-grained retrieval — fetching a 3-sentence chunk is better than fetching a 50-page document.

The chunking strategy matters enormously. The naive approach is to cut every N characters. This is fast to implement but semantically blind — it cuts wherever the character counter runs out, not where the meaning naturally ends. The result is chunks that start mid-sentence, end mid-argument, or split a cause from its effect across a boundary.

The critical insight: **a chunk is only as useful as its standalone meaning**. If you retrieve a chunk that says "...in which case the penalty applies immediately," without the preceding sentence that explains what "the case" is — the chunk is useless and potentially misleading.

Chunk overlap is a partial mitigation: you repeat N tokens at the start of each chunk from the end of the previous one. But this is a band-aid over a flawed strategy rather than a true fix.

```
# Example of a dangerous boundary split:
# ─────────────────────────────────────────────────────────────────────────────
# Chunk 1 ends: "...The patient should take 200mg of ibuprofen every 4 hours. In cases of"
# Chunk 2 starts: "kidney disease, this dosage must be reduced by 50%."
# ─────────────────────────────────────────────────────────────────────────────
# If only Chunk 1 is retrieved, the LLM gives dangerously incomplete advice.
```

```python
# BAD chunking — hard character cutoff splits sentences mid-way
def bad_chunker(text, chunk_size=200):
    # Just slices the string at a fixed character count
    # Has zero awareness of sentence or paragraph structure
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# BETTER chunking — respects sentence and paragraph boundaries
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,           # target chunk size in characters
    chunk_overlap=50,         # overlap: copies 50 chars from end of prev chunk into next
                              # this prevents losing boundary sentences entirely
    separators=["\n\n", "\n", ". ", " "]
    # tries separators in order:
    # first split on double newlines (paragraph breaks)
    # then single newlines
    # then sentence-ending periods
    # finally, spaces (last resort)
)

chunks = splitter.split_text(your_document_text)
```

**The deeper fix** is semantic chunking — using embedding similarity itself to detect when the *topic* shifts, and only cutting there. This is covered in Module 6.

---

#### 3. The "Lost in the Middle" Phenomenon

**Theory:**

This failure mode lives entirely inside the LLM, not the retriever. Even after you've successfully retrieved the right chunks, the LLM may ignore them.

Research (Liu et al., 2023 — "Lost in the Middle") showed that transformer-based LLMs have a distinct positional bias: they are significantly more likely to use information from the **beginning** and **end** of their input context. Content placed in the middle of a long prompt receives disproportionately low attention.

The mechanism is rooted in how attention works in transformers. Tokens that appear early establish a strong "priming" effect on later tokens. Tokens at the very end are the most recently "seen" before generation begins. Tokens sandwiched in between have to compete with both ends and often lose.

In a RAG pipeline with 10-20 retrieved chunks, you're practically guaranteed to have important information in the middle. The LLM will process it, but may under-weight it when generating the final answer.

```
# Practical illustration — prompt layout matters:
# ─────────────────────────────────────────
# [System Prompt]          ← LLM is primed here
# [Chunk 1 — Relevant]     ← High attention ✅
# [Chunk 2 — Relevant]     ← Attention starts dropping ⚠️
# [Chunk 3 — Irrelevant]   ← Very low attention 😴
# [Chunk 4 — CRITICAL]     ← Lost in middle — often ignored ❌
# [Chunk 5 — Irrelevant]   ← Very low attention 😴
# [Chunk 6 — Relevant]     ← Attention recovers slightly ⚠️
# [User Query]             ← High attention ✅
# ─────────────────────────────────────────
# The most important chunk (4) is the least likely to influence the answer.
```

**Why this is insidious:** You run your retrieval evaluation and it looks perfect — all the right chunks are retrieved. You run your faithfulness evaluation and it looks fine — no hallucinations. But the answer is still wrong or incomplete. This is because the failure happens in the *attention weighting* step, which no retrieval metric catches.

**Fix:** Rerank retrieved chunks so the most relevant go first or last. Use prompt compression to eliminate low-value chunks entirely, reducing how much ends up "in the middle." Covered in Module 6.

---

### Generation & Synthesis Faults

#### 4. Contextual Overreliance vs. Weight Bias

**Theory:**

LLMs have two sources of knowledge during inference:
- **Parametric knowledge**: facts baked into the model's weights during training. Think of this as the model's "long-term memory."
- **Contextual knowledge**: facts provided in the prompt (your retrieved chunks). Think of this as "working memory."

In theory, RAG supplies the correct facts via context, and the LLM uses them. In practice, the model sometimes trusts its parametric weights over conflicting contextual information. This is called *weight bias* or *knowledge conflict*.

Why does this happen? During training, the model saw a given fact repeated thousands of times across the internet. That repetition created strong weight patterns. When you show the model a single retrieved chunk contradicting that deeply-reinforced pattern, the parametric signal can overpower the contextual signal.

This is particularly dangerous when:
- You're working with domain-specific or recently updated information (outdated training data)
- The model was trained on noisy internet data that contained wrong "facts" at high frequency
- You have numbers, statistics, or proper nouns that the model confidently "knows" but has wrong

```
# Concrete failure example:
# ──────────────────────────────────────────────────────────────────
# Retrieved chunk: "Company X revenue in 2024 was $500M"
# Model's parametric memory (from training): "Company X revenue ≈ $200M"
# LLM's answer: "$200M"  ← parametric weights won over the context
# ──────────────────────────────────────────────────────────────────
```

**Fix:** Explicit prompting instructions that anchor the model to the context. E.g., `"Answer ONLY based on the provided context. If the context contradicts what you know, trust the context. Do not use outside knowledge."` Also consider fine-tuning the model on your domain to align parametric and contextual knowledge.

---

#### 5. Hallucination Subtypes

**Theory:**

"Hallucination" is a broad term that gets thrown around loosely. In production, you need to distinguish between two fundamentally different failure modes because they require different detection methods and have different severity profiles.

**Intrinsic Hallucination:** The LLM says something that *directly contradicts* what the retrieved context says. This is the easier type to detect because you have a ground truth to check against — the retrieved context itself. Natural Language Inference (NLI) models can be used to check if the claim is entailed, neutral, or contradicted by the context.

**Extrinsic Hallucination:** The LLM says something that isn't mentioned anywhere in the retrieved context — and you can't verify it from the context alone. The claim might actually be correct (the LLM recalled a real fact from its parametric memory), or it might be completely fabricated. You can't tell without an external fact-checking source.

The distinction matters for evaluation: intrinsic hallucinations are a *faithfulness failure* (the LLM contradicted what it was told). Extrinsic hallucinations are a *completeness/verification failure* (the LLM went beyond its sources).

| | Intrinsic Hallucination | Extrinsic Hallucination |
|---|---|---|
| **Definition** | Contradicts retrieved context | Adds facts absent from context |
| **Detectability** | High — use NLI against context | Low — requires external verification |
| **Root Cause** | Weight bias overpowering context | Over-generation, parametric leakage |
| **Severity** | High — actively wrong | Medium — unverifiable |
| **Fix** | Stronger context grounding prompts | Citation requirements, source linking |

---

#### 6. Fragmented Aggregation Failure

**Theory:**

This failure mode is about the fundamental mismatch between how top-K vector search works and what certain queries actually need.

Top-K vector search is a *local* operation. It finds the K chunks most similar to the query — the K nearest neighbors in vector space. It is inherently designed to find localized, specific answers. The query "What is the refund policy?" will correctly find the chunk describing the refund policy.

But some queries are *global* by nature. "Summarize all regional travel policies," "What are all the exceptions to Rule 4.2?", or "List every product that contains peanuts" require scanning *all* relevant chunks across the *entire* knowledge base. Top-K retrieval doesn't do this — it only finds the K chunks that most *look like* the query.

The failure is silent: the LLM gets 5 chunks, synthesizes them faithfully, and produces a confident-looking answer — but it only covered 5 of the 20 regional policies that exist. There's no error. The LLM doesn't know it's missing 15 policies.

```
# Why top-K fails on aggregation queries:
#
# Query: "Summarize ALL regional travel policies"
# Vector search finds the 5 chunks MOST SIMILAR to this query
#
# ┌─────────────────────────────────────────────┐
# │  Vector DB has 20 regional policy chunks    │
# │  ● EMEA Policy                              │
# │  ● APAC Policy                              │
# │  ● LATAM Policy   ← top-5 retrieved ✅     │
# │  ● North America Policy ← retrieved ✅      │
# │  ● UK Policy      ← retrieved ✅            │
# │  ● Germany Policy ← NOT retrieved ❌        │
# │  ● France Policy  ← NOT retrieved ❌        │
# │  ... 13 more not retrieved ❌               │
# └─────────────────────────────────────────────┘
# LLM sees 5 policies, summarizes them perfectly,
# and confidently omits 15 policies it never saw.
```

**Fix:** For aggregation queries, use a *query decomposition* + *metadata filtering* strategy. Decompose "summarize all regional policies" into explicit sub-queries per region, or use metadata filters to retrieve *all* chunks with tag `type=regional_policy` regardless of semantic similarity.

---

## Module 2 — Component-Level IR Metrics (Retriever Evaluation)

### 🌐 Broad View

A RAG pipeline has two distinct components: the retriever and the generator. Before diagnosing the LLM, you must evaluate the retriever *in complete isolation*. These metrics come from the field of Information Retrieval (IR), which predates LLMs by decades and was developed for search engines.

The key mental model: **imagine the retriever as a search engine, and you're evaluating search quality.** You have a set of test queries, and for each query you know (from human annotation or synthetic generation) which chunks are "relevant." You measure how well the retriever finds those chunks.

---

### Set-Based Metrics

These metrics treat retrieval as a *set membership* problem — a chunk is either relevant or it isn't (binary judgment). The rank/order of results doesn't matter here.

#### Precision@K

**Theory:**

Precision@K answers: *"Of the K results I returned, how many were actually worth returning?"* It measures the *signal-to-noise ratio* of your retriever.

A retriever with low Precision@K brings back a lot of irrelevant chunks alongside the relevant ones. This directly harms generation quality because the LLM now has noisy context — it must "find the needle in the haystack" of the retrieved documents. The "lost in the middle" problem gets significantly worse with noisy retrievals.

Mathematically: `Precision@K = (# relevant chunks in top-K) / K`

A score of 1.0 means every single retrieved chunk was relevant. A score of 0.2 means only 1 in 5 retrieved chunks was useful.

```
# Concrete example — K = 5:
# Retrieved: [✅ relevant, ❌ noise, ✅ relevant, ✅ relevant, ❌ noise]
#
# Precision@5 = 3 relevant / 5 retrieved = 0.60
# Meaning: 60% of what was retrieved was actually useful
```


# Example usage
retrieved = ["chunk_3", "chunk_7", "chunk_1", "chunk_9", "chunk_2"]
relevant   = {"chunk_3", "chunk_1", "chunk_5"}  # ground truth — 3 relevant docs exist

print(precision_at_k(retrieved, relevant, k=5))  # 2/5 = 0.40
# chunk_3 ✅, chunk_7 ❌, chunk_1 ✅, chunk_9 ❌, chunk_2 ❌ → 2 hits out of 5
```

---

#### Recall@K

**Theory:**

Recall@K answers the opposite question: *"Of all the relevant chunks that exist in the entire database, how many did I actually find?"* It measures *coverage*.

A retriever with high Recall@K but low Precision@K finds most relevant documents, but also brings back a lot of garbage. A retriever with high Precision@K but low Recall@K is very selective and precise, but may miss important documents.

This creates an unavoidable tradeoff: increasing K (retrieving more documents) almost always improves Recall (you catch more relevant docs) but hurts Precision (you also catch more irrelevant ones).

Mathematically: `Recall@K = (# relevant chunks in top-K) / (total # of relevant chunks in database)`

```
# Example continuing from above:
# 3 total relevant chunks exist in the database: chunk_3, chunk_1, chunk_5
# We retrieved top-5: chunk_3 ✅, chunk_7 ❌, chunk_1 ✅, chunk_9 ❌, chunk_2 ❌
#
# We found chunk_3 and chunk_1 — but MISSED chunk_5
# Recall@5 = 2 found / 3 total relevant = 0.67
# We only covered 67% of the relevant information
```
# Example: 3 total relevant docs exist, we found 2 in top-5
print(recall_at_k(retrieved, relevant, k=5))  # 2/3 ≈ 0.67
```

> 💡 **Practical tradeoff guide:**
> - Legal/compliance RAG → optimize for Recall (missing a clause is dangerous)
> - Customer support chatbot → optimize for Precision (noisy context produces bad answers)
> - Most production systems → balance both, target Precision > 0.7 and Recall > 0.6

---

### Rank-Aware Metrics

Set-based metrics ignore the *order* of results. But order matters — a retriever that puts the best result at rank 1 is better than one that buries it at rank 10, even if the set of returned documents is identical. Rank-aware metrics capture this.

#### MRR — Mean Reciprocal Rank

**Theory:**

MRR focuses on a single critical question: *"How deep do I have to look before finding the FIRST relevant result?"*

It is calculated as: `MRR = (1/|Q|) × Σ (1 / rank_of_first_relevant_result)`

If the first relevant result is at rank 1, your score is 1/1 = 1.0 (perfect). If it's at rank 2, you score 1/2 = 0.5. At rank 3: 1/3 = 0.33. If no relevant result is found, score is 0.

MRR assumes a user-centric model: the user scans results from top to bottom and stops when they find the first relevant result. This is a realistic model for applications where you pass only the *top-1* result to the LLM, or where the user directly reads the search results.

**MRR's limitation:** It only cares about the *first* relevant result. If your query has 5 highly relevant chunks and MRR only checks where the first one lands, it misses information about whether the other 4 were also retrieved well.

---

#### NDCG — Normalized Discounted Cumulative Gain

**Theory:**

NDCG is the most sophisticated of the four metrics. It extends MRR in two important ways:

1. **Graded relevance**: Instead of binary (relevant/irrelevant), you can assign relevance scores on a scale (e.g., 0 = irrelevant, 1 = partially relevant, 2 = mostly relevant, 3 = perfect match). This reflects the real world better — not all relevant chunks are equally valuable.

2. **Discounted positions**: Each rank position is *discounted* by log₂(rank+1), so the reward for placing a highly relevant chunk at rank 1 is much greater than placing it at rank 5.

The formula: `DCG@K = Σ relevance(i) / log₂(i+1)` for i in 1..K

"Normalized" means you divide by the *ideal* DCG — the DCG you'd get if everything were in perfect order. This normalizes the score to [0, 1].

NDCG is the most accurate single number for measuring "how good is your ranking?" for complex queries with multiple relevant documents of varying quality.

---

## Module 3 — Inference-Layer Evaluation (RAG Triad & LLM-as-a-Judge)

### 🌐 Broad View

Once you've validated the retriever, you need to evaluate the *full pipeline* — retriever + LLM together. Classic metrics like BLEU and ROUGE measure word overlap between a generated answer and a reference answer. They're too brittle for open-ended generation: a correct paraphrase scores low, and a fluent hallucination can score high.

The modern approach is **LLM-as-a-Judge**: use a capable LLM to evaluate another LLM's output. This sounds circular, but it works well when the judge is given structured, targeted criteria. The RAG Triad provides exactly that structure.

---

### The RAG Triad

The RAG Triad breaks evaluation into three orthogonal questions, each measuring a different potential failure:

```
                    ┌─────────────────────┐
                    │     User Query      │
                    └──────────┬──────────┘
                               │
               ┌───────────────┼───────────────┐
               ▼               ▼               ▼
        [Context          [Answer           [Context
         Recall]          Relevancy]        Precision]
    Did we retrieve    Is the answer      Did we retrieve
    ALL needed info?   on-topic?          ONLY relevant info?
               └───────────────┼───────────────┘
                               ▼
                        [Faithfulness]
                   Does every claim in the answer
                   come from the context?
```

---

#### 1. Faithfulness / Groundedness

**Theory:**

Faithfulness measures: *"Is everything the LLM said actually backed by the retrieved context?"*

This directly targets hallucination. The process works by decomposing the LLM's answer into *atomic claims* — individual, standalone factual assertions. Then for each claim, you run a verification check: is this claim supported by (entailed by) the retrieved context?

The reason for decomposing into atomic claims first is crucial: the LLM might produce a paragraph that is *mostly* faithful with one hallucinated sentence. A holistic check might miss the single bad sentence. Breaking into atoms makes each claim independently checkable.

A faithfulness score of 1.0 means every single claim in the answer is traceable to the retrieved context. A score of 0.7 means 30% of what the LLM said was not grounded — those are your hallucinations.

```
# Example decomposition:
# ─────────────────────────────────────────────────────────────────────
# LLM Answer: "The refund policy allows returns within 30 days.
#              Items must be in original packaging.
#              Refunds are processed within 5-7 business days."
#
# Atomic claims:
#   1. "Returns are allowed within 30 days"    → check vs context
#   2. "Items must be in original packaging"  → check vs context
#   3. "Refunds processed in 5-7 business days" → check vs context
#
# If context only mentions claims 1 and 2:
#   Faithfulness = 2 supported / 3 total claims = 0.67
#   Claim 3 is an extrinsic hallucination
# ─────────────────────────────────────────────────────────────────────
```

---

#### 2. Answer Relevancy

**Theory:**

Answer Relevancy asks: *"Did the LLM actually answer what the user asked, or did it drift to a related but different topic?"*

This is more subtle than faithfulness. An answer can be perfectly grounded in the retrieved context *and* perfectly accurate, but still be off-topic — if the retriever happened to bring back relevant-sounding but tangentially related chunks, the LLM might produce a faithful-but-irrelevant response.

The clever measurement technique: instead of directly comparing the answer to the query (which requires understanding both), generate *synthetic questions* that the LLM's answer would logically be a response to, then measure how similar those synthetic questions are to the original query using embedding similarity.

If the synthetic questions closely match the original query, the answer was on-topic. If they diverge significantly, the answer drifted.

```
# Example:
# ─────────────────────────────────────────────────────────────────────
# User query: "What is the refund timeframe?"
#
# LLM Answer: "Returns within 30 days are accepted. Items must be
#             in original packaging. Our store is open Mon-Sat 9-6."
#
# Synthetic questions generated FROM the answer:
#   - "How long do I have to return an item?"   → relevant ✅
#   - "What are the packaging requirements?"    → somewhat relevant ⚠️
#   - "What are the store's opening hours?"     → NOT what was asked ❌
#
# Average similarity to original query → moderate score → answer drifted
# ─────────────────────────────────────────────────────────────────────
```

---

#### 3. G-Eval Framework

**Theory:**

G-Eval is a generalized evaluation framework that lets you define *custom rubrics* for your specific use case. Rather than measuring a fixed metric, you specify a set of criteria with descriptions, and a judge LLM scores each one.

The key innovation in G-Eval is Chain-of-Thought reasoning: the judge is prompted to *think through* each criterion step by step before assigning a score. This reduces scoring inconsistency and mirrors how a human expert would evaluate output — by reasoning before concluding.

G-Eval is especially useful when you have domain-specific quality dimensions that the standard RAG Triad doesn't cover. For example: "Does the answer use the correct legal terminology?" or "Is the tone appropriate for a medical professional audience?"

```python

# Example usage for a medical RAG system with domain-specific criteria
scores = g_eval(
    answer="The policy allows 14 days of remote work per quarter with manager approval.",
    context="Remote work policy: employees may work remotely for up to 14 days per quarter, subject to manager approval.",
    criteria={
        "accuracy":      "Are all facts in the answer supported by the context?",
        "completeness":  "Does the answer include all key conditions mentioned in the context?",
        "conciseness":   "Is the answer appropriately brief without omitting key details?"
    }
)
# Output: {"accuracy": 5, "completeness": 5, "conciseness": 4}
```

---

## Module 4 — Automated Test Engineering & Benchmarking

### 🌐 Broad View

Manual testing is how you validate a demo. Automated test engineering is how you validate a production system. The goal is to have a regression test suite — a collection of realistic test cases with ground-truth answers — that you can run automatically every time you make a change to your pipeline.

The challenge: building such a test suite by hand requires human experts to read your knowledge base and write hundreds of (question, answer) pairs. This is expensive, slow, and doesn't scale. The solution is to use the LLM itself to generate the test cases from your raw documents.

---

### Why Automated Dataset Generation Matters

Think of it like unit tests in software engineering. When you change a function, you run tests to ensure nothing broke. When you change your chunking strategy, your embedding model, or your prompt template — you need to run your RAG test suite to ensure retrieval quality and answer quality didn't regress.

Without this, you're making changes in the dark and only finding regressions when users complain.

**Test set evolution** is the key concept: Ragas and similar frameworks don't just extract simple Q&A pairs. They *evolve* questions into harder variants to stress-test different failure modes:

- **Simple questions**: "What is the refund timeframe?" — tests basic retrieval
- **Reasoning questions**: "If a customer ordered on Dec 28, what is the last date they can return?" — tests multi-step reasoning
- **Multi-context questions**: Require combining info from 2+ different chunks to answer — tests aggregation
- **Conditional questions**: "Under what conditions does the 30-day policy NOT apply?" — tests negation handling

```python
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_community.document_loaders import DirectoryLoader

# Step 1: Load your raw knowledge base documents
loader = DirectoryLoader("./knowledge_base/", glob="**/*.pdf")
documents = loader.load()

# Step 2: Initialize the test set generator
# It uses an LLM internally to understand and synthesize questions from your docs
generator = TestsetGenerator.with_openai()

# Step 3: Generate test cases across different difficulty levels
# The distributions dict controls what % of each type to generate
testset = generator.generate_with_langchain_docs(
    documents,
    test_size=50,       # total number of test cases to generate
    distributions={
        simple: 0.5,          # 50% straightforward factual questions
        reasoning: 0.25,      # 25% require multi-step inference
        multi_context: 0.25   # 25% need info from multiple chunks combined
    }
)

# Each generated test case contains:
#  - question:      a realistic user query Ragas synthesized
#  - ground_truth:  the correct answer extracted from your documents
#  - contexts:      the specific source chunks the answer was drawn from
df = testset.to_pandas()
print(df[["question", "ground_truth"]].head())
```
---

## Module 5 — Engineering Intervention & Optimization Strategies

### 🌐 Broad View

Evaluation revealed a failing metric. Now you pull a lever. This module is your menu of interventions, organized by what they fix. Each intervention targets a specific failure mode identified in Module 1 and measured by the metrics in Modules 2-3.

```
Metric Failing          →  Likely Root Cause         →  Intervention
─────────────────────────────────────────────────────────────────────
Recall@K < 0.6         →  Fragmentation / wrong K    →  Semantic chunking, increase K
Precision@K < 0.7      →  Too much noise retrieved   →  Cross-encoder reranking
Faithfulness < 0.8     →  LLM hallucinating          →  Stronger grounding prompts
Answer Relevancy < 0.7 →  Retriever drift or HyDE    →  Query transformation / HyDE
Context is long/noisy  →  Many irrelevant chunks      →  LLMLingua compression
Negations failing      →  Dense-only retrieval        →  Hybrid search (BM25 + dense)
```

---

### Retrieval Optimization

#### Advanced Chunking — Semantic + Parent-Child

**Theory:**

The fundamental insight behind advanced chunking is that *retrieval granularity* and *generation context* have opposing requirements:

- **For retrieval**: you want small, precise chunks. A narrow chunk is semantically focused — it will match specific queries with high precision.
- **For generation**: you want large, context-rich chunks. A wide chunk gives the LLM enough surrounding context to understand the retrieved snippet.

**Parent-child chunking** resolves this tension by storing documents at two levels:
- **Child nodes** (small, ~128 tokens): indexed in the vector database for retrieval
- **Parent nodes** (large, ~2048 tokens): stored separately, retrieved only after a child node matches

When the retriever finds a relevant child chunk, it automatically "expands" it by fetching the corresponding parent — giving the LLM wide context while keeping retrieval precise.

**Semantic chunking** takes a different approach: instead of using fixed token counts, it embeds sentences incrementally and cuts a chunk when the semantic similarity between adjacent sentences drops below a threshold. This ensures chunks break at natural topic transitions.

```python
from llama_index.core.node_parser import (
    SemanticSplitterNodeParser,   # cuts at semantic topic shifts
    HierarchicalNodeParser        # creates parent + child levels
)
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding()

# OPTION A: Semantic Chunking
# Embeds each sentence, looks at cosine similarity between consecutive sentences,
# and cuts when similarity drops sharply (topic changes)
semantic_splitter = SemanticSplitterNodeParser(
    buffer_size=1,                      # look 1 sentence ahead/behind for context
    breakpoint_percentile_threshold=95, # only cut at the top 5% sharpest topic breaks
    embed_model=embed_model             # uses the same embedding model as retrieval
)

# OPTION B: Parent-Child Chunking
# Creates a 3-level hierarchy: document → section (2048 tokens) → sentence (128 tokens)
# Vector search runs on the 128-token child nodes (precise)
# LLM gets the 2048-token parent node (contextually rich)
hierarchical_parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]  # levels from coarsest to finest
)
```

---

#### Hybrid Search — BM25 + Dense Vectors

**Theory:**

Dense vector search and sparse keyword search are complementary. Each covers the other's blind spots:

**Dense (vector) search:**
- Excels at: conceptual understanding, paraphrases, synonyms
- Fails at: exact keyword matching, negations, serial numbers, proper nouns, new terminology not in training data

**Sparse (BM25) search:**
- Excels at: exact keyword matches, rare terms, model numbers, domain-specific jargon
- Fails at: conceptual understanding, handles only literal word overlap

**BM25** (Best Match 25) is a probabilistic ranking algorithm that scores documents based on term frequency (how often a term appears in the document) and inverse document frequency (how rare the term is across all documents). It's what Google used before neural search.

Hybrid search runs both in parallel and combines their rankings using **Reciprocal Rank Fusion (RRF)**: each document gets a score of 1/(rank+60) from each retriever, and the scores are summed. This is robust to the individual retrievers having very different score scales.

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma

# BM25: pure keyword matching on the raw text
# Build from documents — it indexes the actual words, not embeddings
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 5   # return top 5 keyword-matched results

# Dense: semantic similarity via embeddings
# Uses cosine similarity between query embedding and stored chunk embeddings
dense_vectorstore = Chroma.from_documents(documents, embedding_function)
dense_retriever = dense_vectorstore.as_retriever(search_kwargs={"k": 5})

# EnsembleRetriever runs both in parallel, then merges via Reciprocal Rank Fusion
# weights control how much to trust each retriever's ranking
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, dense_retriever],
    weights=[0.4, 0.6]  # 40% keyword, 60% semantic
    # Rule of thumb: increase BM25 weight for domain-heavy jargon (legal, medical, technical)
    # Increase dense weight for conversational, general language queries
)

results = hybrid_retriever.get_relevant_documents("ibuprofen 200mg dosage contraindications")
# BM25 matches on exact "ibuprofen", "200mg" → catches the exact product
# Dense matches on "medication dosage safety" semantics → catches related passages
# Both rankings merged → best of both worlds
```

---

#### Cross-Encoder Reranking

**Theory:**

Standard dense retrieval uses a *bi-encoder* architecture: the query and each document are embedded *independently* into separate vectors, and similarity is measured by cosine distance between those pre-computed vectors. This is fast (the document vectors are precomputed and cached), but it's a shallow form of relevance scoring — the model never sees query and document *together*.

A *cross-encoder* takes the query and a candidate document as a single concatenated input and produces a single relevance score. Because it processes both together, it can model complex interactions between query terms and document terms — far more accurately than a cosine similarity between independent embeddings.

The tradeoff: cross-encoders are slow. You cannot pre-compute their scores because the score depends on both the query and the document. Every time a new query arrives, you must run the cross-encoder for every candidate.

**The two-stage solution:** Use the fast bi-encoder to quickly retrieve 50-100 candidates, then use the slow but accurate cross-encoder to re-score and re-rank only those 50-100. The result: the accuracy of cross-encoders at the practical speed of bi-encoders.

```
Stage 1 (fast bi-encoder):       Stage 2 (accurate cross-encoder):
   Query → embed                     Query + each of 50 chunks
   All chunks (pre-embedded)         → cross-encoder together
   Cosine similarity                 → precise relevance score
   → top 50 candidates (ms)          → top 5 final results (seconds)
```

```python
from sentence_transformers import CrossEncoder

# ms-marco is a cross-encoder trained on the MS MARCO passage retrieval dataset
# It is specifically optimized for query-document relevance scoring
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_chunks(query: str, candidate_chunks: list[str], top_n: int = 5) -> list[str]:
    """
    Stage 2 of two-stage retrieval.
    Takes a ~50 candidate pool from bi-encoder retrieval and re-ranks it.
    Returns only the top_n most relevant chunks for injection into the LLM prompt.
    """
    
    # Cross-encoder needs explicit (query, document) pairs as input
    # It processes each pair as a single unit — BOTH texts go in together
    pairs = [(query, chunk) for chunk in candidate_chunks]
    
    # predict() runs inference for each pair — this is the expensive step
    # Output: a relevance score per pair (higher = more relevant)
    scores = reranker.predict(pairs)
    
    # Zip scores with chunks, sort by score descending, take top N
    ranked = sorted(zip(scores, candidate_chunks), reverse=True)
    
    # Return only top N chunk texts — these go into the LLM prompt
    return [chunk for _, chunk in ranked[:top_n]]

# Full two-stage pipeline:
candidates = dense_retriever.get_relevant_documents(query, k=50) # fast stage 1
final_chunks = rerank_chunks(
    query,
    [doc.page_content for doc in candidates],
    top_n=5   # only send 5 highly relevant chunks to the LLM
)
```

---

### Generation Optimization

#### HyDE — Hypothetical Document Embeddings

**Theory:**

HyDE addresses a fundamental asymmetry in RAG: queries and documents inhabit different regions of the embedding space, even when they're semantically related.

Consider: a user types "what's the max dosage?" — a short, casual, conversational query. The document in your knowledge base says "The recommended maximum daily dosage for ibuprofen in adult patients without renal impairment is 1200mg, administered in divided doses not exceeding 400mg per dose." These are about the same thing, but their embeddings are very different: one is a question fragment, the other is a clinical statement.

HyDE's insight: instead of embedding the *question*, generate a *hypothetical answer* and embed that instead. A hypothetical answer ("The maximum dosage is approximately X mg, taken Y times per day...") will have much more similar language patterns to the real document answer — and thus a much closer embedding.

The tradeoff: HyDE adds one extra LLM call per query, increasing latency and cost. Use it when query-document mismatch is your primary retrieval problem, not as a default setting.

```
Without HyDE:
  Query: "what's the max dosage?"
  Vector: [casual question embedding]
  Documents: [clinical text embeddings]
  Cosine similarity: low → retrieves weakly relevant results

With HyDE:
  Query: "what's the max dosage?"
  → LLM generates: "The maximum recommended dosage is X mg per day..."
  Vector: [clinical-style text embedding]
  Documents: [clinical text embeddings]
  Cosine similarity: high → retrieves strongly relevant results
```

```python
def hyde_retrieve(user_query: str, vectorstore, llm_client) -> list:
    """
    HyDE: generate a hypothetical answer, embed it, use it for retrieval.
    The hypothetical answer doesn't need to be correct — it just needs to
    be in the same "style" as real answer documents.
    """
    
    # Step 1: Generate a hypothetical document — what would the answer look like?
    # We don't ask it to "answer the question", we ask it to write a document
    # that CONTAINS the answer. This produces document-like text, not Q&A style.
    response = llm_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": (
                f"Write a short paragraph that a technical document might contain "
                f"to answer this question: {user_query}\n"
                f"Write as if you're the document, not answering a question."
            )
        }]
    )
    hypothetical_doc = response.content[0].text
    
    # Step 2: Use the HYPOTHETICAL DOCUMENT as the search query instead of the original query
    # Its embedding is now "document-shaped" and closer to real documents
    results = vectorstore.similarity_search(hypothetical_doc, k=5)
    
    return results
```

---

#### LLMLingua — Prompt Compression

**Theory:**

After retrieval and reranking, you may still have a large context window. Even 5-10 well-chosen chunks can be 3,000-5,000 tokens. This creates two problems: cost (more tokens = higher API spend) and the lost-in-the-middle problem (long context buries key information).

LLMLingua's approach: use a small, fast language model to *score the information density of every token*. Tokens that carry high-value information (key facts, numbers, conditions) get high scores. Tokens that are low-information (filler words, repeated context, boilerplate) get low scores. Low-scoring tokens are dropped, creating a compressed version of the context.

The compressed context is grammatically weird — it reads like a telegram — but LLMs have been shown to perform equally well or better on compressed contexts because the *information* is preserved even if the syntax is fractured.

At 50% compression, you halve your context window usage while retaining most of the informational content. This directly addresses the lost-in-the-middle problem by making the total context shorter.

```
Original chunk (100 tokens):
"The company's remote work policy was updated in January 2024 and now allows
employees, subject to manager approval, to work from home or any approved
remote location for a maximum period not exceeding fourteen calendar days
per fiscal quarter, provided that the employee maintains full availability
during standard business hours as defined in their employment contract."

After LLMLingua compression at 50%:
"remote work policy updated January 2024, employees with manager approval,
work from home maximum 14 days per fiscal quarter, maintain availability
standard business hours per employment contract."

Key facts preserved: dates, limits, conditions, requirements ✅
Filler removed: "The company's", "was", "now", "any approved", "period", "calendar" ✅
```

```python
from llmlingua import PromptCompressor

# LLMLingua-2 uses a fine-tuned XLM-RoBERTa model to score token importance
# It is orders of magnitude faster than using a full LLM to compress
compressor = PromptCompressor(
    model_name="microsoft/llmlingua-2-xlm-roberta-large-meetingbank",
    use_llmlingua2=True   # use the faster v2 model
)

def compress_context(retrieved_chunks: list[str], compression_ratio: float = 0.5) -> str:
    """
    Compresses multiple retrieved chunks before injecting into the LLM prompt.
    
    compression_ratio = 0.5 means keep ~50% of original tokens.
    This reduces context length, cost, and lost-in-the-middle effects.
    
    Trade-off: too aggressive compression (< 0.3) can drop key facts.
    Sweet spot for most use cases: 0.4 to 0.6.
    """
    
    # Combine all chunks into a single block for holistic compression
    # (The compressor can then decide what's redundant ACROSS chunks, not just within)
    full_context = "\n\n".join(retrieved_chunks)
    
    compressed = compressor.compress_prompt(
        full_context,
        rate=compression_ratio,          # target ratio: keep this fraction of tokens
        force_tokens=["\n", ".", ":", "numbers"],  # always preserve structural tokens and numbers
    )
    
    print(f"Original tokens: ~{len(full_context.split())}")
    print(f"Compressed tokens: ~{len(compressed['compressed_prompt'].split())}")
    
    return compressed["compressed_prompt"]
```

---

## 📋 Interview Questions & Answers

### Module 1 — Failure Modes

**Q1: What is the "Lost in the Middle" problem, and how do you fix it?**

> **A:** When you provide a long list of retrieved chunks to an LLM, the model pays disproportionately high attention to content at the *beginning* and *end* of the prompt. Information placed in the middle receives significantly less attention weight during generation. This is a property of how transformer attention works — tokens at the extremes have stronger gradient paths and priming effects.
>
> In a 10-chunk RAG pipeline, chunks 2-8 are effectively in a "dead zone." The retriever might have done a perfect job, but the LLM's answer will be biased toward the first and last chunks regardless.
>
> **Fixes:**
> - **Reranking + strategic ordering:** Put the most relevant chunk first, and the second-most relevant last. Bury the least relevant ones in the middle.
> - **Prompt compression (LLMLingua):** Remove low-value tokens to reduce total context size — less content means less "middle."
> - **Reduce K:** Retrieve fewer chunks with higher quality (better Precision@K), so the total context is manageable.

---

**Q2: Explain the difference between intrinsic and extrinsic hallucination. Why does the distinction matter for building evaluation systems?**

> **A:** Both are forms of hallucination, but they have fundamentally different causes and detection strategies.
>
> **Intrinsic hallucination**: The LLM contradicts the retrieved context directly. For example, the context says "200mg" and the LLM says "400mg." This is caused by the LLM's parametric weights (its pre-trained knowledge) overriding the contextual knowledge provided in the prompt. It is detectable using NLI (Natural Language Inference): if the LLM's claim is labeled CONTRADICTION against the retrieved context, you've found an intrinsic hallucination.
>
> **Extrinsic hallucination**: The LLM adds facts not mentioned anywhere in the context. These may or may not be true — the model could be correctly recalling something from its training data, or it could be fabricating. You can't determine which without an external fact-checking source. Detection requires either human review or an external knowledge graph.
>
> The distinction matters because they require different mitigations: intrinsic hallucinations respond to stronger context-grounding prompts and NLI-based filtering. Extrinsic hallucinations require citation requirements (forcing the LLM to cite specific chunk IDs for every claim) or domain fine-tuning to restrict output scope.

---

**Q3: Why do dense vector embeddings fail on logical negations? What is happening mathematically?**

> **A:** Dense embeddings work by projecting text into a high-dimensional vector space where semantically *related* text is placed close together. The model is trained to minimize the distance between semantically related text pairs.
>
> "How to format a hard drive" and "How to NOT format a hard drive" are about the same topic domain — hard drive formatting. The dominant semantic signal is the shared topic, not the negation. The embedding model was trained on millions of examples to bring topically-related text close together, and that training creates a strong attractor. The word "NOT" produces a small perturbation in the embedding, but the topic-based attractor is much stronger — so the two queries land very close in vector space.
>
> Mathematically: the cosine similarity between these two queries is often 0.85-0.95, even though they have opposite intent. The retriever cannot distinguish them.
>
> **Fix:** Hybrid search adds BM25, which operates on raw term frequencies. BM25 treats "NOT" as a literal token to match — it scores documents based on exact word presence and absence. Combined with dense retrieval, the hybrid system can catch cases where the semantics converge but the keywords diverge.

---

### Module 2 — IR Metrics

**Q4: What's the difference between Precision@K and Recall@K? When would you prioritize one over the other in a production RAG system?**

> **A:** They measure opposite aspects of retrieval quality.
>
> **Precision@K** measures signal-to-noise: of the K chunks retrieved, what fraction were genuinely relevant? High precision means the LLM gets clean, focused context. Low precision means the LLM must "find the needle in a haystack" of retrieved chunks — directly worsening generation quality and triggering the lost-in-the-middle problem.
>
> **Recall@K** measures coverage: of all the relevant chunks that exist in the entire database, what fraction made it into the top-K? High recall means you captured everything important. Low recall means important information was never given to the LLM — it simply cannot appear in the answer.
>
> **Prioritize Precision** in customer-facing chatbots and Q&A systems where noisy context directly degrades user experience.
>
> **Prioritize Recall** in high-stakes domains like legal, medical, or compliance, where missing a single relevant clause can have serious consequences. In these cases, it's better to send the LLM more context (even with some noise) than to risk missing a critical document.

---

**Q5: When would you choose NDCG over MRR as your primary retrieval metric?**

> **A:** Use MRR when you only pass the *top-1* retrieved result to the LLM, or when your use case has a binary relevant/irrelevant distinction. MRR answers "how fast does the retriever find any relevant result?"
>
> Use NDCG when: (1) you pass multiple chunks to the LLM (top-5, top-10), and you need to ensure the *best* chunks appear first — not just any relevant chunk; or (2) your domain has graded relevance (some chunks are perfect answers, others are partially related, others are tangential). NDCG's graded relevance scoring and positional discount make it more informative in both cases.
>
> For most multi-chunk RAG pipelines where retrieval order matters for the LLM's attention, NDCG is the more honest metric.

---

### Module 3 — Evaluation

**Q6: Why is BLEU/ROUGE inadequate for evaluating RAG systems?**

> **A:** BLEU and ROUGE were designed for machine translation and text summarization, where there's a known "reference" translation or summary. They work by counting n-gram (word sequence) overlap between the generated text and the reference.
>
> They fail for RAG for three reasons:
>
> 1. **Semantic insensitivity**: "The policy permits 14 days of remote work" and "Employees may work from home for up to two weeks" have zero word overlap but mean the same thing. BLEU would score this near zero despite being a correct answer.
>
> 2. **No groundedness check**: A fluent, well-phrased hallucination can score higher on BLEU than a correct but awkwardly worded grounded answer. BLEU has no mechanism to verify if facts are supported by context.
>
> 3. **Single reference assumption**: BLEU compares to a fixed reference answer. Open-ended generation has many valid phrasings and interpretations. The RAG Triad measures the *properties* of an answer (faithful? relevant? contextually complete?) rather than string similarity to one specific phrasing.

---

**Q7: Describe, step by step, how you would implement a faithfulness evaluation system from scratch without using an external library.**

> **A:**
> 1. **Take the LLM's complete answer** as input.
>
> 2. **Decompose into atomic claims**: Prompt a judge LLM to break the answer into individual, standalone factual statements — one claim per line. Each claim should be independently verifiable. For example, "The policy allows 14 days per quarter" and "Manager approval is required" are two separate atomic claims.
>
> 3. **For each claim, run NLI against the retrieved context**: Use a Natural Language Inference model (e.g., DeBERTa-based NLI). Feed it the retrieved context as the *premise* and each claim as the *hypothesis*. The model predicts ENTAILMENT, NEUTRAL, or CONTRADICTION.
>
> 4. **Classify the claim**: ENTAILMENT = grounded, NEUTRAL = potential extrinsic hallucination, CONTRADICTION = intrinsic hallucination.
>
> 5. **Compute the faithfulness score**: `(# ENTAILED claims) / (total # of claims)`. Optionally produce separate intrinsic and extrinsic hallucination rates.
>
> 6. **Log failed claims**: Any claim scoring CONTRADICTION or NEUTRAL should be logged with the trace ID for debugging — this tells you exactly *what* the LLM hallucinated and from which query.

---

### Module 4 — Test Engineering

**Q8: What is "test set evolution" in Ragas and why is it important?**

> **A:** Test set evolution is the process of taking simple factual Q&A pairs extracted from your documents and systematically mutating them into harder variants that stress-test different failure modes.
>
> Starting with a simple question ("What is the refund period?"), Ragas evolves it through multiple paths:
> - **Reasoning evolution**: Add calculation or inference ("If a product was bought Dec 28th, what is the last return date?")
> - **Multi-context evolution**: Require combining facts from multiple documents ("What is the refund policy for international customers who paid by credit card?")
> - **Conditional evolution**: Add conditions that change the answer ("What is the refund period if the item was on sale?")
>
> This matters because simple Q&A pairs can pass evaluation while the system fails in exactly the ways real users stress it. A system that scores 0.9 on simple questions might score 0.4 on multi-context questions — and real users ask multi-context questions constantly. Test set evolution ensures your benchmark reflects actual usage complexity.

---

### Module 5 — Observability

**Q9: A user reports that your RAG chatbot gave a dangerously wrong answer. Walk me through how you would use distributed tracing to diagnose the root cause.**

> **A:** With a tracing system like Arize Phoenix or LangSmith in place, each user query generates a unique trace ID logged alongside the response.
>
> 1. **Retrieve the trace**: Using the timestamp or the conversation ID, find the specific trace in the observability dashboard.
>
> 2. **Inspect the retrieval span**: Check which chunks were actually retrieved — their IDs, content, and cosine similarity scores. Was the relevant chunk retrieved at all? If not, the problem is a *retrieval failure* (wrong chunking, semantic compression mismatch, or query drift).
>
> 3. **Inspect the prompt assembly span**: View the exact prompt that was sent to the LLM — system prompt, all retrieved chunks in their actual order, and the user query. Was the most relevant chunk buried in the middle? Was the context too long?
>
> 4. **Inspect the generation span**: View the exact LLM output and the input/output token counts. Was the context window filled?
>
> 5. **Run post-hoc evaluation**: Feed the trace's (query, retrieved_chunks, answer) triple through your faithfulness checker. If faithfulness is low, the problem is in generation. If context precision/recall is low, the problem is in retrieval.
>
> This process typically diagnoses a production failure in under 10 minutes rather than hours of log parsing.

---

### Module 6 — Optimization

**Q10: Explain the two-stage retrieval pattern. Why can't you just use a cross-encoder for all retrieval?**

> **A:** Two-stage retrieval combines the speed of bi-encoder retrieval with the accuracy of cross-encoder reranking.
>
> **Stage 1 (bi-encoder, fast)**: The query is embedded into a vector, and cosine similarity is computed against pre-computed document embeddings. Because document embeddings are stored in advance, this step is essentially an approximate nearest-neighbor lookup — extremely fast regardless of database size. Returns 50-100 candidates.
>
> **Stage 2 (cross-encoder, accurate)**: The query and each candidate document are fed into the cross-encoder *together* as a single input. The model reads both simultaneously, capturing fine-grained relevance signals like term co-occurrence, entity overlap, and logical consistency. It produces a precise relevance score per (query, document) pair. The 50 candidates are re-sorted, and the top 5 go to the LLM.
>
> **Why not just cross-encoder throughout?** Cross-encoders have O(n) complexity at query time — every query must run inference against *every document* in the database. For a 1-million-document knowledge base, that's 1 million forward passes per query, taking minutes. Bi-encoders are fast because embeddings are pre-computed; the query-time work is just a vector similarity calculation. The two-stage design exploits the fast bi-encoder for broad candidate selection and reserves the slow, accurate cross-encoder for final re-ranking of a small candidate set.

---

**Q11: What is HyDE and when would you use it versus when would you avoid it?**

> **A:** HyDE (Hypothetical Document Embeddings) addresses the query-document embedding asymmetry. Queries are typically short, informal, and question-shaped. Documents are long, formal, and statement-shaped. Even when semantically aligned, they inhabit different regions of the embedding space.
>
> HyDE's fix: before retrieving, use an LLM to generate a *hypothetical answer document* — a paragraph written in the same style and language as the documents in your knowledge base. This hypothetical document is used as the retrieval query instead of the original question. Because it's document-shaped, it embeds much closer to the real answer documents.
>
> **Use HyDE when**: Queries are very short or conversational and your documents are dense technical text. When you observe low Recall@K despite having the right documents in the database — suggesting query-document mismatch.
>
> **Avoid HyDE when**: Latency is critical (it adds one full LLM inference call per query, typically 0.5-2s). When your queries are already long and document-like (e.g., users paste in paragraphs). When your LLM generates hypothetical documents that are systematically biased toward certain topics, causing retrieval to drift.

---

**Q12: What is embedding drift and what would your monitoring and response strategy be?**

> **A:** Embedding drift is the gradual divergence between the distribution of user queries your system was built and evaluated on, and the distribution of queries arriving in production over time. Products evolve, terminology changes, new user personas emerge — and the RAG system doesn't automatically adapt.
>
> It's insidious because your offline evaluation metrics don't capture it. Your test set was generated from your baseline query distribution. As queries drift, the test set becomes less representative, and your metrics stay green while real users experience degrading quality.
>
> **Detection strategy:**
> - Embed all incoming queries and log their vectors.
> - Nightly: compute the centroid of the last 7 days of queries.
> - Compare to your baseline centroid (from deployment day) using cosine distance.
> - Alert if drift > 0.15 (tune this threshold based on your domain volatility).
> - Also monitor: average cosine similarity scores on live queries (falling scores = retriever struggling with new query types), and user feedback rates.
>
> **Response strategy:**
> - Sample 100-200 recent queries where similarity scores were low or feedback was negative.
> - Run Ragas test set generation on any new or updated documents.
> - Evaluate the pipeline on the sampled drifted queries.
> - If the gap is large: update your knowledge base, re-evaluate your chunking strategy on the new content, and consider fine-tuning the embedding model on your domain.

---
