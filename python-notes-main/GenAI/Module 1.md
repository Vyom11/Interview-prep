# One-Day GenAI Master Revision Handbook
> Senior Engineer Edition | Rapid Revision | Interview + System Design Ready

---

# TOPIC 1: NLP Fundamentals

## 1. Executive Summary
- NLP = making machines understand, process, and generate human language
- Exists because language is unstructured; computers need structured representations
- Solves: tokenization, parsing, semantic understanding, generation
- Sits at the base of the GenAI stack — everything above depends on it
- Pre-transformer NLP: rule-based → statistical (TF-IDF, n-grams) → neural (RNNs, LSTMs)
- Transformers (2017) made NLP scalable, parallelizable, and context-aware
- Modern LLMs are the result of scaling transformer NLP to billions of parameters
- Core primitives: tokens, embeddings, attention, context windows
- Engineers care because: chunking strategy, tokenization costs, context limits, retrieval quality all trace to NLP fundamentals

## 2. Mental Model
- **Text as a number**: Language is discretized into tokens, tokens mapped to high-dimensional vectors
- **Analogy**: A library catalogue system — words are books, tokens are ISBNs, embeddings are GPS coordinates on a semantic map
- **Visual model**:
```
Raw Text → Tokenizer → Token IDs → Embedding Layer → Dense Vectors
"The cat sat" → [464, 3797, 3332] → [[0.2, -0.1, ...], ...]
```
- Meaning lives in the **geometry** of vector space — similar meanings cluster together

## 3. Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| Tokenization | Splitting text into sub-word units | Affects cost, context window, model behavior |
| Token | Atomic unit processed by the model (~4 chars for English) | Pricing unit for all LLM APIs |
| Embedding | Dense float vector representing semantic meaning | Foundation of search, RAG, similarity |
| Attention | Mechanism for each token to "attend" to others | Why transformers understand context |
| Context Window | Max tokens a model can process at once | Hard constraint in production systems |
| TF-IDF | Term frequency × inverse document frequency | Classic keyword relevance scoring |
| N-gram | Contiguous sequence of N tokens | Language modeling primitive |
| Stemming/Lemmatization | Reducing words to base form | Vocabulary normalization |
| Named Entity Recognition (NER) | Identifying entities (person, place, org) | Structured extraction |
| POS Tagging | Labeling words with grammatical roles | Parsing, understanding |
| BPE | Byte-Pair Encoding — subword tokenization algo | Used by GPT, RoBERTa |
| WordPiece | Google's subword tokenization | Used by BERT |
| Cosine Similarity | Angle between two vectors | Primary similarity metric |

## 4. Engineering Deep Dive

### How Tokenization Works Internally
```
Text: "ChatGPT is amazing!"
BPE Tokens: ["Chat", "G", "PT", " is", " amazing", "!"]
Token IDs: [14126, 38, 2577, 318, 4998, 0]
```
- BPE starts with characters, merges frequent pairs iteratively
- Vocabulary size: GPT-4 uses ~100K tokens, BERT uses ~30K
- **Critical**: "gpt-4" vs "GPT-4" → different token counts → different costs

### TF-IDF Formula
```
TF(t,d) = count of term t in document d / total terms in d
IDF(t) = log(N / df(t))   # N=total docs, df=docs containing t
TF-IDF(t,d) = TF(t,d) × IDF(t)
```

### Attention Mechanism (Simplified)
```
Q, K, V = linear projections of input embeddings
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```
- Q = "what I'm looking for"
- K = "what I have to offer"  
- V = "what I actually return"
- Multi-head: run attention H times with different projections, concatenate

### Important Libraries
| Library | Use Case |
|---------|----------|
| `tiktoken` | OpenAI tokenizer (count tokens) |
| `transformers` (HF) | Tokenizers, models, pipelines |
| `spaCy` | NLP pipelines (NER, POS, dep parsing) |
| `nltk` | Classic NLP primitives |
| `sentence-transformers` | Embedding generation |

### Performance Considerations
- Tokenization: fast, usually not a bottleneck
- Context window: quadratic attention cost O(n²) with sequence length
- Embeddings: fixed cost per document at indexing time; reused at query time
- BPE vs character tokenization: BPE is more efficient per token

### Cost Considerations
- LLM APIs charge per token (input + output)
- Counting tokens before API call: always use `tiktoken` or provider SDK
- Long contexts = expensive; chunk smartly

## 5. Architecture Perspective

### When to Use Classic NLP
- Keyword extraction, regex, entity detection on structured data
- When explainability is required
- When latency/cost constraints prevent LLM calls
- Preprocessing pipeline for RAG (cleaning, normalization)

### When NOT to Use Classic NLP
- Complex semantic understanding → use embeddings/LLMs
- Multilingual at scale → use multilingual transformer models
- Open-ended generation → LLMs only

### Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| Rule-based NLP | Fast, explainable, zero cost | Brittle, high maintenance |
| Statistical (TF-IDF) | Scalable, no GPU | No semantic understanding |
| Embedding models | Semantic, reusable | Requires GPU for training |
| LLM | Most capable | Expensive, slow, non-deterministic |

## 6. Failure Modes & Debugging

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Token count mismatch | Different tokenizer than model | Count with model's tokenizer | Always use `tiktoken` for OpenAI |
| Context overflow | Chunk too large, prompt too long | `context_length_exceeded` error | Hard truncation, sliding window |
| Tokenization artifacts | Punctuation, unicode | Garbled outputs | Normalize text pre-tokenization |
| Poor TF-IDF retrieval | Query terms not in docs | Low recall | Hybrid search (TF-IDF + embeddings) |
| Encoding errors | Non-UTF8 text | UnicodeDecodeError | Normalize to UTF-8 at ingestion |
| OOV tokens | Rare words split into many tokens | High token counts for rare terms | Accept or use character models |

## 7. End-to-End Flow
```
Raw Document
    ↓ (Text Extraction — Textract, pdfminer)
Clean Text
    ↓ (Normalization — lowercase, unicode fix, de-noise)
Normalized Text
    ↓ (Tokenization — BPE, WordPiece)
Token IDs
    ↓ (Embedding Model — BERT, sentence-transformers)
Dense Vectors [1536-dim or 768-dim]
    ↓ (Vector Store — OpenSearch, Pinecone, FAISS)
Indexed Corpus
```

## 8. Terminology Cheat Sheet

