# 🧠 Ultimate GenAI Revision Cheat Sheet
### Beginner → Senior GenAI Engineer | Last-Minute Interview Prep | Production AI Systems

---

> **How to use this guide:** Each topic follows the same 16-section structure. Use the Knowledge Ladder to self-assess. Jump to "Ultimate Revision Sheet" per topic for 30-min reviews.

---

# PART 1: FOUNDATIONS

---

# Topic 1: Text Preprocessing & NLP Basics

## 1. Executive Summary
- Raw text is noisy, inconsistent, and unstructured — models can't consume it directly
- Preprocessing converts text → clean, normalized, machine-consumable tokens
- **Problem solved:** Vocabulary explosion, noise, ambiguity, linguistic variation
- Tokenization splits text into units (characters, subwords, words, sentences)
- Normalization: lowercasing, stemming, lemmatization, punctuation removal
- Stopword removal reduces noise but can remove signal (context-dependent)
- Named Entity Recognition (NER) extracts structured entities from unstructured text
- Part-of-Speech (POS) tagging provides grammatical context
- In LLM era: subword tokenization (BPE/WordPiece) replaced classical preprocessing for neural models
- Classical NLP preprocessing still relevant for: search indexing, feature engineering, data cleaning pipelines

## 2. Mental Model
> "Text preprocessing is like cleaning raw vegetables before cooking. You wash (normalize), chop (tokenize), remove inedible parts (stopwords), and categorize (POS/NER) — all before the actual recipe (model) starts."

**Visual:**
```
Raw Text → [Normalize] → [Tokenize] → [Filter] → [Transform] → Clean Tokens
"Hello, World!!" → "hello world" → ["hello", "world"] → ["hello", "world"] → [token_ids]
```

## 3. Beginner Level

### Core Concepts
| Concept | Definition | Example |
|---------|-----------|---------|
| **Tokenization** | Split text into tokens | "I love NLP" → ["I", "love", "NLP"] |
| **Stemming** | Reduce word to root form (aggressive) | "running" → "run" |
| **Lemmatization** | Reduce to dictionary base form | "better" → "good" |
| **Stopwords** | Common words filtered out | "the", "is", "at" |
| **NER** | Identify named entities | "Apple Inc" → ORG |
| **POS Tagging** | Label grammatical roles | "runs" → VBZ (verb) |
| **N-grams** | Contiguous token sequences | "New York" = bigram |
| **Sentence Segmentation** | Split text into sentences | Period-based splitting |

### Common Mistakes (Beginner)
1. Removing ALL punctuation (breaks "U.S.A.", decimals)
2. Applying stemming when you need lemmatization (stemming can produce non-words)
3. Stripping stopwords before TF-IDF (removes important context)
4. Not lowercasing before vocabulary building
5. Ignoring encoding issues (UTF-8 vs Latin-1)

### Interview Basics
- Q: "What is the difference between stemming and lemmatization?" → Stemming is rule-based/aggressive; lemmatization uses vocabulary and morphological analysis
- Q: "When would you NOT remove stopwords?" → Sentiment analysis ("not good" vs "good"), question answering

## 4. Practitioner Level

### Typical Workflow
```python
import spacy
nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc 
              if not token.is_stop and not token.is_punct and token.is_alpha]
    return tokens
```

### Key Libraries
| Library | Purpose | When to Use |
|---------|---------|-------------|
| **spaCy** | Industrial NLP | Production pipelines |
| **NLTK** | Research/education | Prototyping |
| **HuggingFace tokenizers** | Subword tokenization | LLM preprocessing |
| **regex** | Pattern matching | Custom cleaning |
| **ftfy** | Unicode fixing | Dirty web data |

### BPE (Byte-Pair Encoding) — The LLM Standard
```
Vocabulary starts with characters: ["h","e","l","o"," "]
Merge most frequent pairs iteratively: "he" → "hel" → "hell" → "hello"
Result: Subword tokens that handle OOV words gracefully
"unhappiness" → ["un", "happ", "iness"]
```

### Best Practices
- Use **spaCy** for production, **NLTK** for learning
- For LLMs, use the model's own tokenizer (never re-tokenize)
- Always profile vocabulary size before and after preprocessing
- Handle Unicode normalization (NFKC) before anything else
- Log examples of tokenization output during development

## 5. Advanced GenAI Engineering

### Subword Tokenization Deep Dive
| Method | Used By | Mechanism |
|--------|---------|-----------|
| **BPE** | GPT family | Merge frequent byte pairs |
| **WordPiece** | BERT | Maximize likelihood of corpus |
| **SentencePiece** | T5, LLaMA | Language-agnostic, trained end-to-end |
| **Unigram** | XLNet | Probabilistic subword selection |

### Tokenization Impact on LLMs
- Token count directly affects **cost** and **latency**
- Non-English languages typically need more tokens per word (2-3x)
- Numbers tokenize inefficiently: "12345" → ["1","2","3","4","5"] in some tokenizers
- Code tokenization: whitespace-sensitive, consider specialized tokenizers

### Performance Considerations
```
Tokenization Throughput Targets:
- spaCy: ~100K tokens/sec (CPU)
- HuggingFace Fast Tokenizers: ~1M tokens/sec (Rust-based)
- Rule-based regex: ~5M tokens/sec
```

## 6. Senior Engineer Perspective

### Architecture Decisions
- **Build vs Buy:** Always use pre-trained tokenizers for LLM work; only build custom tokenizers for specialized domains (genomics, legal codes, chemical formulas)
- **When to do classical preprocessing:** Feature engineering for classical ML (SVM, LogReg), search indexing (Elasticsearch), data quality pipelines
- **When NOT to:** Direct LLM input — let the model's tokenizer handle it; adding your own preprocessing can degrade performance

