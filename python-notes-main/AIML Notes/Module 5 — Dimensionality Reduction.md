# Module 5 — Dimensionality Reduction
> *"All models are compressed views of reality. The art is choosing which view preserves what matters."*

---

## Table of Contents
- [Why This Module Matters](#why-this-module-matters)
- [ELI5](#eli5)
- [Core Concepts](#core-concepts)
- [Math Intuition](#math-intuition)
- [Key Formulas and Equations](#key-formulas-and-equations)
- [Algorithms Breakdown](#algorithms-breakdown)
- [Visual Mental Models](#visual-mental-models)
- [Real-World Applications](#real-world-applications)
- [Engineering Insights](#engineering-insights)
- [Production Notes](#production-notes)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)
- [Minimal Practical Workflow](#minimal-practical-workflow)
- [Python Ecosystem](#python-ecosystem)
- [Interview Questions](#interview-questions)
- [How to Explain in an Interview](#how-to-explain-in-an-interview)
- [Summary Cheatsheet](#summary-cheatsheet)

---

## Why This Module Matters

Every real-world dataset is embedded in a high-dimensional space — hundreds of pixels, thousands of genes, millions of tokens. Raw dimensionality is almost always **wasteful**:

- Most dimensions are **correlated** (redundant)
- Many dimensions are **noise** (irrelevant)
- A handful of **latent directions** explain nearly all meaningful structure

Dimensionality reduction is the bridge between raw data and **latent representation** — the compact, structured space that machine learning models actually reason in. This is not merely a preprocessing trick. It is the conceptual foundation of:

| Downstream Technique | DR Role |
|---|---|
| Deep Autoencoders | Learn nonlinear DR end-to-end |
| Word Embeddings (Word2Vec, GloVe) | Project words into latent semantic space |
| Diffusion Models / VAEs | Sample from compressed latent manifolds |
| Face Recognition | Identity lives in ~50D subspace of 10⁶-pixel images |
| Drug Discovery | Molecular property manifolds in chemical space |

Understanding **PCA**, **ICA**, and **LDA** geometrically is foundational to understanding representation learning at any scale.

---

## ELI5

Imagine you photograph a coffee mug from 1000 different angles. You have 1000 images — but there are really only **3 degrees of freedom**: rotation around X, Y, Z. The other 999 dimensions are redundant noise.

**Dimensionality reduction** asks: *"What are the smallest number of knobs that explain the data you see?"*

- **PCA** finds the directions of **maximum spread** — the axes along which data varies most.
- **ICA** finds directions that are **statistically independent** — the true hidden sources mixed together.
- **LDA** finds directions that **best separate classes** — the knife-edge between categories.

Each is a different answer to: *"Which way should I look to see the most signal?"*

---

## Core Concepts

### 1. Curse of Dimensionality

High-dimensional spaces behave counterintuitively:

```
In d dimensions, the volume of a unit hypersphere relative to the
enclosing hypercube → 0 as d → ∞.

All points become equidistant.
All vectors become nearly orthogonal.
Nearest-neighbor search becomes meaningless.
```

**Geometric intuition:**

```
1D:  [----X----X----X----]          Distances meaningful
2D:  [  X       X        ]          Still okay
     [        X          ]
10D: Every X is the same distance from every other X
     Euclidean distances lose discriminative power
```

**The practical consequences:**
- k-NN accuracy collapses
- Density estimates require exponentially more data
- Regularization becomes critical
- Models that don't reduce dimensionality implicitly overfit the ambient space

> **Key insight:** Data doesn't actually *live* in its ambient dimension. It lives on a low-dimensional **manifold** embedded within it. Dimensionality reduction finds that manifold.

---

### 2. Latent Space

A **latent space** is a lower-dimensional coordinate system that captures the underlying structure of data.

```
Ambient Space (observed)       Latent Space (discovered)
────────────────────────       ─────────────────────────
28×28 = 784 pixel values  ──►  2D: (style, digit identity)
1000-gene expression      ──►  3D: (cell type, stress, cycle)
BERT token embeddings     ──►  k-D: (semantics, syntax, ...)
```

The **encoder** maps `x ∈ ℝᵈ → z ∈ ℝᵏ` where `k ≪ d`.  
The **decoder** reconstructs `z ∈ ℝᵏ → x̂ ∈ ℝᵈ`.

Linear DR methods (PCA, ICA, LDA) use a **linear projection matrix** `W ∈ ℝᵈˣᵏ`:

```
z = Wᵀx       (encode: project onto latent axes)
x̂ = Wz        (decode: reconstruct from latent code)
```

---

### 3. Projection

Projection is the mechanism of dimensionality reduction. To project vector **x** onto direction **w**:

```
          x·w
proj =  ───────  ×  w
          w·w

Scalar coordinate:  z = xᵀw / ‖w‖
```

**Geometric picture:**

```
        x
        ●
       /|
      / |
     /  |  ← "shadow" / perpendicular drop
    /   |
───●────●──────────────── w direction
   0    z = xᵀw̃
```

The projected value `z` is **how far along direction w the point x lies**.  
DR finds the set of `w` vectors (axes) that make these projections maximally informative.

---

### 4. Variance as Signal

If projected values of all data points cluster near zero → the direction carries no information.  
If projected values spread widely → the direction captures real structure.

```
Low-variance direction:        High-variance direction:
   ● ● ● ●●● ● ● ●               ●   ●     ●        ●
   All bunched together           Spread out → signal!
```

**PCA's core principle:** find directions in which projections have **maximum variance**.

---

## Math Intuition

### Covariance Matrix: The Shape of the Cloud

Given data matrix `X ∈ ℝⁿˣᵈ` (n samples, d features), the **covariance matrix** is:

```
         1
Σ =  ───────  XᵀX        (when X is mean-centered)
       n - 1
```

`Σ ∈ ℝᵈˣᵈ` encodes:
- **Diagonal entries** `Σᵢᵢ = Var(xᵢ)` — how much feature i varies
- **Off-diagonal entries** `Σᵢⱼ = Cov(xᵢ, xⱼ)` — how features i and j co-vary

**Geometric meaning:**

```
Σ is the matrix that describes the shape, orientation,
and scale of the data ellipsoid.

Circular cloud:        Σ = σ²I    (isotropic, no preferred direction)
Elongated ellipsoid:   Σ has large off-diagonal entries
                       (strong correlations = redundant dimensions)
```

The **eigenvectors of Σ** point along the principal axes of the data ellipsoid.  
The **eigenvalues of Σ** give the squared semi-axis lengths (= variances along those axes).

---

### Eigen Decomposition: Rotating to the Natural Axes

Any symmetric matrix `Σ` can be decomposed as:

```
Σ = Q Λ Qᵀ

where:
  Q  = matrix of eigenvectors (rotation matrix — orthonormal basis)
  Λ  = diagonal matrix of eigenvalues λ₁ ≥ λ₂ ≥ ... ≥ λd ≥ 0
  Qᵀ = inverse rotation (since Q is orthogonal)
```

**Intuition: Eigen decomposition rotates to the coordinate system where the covariance matrix is diagonal — where all dimensions are uncorrelated.**

```
Original space:           Eigenvector space:
  x₂ ↑                     z₂ ↑
     |  ↗↗↗ (correlated)       |
     | ↗↗↗                     |●  ●    (uncorrelated)
     |↗↗↗                   ●  |  ●
  ───┼──────── x₁          ────┼──────── z₁ (PC1)
                             ●● | ●
```

Each **eigenvector** `qᵢ` is a direction in the original feature space.  
Each **eigenvalue** `λᵢ` tells you how much variance is captured along `qᵢ`.

---

### The PCA Objective (Geometric Derivation)

**Step 1.** Find `w₁` that maximizes projected variance:

```
            wᵀΣw
w₁ = argmax ──────
  ‖w‖=1      wᵀw

Solution: w₁ = eigenvector of Σ with largest eigenvalue λ₁
```

**Step 2.** Find `w₂` perpendicular to `w₁` that maximizes remaining variance.

**Step 3.** Repeat. The k-th PC is the k-th eigenvector of Σ.

The result: a set of **orthogonal axes** (principal components) ranked by explained variance.

---

### Statistical Independence vs. Uncorrelatedness

This is the key distinction between **PCA** and **ICA**:

| Property | Definition | Implication |
|---|---|---|
| **Uncorrelated** | `E[xᵢxⱼ] = 0` | Linear relationship removed |
| **Independent** | `p(xᵢ, xⱼ) = p(xᵢ)p(xⱼ)` | No relationship of any kind |

Independence is **strictly stronger** than uncorrelatedness.

```
PCA guarantees: Cov(z₁, z₂) = 0   (uncorrelated PCs)
ICA guarantees: p(z₁, z₂) = p(z₁)p(z₂)  (independent components)

Uncorrelated ≠ Independent (except for Gaussians, where they're equivalent)
```

**Geometric intuition:**

```
Two variables can have zero covariance but still be dependent:
  z₁ ~ Uniform[-1, 1],   z₂ = z₁²
  Cov(z₁, z₂) = 0 ✓     but knowing z₁ tells you |z₂| ✗
```

ICA exploits **non-Gaussianity** to find directions of true independence. It uses higher-order statistics (kurtosis, negentropy) as its compass.

---

### Fisher's Criterion (LDA)

LDA asks a different question: not "where does data spread?" but "where do classes separate?"

```
         Between-class scatter
J(w) = ──────────────────────────
          Within-class scatter

       wᵀ Sᵦ w
     = ────────     →   maximize this ratio
       wᵀ Sᵥ w
```

Where:
- `Sᵦ = Σᵢ nᵢ(μᵢ - μ)(μᵢ - μ)ᵀ` — **between-class scatter** (how far class means are from global mean)
- `Sᵥ = Σᵢ Σⱼ∈classᵢ (xⱼ - μᵢ)(xⱼ - μᵢ)ᵀ` — **within-class scatter** (spread inside each class)

**Solution:** Eigenvectors of `Sᵥ⁻¹Sᵦ`

**Geometric picture:**

```
PCA finds:                    LDA finds:
  ●●●○○○○                       ●●●  |  ○○○
  ●●●○○○    ←── PC1              ●●● |  ○○○    ←── LD1
  Maximizes total spread         Maximizes class gap / within spread

PCA ignores labels.           LDA uses labels to sharpen separation.
```

---

## Key Formulas and Equations

### PCA

$$\Sigma = \frac{1}{n-1} X^T X \quad \text{(covariance matrix, mean-centered X)}$$

$$\Sigma = Q \Lambda Q^T \quad \text{(eigen decomposition)}$$

$$Z = X Q_k \quad \text{(projection to k-dimensional latent space)}$$

$$\text{Explained Variance Ratio} = \frac{\lambda_i}{\sum_j \lambda_j}$$

$$\text{Reconstruction: } \hat{X} = Z Q_k^T$$

$$\text{Reconstruction Error: } \|X - \hat{X}\|_F^2 = \sum_{i=k+1}^d \lambda_i$$

---

### ICA (FastICA)

$$X = AS \quad \text{(mixing model: A = mixing matrix, S = sources)}$$

$$S = WX \quad \text{(W = A⁻¹ = unmixing matrix)}$$

$$\text{Negentropy: } J(y) \approx [E\{G(y)\} - E\{G(\nu)\}]^2$$

where `G` is a nonquadratic function (e.g., `G(u) = log cosh(u)`) and `ν ~ N(0,1)`.

**FastICA update rule:**

$$w \leftarrow E\{xg(w^T x)\} - E\{g'(w^T x)\}w$$

$$w \leftarrow w / \|w\|$$

---

### LDA

$$S_B = \sum_i n_i (\mu_i - \mu)(\mu_i - \mu)^T$$

$$S_W = \sum_i \sum_{x \in C_i} (x - \mu_i)(x - \mu_i)^T$$

$$J(w) = \frac{w^T S_B w}{w^T S_W w} \quad \text{(Fisher criterion — maximize)}$$

$$\text{Solve: } S_W^{-1} S_B w = \lambda w$$

$$\text{Max discriminant directions: } \min(d, C-1) \quad \text{(C = number of classes)}$$

---

### Explained Variance and Scree Plot

```
Cumulative Explained Variance:

CVR(k) = Σᵢ₌₁ᵏ λᵢ / Σᵢ₌₁ᵈ λᵢ

Scree plot: λᵢ vs. i
Look for the "elbow" — where eigenvalues stop dropping sharply
```

---

## Algorithms Breakdown

### PCA — Step by Step

```
Input:  X ∈ ℝⁿˣᵈ (n samples, d features)
Output: Z ∈ ℝⁿˣᵏ (n samples, k latent dimensions), k ≪ d

1. CENTER:      X̃ = X - mean(X, axis=0)
2. COVARIANCE:  Σ = (1/n-1) X̃ᵀX̃          [d×d matrix]
3. EIGEN:       Σ = QΛQᵀ                   [sort by λ descending]
4. SELECT:      Qₖ = Q[:, :k]              [top-k eigenvectors]
5. PROJECT:     Z = X̃ Qₖ                  [n×k latent codes]
6. RECONSTRUCT: X̂ = Z Qₖᵀ + mean(X)       [n×d reconstruction]
```

**Practical:** Use SVD instead of explicit covariance for numerical stability:

```
X̃ = U Σ Vᵀ    (SVD)

PCs = V columns
Scores = U Σ = X̃ V
Variance explained by PC i = σᵢ² / Σ σⱼ²
```

---

### ICA — FastICA Algorithm

```
Input:  X ∈ ℝⁿˣᵈ (assumed to be mixtures of d independent sources)
Output: S ∈ ℝⁿˣᵈ (estimated source signals)

PREPROCESSING:
1. Center: X̃ = X - mean(X)
2. Whiten: X_w = Λ⁻¹/² Qᵀ X̃   [decorrelate + normalize variance]
   → After whitening: Cov(X_w) = I (spherical cloud)

CORE LOOP (for each independent component):
3. Initialize w randomly, ‖w‖ = 1
4. Repeat until convergence:
   a. w_new = E{X_w g(wᵀX_w)} - E{g'(wᵀX_w)} w
   b. Orthogonalize w_new w.r.t. previous components (Gram-Schmidt)
   c. Normalize: w = w_new / ‖w_new‖
5. Source i = wᵢᵀ X_w

INTUITION:
- Whitening removes second-order structure (correlations) → PCA step
- FastICA then uses higher-order statistics (kurtosis / negentropy) to
  find the directions of maximum non-Gaussianity
- Central Limit Theorem guarantees: mixtures of signals are MORE Gaussian
  than the original sources. So maximum non-Gaussianity ≈ original sources.
```

---

### LDA — Step by Step

```
Input:  X ∈ ℝⁿˣᵈ with class labels y ∈ {1,...,C}
Output: Z ∈ ℝⁿˣᵏ, k = min(d, C-1)

1. MEANS:     μᵢ = mean(X[y==i]),  μ = mean(X)
2. SCATTER:   Compute Sᵦ (between-class) and Sᵥ (within-class)
3. SOLVE:     Sᵥ⁻¹Sᵦ W = W Λ    [generalized eigenproblem]
4. SELECT:    Top-k eigenvectors W_k ∈ ℝᵈˣᵏ
5. PROJECT:   Z = X W_k

NOTES:
- Sᵥ may be singular if n < d → use pseudoinverse or PCA-then-LDA
- LDA is a generative model: assumes Gaussian class-conditionals
- Maximum k = C - 1 (hard constraint from rank of Sᵦ)
```

---

## Visual Mental Models

### The Data Ellipsoid

```
       x₂
        │    ╭──────────────╮
        │  ╭──────────────────╮
        │ ╭──────────────────────╮
        │ │     ↗ PC1 (major axis)│
        │ │   ↗                   │
        │ │ ↗                     │
        │╰──────────────────────╯
        │  ╰──────────────────╯
        │    ╰──────────────╯
        └─────────────────────── x₁

PC1 = direction of largest spread (longest ellipsoid axis)
PC2 = direction of second-largest spread, ⊥ to PC1
λ₁  = variance along PC1 (long axis length²)
λ₂  = variance along PC2 (short axis length²)

Discarding PC2: project all points onto PC1 line
→ 1D representation, minimal information loss
```

---

### Scree Plot and Elbow Method

```
Eigenvalue
   │
 4 ┤ ●
   │   ●
 2 ┤     ●
   │       ●
 1 ┤         ● ● ● ● ● ● ●
   │
   └─────────────────────── Component #
       1  2  3  4  5  6  7

         ↑
        Elbow here → retain 3 components
        Everything after ≈ noise floor

Cumulative Variance Curve:
100% ┤              ●─────────●
 80% ┤          ●
 60% ┤      ●
 40% ┤   ●
 20% ┤  ●
  0% └──────────────────────────
     PC1 PC2 PC3 PC4 PC5 PC6

→ "95% rule": choose k where CVR(k) ≥ 0.95
```

---

### PCA vs ICA Mental Model

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ORIGINAL SOURCES (unknown to us)
   Source 1: ─/\/\/\/\/─   (speech signal)
   Source 2: ─▓░▓░▓░▓░─   (music signal)

MIXING MATRIX A scrambles them:
   Observed 1 = 0.7×S1 + 0.3×S2
   Observed 2 = 0.4×S1 + 0.6×S2

PCA would:
   Find the orthogonal directions of max variance
   Result: rotated versions of mixtures — still mixed!
   Gives uncorrelated components, not independent sources.

ICA would:
   Exploit non-Gaussianity to "unmix"
   Result: recovered S1 and S2 (up to scale and order)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### LDA Class Separation Geometry

```
           LD1 direction →
─────────────────────────────────────
   Class A: ●●●●●●         (tight cluster)
   Class B:         ○○○○○  (tight cluster)

           ↑
   Fisher wants:
     Large GAP between cluster centers (maximize Sᵦ)
     Small SPREAD within each cluster  (minimize Sᵥ)

   PCA might find this:      LDA finds this:

   ●●  ○○                   ●●●● | ○○○○
   ●● ○○     PC1 →          ████ | ████  LD1 →
   ●○ ○                     (maximally separated)
   (classes mixed on PC1)
```

---

### Dimensionality Reduction Taxonomy

```
                    DIMENSIONALITY REDUCTION
                            │
            ┌───────────────┼───────────────┐
          Linear          Linear          Linear
         (Variance)   (Independence)   (Supervision)
            │                │                │
           PCA              ICA              LDA
            │
    ┌───────┴────────┐
  Kernel-PCA      Randomized
  (nonlinear)     SVD (fast)

          Nonlinear Methods (beyond this module):
          t-SNE, UMAP, Autoencoders, Isomap
```

---

## Real-World Applications

### PCA Applications

| Domain | Input Dimensions | PCA Finds |
|---|---|---|
| Face Recognition (Eigenfaces) | 10,000 pixels | ~50 "eigenfaces" |
| Finance | 500 stocks | Market/sector/idio factors |
| Genomics | 20,000 genes | Population structure |
| NLP | 50,000-dim BoW | Latent semantic axes |
| Sensor Arrays | 1000 sensors | Common-mode noise, signal modes |

**Eigenfaces intuition:**
```
Any face ≈ mean_face + α₁×eigenface₁ + α₂×eigenface₂ + ...

The latent code [α₁, α₂, ..., α₅₀] is the "face fingerprint"
in a 50D space rather than a 10,000D space.
```

---

### ICA Applications

- **Blind Source Separation:** Separate cocktail party voices recorded by mixed microphones
- **EEG/MEG artifact removal:** Eye blinks, heartbeat, muscle noise are independent sources
- **fMRI:** Identify independent functional brain networks
- **Financial markets:** Identify latent economic factors driving multiple assets

---

### LDA Applications

- **Face recognition:** Fisherfaces (LDA outperforms PCA for same-class lighting variation)
- **Medical diagnosis:** Optimal projection for class separation in biomarker space
- **Text classification:** Find the discriminant direction in document space
- **Feature extraction before SVM/logistic regression**

---

## Engineering Insights

### Numerical: PCA via SVD

Never compute `XᵀX` explicitly — it squares the condition number:

```python
# ❌ Numerically unstable for large/ill-conditioned data
cov = X.T @ X / (n - 1)
eigenvalues, eigenvectors = np.linalg.eigh(cov)

# ✅ Use SVD directly (scipy/sklearn do this internally)
U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)
# Principal components = Vt rows
# Singular values s relate to eigenvalues: λᵢ = sᵢ² / (n-1)
# Scores = U @ diag(s) = X_centered @ Vt.T
```

### Whitening Before ICA

ICA requires whitened (sphericalized) data. Whitening is itself a PCA:

```python
# Whitening: transform to unit covariance sphere
X_pca = X_centered @ eigenvectors        # rotate to PC axes
X_white = X_pca / np.sqrt(eigenvalues)  # scale to unit variance
# Now Cov(X_white) = I
# ICA then only needs to find a rotation of this sphere
```

### LDA with Singular `Sᵥ` (n < d case)

When `n < d`, within-class scatter `Sᵥ` is rank-deficient:

```
Strategy: PCA first, then LDA
1. PCA to reduce d → min(n-C, d_pca)  (ensure Sᵥ is full rank)
2. LDA on PCA-reduced space
3. Combined: optimal compression + discrimination
```

### Incremental / Online PCA

For streaming data or data too large for memory:

```python
from sklearn.decomposition import IncrementalPCA
ipca = IncrementalPCA(n_components=50)
for batch in data_stream:
    ipca.partial_fit(batch)
Z = ipca.transform(new_data)
```

---

## Production Notes

```
┌─────────────────────────────────────────────────────────────┐
│  PRODUCTION CHECKLIST                                       │
├─────────────────────────────────────────────────────────────┤
│ ✅ Fit scaler and PCA on TRAINING data only                 │
│ ✅ Apply same fitted transform to val/test (no re-fit)      │
│ ✅ Save the fitted PCA object (not just the components)     │
│ ✅ Monitor explained variance ratio — log to MLflow         │
│ ✅ Use sklearn Pipeline to prevent data leakage             │
│ ✅ For ICA: set random_state for reproducibility            │
│ ✅ For LDA: verify class balance before computing scatter   │
│ ✅ Version the preprocessing pipeline with the model        │
│ ✅ Document number of components and selection rationale    │
└─────────────────────────────────────────────────────────────┘
```

### Pipeline Pattern

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('pca',    PCA(n_components=0.95)),  # retain 95% variance
    ('clf',    LogisticRegression())
])

pipe.fit(X_train, y_train)
# PCA is fitted only on X_train — no leakage
score = pipe.score(X_test, y_test)
```

### Model Serialization

```python
import joblib

# Save entire fitted pipeline
joblib.dump(pipe, 'model_v1.pkl')

# Load and transform new data — exact same PCA transform
pipe_loaded = joblib.load('model_v1.pkl')
z_new = pipe_loaded.named_steps['pca'].transform(X_new_scaled)
```

---

## Common Mistakes

### ❌ Mistake 1: Fitting PCA on the full dataset (data leakage)

```python
# ❌ WRONG — test statistics leak into PCA fit
pca = PCA(n_components=50).fit(X_all)   # includes test set!
X_train_pca = pca.transform(X_train)
X_test_pca  = pca.transform(X_test)

# ✅ CORRECT
pca = PCA(n_components=50).fit(X_train)   # train only
X_train_pca = pca.transform(X_train)
X_test_pca  = pca.transform(X_test)       # apply fitted transform
```

---

### ❌ Mistake 2: Forgetting to standardize before PCA

```
Features:  Age (range 0-100), Income (range 0-1,000,000)

Without scaling: Income dominates variance purely due to scale.
PC1 ≈ income direction regardless of true structure.

With StandardScaler: each feature contributes based on structure.
```

```python
# ✅ Always scale first
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
pca = PCA().fit(X_scaled)
```

---

### ❌ Mistake 3: Interpreting PCA components as features

PCA components are **linear combinations of all original features**.  
They are not new features with independent meaning — they are **rotated coordinate axes**.

```
PC1 = 0.3×age + 0.7×income - 0.2×debt + ...
# PC1 has no clean real-world interpretation unless you analyze loadings
```

---

### ❌ Mistake 4: Using ICA when sources are Gaussian

ICA fundamentally requires non-Gaussian sources (it exploits higher-order statistics).  
For Gaussian sources, PCA and ICA give the same solution — ICA provides no benefit.

---

### ❌ Mistake 5: Ignoring LDA's maximum-rank constraint

```
With C classes, LDA produces at most C-1 discriminant directions.
→ Binary classification: only 1 LDA direction (scalar projection!)
→ 5-class: at most 4 directions

Don't try to request more components than C-1.
```

---

### ❌ Mistake 6: Using PCA for feature selection

PCA is **feature extraction** (creates new axes), not **feature selection** (selects original features).  
If interpretability requires original features, use variance thresholds or mutual information instead.

---

## Best Practices

### Choosing k (Number of Components)

```python
pca = PCA().fit(X_scaled)
cumvar = np.cumsum(pca.explained_variance_ratio_)

# Rule 1: 95% variance threshold
k_95 = np.searchsorted(cumvar, 0.95) + 1

# Rule 2: Elbow in scree plot (visual)
plt.plot(pca.explained_variance_ratio_)
plt.xlabel('Component'); plt.ylabel('Explained Variance Ratio')

# Rule 3: Kaiser criterion — keep components with λ > 1
#          (in standardized data: average eigenvalue = 1)
k_kaiser = np.sum(pca.explained_variance_ > 1)

# Rule 4: Cross-validation on downstream task
#          Tune k as a hyperparameter in the pipeline
```

### Choosing Between PCA / ICA / LDA

```
┌──────────────────────────────────────────────────────────┐
│  Has class labels?                                       │
│    YES → LDA (maximizes class separation)                │
│    NO  → PCA or ICA                                      │
│                                                          │
│  Non-Gaussian, independent sources?                      │
│    YES → ICA (cocktail party, EEG, blind separation)     │
│    NO  → PCA (compression, visualization, denoising)     │
│                                                          │
│  n ≫ d?    → Any method works                            │
│  n ≈ d?    → Use regularized variants                    │
│  n ≪ d?    → PCA first, then LDA (PCA-LDA pipeline)      │
└──────────────────────────────────────────────────────────┘
```

---

## Minimal Practical Workflow

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, FastICA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.datasets import load_digits
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# ─── Load and Split ───────────────────────────────────────────
X, y = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ─── 1. PCA: Visualization and Compression ───────────────────
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

pca = PCA().fit(X_train_s)

# Scree plot
cumvar = np.cumsum(pca.explained_variance_ratio_)
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.bar(range(1, 21), pca.explained_variance_ratio_[:20])
plt.xlabel('Component'); plt.ylabel('Explained Variance Ratio')
plt.title('Scree Plot')
plt.subplot(1, 2, 2)
plt.plot(cumvar); plt.axhline(0.95, color='r', linestyle='--')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Variance')
plt.title('Variance Explained')
plt.tight_layout(); plt.show()

# 2D visualization
pca2 = PCA(n_components=2).fit(X_train_s)
Z_2d = pca2.transform(X_train_s)
plt.figure(figsize=(8, 6))
scatter = plt.scatter(Z_2d[:, 0], Z_2d[:, 1], c=y_train,
                      cmap='tab10', alpha=0.6, s=10)
plt.colorbar(scatter); plt.title('PCA 2D Projection')
plt.xlabel('PC1'); plt.ylabel('PC2'); plt.show()

# ─── 2. LDA: Supervised Projection ───────────────────────────
lda = LinearDiscriminantAnalysis(n_components=2)
Z_lda = lda.fit_transform(X_train_s, y_train)
plt.figure(figsize=(8, 6))
scatter = plt.scatter(Z_lda[:, 0], Z_lda[:, 1], c=y_train,
                      cmap='tab10', alpha=0.6, s=10)
plt.colorbar(scatter); plt.title('LDA 2D Projection')
plt.xlabel('LD1'); plt.ylabel('LD2'); plt.show()

# ─── 3. ICA: Source Separation ────────────────────────────────
ica = FastICA(n_components=10, random_state=42, max_iter=500)
Z_ica = ica.fit_transform(X_train_s)
print(f"ICA components shape: {Z_ica.shape}")

# ─── 4. Classification Pipeline ──────────────────────────────
results = {}
for name, reducer in [
    ('PCA-95%',  PCA(n_components=0.95)),
    ('LDA',      LinearDiscriminantAnalysis(n_components=9)),
    ('Baseline', PCA(n_components=64)),
]:
    pipe = Pipeline([
        ('scaler',  StandardScaler()),
        ('reducer', reducer),
        ('clf',     LogisticRegression(max_iter=500))
    ])
    pipe.fit(X_train, y_train)
    results[name] = pipe.score(X_test, y_test)

for name, acc in results.items():
    print(f"{name:12s}: {acc:.4f}")
```

---

## Python Ecosystem

| Library | Use Case | Key API |
|---|---|---|
| `sklearn.decomposition.PCA` | PCA, Incremental PCA, Kernel PCA | `.fit()`, `.transform()`, `.explained_variance_ratio_` |
| `sklearn.decomposition.FastICA` | ICA / BSS | `.fit_transform()`, `.components_` |
| `sklearn.discriminant_analysis.LinearDiscriminantAnalysis` | Supervised DR | `.fit_transform()`, `.scalings_` |
| `sklearn.decomposition.TruncatedSVD` | Sparse data, text | `.fit_transform()` |
| `sklearn.decomposition.KernelPCA` | Nonlinear PCA | `kernel='rbf'` |
| `scipy.linalg.svd` | Low-level SVD | Numerical control |
| `numpy.linalg.eigh` | Symmetric eigen decomp | Faster than `eig` for symmetric |
| `plotly.express.scatter` | Interactive latent space plots | `color=labels` |
| `umap-learn` | Nonlinear DR (UMAP) | `UMAP().fit_transform()` |
| `yellowbrick` | Scree plots, DR viz | `PCADecomposition(X, y)` |

---

## Interview Questions

### Conceptual

**Q1: Why does PCA find eigenvectors of the covariance matrix?**
> PCA maximizes the variance of projections. By Lagrangian optimization with orthogonality constraint, the solution is the eigenvectors of `Σ`. The eigenvector with eigenvalue `λ₁` gives the projection with variance `λ₁` — the maximum. This is the **Rayleigh quotient** result.

**Q2: What does the covariance matrix geometrically represent?**
> It describes the shape of the data distribution: a d-dimensional ellipsoid. Its eigenvectors are the principal axes of this ellipsoid, and its eigenvalues are the squared lengths of those axes (proportional to variance).

**Q3: Why does ICA fail when sources are Gaussian?**
> The Central Limit Theorem states that sums of random variables become more Gaussian. ICA identifies sources by finding maximally non-Gaussian directions. If sources are Gaussian, all rotations of them produce identically Gaussian distributions — ICA's objective is flat and has no unique solution. PCA and ICA are equivalent in this case.

**Q4: What is the Fisher criterion and why does it maximize class separation?**
> Fisher's criterion is the ratio of between-class variance to within-class variance. Maximizing it ensures projected class means are far apart while each class's projected spread is small — like pushing clusters apart while squeezing them tight. This is exactly what you want for classification.

**Q5: When does PCA fail as a preprocessing step for classification?**
> PCA maximizes variance, which may be driven by noise or class-irrelevant variation. The most variance-explaining direction could be orthogonal to the class separation direction. LDA avoids this by directly optimizing class separability. Rule of thumb: if the discriminant structure is weaker than other variance sources, PCA can hurt classification.

**Q6: What is the relationship between PCA and SVD?**
> For mean-centered data matrix `X = UΣVᵀ` (SVD), the right singular vectors `V` are the PCA eigenvectors (principal components), `U` contains the normalized scores, and the singular values relate to eigenvalues by `λᵢ = σᵢ²/(n-1)`. SVD is the numerically preferred way to compute PCA — it avoids squaring the condition number.

**Q7: How does reconstruction error relate to eigenvalues?**
> When projecting to the top-k components, the reconstruction error is the sum of **discarded eigenvalues**: `‖X - X̂‖² = Σᵢ₌ₖ₊₁ᵈ λᵢ`. Each eigenvalue represents variance along its eigenvector. Discarding a direction discards that variance as reconstruction error.

**Q8: What is whitening and why does ICA require it?**
> Whitening transforms data so `Cov(X) = I` — a spherical distribution. It removes second-order structure (correlations), reducing the problem from finding a general linear transform to finding just a **rotation** of the whitened data. ICA becomes a rotation search problem after whitening, which is both simpler and more numerically stable.

---

## How to Explain in an Interview

### "Explain PCA in 60 seconds"

> *"PCA finds the directions in which your data spreads the most. Imagine fitting an ellipsoid to your data cloud — PCA finds the principal axes of that ellipsoid, ordered by their length. The first axis points along the direction of maximum spread. We then project all points onto the top-k axes. This is both dimensionality reduction and decorrelation — the projected coordinates are uncorrelated. The key formula: eigenvectors of the covariance matrix, sorted by eigenvalue."*

---

### "Why would you choose LDA over PCA?"

> *"PCA is unsupervised — it finds directions of maximum variance regardless of class labels. If I have class structure in my data, the directions of maximum variance might have nothing to do with class separation. LDA uses the labels to find the projection that maximizes the ratio of between-class scatter to within-class scatter. It's Fisher's criterion. LDA is what you want when your goal is classification — you're literally optimizing the representation for discrimination, not for variance."*

---

### "What's the intuition behind ICA?"

> *"ICA solves the cocktail party problem: multiple microphones recording mixed conversations, can you recover the original speakers? The key insight is the Central Limit Theorem — mixed signals are more Gaussian than pure sources. So ICA searches for directions that are maximally non-Gaussian. It's exploiting higher-order statistics — kurtosis, negentropy — instead of just variance. PCA gives uncorrelated components. ICA gives statistically independent components, which is stronger."*

---

## Summary Cheatsheet

```
╔══════════════════════════════════════════════════════════════════════╗
║             MODULE 5 — DIMENSIONALITY REDUCTION CHEATSHEET          ║
╠══════════════════════╦══════════════════════╦════════════════════════╣
║       PCA            ║        ICA           ║        LDA             ║
╠══════════════════════╬══════════════════════╬════════════════════════╣
║ Unsupervised         ║ Unsupervised         ║ Supervised             ║
║ Maximizes variance   ║ Maximizes indep.     ║ Maximizes class sep.   ║
║ Eigenvec of Σ        ║ FastICA / negentropy ║ Eigenvec of Sw⁻¹Sb     ║
║ Uncorrelated output  ║ Independent output   ║ Discriminant axes      ║
║ Gaussian OK          ║ Non-Gaussian req'd   ║ Gaussian classes OK    ║
║ Any # components     ║ Any # components     ║ Max C-1 components     ║
║ Compression/denoise  ║ Source separation    ║ Classification prep    ║
╚══════════════════════╩══════════════════════╩════════════════════════╝

CURSE OF DIMENSIONALITY:
  → Distances equalize | Manifold hypothesis | Data on low-d subspace

KEY FORMULAS:
  Covariance:       Σ = (1/n-1) XᵀX
  Eigen decomp:     Σ = QΛQᵀ
  PCA projection:   Z = X Qₖ
  PCA reconstruction: X̂ = Z Qₖᵀ
  PCA error:        ‖X - X̂‖² = Σᵢ>ₖ λᵢ
  Explained var:    EVRᵢ = λᵢ / Σλ
  Fisher criterion: J(w) = wᵀSᵦw / wᵀSᵥw
  ICA model:        X = AS, recover W = A⁻¹

GEOMETRIC INTUITIONS:
  Covariance matrix  → shape of data ellipsoid
  Eigenvectors       → principal axes of ellipsoid
  Eigenvalues        → squared axis lengths (= variances)
  Projection         → shadow onto a direction
  Whitening          → sphericalize the ellipsoid
  Independence       → statistical factorization, not just rotation

PRODUCTION RULES:
  ① Always StandardScaler before PCA/ICA
  ② Fit transforms on TRAIN only → apply to test
  ③ Use SVD-based PCA (sklearn default) not explicit covariance
  ④ Use sklearn Pipeline to prevent leakage
  ⑤ For n < d: PCA-first then LDA
  ⑥ Choose k by: 95% variance | Elbow | Kaiser | CV
  ⑦ ICA needs random_state for reproducibility

WHEN TO USE WHAT:
  Visualization (2D/3D)    → PCA or LDA (if labeled)
  Noise removal            → PCA (discard small eigenvalues)
  Source separation / EEG  → ICA
  Pre-classification       → LDA (labeled) or PCA (unlabeled)
  Highly non-Gaussian      → ICA
  Large-scale / sparse     → TruncatedSVD
  Nonlinear manifold       → UMAP / t-SNE / Kernel PCA
```

---

> **Next Module:** Nonlinear Dimensionality Reduction — t-SNE, UMAP, Autoencoders, and Variational Latent Spaces.