| Term | Meaning | Why It Matters |
|------|---------|---------------|
| BPE | Byte-Pair Encoding subword tokenizer | Used in GPT series |
| WordPiece | Google's subword tokenizer | Used in BERT |
| Perplexity | How well model predicts sample (lower=better) | LM evaluation metric |
| BLEU | Precision-based NLG eval metric | MT and summarization |
| ROUGE | Recall-based NLG eval metric | Summarization eval |
| Softmax | Converts logits to probability distribution | Output layer of classifiers |
| Logits | Raw unnormalized model outputs | Pre-softmax scores |
| Vocab Size | Number of distinct tokens | Affects model size, coverage |
| Padding | Adding special tokens to equalize batch lengths | Batching requirement |
| Truncation | Cutting sequence to fit context window | Hard context limit handling |

## 9. Comparison Tables

### TF-IDF vs Embeddings

| Aspect | TF-IDF | Embeddings |
|--------|--------|-----------|
| Representation | Sparse vector | Dense vector |
| Semantic understanding | No | Yes |
| Out-of-vocabulary | No (ignores) | Handles via subwords |
| Speed | Very fast | Requires inference |
| Interpretability | High | Low |
| Memory | Sparse → efficient | Dense → larger |
| Best for | Exact keyword match | Semantic search |

### Tokenizers Comparison

| Tokenizer | Used By | Vocab Size | Key Property |
|-----------|---------|-----------|-------------|
| BPE | GPT-2/3/4 | 50K-100K | Frequency-based merges |
| WordPiece | BERT | 30K | Likelihood-based merges |
| SentencePiece | T5, LLaMA | 32K+ | Language-agnostic |
| Unigram | XLNet | Variable | Probabilistic |

## 10. Interview Revision

### Top 10 Beginner Questions

**Q1: What is tokenization and why does it matter?**
- **Answer**: Splitting text into sub-word units that models process. Matters because it determines cost, context usage, and how well rare words are handled.
- **Expectation**: Understand BPE, know tokens ≠ words, know it's priced per token.
- **Mistake**: Confusing tokens with words (1 word ≈ 1.3 tokens on average for English).

**Q2: What is the difference between stemming and lemmatization?**
- **Answer**: Stemming chops suffixes heuristically ("running" → "run"). Lemmatization uses vocabulary to return base form ("ran" → "run").
- **Expectation**: Know when lemmatization is preferred (higher quality, slower).
- **Mistake**: Using stemming for semantic tasks → lossy.

**Q3: What is TF-IDF?**
- **Answer**: TF = how often term appears in doc; IDF = inverse of how many docs contain the term. Product = relevance score that rewards rare-but-present terms.
- **Expectation**: Know the formula, know it's the backbone of BM25 (used in ES/OpenSearch).

**Q4: What is cosine similarity?**
- **Answer**: cos(θ) = (A·B) / (|A||B|). Measures angle between vectors; 1 = identical direction, 0 = orthogonal.
- **Expectation**: Know why we use angle (not distance) — magnitude is irrelevant for meaning.
- **Mistake**: Using Euclidean distance for high-dimensional vectors (curse of dimensionality).

**Q5: What is attention mechanism?**
- **Answer**: Each token computes a weighted sum over all other tokens, where weights (attention scores) indicate how much each other token is relevant.
- **Expectation**: Understand Q/K/V roles. Know self-attention vs cross-attention.

**Q6: What is context window?**
- **Answer**: Max token length the model can process in one forward pass. Beyond this, information is lost.
- **Expectation**: Know production implications (chunking, cost, retrieval tradeoffs).

**Q7: How does BERT differ from GPT?**
- **Answer**: BERT = bidirectional encoder (sees full context both ways, good for understanding). GPT = causal decoder (left-to-right, good for generation).
- **Expectation**: Know the architectural difference, when to use each.

**Q8: What is Named Entity Recognition?**
- **Answer**: Classification of tokens into entity types (PERSON, ORG, LOC, DATE, etc.)
- **Expectation**: Know it's used in information extraction, query understanding.

**Q9: What is the difference between classification and generation?**
- **Answer**: Classification: input → fixed label. Generation: input → variable-length sequence.
- **Expectation**: Know sequence-to-sequence models bridge both.

**Q10: What is perplexity?**
- **Answer**: Measures how surprised a language model is by a test sequence. Lower = better. PP = 2^(cross_entropy).
- **Expectation**: Know it's a comparative metric, not absolute.

### Top 10 Intermediate Questions

**Q1: Explain multi-head attention.**
- **Answer**: Run attention H times in parallel with different learned projection matrices. Each head can attend to different parts of the sequence. Outputs concatenated and projected.
- **Expectation**: Know number of heads × head_dim = model_dim. GPT-3: 96 heads.

**Q2: What is the difference between encoder-only, decoder-only, and encoder-decoder models?**
- **Answer**: Encoder-only (BERT): bidirectional, embedding/classification. Decoder-only (GPT): autoregressive generation. Encoder-decoder (T5, BART): seq2seq tasks (translation, summarization).

**Q3: Why does chunking strategy matter for RAG?**
- **Answer**: Poor chunking breaks semantic units, degrades retrieval, and wastes context. Chunk too small: loses context. Too large: dilutes relevance and wastes tokens.
- **Expectation**: Know chunk_size, chunk_overlap, and semantic chunking strategies.

**Q4: How does BPE tokenization handle out-of-vocabulary words?**
- **Answer**: Splits into known subwords. "unhappiness" → ["un", "happiness"] or ["un", "happi", "ness"]. Falls back to individual characters in worst case.

**Q5: What is positional encoding and why is it needed?**
- **Answer**: Attention is permutation-invariant; it doesn't know word order. Positional encoding adds order information. Absolute (original BERT) or relative (RoPE, ALiBi).
- **Expectation**: Know RoPE (used by LLaMA) allows extrapolation to longer sequences.

**Q6: What are the implications of tokenizer mismatch in RAG?**
- **Answer**: If you count tokens with wrong tokenizer, chunks may exceed model's context limit, causing truncation and retrieval degradation. Always use model-specific tokenizer.

**Q7: Explain the curse of dimensionality in vector search.**
- **Answer**: As dimensions increase, distances between points converge. Nearest-neighbor becomes meaningless. Mitigated by HNSW, IVF indexing, and dimensionality reduction (PCA).

**Q8: What is BM25 and how does it compare to dense retrieval?**
- **Answer**: BM25 = probabilistic extension of TF-IDF with term saturation and document length normalization. Better than raw TF-IDF but still lexical. Dense retrieval: semantic. Hybrid = both.

**Q9: What is the difference between word2vec and sentence transformers?**
- **Answer**: word2vec: static per-word embeddings, no context ("bank" is same vector regardless of context). Sentence transformers: contextual, full-sequence embedding that captures meaning.