### What Juniors Miss
- Token count ≠ word count (important for cost estimation)
- Language-specific edge cases (CJK languages, Arabic RTL, compound words in German)
- The tokenizer is part of the model — mismatch = silent degradation

### What Seniors Focus On
- Tokenizer compatibility across versions
- Multilingual tokenization budgets
- Data preprocessing as a versioned, tested pipeline
- Monitoring token distribution drift in production

## 7. End-to-End Architecture Flow

```
Raw Input Text
      ↓
[Unicode Normalization] ← NFKC, fix encoding
      ↓
[Language Detection] ← fasttext/langdetect
      ↓
[Sentence Segmentation] ← spaCy/NLTK
      ↓
[Tokenization] ← Model-specific tokenizer
      ↓
[Cleaning] ← Strip noise, handle special chars
      ↓
[Token IDs] → Model Input
```

## 8. Terminology Cheat Sheet

| Term | Definition | Importance |
|------|-----------|-----------|
| **Token** | Smallest unit of text for a model | Core to all LLM cost/performance |
| **Vocabulary** | Set of all known tokens | Determines OOV handling |
| **OOV** | Out-of-vocabulary token | Causes information loss |
| **BPE** | Byte-Pair Encoding subword algorithm | Default for GPT models |
| **Morpheme** | Smallest meaningful linguistic unit | Foundation of lemmatization |
| **Corpus** | Large text dataset for training | Quality determines model quality |
| **Stopword** | High-frequency, low-value word | Context-dependent removal |

## 9. Production Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|-----------|
| Token budget exceeded | Input too long | Monitor token counts | Truncate/summarize input |
| Encoding errors | Mixed UTF-8/Latin-1 | Decode errors in logs | `ftfy` + explicit encoding |
| Language mismatch | Wrong tokenizer for language | Poor model output | Detect language first |
| Whitespace normalization breaks code | Aggressive cleaning | Test on code inputs | Domain-specific pipelines |
| Number fragmentation | Token-per-digit | Accuracy degradation | Use structured extraction |

## 10. Metrics That Matter
| Metric | Why It Matters | Warning Sign |
|--------|---------------|-------------|
| **Tokens per document** | Cost prediction | Unexpected spikes |
| **OOV rate** | Coverage | >5% suggests domain mismatch |
| **Compression ratio** | Tokenizer efficiency | Low ratio = expensive |
| **Pipeline latency** | User experience | >100ms for preprocessing |

## 11. Interview Preparation

**Beginner:**
1. What is tokenization? → Splitting text into model-digestible units
2. Stemming vs Lemmatization? → Stemming is rule-based/crude; lemmatization uses vocabulary
3. What are stopwords? → Common words (the, is) filtered to reduce noise
4. What is BPE? → Iterative byte-pair merging to create subword vocabulary
5. Why do we normalize text? → Reduce vocabulary size, handle variations

**Intermediate:**
1. How does WordPiece differ from BPE? → WordPiece maximizes likelihood; BPE maximizes merge frequency
2. Why is tokenization language-dependent? → Different morphologies, character sets, word boundaries
3. How do token counts affect LLM costs? → API pricing is per-token; more tokens = more cost
4. What problems does subword tokenization solve? → OOV, vocabulary size, morphological variations
5. When should you NOT preprocess text before LLM input? → When the model was trained on raw text; preprocessing changes distribution

**Senior:**
1. Design a multilingual preprocessing pipeline for a global RAG system
2. How do you handle tokenizer version mismatches in production?
3. What's your strategy for token budget management in a long-context application?
4. How do you test preprocessing correctness at scale?
5. Describe tradeoffs between custom domain tokenizer vs reusing existing one

## 12. Knowledge Ladder

```
Beginner:     Knows tokenization, stemming, stopwords
      ↓
Intermediate: Understands subword tokenization (BPE/WordPiece), 
              can build preprocessing pipelines
      ↓
Engineer:     Handles multilingual, domain-specific preprocessing,
              monitors token budgets in production
      ↓
Senior:       Designs versioned preprocessing systems, 
              understands tokenizer impact on model behavior,
              makes build-vs-buy decisions
```

## 13. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | Tokenization types, BPE, stemming vs lemmatization, token cost impact |
| **Good To Know** | WordPiece vs SentencePiece, multilingual tokenization, fasttext |
| **Expert Knowledge** | Tokenizer training, vocabulary optimization, cross-lingual alignment |
| **Architecture Nuggets** | Token budget = cost budget; preprocessing is versioned; language detection before tokenization |
| **Interview Nuggets** | "BPE handles OOV" — "Token count drives API cost" — "Model's tokenizer ≠ custom preprocessing" |
| **Red Flags** | Applying your own preprocessing before LLM input; treating all text the same regardless of language |
| **Production Lessons** | Monitor token distribution drift; use fast tokenizers (Rust-backed) in pipelines; always test on multilingual data |

---

# Topic 2: Classical NLP — BoW, TF-IDF & Text Classification

## 1. Executive Summary
- Bag-of-Words (BoW): Represent text as word frequency vectors, ignoring order
- TF-IDF: Weights words by frequency in doc vs rarity across corpus (importance signal)
- **Problem solved:** Converting unstructured text → numerical features for ML models
- Enables: document classification, spam detection, topic modeling, search ranking
- Simple, interpretable, fast — still valuable for production where LLMs are overkill
- TF-IDF outperforms raw BoW for most tasks; both lose semantic meaning
- Classical text classification: Naïve Bayes, SVM, Logistic Regression on TF-IDF features
- Limitations: No word order, no semantics ("not good" ≈ "good" in BoW)
- When to still use: Low latency requirements, small data, interpretability needed, cost-sensitive
- LLMs replaced classical NLP for most accuracy-critical tasks

