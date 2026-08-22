# 🧠 The NLP to LLM Roadmap: Architectural Foundations & Engineering Excellence

> **“Those who cannot remember the past are condemned to reimplement it badly in production.”**
> — Every Senior ML Engineer, eventually.

-----

## 📋 Table of Contents

1. [The Preprocessing Pipeline (Data Engineering)](#-section-1-the-preprocessing-pipeline-data-engineering)
1. [Statistical Representations (Feature Engineering)](#-section-2-statistical-representations-feature-engineering)
1. [From Dense Vectors to Transformers (Modeling)](#-section-3-from-dense-vectors-to-transformers-modeling)

-----

## 🔬 Section 1: The Preprocessing Pipeline (Data Engineering)

> **The unglamorous truth:** 80% of an ML engineer’s life is data cleaning. The other 20% is arguing about data cleaning.

### 1.1 Tokenization: Splitting the Atom of Language

Tokenization is the process of decomposing raw text into discrete units — **tokens** — that a model or algorithm can operate on. It sounds trivially simple. It is not.

Consider the sentence: `"Don't you think Mr. O'Brien's 2024 Q3 report (pg. 7) is... fine?"`.

A naïve split on whitespace gives you garbage. A production tokenizer must handle:

|Challenge    |Example    |Naïve Result                  |Correct Result            |
|-------------|-----------|------------------------------|--------------------------|
|Contractions |`Don't`    |`["Don't"]`                   |`["Do", "n't"]`           |
|Possessives  |`O'Brien's`|`["O'Brien's"]`               |`["O'Brien", "'s"]`       |
|Punctuation  |`fine?`    |`["fine?"]`                   |`["fine", "?"]`           |
|Abbreviations|`Mr.`      |`["Mr."]` (sentence boundary?)|`["Mr."]` (not a boundary)|

#### Tokenization Strategies

```
Word-level:    "the cat sat" → ["the", "cat", "sat"]
Char-level:    "cat"         → ["c", "a", "t"]
Subword (BPE): "unhappiness" → ["un", "happy", "ness"]  ← What LLMs actually use
```

**Byte-Pair Encoding (BPE)** — the backbone of GPT tokenizers — iteratively merges the most frequent character pairs, producing a vocabulary that gracefully handles out-of-vocabulary words by decomposing them into known subword units. `tiktoken` is OpenAI’s production implementation.

-----

### 1.2 Stemming vs. Lemmatization: The Spectrum of Normalization

Both techniques reduce inflectional forms to a common base. They differ radically in *how*.

#### Stemming (Fast, Crude, Rule-Based)

A stemmer algorithmically chops suffixes using heuristic rules. The Porter Stemmer, the most famous, applies a cascade of rewrite rules (e.g., `ATIONAL → ATE`).

```
"running"    → "run"
"studies"    → "studi"      ← not a real word
"generously" → "generous"
"university" → "univers"    ← loses meaning
```

> [!CAUTION]
> **The Over-Stemming Problem.** `"universe"` and `"university"` both stem to `"univers"`. Your classifier has now decided these are semantically equivalent. This is the algorithmic equivalent of a Freudian slip — confidently, catastrophically wrong.

#### Lemmatization (Slower, Principled, Linguistically Aware)

A lemmatizer uses a morphological dictionary and part-of-speech context to return the **dictionary form** (lemma) of a word.

```
"running" (verb) → "run"
"better"  (adj)  → "good"
"studies" (noun) → "study"
"studies" (verb) → "study"
```

The crucial difference: `lemmatize("better")` requires *knowing* it’s an adjective. Context matters.

|Property           |Stemming                                            |Lemmatization                       |
|-------------------|----------------------------------------------------|------------------------------------|
|Speed              |⚡ Very fast                                         |🐢 Slower                            |
|Linguistic accuracy|Low                                                 |High                                |
|Returns real word  |❌ Not guaranteed                                    |✅ Always                            |
|Requires POS tag   |No                                                  |Yes                                 |
|Best for           |IR / search engines, speed-critical batch processing|NLU tasks, classification, sentiment|

-----

### 1.3 Stopword Removal

Stopwords are high-frequency, low-information tokens: `"the"`, `"is"`, `"at"`, `"which"`, etc. Removing them reduces dimensionality and noise for many classical NLP tasks.

> [!CAUTION]
> **The “Not” Problem.** `"I am NOT happy"` after naive stopword removal becomes `"happy"`. Your sentiment classifier will hallucinate joy. Always audit which words your stopword list removes — `"not"`, `"no"`, `"never"` are context-critical negations that many lists happily discard.

-----

### 1.4 The Senior Perspective: “Why Do We Still Care in the LLM Era?”

This is the question every junior engineer asks before shipping raw, unprocessed text into a RAG pipeline and watching costs explode.

> [!TIP]
> **The Three Production Reasons to Still Preprocess:**
> 
> 1. **Context Window Cost.** GPT-4 Turbo charges per token. A corpus of legal documents filled with boilerplate headers, page numbers, and repeated disclaimers is burning your budget. Aggressive deduplication, header stripping, and normalization *directly* reduces your inference bill. This is not a theoretical concern — it is a line item on your AWS invoice.
> 1. **RAG Pipeline Noise Reduction.** In Retrieval-Augmented Generation, your vector store’s retrieval quality depends on signal-to-noise in the indexed chunks. A chunk containing `"Page 7 of 42 | CONFIDENTIAL | © Acme Corp 2019"` followed by one sentence of actual content will embed poorly and pollute your similarity search. Preprocessing is your data quality gate.
> 1. **Evaluation Integrity.** When computing BLEU, ROUGE, or BERTScore for model evaluation, inconsistent text normalization (mixed casing, smart quotes vs. ASCII quotes, em-dashes) introduces measurement artifacts. Your model may appear to perform 3% worse simply because your gold labels weren’t normalized. Reproducible evaluation requires a deterministic preprocessing contract.

-----

### 1.5 Production Preprocessing with spaCy

```python
"""
nlp/preprocessing.py

Production-grade text preprocessing pipeline using spaCy.
Designed for reusability across classical NLP and RAG workflows.
"""

from __future__ import annotations

import re
import spacy
from spacy.language import Language
from dataclasses import dataclass, field


@dataclass
class PreprocessingConfig:
    """
    Configuration object for the preprocessing pipeline.
    Centralise your choices here — don't scatter magic booleans through your codebase.
    """
    remove_stopwords: bool = True
    lemmatize: bool = True
    remove_punctuation: bool = True
    lowercase: bool = True
    min_token_length: int = 2
    # POS tags to retain. Nouns, verbs, adjectives, adverbs carry the most signal.
    allowed_pos: set[str] = field(
        default_factory=lambda: {"NOUN", "VERB", "ADJ", "ADV", "PROPN"}
    )


def load_nlp_model(model_name: str = "en_core_web_sm") -> Language:
    """
    Load a spaCy language model.
    
    Args:
        model_name: spaCy model identifier. Use 'en_core_web_lg' in
                    production for better NER and lemmatization accuracy.
    
    Returns:
        A loaded spaCy Language pipeline.
    
    Raises:
        OSError: If the model is not installed. Run:
                 `python -m spacy download en_core_web_sm`
    """
    # Disable pipeline components we don't need — significant speed gains
    # for large corpora. NER and parsing are expensive; skip if unused.
    return spacy.load(model_name, disable=["ner", "parser"])


def preprocess_text(
    text: str,
    nlp: Language,
    config: PreprocessingConfig | None = None,
) -> str:
    """
    Clean and normalize a single document string.

    This function is intentionally stateless and pure — same input always
    yields same output. This is non-negotiable for reproducible ML pipelines.

    Args:
        text:   Raw input text to process.
        nlp:    A loaded spaCy Language model (load once, reuse everywhere).
        config: Preprocessing configuration. Defaults to PreprocessingConfig().

    Returns:
        A single normalized string of processed tokens.

    Example:
        >>> nlp = load_nlp_model()
        >>> preprocess_text("The dogs were running quickly!", nlp)
        'dog run quickly'
    """
    if config is None:
        config = PreprocessingConfig()

    # Step 1: Coarse cleaning before spaCy parsing (cheaper than token-level)
    text = re.sub(r"http\S+|www\S+", "", text)          # Remove URLs
    text = re.sub(r"\S+@\S+\.\S+", "", text)            # Remove emails
    text = re.sub(r"\s+", " ", text).strip()             # Normalise whitespace

    if config.lowercase:
        text = text.lower()

    # Step 2: spaCy linguistic processing
    doc = nlp(text)

    tokens: list[str] = []
    for token in doc:
        # Gate 1: Stopword removal
        if config.remove_stopwords and token.is_stop:
            continue

        # Gate 2: Punctuation / space removal
        if config.remove_punctuation and (token.is_punct or token.is_space):
            continue

        # Gate 3: POS filtering (retain only content-bearing tags)
        if config.allowed_pos and token.pos_ not in config.allowed_pos:
            continue

        # Gate 4: Minimum length (removes artifacts like "s", "n")
        raw_form = token.lemma_ if config.lemmatize else token.text
        if len(raw_form) < config.min_token_length:
            continue

        tokens.append(raw_form)

    return " ".join(tokens)


def preprocess_corpus(
    documents: list[str],
    nlp: Language,
    config: PreprocessingConfig | None = None,
) -> list[str]:
    """
    Process a list of documents using spaCy's efficient pipe() method.

    spaCy's nlp.pipe() batches documents for vectorised processing — 
    significantly faster than calling nlp() in a Python loop for large corpora.

    Args:
        documents: List of raw document strings.
        nlp:       A loaded spaCy Language model.
        config:    Preprocessing configuration.

    Returns:
        List of preprocessed document strings, same order as input.
    """
    if config is None:
        config = PreprocessingConfig()

    processed: list[str] = []

    # nlp.pipe() is the production-grade way: batches internally, GIL-friendly
    for doc in nlp.pipe(documents, batch_size=64):
        tokens: list[str] = []
        for token in doc:
            if config.remove_stopwords and token.is_stop:
                continue
            if config.remove_punctuation and (token.is_punct or token.is_space):
                continue
            if config.allowed_pos and token.pos_ not in config.allowed_pos:
                continue
            raw_form = token.lemma_ if config.lemmatize else token.text
            if len(raw_form) < config.min_token_length:
                continue
            tokens.append(raw_form)
        processed.append(" ".join(tokens))

    return processed


# ── Quick sanity check ──────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = [
        "The dogs were running quickly through the beautiful garden.",
        "She has been studying machine learning for three years.",
        "NLP engineers don't sleep; they just process tokens.",
    ]

    nlp_model = load_nlp_model()
    results = preprocess_corpus(sample, nlp_model)

    for original, clean in zip(sample, results):
        print(f"  IN : {original}")
        print(f"  OUT: {clean}")
        print()
```

> [!TIP]
> **Performance Note.** For datasets exceeding 1M documents, consider running your spaCy pipeline with multiple processes via `multiprocessing` or offloading to a distributed compute framework like Dask. A single-threaded Python loop is a career-limiting choice at scale.

-----

## 📊 Section 2: Statistical Representations (Feature Engineering)

> **“All models are wrong, but some are useful. Bag-of-Words is wrong in a deeply principled way.”**

Before the embedding revolution, we represented language as sparse, high-dimensional vectors. Understanding *why* these methods work (and fail) is essential to understanding *why* Transformers work better.

-----

### 2.1 Bag-of-Words (BoW)

BoW represents each document as a vector of **token counts** over a fixed vocabulary $V$. Order is discarded entirely — hence the name.

**Formal Definition:**

Given vocabulary $V = {w_1, w_2, \ldots, w_{|V|}}$ and document $d$, the BoW vector $\mathbf{x} \in \mathbb{R}^{|V|}$ is:

$$x_i = \text{count}(w_i, d) = \sum_{t \in d} \mathbf{1}[t = w_i]$$

**Example:**

```
Doc 1: "the cat sat on the mat"  →  {"the": 2, "cat": 1, "sat": 1, "on": 1, "mat": 1}
Doc 2: "the dog sat on the log"  →  {"the": 2, "dog": 1, "sat": 1, "on": 1, "log": 1}
```

**The core failure:** `"cat"` and `"dog"` are equidistant in BoW space even though they’re both animals. `"cat"` and `"tiger"` are also equidistant, despite being in the same biological family. The representational geometry is completely arbitrary.

-----

### 2.2 TF-IDF: Teaching BoW to Recognise the Rare and Valuable

TF-IDF weights token counts by their **discriminative power across the corpus** — rewarding rare, document-specific terms and penalising ubiquitous ones.

**Term Frequency (TF):**

$$\text{TF}(t, d) = \frac{\text{count}(t, d)}{\sum_{t’ \in d} \text{count}(t’, d)}$$

This normalises for document length. A 1000-word document mentioning “entropy” 5 times is not more about entropy than a 50-word document mentioning it 3 times.

**Inverse Document Frequency (IDF):**

$$\text{IDF}(t, D) = \log\left(\frac{|D| + 1}{|{d \in D : t \in d}| + 1}\right) + 1$$

> [!TIP]
> The `+1` smoothing (Laplace correction) prevents division by zero for unseen terms and ensures even terms appearing in every document get a non-zero (though small) IDF weight. scikit-learn uses this exact formulation.

**TF-IDF Score:**

$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$

**Intuition with a Worked Example:**

In a corpus of 1,000 medical papers:

- `"the"` appears in all 1,000 documents → IDF ≈ 0 → near-zero weight regardless of frequency ✓
- `"metformin"` appears in 50 documents → IDF = log(1000/50) ≈ 3.0 → high weight ✓
- `"diabetes"` appears in 400 documents → IDF = log(1000/400) ≈ 0.9 → moderate weight ✓

-----

### 2.3 Decision Matrix: When to Use What

|Feature                    |Bag-of-Words                                   |TF-IDF                                                            |One-Hot Encoding                                               |
|---------------------------|-----------------------------------------------|------------------------------------------------------------------|---------------------------------------------------------------|
|**What it captures**       |Raw token counts                               |Discriminative term weights                                       |Token identity (binary)                                        |
|**Dimensionality**         |$|V|$ (sparse)                                 |$|V|$ (sparse)                                                    |$|V|$ (sparse)                                                 |
|**Handles stop words?**    |❌ Poorly                                       |✅ Implicitly down-weights                                         |❌ No                                                           |
|**Document length bias?**  |✅ Yes (longer docs score higher)               |✅ Normalised                                                      |N/A                                                            |
|**Semantic understanding** |❌ None                                         |❌ None                                                            |❌ None                                                         |
|**Best use case**          |Baseline text classification, quick prototyping|Information retrieval, document similarity, classical ML pipelines|Categorical feature encoding (not typically for full documents)|
|**Handles OOV terms?**     |❌ No                                           |❌ No                                                              |❌ No                                                           |
|**Interpretable features?**|✅ Yes                                          |✅ Yes                                                             |✅ Yes                                                          |
|**Production viability**   |⚠️ Low (use TF-IDF instead)                     |✅ Solid baseline                                                  |⚠️ Context-dependent                                            |


> [!CAUTION]
> **The Vocabulary Drift Problem.** Both BoW and TF-IDF are fit on a training corpus. Any term appearing in production data that wasn’t in your training vocabulary is silently ignored. In dynamic domains (social media, news), this drift can be severe. Monitor your OOV (out-of-vocabulary) rate in production — if it exceeds ~5%, retrain your vectorizer.

-----

### 2.4 From TF-IDF to a Classification Pipeline

```python
"""
ml/tfidf_pipeline.py

A reproducible scikit-learn pipeline: TF-IDF → Logistic Regression.

Using sklearn.pipeline.Pipeline is non-negotiable in production. It:
  1. Prevents data leakage (the vectorizer fits only on training data).
  2. Enables clean cross-validation via cross_val_score().
  3. Serialises as a single artefact (pickle/joblib), simplifying deployment.
"""

from __future__ import annotations

import joblib
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline


def build_tfidf_pipeline(
    max_features: int = 50_000,
    ngram_range: tuple[int, int] = (1, 2),
    C: float = 1.0,
    max_iter: int = 1000,
) -> Pipeline:
    """
    Construct a TF-IDF → LogisticRegression sklearn Pipeline.

    Args:
        max_features:  Cap vocabulary size. Prevents memory blowout on large corpora.
        ngram_range:   (1,2) captures both unigrams and bigrams.
                       "not good" as a bigram is far more informative than
                       "not" and "good" as independent unigrams.
        C:             Inverse regularisation strength. Smaller = stronger L2 regularisation.
        max_iter:      Solver iteration limit. Increase if convergence warnings appear.

    Returns:
        An unfitted sklearn Pipeline.
    """
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=max_features,
                    ngram_range=ngram_range,
                    sublinear_tf=True,     # Apply log(1 + TF) — compresses outlier counts
                    strip_accents="unicode",
                    analyzer="word",
                    min_df=2,              # Ignore terms appearing in < 2 docs (noise)
                    max_df=0.95,           # Ignore terms in > 95% of docs (stopwords)
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    C=C,
                    max_iter=max_iter,
                    solver="saga",         # Efficient for large, sparse matrices
                    multi_class="multinomial",
                    n_jobs=-1,             # Parallelise across all CPU cores
                ),
            ),
        ]
    )


def evaluate_pipeline(
    pipeline: Pipeline,
    X_train: list[str],
    X_test: list[str],
    y_train: list[int | str],
    y_test: list[int | str],
    target_names: list[str] | None = None,
) -> dict:
    """
    Fit a pipeline and return a structured evaluation report.

    Args:
        pipeline:     An unfitted sklearn Pipeline.
        X_train/test: Raw text documents.
        y_train/test: Labels.
        target_names: Human-readable class names for the report.

    Returns:
        Dictionary containing accuracy, cv_scores, and the classification report string.
    """
    # Train: the pipeline ensures TF-IDF is fit ONLY on training data
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    # Cross-validation on the training set for a more honest estimate
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1_macro")

    report = classification_report(y_test, y_pred, target_names=target_names)
    accuracy = np.mean(y_pred == y_test)

    print(f"\n{'='*60}")
    print(f"  Test Accuracy:  {accuracy:.4f}")
    print(f"  CV F1 (macro):  {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"{'='*60}\n")
    print(report)

    return {
        "accuracy": accuracy,
        "cv_scores": cv_scores,
        "report": report,
    }


def save_pipeline(pipeline: Pipeline, path: str) -> None:
    """Serialise a fitted pipeline to disk using joblib (preferred over pickle for sklearn)."""
    joblib.dump(pipeline, path)
    print(f"✅ Pipeline saved → {path}")


# ── Demo run on 20 Newsgroups ───────────────────────────────────────────────
if __name__ == "__main__":
    # Four semantically distinct categories to keep the demo clean
    categories = ["sci.med", "sci.space", "talk.politics.guns", "rec.sport.baseball"]

    print("📥 Loading 20 Newsgroups dataset...")
    data = fetch_20newsgroups(
        subset="all",
        categories=categories,
        remove=("headers", "footers", "quotes"),  # Remove metadata — test generalisation
    )

    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42, stratify=data.target
    )

    pipeline = build_tfidf_pipeline(max_features=30_000, ngram_range=(1, 2))
    results = evaluate_pipeline(
        pipeline, X_train, X_test, y_train, y_test, target_names=data.target_names
    )

    save_pipeline(pipeline, "models/tfidf_logreg_pipeline.joblib")
```

> [!TIP]
> **The `sublinear_tf=True` trick.** Raw TF gives `"python"` a score of 10 if it appears 10 times vs. 1. But does ten mentions *really* mean ten times the relevance? `log(1 + tf)` compresses this — 1 mention gives 1.0, 10 mentions gives 2.4, 100 mentions gives 4.6. Much more representative of actual signal.

-----

## 🤖 Section 3: From Dense Vectors to Transformers (Modeling)

> **“The journey from counting words to computing attention is the entire history of NLP, compressed.”**

### 3.1 Word2Vec: Learning Semantic Space

Word2Vec (Mikolov et al., 2013) was the paradigm shift that changed NLP. Instead of hand-crafted sparse features, it **learns dense vector representations** from the distributional hypothesis:

> *“A word is characterised by the company it keeps.”* — Firth (1957)

Words appearing in similar contexts should have similar vectors. `"cat"` and `"dog"` both appear near `"pet"`, `"fur"`, `"veterinarian"` — so they should be geometrically close in embedding space.

#### The Two Architectures

**CBOW (Continuous Bag-of-Words):** Predict the centre word from its surrounding context.

```
Context: ["the", "sat", "on", "mat"]  →  Predict: "cat"
```

$$\text{Objective: } \underset{\theta}{\text{maximise}} \quad \log P(w_t \mid w_{t-c}, \ldots, w_{t-1}, w_{t+1}, \ldots, w_{t+c})$$

CBOW is faster to train and smoother over frequent words — works well for large corpora.

**Skip-Gram:** Predict surrounding context words from the centre word.

```
Input: "cat"  →  Predict: ["the", "sat", "on", "mat"]
```

$$\text{Objective: } \underset{\theta}{\text{maximise}} \quad \sum_{-c \leq j \leq c, j \neq 0} \log P(w_{t+j} \mid w_t)$$

Skip-gram is slower but dramatically better at capturing rare word semantics — the architecture of choice when your vocabulary includes domain-specific jargon or low-frequency technical terms.

#### Semantic Arithmetic: The Magic

The celebrated result: vector arithmetic encodes semantic relationships.

$$\vec{\text{king}} - \vec{\text{man}} + \vec{\text{woman}} \approx \vec{\text{queen}}$$

$$\vec{\text{Paris}} - \vec{\text{France}} + \vec{\text{Germany}} \approx \vec{\text{Berlin}}$$

This is not a trick. It’s a geometric consequence of the co-occurrence structure learned from billions of words. The embedding space has *structure*.

-----

### 3.2 Visualising Semantic Space: The PCA → t-SNE Workflow

You have 300-dimensional word vectors. You want to plot them. You cannot directly visualise 300 dimensions. Here is the professional workflow — and more importantly, *why* each step exists.

#### The Visualisation Paradox

The challenge: t-SNE is notoriously good at revealing local cluster structure, but it has serious weaknesses when applied directly to high-dimensional data:

- **Computational cost scales as** $O(n^2)$ in naive implementations ($O(n \log n)$ with Barnes-Hut approximation, but still painful for 50K+ vectors)
- **Crowding problem:** In high dimensions, all points tend to be equidistant. t-SNE struggles to find meaningful gradients to optimise.
- **t-SNE destroys global structure.** The distance between clusters in a t-SNE plot is *not* meaningful — only within-cluster topology is preserved.

#### The Solution: PCA First, t-SNE Second

**Step 1 — PCA (Principal Component Analysis):** Reduce from $d = 300$ to $d = 50$.

PCA finds the orthogonal directions of maximum variance in the data. It is:

- **Linear** — preserves global structure and inter-cluster relationships
- **Deterministic** — same data always gives same result (reproducible)
- **Noise-filtering** — the last principal components capture noise; discarding them is a feature, not a bug

At 50 dimensions, we’ve removed the bulk of noise while retaining the principal semantic axes. The crowding problem is dramatically reduced.

**Step 2 — t-SNE (t-Distributed Stochastic Neighbour Embedding):** Reduce from $d = 50$ to $d = 2$.

t-SNE minimises the divergence between a probability distribution over pairwise distances in the high-dimensional space and a corresponding distribution in the low-dimensional space, using heavy-tailed Student-t distributions (which alleviate the crowding problem):

$$\text{KL}(P | Q) = \sum_{i \neq j} p_{ij} \log \frac{p_{ij}}{q_{ij}}$$

It excels at revealing **local neighbourhood structure** and **cluster membership** — exactly what you want for visualising whether semantically related words cluster together.

```python
"""
visualisation/semantic_space.py

Visualise Word2Vec embeddings using the PCA → t-SNE workflow.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


def visualise_semantic_space(
    word_vectors: KeyedVectors,
    words: list[str],
    pca_components: int = 50,
    tsne_components: int = 2,
    perplexity: float = 30.0,
    random_state: int = 42,
    figsize: tuple[int, int] = (14, 10),
) -> None:
    """
    Visualise word embeddings via the PCA (denoising) → t-SNE (clustering) pipeline.

    Args:
        word_vectors:    Loaded gensim KeyedVectors (e.g., Word2Vec, FastText).
        words:           List of words to visualise. Filter to words in vocabulary.
        pca_components:  Intermediate PCA dimensions. 50 is the standard default.
        tsne_components: Final visualisation dimensions. Almost always 2.
        perplexity:      t-SNE perplexity (roughly: expected cluster size).
                         Typical range: 5–50. Tune based on dataset size.
        random_state:    Ensures reproducible t-SNE output (important for papers).
        figsize:         Matplotlib figure dimensions in inches.
    """
    # Filter to vocabulary members only
    valid_words = [w for w in words if w in word_vectors]
    if len(valid_words) < len(words):
        missing = set(words) - set(valid_words)
        print(f"⚠️  {len(missing)} words not in vocabulary: {missing}")

    vectors = np.array([word_vectors[w] for w in valid_words])
    n_samples, n_dim = vectors.shape
    print(f"📐 Input shape: {n_samples} words × {n_dim} dimensions")

    # ── Step 1: PCA ──────────────────────────────────────────────────────────
    effective_pca = min(pca_components, n_samples - 1, n_dim)
    print(f"🔵 PCA: {n_dim}D → {effective_pca}D (noise reduction + cost savings)")
    pca = PCA(n_components=effective_pca, random_state=random_state)
    vectors_pca = pca.fit_transform(vectors)

    explained_var = pca.explained_variance_ratio_.sum()
    print(f"   Variance retained: {explained_var:.1%}")

    # ── Step 2: t-SNE ────────────────────────────────────────────────────────
    effective_perplexity = min(perplexity, n_samples - 1)
    print(f"🟣 t-SNE: {effective_pca}D → {tsne_components}D (local cluster visualisation)")
    tsne = TSNE(
        n_components=tsne_components,
        perplexity=effective_perplexity,
        n_iter=1000,
        random_state=random_state,
        learning_rate="auto",
        init="pca",             # PCA init is more stable than random
    )
    vectors_2d = tsne.fit_transform(vectors_pca)

    # ── Plot ─────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(vectors_2d[:, 0], vectors_2d[:, 1], alpha=0.7, s=80, color="#4A90D9")

    for i, word in enumerate(valid_words):
        ax.annotate(
            word,
            xy=(vectors_2d[i, 0], vectors_2d[i, 1]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
        )

    ax.set_title(
        f"Semantic Space: Word2Vec Embeddings\n"
        f"PCA ({n_dim}D → {effective_pca}D) → t-SNE ({effective_pca}D → 2D)",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel("t-SNE Dimension 1 (local structure only — axis values have no absolute meaning)")
    ax.set_ylabel("t-SNE Dimension 2")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("outputs/semantic_space.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("✅ Saved → outputs/semantic_space.png")
```

> [!CAUTION]
> **The t-SNE Interpretation Trap.** The **distances between clusters** in a t-SNE plot are **not interpretable**. Two clusters that look far apart may be close in the original space; two that look adjacent may be far apart. This is the most common misinterpretation of t-SNE visualisations in published papers. If you need inter-cluster distance preservation, use UMAP instead — it preserves both local and (approximately) global structure.

-----

### 3.3 The Transformer Shift: Attention Is All You Need

#### The Core Problem with Word2Vec

Word2Vec assigns each word a **single static vector**. But `"bank"` in `"river bank"` and `"bank account"` are entirely different senses. Word2Vec has no mechanism to distinguish them — it averages over all contexts during training, producing a semantic compromise that precisely captures neither.

The Transformer solves this with **contextualised representations**: the vector for `"bank"` is computed *dynamically* based on the full surrounding sequence.

#### Self-Attention: The Mechanism

For each token in a sequence, self-attention computes a weighted sum of all other tokens’ representations. The weights are determined by learned **Query**, **Key**, and **Value** projections.

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

Where:

- $Q = XW_Q$ — “What am I looking for?”
- $K = XW_K$ — “What information do I hold?”
- $V = XW_V$ — “What information do I pass forward?”
- $\sqrt{d_k}$ — Scaling factor preventing softmax saturation in high dimensions

**Multi-Head Attention** runs $h$ attention mechanisms in parallel, each attending to different representational subspaces (syntactic vs. semantic, local vs. long-range dependencies), then concatenates and projects:

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) W_O$$

#### BERT vs. GPT: The Architectural Fork

The Transformer architecture can be used in fundamentally different ways, and the choice determines *everything* about what tasks the model excels at.

```
ENCODER-ONLY (BERT family)              DECODER-ONLY (GPT family)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BIDIRECTIONAL ATTENTION                 CAUSAL (UNIDIRECTIONAL) ATTENTION
                                        
[CLS] The cat [MASK] on the mat        The cat sat on the [NEXT TOKEN?]
  ↑     ↑      ↑   ← ← ↑    ↑           ↑     ↑    ↑    ↑     ↑
  └─────┴──────┴─── ALL ─────┘           └─────┴────┴────┘     ↑
                                                          (only past visible)

Every token attends to every other.     Each token attends only to prior tokens.
Full context awareness.                 Autoregressive generation.

PRE-TRAINING TASK:                      PRE-TRAINING TASK:
Masked Language Modelling (MLM)         Next Token Prediction (CLM)
+ Next Sentence Prediction (NSP)

STRENGTHS:                              STRENGTHS:
✅ Text classification                  ✅ Text generation
✅ Named Entity Recognition             ✅ Completion & summarisation  
✅ Question Answering (extractive)      ✅ Code generation
✅ Sentence embeddings                  ✅ In-context learning (few-shot)

EXAMPLES:                               EXAMPLES:
BERT, RoBERTa, DeBERTa, ALBERT          GPT-2/3/4, LLaMA, Mistral, Claude
```

> [!TIP]
> **The Practical Decision Rule.** If you’re building a **classifier, information extractor, or RAG retriever** — reach for an encoder (e.g., `sentence-transformers` with a RoBERTa backbone). If you’re building a **generation system, chatbot, or agent** — reach for a decoder (GPT-4, Claude, LLaMA). The architectural choice isn’t aesthetic — it’s fundamental to what the model *can* do.

> [!CAUTION]
> **The Fine-Tuning Trap.** BERT-family models are frequently fine-tuned for generation tasks where a decoder is the correct architecture. The bidirectional attention masks prevent genuine left-to-right generation — you’re fighting the model’s own inductive biases. Use the right architecture for the right task. This is a common mistake in production systems built by teams who learned from outdated tutorials.

-----

## 🗺️ The Full Roadmap at a Glance

```
Classical NLP                          Modern LLM Engineering
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tokenisation    →    Still essential for context management & RAG chunking
Stemming/Lemma  →    Text normalisation in evaluation & retrieval
BoW / TF-IDF    →    Lightweight re-rankers in hybrid RAG pipelines
Word2Vec        →    Foundation for understanding dense retrieval & FAISS
PCA + t-SNE     →    Embedding space debugging & cluster analysis
Self-Attention  →    The engine of every production LLM
BERT            →    Backbone of embedding models & semantic search
GPT             →    The architecture of every chat/generation system
```
-----

## 📚 Further Reading

|Resource                                                                                        |Why It Matters                                                 |
|------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
|[Speech and Language Processing — Jurafsky & Martin](https://web.stanford.edu/~jurafsky/slp3/)  |The canonical NLP textbook. Free online. Non-negotiable.       |
|[The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)|The clearest visual explanation of self-attention in existence.|
|[Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762)                            |The paper. Read it. Annotate it. Read it again.                |
|[BERT: Pre-training of Deep Bidirectional Transformers (2018)](https://arxiv.org/abs/1810.04805)|Understand what you’re fine-tuning.                            |
|[Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers)             |Production-grade API reference.                                |
|[spaCy Documentation](https://spacy.io/usage)                                                   |The industrial-strength NLP library reference.                 |
|[Conventional Commits Spec](https://conventionalcommits.org)                                    |The commit message standard. Adopt it.                         |

-----