**Q10: How do you handle multilingual NLP?**
- **Answer**: mBERT, XLM-R, multilingual sentence transformers. LaBSE is strong for cross-lingual semantic similarity. Beware: some tokenizers are byte-level (SentencePiece), more efficient for non-Latin scripts.

### Top 10 Senior Engineer Questions

**Q1: You're seeing retrieval quality degrade over time in your RAG system. What do you investigate?**
- **Answer**: Check: (1) data drift — new docs with vocabulary not in embedding space, (2) chunking bugs after schema change, (3) embedding model version change, (4) index corruption, (5) query distribution shift. Add RAGAS metrics and monitor hit rate.

**Q2: How do you decide chunk size for a production RAG system?**
- **Answer**: Empirical — test RAGAS context_precision/recall at different sizes. Generally: 256-512 tokens for dense retrieval, 1024 for context-rich tasks. Add 10-20% overlap. Consider: document type, average query length, downstream context window size.

**Q3: Design a multilingual NLP pipeline that handles 50 languages with minimal latency.**
- **Answer**: Single multilingual embedding model (mE5-large or LaBSE) for semantic search. Language detection at ingestion (langdetect). Per-language text normalization. Shared vector index with language metadata filter. Translate only for LLM if needed (not at retrieval).

**Q4: How would you handle very long documents (100K+ tokens) in a RAG system?**
- **Answer**: Hierarchical chunking (coarse + fine), parent-child retrieval, summary-first indexing. Consider: map-reduce summarization, sliding window with positional overlap, or models with 200K+ context (GPT-4o, Claude 3).

**Q5: What are the tradeoffs between sparse and dense retrieval in production?**
- **Answer**: Sparse (BM25): fast, interpretable, exact keyword match, no GPU. Dense: semantic, generalization, needs embedding model. Hybrid is production standard. Reranking (cross-encoder) as final step for quality. Latency vs quality SLA drives the choice.

## 11. Senior Engineer Notes

| Dimension | Junior Focus | Senior Focus |
|-----------|-------------|-------------|
| Tokenization | How to use it | Cost implications, tokenizer choice |
| Embeddings | How to generate | Dimensionality, model selection, index strategy |
| Chunking | Fixed-size chunks | Semantic chunking, evaluation |
| Retrieval | cosine similarity | Hybrid, reranking, recall@k |
| Context | Fitting in context | Context budget allocation, cost optimization |

**Production Lessons:**
- Always instrument token counts — unexplained cost spikes = token count bugs
- Normalize text aggressively at ingestion: unicode, whitespace, encoding
- Test chunking strategy changes against held-out query set before deploying
- BM25 still beats dense retrieval on exact product codes, serial numbers, technical terms

## 12. One-Page Revision Sheet

### Must Know
- Tokenization: BPE, WordPiece; token ≠ word; ~4 chars/token
- Attention: Q/K/V; self-attention; multi-head
- TF-IDF vs Embeddings: sparse vs dense; keyword vs semantic
- Cosine similarity; context window limits

### Good To Know
- Positional encoding: absolute vs RoPE; why models extrapolate
- BM25: TF-IDF improvement; used in Elasticsearch
- Encoder-only vs decoder-only vs seq2seq tradeoffs
- Cross-encoder reranking for improved precision

### Expert Knowledge
- RoPE vs ALiBi for context extrapolation
- Subword tokenization internals (merge rules)
- Mixture of Experts and how it changes inference cost

### Interview Nuggets
- "Tokens ≠ words" catches many candidates off guard
- Always say "hybrid retrieval" for production
- Know why cosine > euclidean for high-dim vectors

### Architecture Nuggets
- Tokenizer must match the model (never mix)
- Chunk overlap prevents boundary information loss
- Hierarchical indexing for long documents

### Production Nuggets
- Use `tiktoken` to count tokens before API calls
- Monitor token distribution in production
- BM25 + dense = hybrid search standard

### Common Traps
- Forgetting chunking overlap → cut sentences at boundaries
- Using wrong tokenizer for token counting → context overflow
- Treating embeddings as immutable after retraining — must re-index

---

# TOPIC 2: LLM and Prompt Engineering

## 1. Executive Summary
- LLMs: large transformer models trained on internet-scale text to predict next tokens
- Prompt Engineering: designing input text to elicit desired model behavior
- Exists because LLMs are instruction-following generalists — behavior controlled by input
- Solves: how to extract reliable, structured, accurate outputs from probabilistic models
- Where it fits: sits above the model, below RAG/agents; everything relies on it
- Engineering concern: prompt quality directly determines system quality
- Key insight: LLMs are not databases; they don't retrieve — they synthesize
- Key risk: hallucination — confident wrong answers — mitigated by RAG and grounding
- Prompt engineering is not magic; it's systematic input engineering
- Production prompt engineering = version control + evaluation + iteration

## 2. Mental Model
- **LLM as next-token predictor**: At each step, model predicts probability distribution over vocabulary, samples from it
- **Analogy**: A very sophisticated autocomplete trained on all human knowledge
- **Prompt as program**: The prompt IS the source code; garbage in = garbage out
- **Temperature analogy**: Temperature = randomness dial. 0 = deterministic (pick highest probability token), 2 = chaotic (uniform sampling)

```
Prompt (System + User + Context)
    ↓
Token Embeddings
    ↓
N × Transformer Blocks (Attention + FFN)
    ↓
Logits (vocab_size)
    ↓
Softmax → Probability Distribution
    ↓
Sample/Argmax → Next Token
    ↓
Repeat until EOS
```

## 3. Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| System Prompt | Instructions defining model behavior/persona | Controls every response |
| User Prompt | Human's input | Contains the task |
| Few-Shot | Examples in prompt | Guides format/style/reasoning |
| Zero-Shot | No examples | Tests model's default behavior |
| Chain of Thought (CoT) | "Think step by step" | Improves reasoning accuracy |
| Temperature | Sampling randomness (0-2) | Controls creativity vs determinism |
| Top-p / Nucleus Sampling | Sample from top p% cumulative probability | Better than temperature alone |
| Max Tokens | Output length limit | Cost and latency control |
| Stop Sequences | Tokens that terminate generation | Structured output control |
| Hallucination | Confident but false output | #1 production risk |
| Grounding | Anchoring output to provided context | RAG's primary purpose |
| In-Context Learning | Learning from examples in the prompt | No fine-tuning required |
| RLHF | Reinforcement Learning from Human Feedback | How models are aligned |

## 4. Engineering Deep Dive

### How LLM Inference Works Internally
```
1. Tokenize prompt
2. Run tokens through N transformer layers
   - Each layer: Multi-Head Attention + FFN + LayerNorm
   - KV Cache: store past key/value pairs to avoid recomputation
3. Logits for next token
4. Sample using temperature/top-p
5. Append to sequence, repeat
```