## 2. Mental Model
> "TF-IDF is like a journalist's nose for a story: words that appear often in one article (TF) but rarely across all articles (IDF) are the distinctive, newsworthy ones."

**Visual:**
```
"The cat sat on the mat"
         ↓
BoW:  {the:2, cat:1, sat:1, on:1, mat:1}
         ↓
TF-IDF: {cat:0.31, sat:0.31, mat:0.31, the:0.0}
         ↓ (downweights "the" because it's everywhere)
Feature Vector → ML Classifier → Label
```

## 3. Beginner Level

### Core Concepts
**Bag of Words:**
```python
from sklearn.feature_extraction.text import CountVectorizer
corpus = ["I love NLP", "NLP is great", "I love AI"]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
# X is a sparse matrix: docs × vocabulary
```

**TF-IDF Formula:**
```
TF(t,d)  = count of term t in document d / total terms in d
IDF(t)   = log(N / df(t))   [N=total docs, df=docs containing term]
TF-IDF   = TF × IDF
```

**Naïve Bayes Text Classifier:**
```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
clf = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('nb', MultinomialNB())
])
clf.fit(X_train, y_train)
```

### Common Mistakes
1. Not using sparse matrices (BoW vectors are 99%+ zeros)
2. Fitting vectorizer on test data (data leakage!)
3. Using BoW for semantic tasks ("not good" ≠ "not bad")
4. Ignoring n-grams (bigrams often critical: "New York", "not good")
5. Forgetting to tune `max_features` (vocabulary explosion)

## 4. Practitioner Level

### Design Patterns
```python
# Production TF-IDF Pipeline
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1,2),      # Unigrams + bigrams
        max_features=50000,     # Cap vocabulary
        sublinear_tf=True,      # Log normalization
        min_df=2,               # Ignore very rare terms
        max_df=0.95             # Ignore very common terms
    )),
    ('clf', LogisticRegression(C=1.0, max_iter=1000))
])
```

### Classifier Comparison for Text

| Classifier | Pros | Cons | Best For |
|-----------|------|------|---------|
| **Naïve Bayes** | Fast, good with small data | Assumes independence | Spam, short docs |
| **Logistic Regression** | Interpretable, calibrated | Linear decision boundary | General classification |
| **SVM (Linear)** | High-dimensional performance | Slower to train | High-dim text features |
| **Random Forest** | Non-linear, robust | Slow, less effective on text | Mixed feature sets |
| **XGBoost** | Strong baseline | Complex tuning | Structured + text features |

## 5. Advanced GenAI Engineering

### When Classical NLP Still Wins

| Scenario | Classical NLP | LLM |
|---------|--------------|-----|
| Latency < 5ms | ✅ | ❌ |
| 1B+ docs/day | ✅ (cheap) | ❌ (cost) |
| Fully interpretable | ✅ | ❌ |
| Small labeled data (<100) | ❌ | ✅ (few-shot) |
| Semantic understanding | ❌ | ✅ |
| Multilingual without retraining | ❌ | ✅ |

### TF-IDF vs Embeddings
| Dimension | TF-IDF | Dense Embeddings |
|-----------|--------|-----------------|
| **Dimensionality** | 10K-100K (sparse) | 384-4096 (dense) |
| **Semantics** | None ("king" ≠ "monarch") | Captured (cosine similarity) |
| **OOV handling** | Ignores | Subword handles it |
| **Speed** | Very fast | GPU-optimized |
| **Interpretability** | High | Low |
| **Training data needed** | Low | High |
| **Best for** | Keyword matching, exact recall | Semantic search |

## 6. Senior Engineer Perspective

### Production Architecture Decision
```
Traffic Volume > 10K req/sec + latency < 10ms?
    → Classical NLP (TF-IDF + SVM)
    
Need semantic understanding?
    → Embeddings + Vector Search
    
Budget constrained + labeled data available?
    → Fine-tuned classical > zero-shot LLM
    
Hybrid approach (Best of both):
    → TF-IDF for recall + Embeddings for re-ranking
```

### What Seniors Focus On
- Vocabulary drift: TF-IDF vectors must be retrained when domain vocabulary changes
- Pipeline versioning: vectorizer + model must be deployed together (pickle version mismatch = silent errors)
- Sparse vs dense storage tradeoffs in serving infrastructure

## 7. End-to-End Architecture: Text Classification System

```
Input Documents
      ↓
[Preprocessing] → tokenize, clean, normalize
      ↓
[TF-IDF Vectorizer] → fit on training set only
      ↓
[Feature Matrix] → sparse (n_docs × vocab_size)
      ↓
[Classifier] → Logistic Regression / SVM / NB
      ↓
[Calibration] → Platt scaling for probabilities
      ↓
[Prediction + Confidence Score]
      ↓
[Monitoring] → accuracy drift, distribution shift
```

## 8. Production Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|-----------|
| Accuracy drops post-deploy | Vocabulary/domain drift | Monitor feature coverage | Periodic retraining |
| Vectorizer-model mismatch | Wrong pickle versions | Load-time errors | Version lock both together |
| Memory OOM | Large vocabulary matrix | Memory profiling | `max_features`, sparse matrices |
| Slow inference | Dense BoW vectors | Latency monitoring | Use sparse format |
| Class imbalance | Training data skew | F1 per class | SMOTE, class weights |