### KV Cache — Critical for Production
- Caches key/value matrices for already-processed tokens
- Eliminates O(n²) recomputation for each new token
- Grows with sequence length: VRAM cost = `2 × layers × heads × head_dim × seq_len × precision`
- Shared prefix caching: if many calls share system prompt, cache it (Anthropic, OpenAI both support this → cost reduction)

### Prompt Engineering Patterns

**Pattern 1: Zero-Shot**
```
Classify the sentiment: "I love this product"
Answer: Positive
```

**Pattern 2: Few-Shot**
```
Text: "Great quality" → Positive
Text: "Terrible service" → Negative
Text: "I love this product" → ?
```

**Pattern 3: Chain of Thought**
```
Q: If there are 3 boxes with 4 apples each, how many apples total?
A: Let me think step by step. 3 boxes × 4 apples = 12 apples. Answer: 12
```

**Pattern 4: Structured Output**
```
Return ONLY valid JSON. No preamble. No markdown.
Schema: {"sentiment": "positive|negative|neutral", "confidence": 0.0-1.0}
```

**Pattern 5: Role/Persona**
```
You are a senior financial analyst. Answer only with data-backed facts.
Do not speculate. If uncertain, say "I don't know".
```

**Pattern 6: ReAct (Reason + Act)**
```
Thought: I need to find X
Action: search("X")
Observation: [result]
Thought: Now I can answer
Answer: ...
```

### Best Practices
1. Be explicit about format (JSON, markdown, numbered list)
2. Use negative examples ("Do NOT include preamble")
3. Set temperature=0 for deterministic tasks; 0.7-1.0 for creative
4. Add output validation — never trust LLM output directly
5. Version control prompts like code
6. Measure prompt performance with eval dataset
7. Use system prompt for stable instructions, user prompt for variable input
8. Add "Think step by step" for reasoning tasks
9. Use XML tags for complex prompt sections: `<context>`, `<task>`, `<format>`
10. Specify target audience: "Explain to a 5th grader" or "as a PhD"

### Important Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| temperature | 0-2 | 0=deterministic, 1=balanced, 2=random |
| top_p | 0-1 | 0.1=conservative, 0.9=diverse |
| max_tokens | 1-128K | Output length cap |
| frequency_penalty | 0-2 | Reduces repetition of tokens |
| presence_penalty | 0-2 | Encourages new topic introduction |

## 5. Architecture Perspective

### When to Use Prompt Engineering (vs Fine-Tuning)
- New task, limited data → prompt engineering first
- Need to change model behavior cheaply → system prompt
- Few-shot examples give good results → stay with prompting
- Need to inject proprietary knowledge → RAG, not fine-tuning

### When to Fine-Tune
- Consistent output style/format required at scale
- Specific domain vocabulary (legal, medical)
- Cost: 10K+ calls/day at high token count → fine-tuning cheaper
- Latency: smaller fine-tuned model can beat prompting larger model

### Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| Prompt Engineering | Fast, zero training cost, flexible | Fragile, prompt injection risk |
| Few-Shot | Improves output quality | Consumes context window |
| Fine-Tuning | Consistent quality, lower cost at scale | Expensive to train, less flexible |
| RAG | Fresh data, grounded | Extra infrastructure |
| CoT | Better reasoning | Longer output, more tokens, more cost |

## 6. Failure Modes & Debugging

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Hallucination | Model generates plausible-sounding false info | Fact-checking eval, RAGAS faithfulness | RAG grounding, reduce temperature |
| Prompt injection | User input overrides system prompt | Red team testing | Input sanitization, output filtering |
| Inconsistent format | Model ignores format instructions | Output parsing errors | Few-shot examples + strict schema |
| Verbose/padded output | Model adds unnecessary preamble | Response parsing | "Return ONLY X, no preamble" |
| Instruction following failure | Ambiguous instructions | Manual review | Clearer wording, negative examples |
| Context bleed | Earlier examples bias later outputs | Eval on fresh sessions | Clear context boundaries |
| Jailbreak | Adversarial prompts bypass safety | Red teaming | Input/output guardrails |
| Token limit exceeded | Long prompts + long outputs | `max_tokens` error | Truncate, summarize, chunk |

## 7. End-to-End Flow
```
User Request
    ↓
Prompt Template (system + user + few-shot)
    ↓
Context Injection (from RAG or tool calls)
    ↓
Token Count Check (≤ context limit)
    ↓
LLM API Call (temperature, max_tokens, stop sequences)
    ↓
Raw Response
    ↓
Output Parser (JSON, regex, Pydantic)
    ↓
Validation (schema check, hallucination guard)
    ↓
Final Response
```

## 8. Terminology Cheat Sheet

| Term | Meaning | Why It Matters |
|------|---------|---------------|
| Instruction Tuning | Fine-tuning on instruction-response pairs | How chat models are trained |
| RLHF | Human feedback shapes reward model used in PPO | Alignment technique |
| DPO | Direct Preference Optimization | Simpler RLHF alternative |
| Quantization | Reducing model precision (FP16→INT8) | Cost/speed vs quality tradeoff |
| PEFT / LoRA | Parameter-efficient fine-tuning | Cheap fine-tuning method |
| Prompt Injection | Malicious input overrides system instructions | #1 security risk in LLM apps |
| System Prompt Leaking | Extracting confidential system prompts | Security concern |
| Token Budget | Max tokens allocated for a call | Cost control primitive |
| Softmax Temperature | Sharpens/flattens probability distribution | Sampling control |
| Beam Search | Keep top K sequences during generation | Alternative to sampling |
| Greedy Decoding | Always pick highest probability token | Deterministic but suboptimal |
| Self-Consistency | Sample multiple CoT paths, vote on answer | Improves reasoning accuracy |

## 9. Comparison Tables

### GPT (Decoder-Only) vs BERT (Encoder-Only)

| Aspect | GPT / Decoder-Only | BERT / Encoder-Only |
|--------|-------------------|---------------------|
| Direction | Left-to-right (causal) | Bidirectional |
| Pretraining | Next token prediction | Masked Language Model |
| Best for | Text generation, chat | Classification, embeddings |
| Context | Past tokens only | Full sequence |
| Examples | GPT-4, LLaMA, Claude | BERT, RoBERTa, DistilBERT |

### Fine-Tuning vs RAG vs Prompt Engineering

| Aspect | Prompt Engineering | RAG | Fine-Tuning |
|--------|-------------------|-----|-------------|
| Training cost | Zero | Zero | High |
| Latency | Low | Medium | Low |
| Knowledge freshness | Base model only | Fresh | Stale after training |
| Data requirement | None | Corpus | Labeled pairs |
| Best for | General tasks | Domain knowledge | Style/behavior |
| Hallucination risk | High | Low (with grounding) | Medium |

## 10. Interview Revision

### Top 10 Beginner Questions

**Q1: What is temperature in LLMs?**
- **Answer**: Scales the logits before softmax. Low = peaked distribution = deterministic. High = flat = random. Production: 0 for structured tasks, 0.7 for chat, 1.0+ for creative.
- **Mistake**: Thinking temperature = accuracy. Low temp = consistent, not necessarily correct.

**Q2: What is few-shot prompting?**
- **Answer**: Including examples of input-output pairs in the prompt to guide model behavior.
- **Expectation**: Know it's in-context learning — no weights are updated.

**Q3: What are system prompts?**
- **Answer**: Instructions given to the model before the user message, defining behavior, persona, constraints. More persistent than user prompts.

**Q4: What is hallucination?**
- **Answer**: Model generates factually incorrect information with high confidence. Root cause: LLMs are trained to produce plausible sequences, not factual ones.

**Q5: What is Chain of Thought prompting?**
- **Answer**: Instructing model to reason step by step before answering. "Let's think step by step." Dramatically improves multi-step reasoning.

### Top 10 Senior Engineer Questions

**Q1: How do you prevent prompt injection in production?**
- **Answer**: Input sanitization (strip/escape special tokens), separate user input from instructions structurally, output filtering, don't pass raw user input to system prompt, use structured APIs where possible.

**Q2: How do you version control and evaluate prompts?**
- **Answer**: Store prompts in git-tracked config files or LangSmith/LangFuse. Eval dataset with golden answers. Regression testing on prompt changes. A/B test in production with metrics.

**Q3: Design a reliable structured output pipeline.**
- **Answer**: Prompt specifies strict JSON schema → parse response → validate with Pydantic → retry with error message if invalid → fallback to default. Use function calling/JSON mode if available (OpenAI, Anthropic).

**Q4: How do you optimize LLM cost in production?**
- **Answer**: Prompt caching (shared prefix), model routing (cheap model for simple tasks), caching deterministic responses (Redis), reduce max_tokens, trim context aggressively, batch requests, move to smaller fine-tuned model for high-volume tasks.

**Q5: What's the difference between self-consistency and majority voting?**
- **Answer**: Same thing — sample N CoT responses, take majority vote on final answer. Improves reasoning by 5-15% at 3-5x cost.

## 11. Senior Engineer Notes

**What juniors focus on**: Making prompt work once.
**What seniors focus on**: 
- Prompt reliability at scale (edge cases, adversarial inputs)
- Cost per call and cost per user
- Evaluation pipelines (not vibes)
- Prompt versioning and rollback capability
- Graceful degradation when LLM fails or is slow

**Production Lessons:**
- Add retry logic with backoff — LLM APIs have transient failures
- Never parse JSON with regex — use `json.loads` with try/catch
- Always cap `max_tokens` — runaway generations burn budget
- Log all inputs/outputs (appropriately redacted) for debugging

## 12. One-Page Revision Sheet

### Must Know
- Temperature=0 for deterministic, 0.7 for balanced, 1+ for creative
- Zero-shot vs few-shot vs CoT — when to use each
- Hallucination mitigation: RAG + grounding + output validation
- Prompt injection: #1 security risk

### Good To Know
- KV cache mechanics and shared prefix caching for cost reduction
- Self-consistency sampling for reasoning
- JSON mode / function calling for structured outputs

### Expert Knowledge
- RLHF vs DPO for alignment
- LoRA/QLoRA for cheap fine-tuning
- Speculative decoding for latency optimization

### Interview Nuggets
- "Prompt engineering is not magic — it's systematic input engineering with evaluation"
- Always mention evaluation when discussing prompts
- Mention cost optimization (caching, model routing) to signal seniority

### Architecture Nuggets
- Separate system prompt (stable) from user prompt (variable) for caching
- Validate LLM output at runtime — never trust it blindly
- Route easy queries to cheaper/faster models

### Production Nuggets
- Version prompts in config files, not code strings
- Eval dataset before and after every prompt change
- Monitor output token distribution — cost anomaly detection

### Common Traps
- Not handling LLM output parsing failures → system crashes
- Forgetting to set `max_tokens` → runaway cost
- Trusting LLM JSON output without validation

---

# TOPIC 3: AWS Services (Bedrock, S3, Textract, SageMaker, OpenSearch)

## 1. Executive Summary
- AWS provides managed infrastructure for the entire GenAI stack
- Bedrock: managed LLM API service — access to Anthropic, Mistral, Meta, Cohere, etc.
- S3: scalable object storage — the universal data lake for GenAI pipelines
- Textract: managed OCR + document intelligence (tables, forms, handwriting)
- SageMaker: end-to-end ML platform (training, hosting, pipelines, feature store)
- OpenSearch: managed search and analytics — primary vector DB choice in AWS ecosystem
- These services form the backbone of enterprise GenAI on AWS
- Why engineers care: avoid undifferentiated heavy lifting; managed = less ops, more product

## 2. Mental Model
- **Bedrock** = LLM API gateway (like OpenAI but with multiple models + AWS integrations)
- **S3** = infinite hard drive for everything in the pipeline
- **Textract** = smart scanner that understands document structure
- **SageMaker** = ML factory — from raw data to deployed model
- **OpenSearch** = search engine with superpowers (vector + keyword + aggregations)

```
Raw Documents (S3)
    ↓ Textract (OCR, structure)
    ↓ SageMaker (processing, embedding)
    ↓ OpenSearch (indexing, retrieval)
    ↓ Bedrock (generation)
    → Answer
```

## 3. Core Concepts

### Bedrock
| Concept | Detail |
|---------|--------|
| Model IDs | `anthropic.claude-3-5-sonnet-20241022-v2:0` |
| Converse API | Unified API across all models |
| Knowledge Bases | Managed RAG pipeline on Bedrock |
| Agents | Tool-calling framework on Bedrock |
| Guardrails | Content filtering (PII, topics, grounding) |
| Provisioned Throughput | Reserved capacity; needed for production SLAs |
| On-demand | Pay per token; no reservation |

### S3
| Concept | Detail |
|---------|--------|
| Bucket | Namespace for objects |
| Object Key | Unique identifier (path-like: `docs/2024/file.pdf`) |
| Storage Classes | Standard, IA, Glacier — cost vs access speed |
| Versioning | Store all versions of an object |
| Event Notifications | Trigger Lambda on PutObject → ingestion pipeline |
| Presigned URLs | Temp access URL (used for secure file upload/download) |
| S3 Select | SQL on S3 objects — avoid full download |