## 9. Interview Preparation

**Beginner:**
1. What is TF-IDF? → Term Frequency × Inverse Document Frequency; weights important words
2. Why do we use IDF? → Downweight common words; upweight distinctive ones
3. What's the curse of dimensionality in BoW? → Vocabulary size → sparse high-dim vectors
4. Why is Naïve Bayes "naïve"? → Assumes feature (word) independence
5. What's a confusion matrix? → TP/FP/TN/FN breakdown of classifier performance

**Intermediate:**
1. How do n-grams improve TF-IDF? → Capture phrase context ("not good" as feature)
2. When does logistic regression beat NB? → More training data, correlated features
3. What is `sublinear_tf` in sklearn? → Uses 1 + log(tf) instead of tf; reduces impact of very frequent terms
4. How do you handle class imbalance? → Oversample, undersample, class_weight='balanced', SMOTE
5. How would you detect vocabulary drift? → Monitor OOV rate, feature coverage, model confidence distribution

**Senior:**
1. Design a document classification system for 100M docs/day with 10ms SLA
2. How do you A/B test a new vectorizer without downtime?
3. Classical NLP vs LLM for a legal document classification task — your recommendation?

## 10. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | TF-IDF formula, BoW limitations, sklearn Pipeline, Naïve Bayes |
| **Good To Know** | N-gram ranges, sublinear TF, class imbalance techniques |
| **Expert Knowledge** | Vocabulary drift, sparse matrix optimization, online learning |
| **Architecture Nuggets** | TF-IDF = fast + cheap; Embeddings = semantic; use hybrid for best recall |
| **Interview Nuggets** | "TF-IDF is bag of words with importance weighting" — "NB assumes independence" |
| **Red Flags** | Fitting vectorizer on test data; not versioning vectorizer with model |
| **Production Lessons** | Monitor OOV rate; always use sparse matrices; retrain on new domain data |

---

# Topic 3: Word Embeddings (Word2Vec & Dense Vectors)

## 1. Executive Summary
- Word embeddings map words to dense numerical vectors capturing semantic meaning
- **Problem solved:** BoW loses all meaning; embeddings encode relationships
- Word2Vec (2013, Google): learns embeddings from co-occurrence patterns
- Famous property: `king - man + woman ≈ queen` (vector arithmetic)
- Two architectures: CBOW (predict word from context) and Skip-gram (predict context from word)
- GloVe (Stanford): global co-occurrence matrix factorization
- FastText: adds subword information → handles OOV
- Foundation for all modern NLP; Transformers evolved from this paradigm
- Static embeddings (Word2Vec) vs contextual (BERT) — key distinction
- Used in: recommendation systems, search, entity resolution, anomaly detection

## 2. Mental Model
> "Word embeddings are GPS coordinates for meaning. Just as (lat, lon) encodes location, (dim1..dim300) encodes semantic position in meaning-space. Words with similar meanings cluster together."

**Vector Space Geometry:**
```
          queen •
king •          
          woman •
man  •
          
king - man ≈ queen - woman  (gender direction)
Paris - France ≈ Rome - Italy  (capital-country direction)
```

## 3. Beginner Level

### Core Concepts

**Word2Vec — Two Architectures:**
```
CBOW (Continuous Bag of Words):
[the] [cat] [___] [on] [the] → predict: "sat"
Context words → Center word

Skip-gram:
[sat] → predict: [the, cat, on, the]
Center word → Context words
(Better for rare words, slower)
```

**Training:**
```python
from gensim.models import Word2Vec

sentences = [["I", "love", "NLP"], ["NLP", "is", "amazing"]]
model = Word2Vec(
    sentences,
    vector_size=100,   # Embedding dimensions
    window=5,          # Context window size
    min_count=2,       # Ignore rare words
    sg=1               # 1=skip-gram, 0=CBOW
)

# Usage
vector = model.wv["NLP"]          # Get vector
similar = model.wv.most_similar("NLP", topn=5)
analogy = model.wv.most_similar(positive=["king","woman"], negative=["man"])
```

### Common Mistakes
1. Using Word2Vec when you need contextual understanding (BERT is better)
2. Training on too little data (<1M words → poor embeddings)
3. Not normalizing vectors before cosine similarity
4. Ignoring OOV for words not in training vocabulary

## 4. Practitioner Level

### Word2Vec vs GloVe vs FastText

| Property | Word2Vec | GloVe | FastText |
|----------|---------|-------|---------|
| **Training approach** | Local context window | Global co-occurrence | Subword n-grams |
| **OOV handling** | ❌ No | ❌ No | ✅ Yes |
| **Morphology** | Ignored | Ignored | Captured |
| **Speed** | Fast | Moderate | Slower |
| **Best for** | General NLP | Large corpus | Morphologically rich languages, domain text |

### Negative Sampling (How Word2Vec Actually Trains)
```
For each (word, context) pair:
1. True pair: maximize similarity → positive sample
2. Random words: minimize similarity → k negative samples (k=5-20)
Avoids computing softmax over entire vocabulary (expensive!)
```

### Pre-trained Embeddings
```python
# Always prefer pre-trained for production
import gensim.downloader as api
model = api.load("word2vec-google-news-300")  # 300-dim, trained on 100B words

# Or use FastText pre-trained
from gensim.models import FastText
ft = FastText.load_fasttext_format("cc.en.300.bin")
ft.wv["unfathomable"]  # Works even for OOV via subwords!
```

## 5. Advanced GenAI Engineering