### Textract
| Concept | Detail |
|---------|--------|
| DetectDocumentText | Raw OCR (blocks, lines, words) |
| AnalyzeDocument | Forms (key-value pairs), Tables |
| AnalyzeExpense | Invoice/receipt specific extraction |
| StartDocumentAnalysis | Async for large documents |
| Confidence scores | Per-block confidence → filter low-quality extractions |
| Query API | Ask questions about documents directly |

### SageMaker
| Concept | Detail |
|---------|--------|
| Training Jobs | Managed distributed training |
| Endpoints | Real-time inference hosting |
| Batch Transform | Offline/bulk inference |
| Pipelines | MLOps workflow automation |
| Feature Store | Centralized feature management |
| JumpStart | Pre-trained model hub (fine-tune in 1 click) |
| SageMaker Studio | IDE for ML development |

### OpenSearch
| Concept | Detail |
|---------|--------|
| Index | Collection of documents (like a table) |
| Mapping | Schema definition for fields |
| k-NN plugin | Vector similarity search (HNSW, IVF) |
| BM25 | Default text relevance scoring |
| Hybrid Search | BM25 + k-NN combined |
| Aggregations | Analytics on search results |
| ISM Policies | Automated index lifecycle management |

## 4. Engineering Deep Dive

### Bedrock: Making API Calls
```python
import boto3
client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.converse(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    messages=[{"role": "user", "content": [{"text": "Hello"}]}],
    system=[{"text": "You are a helpful assistant."}],
    inferenceConfig={"maxTokens": 1000, "temperature": 0}
)
text = response["output"]["message"]["content"][0]["text"]
```

### S3: Ingestion Pipeline Pattern
```python
# Trigger: S3 Event → Lambda → Process Document
import boto3
s3 = boto3.client('s3')

# Read object
obj = s3.get_object(Bucket='my-bucket', Key='docs/file.pdf')
content = obj['Body'].read()

# List all PDFs
paginator = s3.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket='my-bucket', Prefix='docs/'):
    for obj in page.get('Contents', []):
        process(obj['Key'])
```

### Textract: Document Processing
```python
import boto3
textract = boto3.client('textract')

# Synchronous (< 10 pages)
response = textract.detect_document_text(
    Document={'S3Object': {'Bucket': 'my-bucket', 'Name': 'doc.pdf'}}
)

# Async (large docs)
job = textract.start_document_analysis(
    DocumentLocation={'S3Object': {'Bucket': 'my-bucket', 'Name': 'doc.pdf'}},
    FeatureTypes=['TABLES', 'FORMS']
)
# Poll with GetDocumentAnalysis using job['JobId']
```

### OpenSearch: Vector Search
```python
from opensearchpy import OpenSearch

client = OpenSearch(hosts=[{'host': 'endpoint', 'port': 443}], http_auth=('user', 'pass'))

# Create vector index
client.indices.create(index='docs', body={
    'mappings': {
        'properties': {
            'content': {'type': 'text'},
            'embedding': {'type': 'knn_vector', 'dimension': 1536,
                         'method': {'name': 'hnsw', 'space_type': 'cosine'}}
        }
    },
    'settings': {'index': {'knn': True}}
})

# k-NN search
query = {
    'query': {
        'knn': {'embedding': {'vector': query_vector, 'k': 10}}
    }
}
```

### Best Practices

**Bedrock:**
- Use Provisioned Throughput for production SLAs (on-demand has rate limits)
- Enable guardrails for PII, topic restrictions, grounding
- Use streaming for chatbot applications
- Cache responses for deterministic queries (DynamoDB TTL)

**S3:**
- Enable versioning for document corpora
- Use S3 lifecycle policies to move old docs to Glacier
- Structure keys for efficient listing: `{domain}/{year}/{month}/{doc_id}.pdf`
- Enable server-side encryption (SSE-S3 or SSE-KMS)

**OpenSearch:**
- Choose HNSW for real-time; IVF for large offline indices
- Set `ef_construction=512, m=16` for high recall HNSW
- Use Index State Management to manage hot/warm/cold tiers
- Monitor JVM heap usage — primary failure mode

## 5. Architecture Perspective

### AWS GenAI Reference Architecture
```
User Request
    ↓
API Gateway
    ↓
Lambda / ECS
    ↓ ←────────────────────────────────────────
Bedrock (LLM)          OpenSearch (Vector DB)
    ↑                          ↑
S3 (raw docs) → Textract → SageMaker (embed) → OpenSearch (index)
```

### Build vs Buy

| Component | Build (Self-managed) | Buy (AWS Managed) |
|-----------|---------------------|------------------|
| LLM inference | EC2 GPU (expensive, flexible) | Bedrock (easy, less control) |
| Vector DB | Self-managed OpenSearch / Qdrant | OpenSearch Service |
| Document OCR | Tesseract on Lambda | Textract |
| Model training | EC2 + DL AMIs | SageMaker |

**Enterprise consideration**: Bedrock has VPC endpoints → data never leaves AWS network → compliance-friendly.

**Startup consideration**: Use Bedrock on-demand → zero upfront, pay as you grow.

## 6. Failure Modes & Debugging

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Bedrock throttling | Exceeded on-demand rate limits | ThrottlingException | Exponential backoff + Provisioned Throughput |
| Textract timeout | Large document sync call | TimeoutError | Use async API for >5 pages |
| OpenSearch OOM | Large k-NN index in JVM heap | JVM heap > 85% | Increase instance size, use Faiss engine |
| S3 429 errors | >3500 PUT/s to same prefix | HTTP 429 | Randomize key prefixes |
| Bedrock model not available | Region/model mismatch | 404 error | Check model availability per region |
| SageMaker endpoint cold start | Auto-scaling to zero | High first-request latency | Keep min instances = 1 |
| OpenSearch split-brain | Network partition in cluster | Cluster health = RED | Use dedicated master nodes |

## 7. End-to-End Flow
```
Document Upload to S3
    ↓
S3 Event → Lambda
    ↓
Textract (extract text, tables, forms)
    ↓
Text Cleaning + Chunking
    ↓
Bedrock / SageMaker Embedding Model
    ↓
OpenSearch: Index chunks with embeddings
    ↓
[Query Time]
User Query → Embed (Bedrock) → k-NN Search (OpenSearch) → Top K chunks
    ↓
Prompt + Chunks → Bedrock LLM → Response
```

## 8. Terminology Cheat Sheet

| Term | Meaning | Why It Matters |
|------|---------|---------------|
| Provisioned Throughput | Reserved Bedrock capacity | Production SLA requirement |
| Cross-Region Inference | Bedrock routes to available region | Higher throughput, failover |
| VPC Endpoint | Private connectivity to AWS services | Data compliance |
| S3 SSE-KMS | Server-side encryption with KMS | Compliance requirement |
| OpenSearch HNSW | Hierarchical Navigable Small World graph | Default ANN index |
| k-NN | k-Nearest Neighbor search | Vector similarity retrieval |
| ISM | Index State Management (OpenSearch) | Automated index lifecycle |
| Textract FeatureType | TABLES, FORMS, SIGNATURES, LAYOUT | Controls extraction types |
| SageMaker Endpoint | Real-time inference HTTP endpoint | How you call deployed models |

## 9. Comparison Tables

### OpenSearch vs Alternatives for Vector Search

| Aspect | OpenSearch | Pinecone | Weaviate | FAISS |
|--------|-----------|---------|---------|-------|
| Type | Managed search + vector | Managed vector-only | Open source / managed | Library (in-memory) |
| Hybrid search | Yes (BM25 + k-NN) | Limited | Yes | No (pure vector) |
| AWS native | Yes | No | No | Can embed in Lambda |
| Operational overhead | Low (managed) | Zero | Medium | High |
| Cost | By instance size | By vectors + reads | By instance | Free |
| Filtering | Rich (aggregations) | Limited | GraphQL | Limited |

## 10. Interview Revision

### Top 10 Senior Engineer Questions

**Q1: How do you design a cost-efficient document processing pipeline on AWS?**
- **Answer**: S3 for raw storage → SQS queue for async processing → Lambda for small docs, Fargate for large → Textract async API → embedding batch job in SageMaker → bulk index to OpenSearch. Cost controls: S3 lifecycle policies, Lambda right-sizing, Bedrock token budgets.

**Q2: How do you handle Bedrock rate limiting in production?**
- **Answer**: Implement exponential backoff with jitter. Use Provisioned Throughput for stable workloads. Distribute load across Cross-Region Inference. Queue requests with SQS for burst absorption.

**Q3: How do you ensure data doesn't leave your AWS account when using Bedrock?**
- **Answer**: Use VPC endpoints for Bedrock (no public internet traffic). IAM policies restrict API calls. Bedrock models don't train on your data by default. Audit with CloudTrail.

**Q4: How do you scale OpenSearch for 100M+ vector documents?**
- **Answer**: Multi-node cluster with dedicated master. Shard strategy: each shard 10-50GB. Use IVF (not HNSW) for extreme scale — approximates better under memory pressure. Cold/warm architecture with ISM.

## 11. Senior Engineer Notes

**Junior**: "Let me use Bedrock to call the LLM."
**Senior**: "What's our Provisioned Throughput strategy? Are we within VPC? What's our retry budget? How are we monitoring per-model latency and cost?"

**Production Lessons:**
- OpenSearch HNSW index lives in JVM heap — this is the #1 operational gotcha
- Textract returns bounding box data — use it for document highlighting in UI
- S3 key design affects listing performance — avoid timestamp-prefixed keys

## 12. One-Page Revision Sheet

### Must Know
- Bedrock: managed multi-model LLM API; Converse API; Provisioned Throughput for prod
- S3: universal storage; event notifications for ingestion pipelines; SSE-KMS for compliance
- Textract: async for large docs; FeatureTypes for tables/forms
- OpenSearch: k-NN plugin (HNSW/IVF); hybrid search; JVM heap watch

### Interview Nuggets
- VPC endpoints = data compliance in Bedrock
- HNSW in JVM heap = primary OpenSearch scaling failure
- Cross-Region Inference = high availability for Bedrock

### Production Nuggets
- S3 key structure affects performance at scale
- OpenSearch: HNSW for fresh index, IVF for large offline
- Textract async for anything > 5 pages

### Common Traps
- Using Bedrock on-demand for sustained high traffic → throttled
- Forgetting Textract async vs sync limits
- OpenSearch JVM heap sizing for vector workloads

---

# TOPIC 4: Sentence Embeddings & Similarity Search

## 1. Executive Summary
- Sentence embeddings: fixed-size dense vectors representing semantic meaning of text
- Enable machines to measure "how similar" two pieces of text are
- Solves: semantic search (find meaning, not just keywords), clustering, dedup, classification
- Where it fits: the bridge between raw text and vector databases
- Why engineers care: embedding model choice determines retrieval quality ceiling
- Key insight: quality of embeddings directly sets the upper bound on RAG performance
- Modern embeddings (OpenAI, E5, BGE) capture nuance, context, cross-lingual meaning
- Embeddings are reusable — compute once, query forever
- Dimensionality vs quality tradeoff is a core production decision

## 2. Mental Model
- **Embeddings = GPS coordinates for meaning** — semantically similar text → nearby coordinates
- **Analogy**: Map of a city where neighborhoods cluster by similarity (restaurants near restaurants, hospitals near hospitals)
- **Intuition**: "The bank by the river" and "A financial bank" → different coordinates despite sharing "bank"

```
Text Input
    ↓
Transformer Encoder (process all tokens simultaneously)
    ↓
[CLS] token OR mean pooling of all token embeddings
    ↓
Optional: normalize to unit sphere (for cosine = dot product)
    ↓
Dense Vector [1536-dim]

"The cat sat"  →  [0.2, -0.1, 0.8, ...]  ← nearby to →
"The kitty rested" → [0.21, -0.09, 0.79, ...]
```

## 3. Core Concepts

| Concept | Definition |
|---------|-----------|
| Embedding | Dense float vector representing semantic content |
| Dimensionality | Vector size (384, 768, 1536, 3072) |
| Pooling | How to get single vector from token embeddings (CLS, mean, max) |
| Normalization | Scale to unit sphere — makes cosine similarity = dot product |
| Bi-encoder | Encode query and document independently — fast, scalable |
| Cross-encoder | Encode query+document together — slow but accurate |
| ANN | Approximate Nearest Neighbor — fast approximate retrieval |
| Exact NN | Brute force — exact but O(n×d) |
| HNSW | Hierarchical Navigable Small World — dominant ANN algorithm |
| IVF | Inverted File Index — cluster-based ANN |
| Recall@k | Fraction of true top-k found by ANN | Core retrieval metric |
| MRR | Mean Reciprocal Rank | Ranking quality metric |

## 4. Engineering Deep Dive

### Popular Embedding Models