### Why Static Embeddings Have Limits
```
"I went to the bank" (river bank or financial bank?)
Word2Vec: bank → SAME vector always
BERT:     bank → DIFFERENT vector based on sentence context
```

### Embedding Dimensions Tradeoff
| Dimensions | Memory | Performance | Speed |
|-----------|--------|-------------|-------|
| 50 | Low | Poor | Fast |
| 100 | Medium | Good | Good |
| 300 | High | Best for Word2Vec | Moderate |
| 768+ | High | Best (contextual) | Slow |

### Applying in Recommendation Systems
```python
# Treat items as "words", sessions as "sentences" (Item2Vec)
# User watched: [Movie_A, Movie_B, Movie_C]
# Train Word2Vec on viewing sequences
# Find similar movies: model.wv.most_similar("Movie_A")
```

## 6. Senior Engineer Perspective

### When to Use Static Embeddings
- ✅ Feature input to classical ML (fast, low memory)
- ✅ Similarity search where context is stable
- ✅ Domain-specific training on proprietary corpus (legal, medical)
- ✅ Edge/embedded deployment (small model size)
- ❌ Polysemy (context-dependent meaning)
- ❌ When BERT/sentence transformers are feasible

### Build vs Buy
- **Always use pre-trained** unless you have large domain-specific corpus (>1B tokens)
- Fine-tuning BERT sentence embeddings >> custom Word2Vec from scratch

## 7. Terminology Cheat Sheet

| Term | Definition | Importance |
|------|-----------|-----------|
| **Embedding** | Dense vector representation of token | Foundation of modern NLP |
| **Cosine similarity** | Angle-based similarity measure | Standard similarity metric |
| **Semantic space** | High-dim space where meaning is geometry | Core mental model |
| **Skip-gram** | Predict context from center word | Better for rare words |
| **CBOW** | Predict center from context | Faster training |
| **Negative sampling** | Train with fake pairs to avoid full softmax | Makes Word2Vec feasible |
| **Analogy task** | king-man+woman=queen | Validates embedding quality |

## 8. Production Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|-----------|
| OOV words ignored | Static vocabulary | Monitor OOV rate | FastText or contextual embeddings |
| Semantic drift | Domain-specific language | Analogy task accuracy drops | Domain fine-tuning |
| Bias in embeddings | Biased training corpus | Bias probing tests | Debiasing or curated training data |
| Memory OOM | Large vocabulary × dimensions | Memory profiling | Quantization, vocabulary pruning |

## 9. Interview Preparation

**Beginner:**
1. What is a word embedding? → Dense vector capturing word semantics
2. What is king - man + woman? → queen (vector arithmetic in embedding space)
3. CBOW vs Skip-gram? → CBOW: context→word; Skip-gram: word→context
4. What problem does Word2Vec solve? → BoW loses all semantic meaning
5. What is cosine similarity? → Measure of vector angle; 1=identical, 0=orthogonal

**Senior:**
1. How would you detect embedding drift in a deployed search system?
2. Word2Vec vs BERT embeddings for a product search system — tradeoffs?
3. Design an item recommendation system using embedding-based approaches
4. How do you handle multiple meanings of a word in a static embedding system?

## 10. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | Word2Vec intuition, CBOW vs Skip-gram, cosine similarity, static vs contextual |
| **Good To Know** | GloVe global co-occurrence, negative sampling, embedding dimensions |
| **Expert Knowledge** | Embedding debiasing, item2vec for recommendations, quantization |
| **Architecture Nuggets** | Static embeddings for speed; contextual for quality; always try pre-trained first |
| **Interview Nuggets** | "Embeddings are GPS coordinates for meaning" — "Skip-gram better for rare words" |
| **Red Flags** | Using Word2Vec for polysemous terms; training from scratch without enough data |
| **Production Lessons** | FastText for OOV; monitor vocabulary coverage; consider contextual if accuracy matters |

---

# Topic 4: Transformer Architecture

## 1. Executive Summary
- **Transformers** (2017, "Attention Is All You Need") revolutionized NLP → foundation of all modern LLMs
- **Problem solved:** RNNs can't parallelize and struggle with long-range dependencies
- Core mechanism: **Self-Attention** — each token attends to all other tokens simultaneously
- Enables: parallel training on TPUs/GPUs, capturing long-range context
- Two variants: **Encoder** (BERT — bidirectional understanding) and **Decoder** (GPT — autoregressive generation)
- Encoder-Decoder: T5, BART (seq2seq tasks: translation, summarization)
- Pre-training on massive text → fine-tuning for downstream tasks (transfer learning)
- **Attention is O(n²)** in sequence length — efficiency is an active research area
- Powers: GPT-4, Claude, Gemini, LLaMA, BERT, T5 — essentially all modern AI
- Understanding Transformers = understanding all modern LLMs

## 2. Mental Model
> "Transformer attention is like a roomful of experts where every expert listens to every other expert simultaneously and decides who to pay attention to. Unlike humans talking in sequence (RNN), everyone speaks at once."

**Self-Attention Intuition:**
```
"The animal didn't cross the street because it was too tired"

When processing "it":
- Attends strongly to "animal" (resolves pronoun reference)
- Low attention to "street", "cross"
- This is learned, not programmed

Attention weights:
it → animal: 0.8
it → tired:  0.6
it → street: 0.1
```

## 3. Beginner Level

### Core Components

```
Transformer Block:
┌─────────────────────────────┐
│  Input Embeddings           │
│         +                   │
│  Positional Encoding        │
│         ↓                   │
│  [Multi-Head Attention]     │  ← Parallel attention heads
│         +                   │
│  [Add & Norm]               │  ← Residual connection
│         ↓                   │
│  [Feed-Forward Network]     │  ← Per-position MLP
│         +                   │
│  [Add & Norm]               │
│         ↓                   │
│  Output                     │
└─────────────────────────────┘
         × N layers
```

### Self-Attention Mechanism (Simplified)
```
Given: Query (Q), Key (K), Value (V) matrices

1. Score = Q × K^T  (how much each token should attend to others)
2. Scale = Score / √d_k  (prevent vanishing gradients)
3. Softmax(Score) = attention weights (sum to 1)
4. Output = weights × V  (weighted sum of values)

Intuitively:
Q = "What am I looking for?"
K = "What information do I have?"  
V = "What should I return if matched?"
```

### Positional Encoding
```python
# Transformers have no inherent notion of order (unlike RNNs)
# Add positional signal to embeddings:
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

# Modern approach: Rotary Position Embedding (RoPE) — used in LLaMA
```

## 4. Practitioner Level

### Encoder vs Decoder vs Encoder-Decoder

| Architecture | Examples | Use Case | Attention Type |
|-------------|---------|---------|---------------|
| **Encoder-only** | BERT, RoBERTa | Classification, NER, embeddings | Bidirectional |
| **Decoder-only** | GPT, LLaMA, Claude | Text generation | Causal (masked) |
| **Encoder-Decoder** | T5, BART, Whisper | Translation, summarization | Cross-attention |

### Attention Variants
| Variant | Description | Use Case |
|---------|-------------|---------|
| **Full attention** | All tokens attend to all | Quality, limited context |
| **Causal attention** | Tokens only attend to past | Autoregressive generation |
| **Sparse attention** | Attend to subset of tokens | Efficiency, long context |
| **Flash Attention** | Memory-efficient exact attention | Production LLMs |
| **Multi-Query Attention** | Shared K,V across heads | Faster inference (GQA) |

### Key Hyperparameters
```
d_model: embedding dimension (768 for BERT-base, 4096 for LLaMA-7B)
n_heads: attention heads (12 for BERT-base) — each head focuses on different aspects
n_layers: transformer blocks stacked (12 for BERT-base, 32 for LLaMA-7B)
FFN size: typically 4× d_model
```

## 5. Advanced GenAI Engineering

### Attention Complexity Problem
```
Standard Attention: O(n²) in sequence length
- 1K tokens: 1M operations
- 10K tokens: 100M operations  ← expensive
- 100K tokens: 10B operations  ← infeasible without optimization

Solutions:
- Flash Attention: Same result, 10× less memory (recompute instead of store)
- Sliding window attention: Attend to local window
- ALiBi: Length extrapolation without positional encoding changes
```

### Pre-training vs Fine-tuning vs Prompting
```
Pre-training:   Train from scratch on massive corpus (billions of tokens)
                Cost: $10M-$100M+. Done by labs only.

Fine-tuning:    Continue training pre-trained model on domain data
                Cost: $100-$10K. Updates all weights.

PEFT (LoRA):    Train small adapter matrices only
                Cost: $10-$1K. Updates <1% of weights.

Prompting:      No training. Guide via instructions.
                Cost: $0. Most practical.

RAG:            Retrieval-augmented context. No weight updates.
                Best for: knowledge-intensive tasks.
```

### KV Cache (Critical for Inference)
```
During generation, K and V for previous tokens don't change.
KV Cache: store them and reuse → massive speedup

Without KV Cache: O(n²) per new token
With KV Cache:    O(n) per new token

Memory: d_model × n_layers × 2 × seq_len × dtype_bytes
At 70B model, 8K context: ~35GB just for KV cache!
```

## 6. Senior Engineer Perspective

### Architecture Decisions for Production

| Decision | Options | Recommendation |
|---------|---------|---------------|
| **Model size** | 7B/13B/70B/GPT-4 | Start with 7B, scale on eval |
| **Context window** | 4K/32K/128K/1M | Match to task; larger = more expensive |
| **Precision** | FP32/FP16/INT8/INT4 | FP16 for quality; INT4 for cost |
| **Attention implementation** | Standard/Flash Attention v2 | Always Flash Attention in production |
| **Batch size** | 1 to 512+ | Larger for throughput; smaller for latency |

### What Seniors Focus On
- Model selection is a business decision, not just technical
- Inference optimization: quantization, batching, speculative decoding, KV cache management
- Monitoring: latency percentiles (p50/p95/p99), token throughput, GPU utilization
- Context window management: cost grows quadratically with sequence length

## 7. End-to-End Architecture: LLM Inference

```
User Request
      ↓
[Tokenizer] → token IDs
      ↓
[Embedding Layer] → token embeddings
      ↓
[+ Positional Encoding]
      ↓
[Transformer Block × N]
  ├─ [Multi-Head Self-Attention] ← uses KV Cache
  ├─ [Add & Norm]
  ├─ [Feed-Forward Network]
  └─ [Add & Norm]
      ↓
[Language Model Head] → logits over vocabulary
      ↓
[Sampling Strategy] → temperature, top-p, top-k
      ↓
[Detokenizer] → text output
```

## 8. Terminology Cheat Sheet

| Term | Definition | Importance |
|------|-----------|-----------|
| **Attention** | Mechanism to weigh token relationships | Core of Transformers |
| **Q, K, V** | Query, Key, Value matrices in attention | Core computation |
| **Multi-head attention** | Multiple parallel attention operations | Captures different relationship types |
| **Residual connection** | Add input to output of each block | Enables training deep networks |
| **Layer normalization** | Normalize across features per sample | Stabilizes training |
| **Positional encoding** | Inject position information | Transformers have no inherent order |
| **KV Cache** | Cached key-value pairs for generation | Critical for inference speed |
| **Flash Attention** | Memory-efficient exact attention | Production standard |
| **LoRA** | Low-Rank Adaptation — efficient fine-tuning | Standard PEFT method |
| **Temperature** | Sampling randomness (0=deterministic) | Controls output diversity |