| Model | Dim | Max Tokens | Notes |
|-------|-----|-----------|-------|
| OpenAI `text-embedding-3-small` | 1536 | 8191 | Cheap, good quality |
| OpenAI `text-embedding-3-large` | 3072 | 8191 | Best OpenAI quality |
| `BAAI/bge-large-en-v1.5` | 1024 | 512 | Best open-source for English |
| `intfloat/e5-large-v2` | 1024 | 512 | Strong multilingual |
| `sentence-transformers/all-MiniLM-L6-v2` | 384 | 256 | Tiny, fast, decent |
| Cohere `embed-english-v3.0` | 1024 | 512 | Excellent, managed |
| Amazon Titan `amazon.titan-embed-text-v2:0` | 1024 | 8192 | AWS native |

### Generating Embeddings
```python
# Using sentence-transformers
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-large-en-v1.5')
embeddings = model.encode(["text1", "text2"], normalize_embeddings=True)

# Using OpenAI
from openai import OpenAI
client = OpenAI()
response = client.embeddings.create(model="text-embedding-3-small", input=["text1"])
vector = response.data[0].embedding

# Using Bedrock (Titan)
bedrock = boto3.client('bedrock-runtime')
response = bedrock.invoke_model(
    modelId='amazon.titan-embed-text-v2:0',
    body=json.dumps({"inputText": "text", "dimensions": 1024})
)
```

### HNSW Algorithm (Conceptual)
- Builds a multi-layer graph; top layers are coarse, bottom layers are fine
- Search: enter at top layer, greedily navigate to nearest neighbor, descend layers
- Parameters: `m` (connections per node), `ef_construction` (build quality), `ef_search` (query quality)
- Higher m/ef = higher recall, more memory/time

### ANN vs Exact Search

| Aspect | Exact NN (brute force) | ANN (HNSW/IVF) |
|--------|----------------------|----------------|
| Recall | 100% | 90-99% |
| Latency | O(n×d) | O(log n) or O(d√n) |
| Memory | Low | Higher (index structures) |
| Use case | < 100K vectors | > 100K vectors |

### Reranking Pipeline
```
Query → Bi-encoder → Top 100 candidates (fast)
    ↓
Cross-encoder → Rerank top 100 → Return top 5 (slow but accurate)
```
- Cross-encoder attends to both query and document together → much better relevance
- Typical models: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Latency: add 50-200ms for reranking 100 docs

## 5. Architecture Perspective

### When to Use Bi-Encoder
- Real-time retrieval from large corpus (10K-10M+ documents)
- Latency < 100ms requirement
- Encode documents once, store; query at runtime

### When to Use Cross-Encoder
- High-precision reranking of small candidate set
- Quality is critical (legal, medical)
- Acceptable: adding 100-200ms latency after initial retrieval

### Trade-offs

| Decision | Option A | Option B |
|----------|----------|----------|
| Embedding dim | High (3072): better quality, more memory | Low (384): faster, cheaper |
| Pooling | CLS: faster | Mean: generally better quality |
| Normalization | Always normalize for cosine similarity | |
| Model | Proprietary (OpenAI): easier, API cost | Open-source: self-host, one-time cost |

## 6. Failure Modes & Debugging

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Embedding mismatch | Query/doc embedded with different models | Inconsistent retrieval | Always use same model for both |
| Stale embeddings | Doc updated, embedding not refreshed | Retrieval returns outdated content | Event-driven re-embedding on update |
| Dimension mismatch | Model changed, old embeddings remain | IndexError or silent wrong results | Migration job when changing models |
| Low recall | ANN index parameters too aggressive | recall@k metric drops | Increase ef_search, rebuild index |
| OOM on embedding batch | Too large batch size | CUDA OOM | Batch size 32-64, use CPU for offline |
| Slow embedding at query time | Large model, no batching | High latency | Use smaller model or cache embeddings |

## 7. End-to-End Flow
```
Document Text
    ↓
Chunking (256-512 tokens, 20% overlap)
    ↓
Embedding Model (bi-encoder)
    ↓
Dense Vectors [dim × n_chunks]
    ↓
ANN Index (HNSW/IVF) in Vector DB
    ↓
[Query Time]
User Query → Embed → ANN Search → Top 100
    ↓
Cross-Encoder Reranker → Top 5
    ↓
RAG Context
```

## 8. Terminology Cheat Sheet

| Term | Meaning | Why It Matters |
|------|---------|---------------|
| Bi-encoder | Separate encoding of query and doc | Enables pre-computation |
| Cross-encoder | Joint encoding of query+doc | High-quality reranking |
| Pooling | How token embeddings → single vector | Quality impact |
| ef_construction | HNSW build quality parameter | Index recall |
| ef_search | HNSW query quality parameter | Query recall vs speed |
| Matryoshka Embeddings | Embeddings that work at any truncated dimension | Flexible dim choice |
| Recall@k | Top k retrieval accuracy | Retrieval quality metric |
| MTEB | Benchmark for embedding models | Model selection guide |

## 9. Comparison Tables

### Embedding Model Comparison

| Model | Quality | Cost | Latency | Self-hostable |
|-------|---------|------|---------|--------------|
| OpenAI 3-large | Excellent | Per API call | Low | No |
| BGE-Large | Very Good | Free | Medium | Yes |
| All-MiniLM-L6 | Good | Free | Very Low | Yes |
| Cohere v3 | Excellent | Per API call | Low | No |
| Titan Embed v2 | Good | Per API call (Bedrock) | Low | No |

## 10. Interview Revision

### Senior Questions

**Q1: How do you handle embedding model changes in production without downtime?**
- **Answer**: Shadow indexing — build new index in parallel. Run dual-read (compare results). Once validated, atomic swap. Keep old index for rollback. Implement as blue/green deployment.

**Q2: How do you evaluate embedding quality for your domain?**
- **Answer**: Create a domain-specific eval set: 100-200 query-document relevance pairs. Compute Recall@5, Recall@10, MRR. Compare models on MTEB and on your eval set (MTEB may not reflect domain-specific performance).

**Q3: Explain Matryoshka Representation Learning (MRL).**
- **Answer**: Training that makes embeddings useful at any prefix dimension. OpenAI 3-small supports 512/1536 dim. Smaller dim = faster search, less memory, small quality loss. Useful for tiered architectures.

## 12. One-Page Revision Sheet

### Must Know
- Bi-encoder (fast) vs cross-encoder (accurate) — use both in pipeline
- HNSW: ANN algorithm; ef_search controls recall vs latency
- Always same model for query and document embedding

### Interview Nuggets
- Mention reranking pipeline (bi-encoder + cross-encoder) to show depth
- Recall@k is the metric that matters
- Model changes require full re-index

### Production Nuggets
- Normalize embeddings for cosine = dot product (faster)
- Batch embedding at ingestion; single embed at query time
- Monitor recall@k in production with sampled labels

---