## 9. Comparison Tables

### BERT vs GPT
| Property | BERT | GPT |
|---------|------|-----|
| **Type** | Encoder-only | Decoder-only |
| **Attention** | Bidirectional | Causal (left-to-right) |
| **Pre-training** | Masked LM + NSP | Next-token prediction |
| **Best for** | Classification, NER, embeddings | Text generation, completion |
| **Representative models** | RoBERTa, DeBERTa, ALBERT | GPT-4, Claude, LLaMA |

## 10. Production Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|-----------|
| OOM on long context | Attention O(n²) | GPU memory monitoring | Flash Attention, context truncation |
| KV cache overflow | Long generation + large batch | Memory alerts | KV cache eviction, sliding window |
| Slow TTFT | No batching | Latency monitoring | Continuous batching, pipelining |
| Model drift | Distribution shift | Output monitoring | Re-evaluation, fallback models |
| Hallucination | Model uncertainty | RAG faithfulness metrics | RAG, RLHF-aligned models |

## 11. Interview Preparation

**Beginner:**
1. What is self-attention? → Mechanism for each token to attend to all others
2. Why Transformers over RNNs? → Parallelizable, handles long-range dependencies
3. What is positional encoding? → Injects order information (no built-in in Transformers)
4. BERT vs GPT difference? → Encoder (bidirectional) vs Decoder (causal)
5. What is multi-head attention? → Multiple parallel attention operations capturing different relationships

**Intermediate:**
1. Why does attention scale with O(n²)? → Every token pair computes a score
2. What is a KV cache? → Cached K,V from previous tokens to speed generation
3. What is Flash Attention? → Memory-efficient attention — recomputes instead of storing
4. What is LoRA? → Low-rank matrices injected into linear layers for efficient fine-tuning
5. What is temperature in LLM sampling? → Scales logits; 0=greedy, high=diverse

**Senior:**
1. Design an LLM inference system for 10K concurrent users
2. How would you optimize a 70B model for sub-100ms TTFT?
3. Explain the tradeoffs between INT4 quantization and FP16
4. How does speculative decoding work and when should you use it?
5. Design a cost-efficient architecture for a 24/7 LLM API service

## 12. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | Self-attention (Q,K,V), encoder vs decoder, positional encoding, KV cache |
| **Good To Know** | Flash Attention, LoRA, PEFT methods, multi-query attention |
| **Expert Knowledge** | Speculative decoding, GQA, rope embeddings, mixture of experts |
| **Architecture Nuggets** | KV cache = inference speed; Flash Attention = memory efficiency; INT4 = 4× cheaper inference |
| **Interview Nuggets** | "Attention is O(n²)" — "KV cache makes generation fast" — "LoRA updates <1% of weights" |
| **Red Flags** | Using standard attention for long contexts; no KV cache in production |
| **Production Lessons** | Always Flash Attention; profile KV cache memory; batch requests for throughput |

---

# Topic 5: boto3 & AWS Bedrock Setup

## 1. Executive Summary
- **boto3**: Official AWS Python SDK — programmatic access to all AWS services
- **AWS Bedrock**: Managed LLM API service — call Claude, Llama, Titan, Mistral without infrastructure
- **Problem solved:** Access foundation models on AWS without managing GPU infrastructure
- Bedrock provides: API access, fine-tuning, embeddings, knowledge bases, agents
- Pay-per-token pricing — no reserved instances needed for variable workloads
- IAM-secured — no API keys floating around; uses AWS credential chain
- Bedrock Knowledge Bases: managed RAG service (OpenSearch Serverless backend)
- Bedrock Agents: managed agent orchestration service
- GuardRails: safety filtering layer for enterprise compliance
- Integration: works with Lambda, ECS, SageMaker, Step Functions natively

## 2. Mental Model
> "boto3 is your remote control for AWS. Bedrock is the TV with all the LLM channels. IAM is the parental controls that decide who can press which buttons."

## 3. Beginner Level

### Setup & Authentication
```python
# Install
# pip install boto3

# Authentication (in order of preference for production):
# 1. IAM Role (on EC2/Lambda) — best practice
# 2. AWS CLI profile (~/.aws/credentials)
# 3. Environment variables (AWS_ACCESS_KEY_ID, etc.) — avoid in production

import boto3

# Default credential chain (picks up automatically)
client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Explicit profile (development only)
session = boto3.Session(profile_name='my-profile')
client = session.client('bedrock-runtime', region_name='us-east-1')
```

### First Bedrock Call
```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Explain transformers in 3 sentences"}
        ]
    }),
    contentType='application/json',
    accept='application/json'
)

body = json.loads(response['body'].read())
print(body['content'][0]['text'])
```

## 4. Practitioner Level

### Model IDs Reference
| Model | Model ID |
|-------|---------|
| Claude 3.5 Sonnet | `anthropic.claude-3-5-sonnet-20241022-v2:0` |
| Claude 3 Haiku | `anthropic.claude-3-haiku-20240307-v1:0` |
| Claude 3 Opus | `anthropic.claude-3-opus-20240229-v1:0` |
| Llama 3.1 70B | `meta.llama3-1-70b-instruct-v1:0` |
| Titan Embeddings | `amazon.titan-embed-text-v2:0` |
| Cohere Command R+ | `cohere.command-r-plus-v1:0` |

### Streaming Responses
```python
# Critical for production — don't wait for full response
response = bedrock.invoke_model_with_response_stream(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({...})
)

stream = response['body']
for event in stream:
    chunk = event.get('chunk')
    if chunk:
        data = json.loads(chunk['bytes'])
        if data['type'] == 'content_block_delta':
            print(data['delta']['text'], end='', flush=True)
```

### Error Handling Pattern
```python
from botocore.exceptions import ClientError
import time

def invoke_with_retry(bedrock_client, model_id, body, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = bedrock_client.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            return json.loads(response['body'].read())
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ThrottlingException':
                wait = 2 ** attempt  # Exponential backoff
                time.sleep(wait)
            elif error_code == 'ModelNotReadyException':
                raise  # Don't retry
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Embeddings with Bedrock
```python
def get_embedding(text: str, bedrock_client) -> list[float]:
    response = bedrock_client.invoke_model(
        modelId='amazon.titan-embed-text-v2:0',
        body=json.dumps({'inputText': text}),
        contentType='application/json',
        accept='application/json'
    )
    return json.loads(response['body'].read())['embedding']
```

## 5. Advanced GenAI Engineering

### IAM Policy for Bedrock (Least Privilege)
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
            ]
        }
    ]
}
```

### Cost Control Pattern
```python
import tiktoken  # Or use anthropic tokenizer

MAX_INPUT_TOKENS = 4000
MAX_OUTPUT_TOKENS = 500

def cost_aware_invoke(prompt: str, bedrock_client):
    # Estimate tokens before invoking
    enc = tiktoken.encoding_for_model("cl100k_base")
    input_tokens = len(enc.encode(prompt))
    
    if input_tokens > MAX_INPUT_TOKENS:
        # Truncate or summarize
        raise ValueError(f"Input too long: {input_tokens} tokens")
    
    return invoke_with_retry(bedrock_client, MODEL_ID, {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_OUTPUT_TOKENS
    })
```

### Connection Pooling for High Throughput
```python
# boto3 clients are thread-safe but session/connection pooling matters
# Use one client per service per region, share across threads

from functools import lru_cache

@lru_cache(maxsize=None)
def get_bedrock_client(region: str = 'us-east-1'):
    return boto3.client(
        'bedrock-runtime',
        region_name=region,
        config=boto3.session.Config(
            max_pool_connections=50,  # Connection pool size
            connect_timeout=5,
            read_timeout=120          # Long for LLM responses
        )
    )
```

## 6. Senior Engineer Perspective

### Bedrock vs OpenAI vs SageMaker

| Dimension | Bedrock | OpenAI API | SageMaker Endpoint |
|----------|---------|-----------|-------------------|
| **Infrastructure** | Managed | Managed | Self-managed |
| **Models** | Multi-vendor | OpenAI only | Any model |
| **Data privacy** | AWS boundary | OpenAI servers | Your VPC |
| **Cost model** | Per-token | Per-token | Hourly instance |
| **Compliance** | HIPAA, SOC2 | SOC2 | HIPAA, FedRAMP |
| **Latency** | Good | Good | Controllable |
| **Fine-tuning** | Limited | Yes | Full control |

### Production Architecture
```
Application
    ↓
[API Gateway + Lambda] — throttling, auth
    ↓
[Bedrock Runtime] — model invocation
    ↓
[CloudWatch] — latency, cost, error metrics
    ↓
[SNS/SQS] — async processing for batch
```

## 7. Production Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|-----------|
| ThrottlingException | Rate limits exceeded | CloudWatch throttle metrics | Exponential backoff, request queuing |
| ModelNotReadyException | Model loading | Immediate error | Retry after delay |
| ValidationException | Wrong payload format | Error logs | Schema validation pre-call |
| High latency spike | Cold start / traffic | p95 latency alerts | Connection warmup, reserved capacity |
| IAM auth failure | Missing permissions | 403 errors | Least-privilege IAM review |
| Cost explosion | No token limits | Cost alerts | `max_tokens`, usage dashboards |

## 8. Interview Preparation

**Beginner:**
1. What is boto3? → AWS Python SDK for all AWS services
2. What is AWS Bedrock? → Managed API for foundation models (Claude, Llama, etc.)
3. How does authentication work? → IAM credential chain (role > profile > env vars)
4. What is invoke_model? → Synchronous LLM call on Bedrock
5. What is streaming? → Receive tokens as they're generated (lower perceived latency)

**Senior:**
1. Design a multi-tenant Bedrock API with per-tenant rate limiting and cost tracking
2. How do you handle Bedrock ThrottlingExceptions under high load?
3. Bedrock vs self-hosted SageMaker — when would you choose each?
4. How do you secure Bedrock access in a zero-trust architecture?

## 9. Ultimate Revision Sheet

| Category | Content |
|----------|---------|
| **Must Know** | invoke_model, streaming, credential chain, model IDs, ThrottlingException handling |
| **Good To Know** | Connection pooling, IAM least-privilege, Bedrock Knowledge Bases |
| **Expert Knowledge** | Bedrock Agents, multi-region routing, cost allocation tags, GuardRails |
| **Architecture Nuggets** | IAM Role > env vars; always stream for UX; implement retry with exponential backoff |
| **Interview Nuggets** | "Bedrock = managed LLM API, no infra; SageMaker = full control, your infra" |
| **Red Flags** | Hardcoding AWS credentials; no retry logic; no token limits; single region |
| **Production Lessons** | Monitor token usage per request; alarm on ThrottlingException rates; use streaming always |
