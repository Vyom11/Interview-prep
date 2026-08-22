# Module 7 — Classification and Metrics

> **Focus:** Evaluation philosophy · Decision boundaries · Classification intuition · Metrics interpretation

-----

## Table of Contents

1. [Why This Module Matters](#why-this-module-matters)
1. [ELI5](#eli5)
1. [Core Concepts](#core-concepts)
1. [Math Intuition](#math-intuition)
1. [Key Formulas and Equations](#key-formulas-and-equations)
1. [Algorithms Breakdown](#algorithms-breakdown)
1. [Visual Mental Models](#visual-mental-models)
1. [Real-World Applications](#real-world-applications)
1. [Engineering Insights](#engineering-insights)
1. [Production Notes](#production-notes)
1. [Common Mistakes](#common-mistakes)
1. [Best Practices](#best-practices)
1. [Minimal Practical Workflow](#minimal-practical-workflow)
1. [Python Ecosystem](#python-ecosystem)
1. [Interview Questions](#interview-questions)
1. [How to Explain in an Interview](#how-to-explain-in-an-interview)
1. [Summary Cheatsheet](#summary-cheatsheet)

-----

## Why This Module Matters

Classification is among the most **practically deployed** capabilities in ML — spam filters, cancer screening, fraud detection, content moderation. But the gap between *a model that runs* and *a model that makes good decisions* is almost entirely determined by:

1. **Which metric you optimize** — Accuracy on an imbalanced dataset is meaningless noise.
1. **Where you draw the decision boundary** — The threshold is a business decision, not a model parameter.
1. **How you handle imbalance** — The real world is never 50/50.
1. **Whether you understand what errors cost** — A false negative in cancer screening has a different cost than a false positive.

This module teaches you to reason about classification as a **decision problem under uncertainty**, not merely a pattern-recognition problem.

-----

## ELI5

Imagine you’re sorting mail:

- **Binary classification**: Is this spam or not spam? Two bins.
- **Multiclass**: Is this a bill, a letter, a package notice, or junk? Many bins.
- **K-NN**: “What bin did the most similar pieces of mail go in?”
- **SVM**: “Draw the thickest possible line between spam and not-spam.”
- **Confusion matrix**: A tally sheet of which bins you put mail in vs. where it actually belonged.
- **Precision**: Of all the things you labeled “bill,” how many were actually bills?
- **Recall**: Of all the actual bills, how many did you catch?
- **Imbalance**: 1% of mail is bills, 99% is junk — a classifier that says “everything is junk” is 99% accurate but utterly useless.

-----

## Core Concepts

### Classification Problems

Classification maps an input vector **x** ∈ ℝⁿ to a discrete label **y** ∈ {C₁, C₂, …, Cₖ}. The model learns a **decision boundary** — a surface in feature space that partitions it into labeled regions.

|Type      |Labels                |Example                         |
|----------|----------------------|--------------------------------|
|Binary    |2                     |Fraud / Not Fraud               |
|Multiclass|>2, mutually exclusive|Digit recognition (0–9)         |
|Multilabel|>2, co-occurring      |Image tags (cat, outdoor, sunny)|
|Ordinal   |Ordered classes       |Rating: 1★ to 5★                |

### Decision Boundaries

The decision boundary is **where** the model changes its mind. Understanding its shape tells you everything about the algorithm:

```
Linear boundary (LDA, SVM linear):     Quadratic (SVM RBF, QDA):
      Class A | Class B                     Class B
    ──────────┼──────────                  ╭─────╮
              │                    Class A │ Cls A│ Class A
              │                            ╰─────╯
```

- **High-capacity models** (deep nets, RBF-SVM) → complex, wiggly boundaries → risk overfitting
- **Low-capacity models** (linear SVM, LDA) → straight boundaries → risk underfitting
- **The art**: right boundary complexity for your data geometry

### Binary vs. Multiclass

**Binary** — One decision surface separates two classes. Probability output is a single value P(y=1|x).

**Multiclass** strategies:

- **One-vs-Rest (OvR)**: Train K binary classifiers; pick the most confident.
- **One-vs-One (OvO)**: Train K(K-1)/2 binary classifiers; majority vote.
- **Softmax / native multiclass**: Output a probability distribution over all classes (sum = 1).

-----

## Math Intuition

### Distance Metrics

Distance metrics define **what “similar” means** for your data. This choice is a modeling decision.

#### Euclidean Distance

The straight-line distance — assumes all features are equally important and uncorrelated.

```
d(a, b) = √Σ(aᵢ - bᵢ)²
```

**Intuition**: Imagine the hypotenuse of a triangle in n-dimensional space. Works well when features are on the same scale and independent.

**Weakness**: Catastrophically sensitive to scale differences and correlated features.

#### Manhattan Distance (L1)

Sum of absolute differences — travels along grid lines.

```
d(a, b) = Σ|aᵢ - bᵢ|
```

**Intuition**: Navigating a city block grid. More robust to outliers than Euclidean. Preferred in high-dimensional spaces (less susceptible to the curse of dimensionality).

#### Mahalanobis Distance

Euclidean distance corrected for feature covariance — accounts for the shape of the data cloud.

```
d(a, b) = √[(a-b)ᵀ Σ⁻¹ (a-b)]
```

Where **Σ** is the covariance matrix of the data.

**Intuition**: Stretches and rotates space so that the data cloud becomes a unit sphere, *then* measures Euclidean distance. Two points that look far apart in raw space but lie along a principal axis are actually “closer” in Mahalanobis terms.

**Use when**: Features are correlated, heteroscedastic, or measured in different units.

#### Cosine Similarity

Measures the angle between two vectors — ignores magnitude.

```
cos(θ) = (a · b) / (‖a‖ · ‖b‖)
```

**Intuition**: Does not care how long the vectors are — only the direction. A short and a long document with the same topic distribution are “identical” under cosine. Essential for text/NLP.

**Distance version**: cosine distance = 1 - cosine similarity

#### Hamming Distance

Count of positions where two binary strings differ.

```
d("1011", "1001") = 1   ← one position differs
```

**Use cases**: DNA sequences, one-hot encoded categorical features, error-correcting codes.

-----

## Key Formulas and Equations

### The Confusion Matrix Decoded

For a binary classifier with Positive (P) and Negative (N) classes:

```
                  Predicted
                  Pos    Neg
Actual  Pos  │  TP   │  FN  │   ← Row = actual positives
        Neg  │  FP   │  TN  │   ← Row = actual negatives
```

|Cell|Name          |Meaning                         |
|----|--------------|--------------------------------|
|TP  |True Positive |Correctly flagged positive      |
|TN  |True Negative |Correctly cleared negative      |
|FP  |False Positive|False alarm (Type I error)      |
|FN  |False Negative|Missed detection (Type II error)|

**Reading philosophy**: Always ask *what does each error cost?* In fraud detection, FN (missed fraud) is expensive. In medical screening, FN (missed disease) can be fatal.

### Accuracy

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

**When to use**: Balanced classes only.  
**When to avoid**: Any imbalanced dataset. A model predicting all negatives on a 99/1 dataset achieves 99% accuracy while being completely useless.

### Precision

```
Precision = TP / (TP + FP)
```

“Of everything I labeled positive, what fraction was actually positive?”

**Optimize when**: False positives are costly. (Spam filter — you don’t want real email in spam.)

### Recall (Sensitivity / True Positive Rate)

```
Recall = TP / (TP + FN)
```

“Of all actual positives, what fraction did I catch?”

**Optimize when**: False negatives are costly. (Cancer screening — you cannot miss a true case.)

### F1 Score

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

Harmonic mean of precision and recall. The harmonic mean punishes extreme imbalances — a model with 100% precision and 0% recall gets F1 = 0.

**F-beta Score** (generalization):

```
Fβ = (1 + β²) × (Precision × Recall) / (β² × Precision + Recall)
```

- β > 1 → weights recall higher (prefer catching positives)
- β < 1 → weights precision higher (prefer clean positives)

### Specificity (True Negative Rate)

```
Specificity = TN / (TN + FP)
```

“Of all actual negatives, how many did I correctly clear?”

**Complements recall**. In medical diagnostics: sensitivity = recall (catches disease), specificity (rules out disease).

### ROC-AUC

The **ROC curve** plots **TPR (Recall)** on the y-axis vs. **FPR (1 - Specificity)** on the x-axis as the **classification threshold** sweeps from 0 to 1.

```
FPR = FP / (FP + TN)   ← False Positive Rate = 1 - Specificity
TPR = TP / (TP + FN)   ← True Positive Rate = Recall

ROC Curve:
TPR
1.0 │         ╭──────────●  ← Perfect classifier
    │      ╭──╯
    │   ╭──╯              ← Real classifier (AUC ≈ 0.85)
    │ ╭─╯
    │╱                    ← Random classifier (AUC = 0.5)
    └──────────────────── FPR
    0                  1.0
```

**AUC intuition**: The probability that the model ranks a randomly chosen positive above a randomly chosen negative. AUC = 0.85 means: given a random (positive, negative) pair, the model correctly orders them 85% of the time.

**AUC vs. threshold-specific metrics**:

- AUC evaluates the model’s **ranking ability** across all thresholds — threshold-agnostic.
- Precision/Recall/F1 evaluate performance at a **specific threshold**.
- For imbalanced data: prefer **PR-AUC** (Precision-Recall curve AUC) over ROC-AUC, because ROC-AUC can be optimistically inflated by a large TN count.

### SVM Decision Boundary

```
Decision boundary:     w·x + b = 0
Margin boundaries:     w·x + b = ±1

Margin width = 2 / ‖w‖

Optimization: minimize ‖w‖²
              subject to yᵢ(w·xᵢ + b) ≥ 1
```

**Soft-margin** (C parameter):

```
minimize  ½‖w‖² + C·Σξᵢ
```

C controls the tradeoff between margin width and training errors.

### K-NN Classification

```
ŷ = argmax_c Σᵢ∈N_k(x) 𝟙[yᵢ = c]
```

Where N_k(x) is the set of k nearest neighbors of x.

-----

## Algorithms Breakdown

### K-Nearest Neighbors (K-NN)

**Mechanism**: Store all training data. At inference, find the K closest points (by chosen distance metric), take majority class vote.

**Hyperparameters**:

- **K**: Small K → complex boundary, noisy; Large K → smooth boundary, biased toward majority class
- **Distance metric**: Euclidean (default), Manhattan, Mahalanobis, cosine
- **Weighting**: Uniform vote vs. distance-weighted vote (closer neighbors count more)

**Decision boundary geometry**:

```
K=1:  Voronoi tessellation — each point owns its region
K=∞:  Predict global majority class everywhere
K=5:  Smooth Voronoi — sensible default
```

**Strengths**: Non-parametric, no training phase, naturally multiclass, captures complex boundaries.  
**Weaknesses**: O(n) inference, curse of dimensionality, sensitive to scale (always normalize!), sensitive to irrelevant features.

**K selection strategy**: Cross-validate on odd K values (avoids ties in binary). Plot validation error vs. K — the “elbow” is your K.

-----

### Support Vector Machines (SVM)

**Core idea**: Find the **maximum-margin hyperplane** — the decision boundary that maximizes the distance to the nearest points of each class (the support vectors). Wide margin → better generalization.

```
Support vectors are the ONLY points that define the boundary.
Remove all non-support vectors → boundary is unchanged.
```

**Kernel Trick**: Map data to higher dimensions implicitly (without computing the transformation) to find a linear boundary in that space.

|Kernel        |Formula                |Use Case                         |
|--------------|-----------------------|---------------------------------|
|Linear        |K(x,z) = xᵀz           |Linearly separable, high-dim text|
|RBF (Gaussian)|K(x,z) = exp(-γ‖x-z‖²) |Default; non-linear problems     |
|Polynomial    |K(x,z) = (xᵀz + c)ᵈ    |Image data, structured patterns  |
|Sigmoid       |K(x,z) = tanh(αxᵀz + c)|Neural net analogy               |

**Key hyperparameters**:

|Parameter  |Effect                     |High value                                        |Low value                                  |
|-----------|---------------------------|--------------------------------------------------|-------------------------------------------|
|**C**      |Margin vs. error tradeoff  |Narrow margin, fewer errors on train, overfit risk|Wide margin, more errors on train, underfit|
|**γ** (RBF)|Influence radius of a point|Wiggly boundary, overfit                          |Smooth boundary, underfit                  |

**Geometric intuition**:

```
Linearly separable data:                Non-linear (RBF kernel):
                                        
     ○ ○ │ × ×                          ○ ○ ○
     ○   │   ×                          ○ ×× ○
   ──────┼──────  ← max margin         ○ ○ ○
     ○ ○ │ × ×                          
                                        Maps to higher dim where
  Support vectors touch the margin      a hyperplane separates them
```

-----

### Linear Discriminant Analysis (LDA) as Classifier

LDA finds the projection that **maximizes between-class scatter** relative to **within-class scatter**.

```
Objective: maximize  J(w) = wᵀ Sᴮ w / wᵀ Sᵂ w

Solution:  w = Sᵂ⁻¹(μ₁ - μ₂)   (Fisher's linear discriminant)
```

**Decision rule**: Assign to the class with the nearest mean in the projected space (using Mahalanobis-like distance).

**Assumptions**: Gaussian class-conditionals, equal covariance matrices across classes, linear boundary.  
**When violated**: Use QDA (quadratic boundary) or a non-parametric method.

**LDA as feature reducer + classifier**: Project to K-1 dimensions (K = number of classes), *then* classify. Often better than PCA+classifier because LDA uses label information.

-----

### Voting Classifiers (Ensemble)

Combine multiple classifiers to reduce variance and improve robustness.

|Type           |Mechanism                                |Best For                   |
|---------------|-----------------------------------------|---------------------------|
|**Hard voting**|Majority class vote                      |Diverse classifiers        |
|**Soft voting**|Average predicted probabilities          |Well-calibrated classifiers|
|**Stacking**   |Meta-learner on base classifiers’ outputs|Heterogeneous ensembles    |

**Key principle**: Voters must be **diverse** (make different errors) and **better than random**. Correlated voters don’t help.

-----

### Semi-Supervised Learning

When labeled data is scarce but unlabeled data is abundant.

#### Self-Training

1. Train on labeled data.
1. Predict on unlabeled data; add high-confidence predictions as pseudo-labels.
1. Retrain on labeled + pseudo-labeled data.
1. Repeat.

**Risk**: Early errors get amplified — confident wrong predictions corrupt the training set.

#### Co-Training

- Requires two **independent views** of the data (e.g., webpage text + hyperlinks).
- Train two classifiers on separate views; each labels data for the other.
- Each classifier teaches the other what it sees from its perspective.

#### Label Propagation

- Build a similarity graph over all data (labeled + unlabeled).
- Propagate labels through the graph weighted by similarity.
- Labels “flow” from labeled nodes to nearby unlabeled nodes.

```
Graph:  ●(+) ─── ○ ─── ○ ─── ●(-)
         label propagates →
         ○ gets +, ○ gets weak +/-, etc.
```

-----

## Visual Mental Models

### Confusion Matrix Intuition Map

```
                 PREDICTED
                 +        -
          ┌──────────┬──────────┐
    + (P) │    TP    │    FN    │  ← All Actual Positives
ACTUAL    │  (HIT)   │  (MISS)  │
          ├──────────┼──────────┤
    - (N) │    FP    │    TN    │  ← All Actual Negatives
          │ (FALSE   │ (CORRECT │
          │  ALARM)  │  REJECT) │
          └──────────┴──────────┘

Precision = TP / (TP+FP) → col 1 purity
Recall    = TP / (TP+FN) → row 1 coverage
Spec.     = TN / (TN+FP) → row 2 coverage
```

### Precision-Recall Tradeoff

```
As threshold ↑ (stricter positive prediction):
  → Fewer positives predicted
  → Precision ↑ (only very confident positives)
  → Recall ↓ (miss many true positives)

As threshold ↓ (looser):
  → More positives predicted
  → Precision ↓ (more false alarms)
  → Recall ↑ (catch more true positives)

Precision
1.0 │╲
    │  ╲
    │    ╲___
    │        ╲___
0.0 └──────────────── Recall 1.0

The PR curve: ideal is upper-right corner (1,1).
```

### ROC vs. PR Curve: When to Use Which

```
ROC-AUC:
  + Threshold-agnostic ranking quality
  + Good for balanced or near-balanced data
  - Optimistically inflated with heavy imbalance
    (large TN denominator inflates TNR/specificity)

PR-AUC:
  + Focused on the positive class
  + Better for imbalanced data
  + Shows precision cost of increasing recall
  - Doesn't evaluate negative class discrimination
```

**Rule of thumb**: If 95% of your data is negative class and you care about finding the 5%, use PR-AUC.

### SVM Margin Visualization

```
Feature 2
  │    ○ ○                            
  │   ○   ○    ←── Support vector     
  │    ○    ╱                         
  │        ╱  ← Decision boundary (w·x+b=0)
  │      ╱                            
  │    ╱    ×   ← Support vector      
  │  ╱   × ×                          
  │       ×                           
  └──────────────── Feature 1         

  ←  margin  →  = 2/‖w‖ (maximize this)
```

### K-NN Decision Boundary at Different K

```
K=1 (overfit):          K=15 (smooth):
  ×○×○○×                   ×  ○  ×
  ○×○○×○                     ╭────╮
  ×○×○○×                  ×  │ ○○ │  ×
  (jagged mosaic)            ╰────╯
                          (smooth contour)
```

### Classification Workflow Diagram

```
Raw Data
    │
    ▼
┌─────────────────────┐
│  EDA + Class Balance │◄── Is it imbalanced? If yes →
└─────────────────────┘    SMOTE / undersample / class_weight
    │
    ▼
┌─────────────────────┐
│  Feature Engineering │
│  (scale, encode)     │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Train/Val/Test Split│
│  (stratified)        │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Model Training      │
│  + Cross-Validation  │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Metric Selection    │◄── What are the error costs?
│  (not just accuracy) │    Choose: F1, ROC-AUC, PR-AUC
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Threshold Tuning    │◄── Don't use 0.5 by default!
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Error Analysis      │
│  (confusion matrix)  │
└─────────────────────┘
    │
    ▼
  Deploy
```

-----

## Real-World Applications

|Domain           |Task                |Key Metric     |Why                                          |
|-----------------|--------------------|---------------|---------------------------------------------|
|Medical screening|Cancer detection    |**Recall**     |Missing a case is catastrophic               |
|Spam filtering   |Email classification|**Precision**  |False positives annoy users                  |
|Fraud detection  |Transaction flagging|**F1 / PR-AUC**|Rare events, both errors costly              |
|Credit scoring   |Default prediction  |**ROC-AUC**    |Ranking customers matters more than threshold|
|Legal NLP        |Document review     |**Recall**     |Must not miss relevant documents             |
|Recommendation   |Content safety      |**Precision**  |Don’t remove good content                    |
|Manufacturing    |Defect detection    |**Recall**     |Miss rate drives warranty costs              |

-----

## Imbalanced Learning

Imbalance is the rule, not the exception. A dataset with 1% positives is not unusual in fraud, medical, or anomaly detection.

### Why Accuracy Fails

```
Dataset: 990 negatives, 10 positives (1% positive rate)
Model: Predict "negative" for everything.
Accuracy = 990/1000 = 99%  ← looks great
Recall   = 0/10     = 0%   ← catches nothing
F1       = 0              ← useless
```

### Strategies

#### Oversampling

Duplicate or synthesize minority class samples.

**Random oversampling**: Simply duplicate minority samples. Risk: overfitting to exact duplicates.

**SMOTE (Synthetic Minority Over-sampling Technique)**:

```
For each minority sample x:
  1. Find its K nearest minority neighbors
  2. Randomly pick one neighbor x̃
  3. Create synthetic point: x_new = x + λ(x̃ - x), λ ∈ [0,1]
  
Interpolates between existing minority points rather than copying them.
```

**SMOTE variants**:

- **Borderline-SMOTE**: Only oversample near the decision boundary
- **ADASYN**: Generate more samples in harder-to-learn regions
- **SMOTE-Tomek**: SMOTE + remove Tomek links (borderline majority samples)

#### Undersampling

Remove majority class samples.

**Random undersampling**: Randomly delete majority instances. Risks discarding useful information.

**Tomek links**: Remove majority samples that are “too close” to minority samples — cleans the boundary.

**NearMiss**: Keep only majority samples nearest to minority samples (several variants).

#### Algorithm-Level Methods

|Method                   |Mechanism                                 |
|-------------------------|------------------------------------------|
|`class_weight='balanced'`|Multiply loss by inverse class frequency  |
|Threshold adjustment     |Move decision threshold below 0.5         |
|Ensemble (EasyEnsemble)  |Multiple balanced subsamples + boosting   |
|Cost-sensitive learning  |Higher misclassification cost for minority|

**Threshold adjustment recipe**:

```
1. Train model as-is
2. Plot precision-recall curve
3. Choose threshold based on business cost ratio:
   threshold* = argmax_t [β × Precision(t) + Recall(t)]
   or use F-beta with appropriate β
```

-----

## Engineering Insights

### Feature Scaling is Mandatory for Distance-Based Methods

```python
# K-NN WITHOUT scaling:
# Feature 1: salary [30000, 100000]  ← dominates distance
# Feature 2: age    [20, 60]         ← ignored

# ALWAYS scale before K-NN, SVM:
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
```

### SVM Hyperparameter Search Strategy

```
Start with RBF kernel (almost always works).
Grid search: C ∈ {0.01, 0.1, 1, 10, 100}
             γ ∈ {'scale', 0.001, 0.01, 0.1, 1}

Rule of thumb: C and γ pull in opposite directions.
If underfitting: ↑C or ↑γ
If overfitting:  ↓C or ↓γ
```

### K-NN Curse of Dimensionality

In high dimensions, all points become approximately equidistant — the concept of “neighbor” collapses. With d dimensions, the ratio of distances between nearest and farthest neighbors approaches 1.

**Solutions**:

- PCA/UMAP dimensionality reduction before K-NN
- Use cosine distance for text (less affected)
- Use Manhattan distance (more robust in high-dim than Euclidean)
- Consider a different algorithm entirely above ~50 features

### Stratified Splitting

Always stratify your train/test split on the label column when data is imbalanced:

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
# Preserves class proportions in both splits
```

-----

## Production Notes

### Calibration

Raw model probabilities are often not true probabilities. Calibrate before using thresholds:

```python
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
calibrated_model = CalibratedClassifierCV(svm_model, method='isotonic', cv=5)
calibrated_model.fit(X_train, y_train)
```

### Threshold is a Business Decision

**Never deploy with threshold = 0.5 on an imbalanced problem.** Optimal threshold depends on:

```
Cost ratio = Cost(FN) / Cost(FP)

For cost ratio = 10 (FN ten times worse than FP):
  → Lower threshold → catch more positives → accept more FP
  → threshold ≈ 1 / (1 + cost_ratio) = ~0.09
```

### K-NN at Scale

K-NN is O(n) per query — infeasible at millions of records. Production solutions:

- **Approximate Nearest Neighbors (ANN)**: FAISS, Annoy, HNSW
- **Ball trees / KD-trees**: Exact but faster for low-dimensional data
- `sklearn.neighbors.KDTree` for moderate scales

### SVM at Scale

Standard SVM is O(n² to n³) — not for millions of points:

- `sklearn.svm.LinearSVC` for linear kernel at scale (liblinear backend)
- **SGD with hinge loss** (`SGDClassifier(loss='hinge')`) for very large data
- **Kernel approximation**: `RBFSampler` + `LinearSVC` ≈ RBF-SVM at linear cost

-----

## Common Mistakes

|Mistake                             |Consequence                                               |Fix                              |
|------------------------------------|----------------------------------------------------------|---------------------------------|
|Using accuracy on imbalanced data   |False confidence                                          |Use F1, PR-AUC, ROC-AUC          |
|Not scaling features before K-NN/SVM|Dominated by high-range features                          |StandardScaler / MinMaxScaler    |
|SMOTE before train/test split       |Data leakage — synthetic points from test bleed into train|Apply SMOTE only to training fold|
|Optimizing threshold at 0.5         |Suboptimal for imbalanced tasks                           |Tune threshold on validation set |
|Ignoring class_weight parameter     |Model ignores minority class                              |Set `class_weight='balanced'`    |
|Using ROC-AUC with heavy imbalance  |Misleadingly high scores                                  |Switch to PR-AUC                 |
|Not stratifying cross-validation    |Fold with no minority samples                             |`StratifiedKFold`                |
|K-NN without cross-validating K     |Arbitrary K selection                                     |CV over range of K               |
|Applying LDA to non-Gaussian data   |Invalid decision boundaries                               |Check assumptions; use QDA       |
|One metric to rule them all         |Miss important failure modes                              |Report full metric suite         |

-----

## Best Practices

### Metric Selection Philosophy

```
Step 1: Understand the cost of each error type
        - What happens if FP? (False alarm cost)
        - What happens if FN? (Miss cost)

Step 2: Match metric to cost structure
        - FN >> FP → maximize Recall
        - FP >> FN → maximize Precision
        - Both matter equally → F1 or F-beta
        - Need ranking quality → ROC-AUC or PR-AUC
        - Heavy imbalance → prefer PR-AUC

Step 3: Report multiple metrics
        Always report: Precision, Recall, F1, AUC, confusion matrix
        Never report: Accuracy alone on imbalanced data

Step 4: Set threshold on business logic, not model default
```

### Imbalance Handling Decision Tree

```
Is class ratio < 10:1?
├── YES → class_weight='balanced' may suffice
└── NO  → Active resampling needed
          │
          ├── < 100k samples? → SMOTE
          ├── > 1M samples?   → Undersampling (random or NearMiss)
          └── Critical domain? → SMOTE + Tomek + threshold tuning
```

### SVM Configuration Checklist

- [ ] Scale all features (StandardScaler)
- [ ] Start with RBF kernel
- [ ] Use `GridSearchCV` or `RandomizedSearchCV` for C and γ
- [ ] Use `class_weight='balanced'` for imbalanced data
- [ ] Check support vector count (too many → overfitting, too few → may be underfitting)
- [ ] For large data: use `LinearSVC` or `SGDClassifier`

-----

## Minimal Practical Workflow

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, average_precision_score,
    ConfusionMatrixDisplay, RocCurveDisplay, PrecisionRecallDisplay
)
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import matplotlib.pyplot as plt

# ── 1. Load and inspect class balance ──────────────────────────────────────
# df = pd.read_csv("data.csv")
# X, y = df.drop("target", axis=1), df["target"]
# print(y.value_counts(normalize=True))  # ← Check imbalance first!

# ── 2. Stratified split ─────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ── 3. Build pipelines (scaling + optional SMOTE + model) ───────────────────
knn_pipe = ImbPipeline([
    ("scaler", StandardScaler()),
    ("smote",  SMOTE(random_state=42)),       # Only applied during .fit()
    ("clf",    KNeighborsClassifier(n_neighbors=7, weights='distance'))
])

svm_pipe = ImbPipeline([
    ("scaler", StandardScaler()),
    ("clf",    SVC(kernel='rbf', C=1.0, gamma='scale',
                  class_weight='balanced', probability=True))
])

lda_pipe = ImbPipeline([
    ("clf", LinearDiscriminantAnalysis())
])

# ── 4. Voting ensemble ──────────────────────────────────────────────────────
voting_clf = VotingClassifier(
    estimators=[('knn', knn_pipe), ('svm', svm_pipe), ('lda', lda_pipe)],
    voting='soft'   # Average probabilities — requires probability=True
)

# ── 5. Cross-validate with multiple metrics ─────────────────────────────────
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scoring = ['f1', 'roc_auc', 'precision', 'recall', 'average_precision']
cv_results = cross_validate(svm_pipe, X_train, y_train, cv=cv, scoring=scoring)

for metric in scoring:
    scores = cv_results[f'test_{metric}']
    print(f"{metric:>20}: {scores.mean():.3f} ± {scores.std():.3f}")

# ── 6. Fit and evaluate on test set ─────────────────────────────────────────
svm_pipe.fit(X_train, y_train)
y_pred      = svm_pipe.predict(X_test)
y_prob      = svm_pipe.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, y_pred, digits=4))

print(f"ROC-AUC:  {roc_auc_score(y_test, y_prob):.4f}")
print(f"PR-AUC:   {average_precision_score(y_test, y_prob):.4f}")

# ── 7. Threshold tuning ──────────────────────────────────────────────────────
from sklearn.metrics import precision_recall_curve, f1_score

precisions, recalls, thresholds = precision_recall_curve(y_test, y_prob)
f1_scores = 2 * precisions[:-1] * recalls[:-1] / (precisions[:-1] + recalls[:-1] + 1e-8)
optimal_threshold = thresholds[np.argmax(f1_scores)]
print(f"\nOptimal threshold (max F1): {optimal_threshold:.3f}")

y_pred_tuned = (y_prob >= optimal_threshold).astype(int)
print(f"Tuned F1: {f1_score(y_test, y_pred_tuned):.4f}")

# ── 8. Visualize ────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=axes[0])
axes[0].set_title("Confusion Matrix")

RocCurveDisplay.from_predictions(y_test, y_prob, ax=axes[1])
axes[1].set_title("ROC Curve")

PrecisionRecallDisplay.from_predictions(y_test, y_prob, ax=axes[2])
axes[2].set_title("Precision-Recall Curve")

plt.tight_layout()
plt.savefig("classification_metrics.png", dpi=150)
plt.show()

# ── 9. Decision boundary visualization (2D) ─────────────────────────────────
def plot_decision_boundary(clf, X, y, title="Decision Boundary", resolution=0.02):
    """Visualize decision boundary for 2-feature datasets."""
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    clf.fit(X_s, y)
    
    x_min, x_max = X_s[:, 0].min() - 1, X_s[:, 0].max() + 1
    y_min, y_max = X_s[:, 1].min() - 1, X_s[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, resolution),
                          np.arange(y_min, y_max, resolution))
    
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.figure(figsize=(7, 5))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='RdBu')
    plt.scatter(X_s[:, 0], X_s[:, 1], c=y, cmap='RdBu', edgecolors='k', s=40)
    plt.title(title)
    plt.tight_layout()
    plt.show()
```

-----

## Python Ecosystem

|Library           |Tool                            |Purpose                |
|------------------|--------------------------------|-----------------------|
|`scikit-learn`    |`KNeighborsClassifier`          |K-NN                   |
|`scikit-learn`    |`SVC`, `LinearSVC`              |SVM                    |
|`scikit-learn`    |`LinearDiscriminantAnalysis`    |LDA                    |
|`scikit-learn`    |`VotingClassifier`              |Ensemble               |
|`scikit-learn`    |`classification_report`         |Full metric suite      |
|`scikit-learn`    |`ConfusionMatrixDisplay`        |Confusion matrix plot  |
|`scikit-learn`    |`RocCurveDisplay`               |ROC curve plot         |
|`scikit-learn`    |`PrecisionRecallDisplay`        |PR curve plot          |
|`scikit-learn`    |`calibration_curve`             |Probability calibration|
|`imbalanced-learn`|`SMOTE`, `ADASYN`               |Oversampling           |
|`imbalanced-learn`|`RandomUnderSampler`, `NearMiss`|Undersampling          |
|`imbalanced-learn`|`SMOTETomek`                    |Combined resampling    |
|`imbalanced-learn`|`Pipeline`                      |SMOTE-safe pipeline    |
|`scikit-learn`    |`label_propagation`             |Semi-supervised        |

```bash
pip install scikit-learn imbalanced-learn
```

-----

## Interview Questions

### Conceptual

**Q1: You have a dataset where 98% of samples are class 0. Your model achieves 98% accuracy. Is it a good model?**  
*Expected answer*: Almost certainly not. The model likely predicts all zeros. Report recall, precision, F1, and PR-AUC. A model that predicts the majority class achieves 98% accuracy with 0% recall on the minority class.

**Q2: When would you choose F1 score over ROC-AUC?**  
*Expected answer*: F1 is a threshold-specific metric — use it when you have chosen a threshold and want to evaluate at that operating point. ROC-AUC is threshold-agnostic and measures overall ranking quality. For imbalanced data, PR-AUC is often more informative than ROC-AUC. Use F1 when you need a single scalar at a specific threshold; ROC/PR-AUC when you want to evaluate the model’s discriminative power independent of threshold.

**Q3: Explain the SVM margin intuitively. Why is maximizing it desirable?**  
*Expected answer*: The margin is the distance from the decision boundary to the nearest training points of each class (support vectors). Maximizing it enforces that the two classes are as far apart as possible at the boundary, which increases tolerance to perturbations in new data. By the structural risk minimization principle, larger margins correspond to simpler functions, which generalize better.

**Q4: What is the kernel trick and why is it computationally valuable?**  
*Expected answer*: The kernel trick computes the dot product in a transformed (possibly infinite-dimensional) feature space without explicitly computing the transformation. Instead of computing φ(x)·φ(z), we evaluate K(x,z) directly. This lets us use highly non-linear decision surfaces with the computational cost of a linear model in the original space.

**Q5: Why should SMOTE only be applied to training data, not before splitting?**  
*Expected answer*: Applying SMOTE before splitting causes data leakage. Synthetic samples are created by interpolating between real minority samples. If test data contains points used to generate synthetic training samples, the model has implicitly seen information about the test distribution during training, leading to optimistically biased evaluation. Always apply SMOTE inside a cross-validation fold or in a pipeline that only transforms training data.

**Q6: Compare Label Propagation to Self-Training for semi-supervised classification.**  
*Expected answer*: Self-training is iterative — train a supervised model, pseudo-label confident unlabeled points, add to training set, retrain. It can propagate early errors. Label propagation is a graph-based method that diffuses labels simultaneously through a similarity graph in one step. LP tends to be more stable (no iterative error amplification) and exploits the manifold structure of the data. Self-training works with any classifier; LP requires a meaningful similarity structure.

### Technical

**Q7: K-NN with K=1 vs. K=100 — describe the decision boundary in each case and the bias-variance tradeoff.**

**Q8: In a multiclass SVM with OvR strategy and 10 classes, how many binary SVMs are trained? What about OvO?**  
*Answer*: OvR = 10; OvO = 10×9/2 = 45.

**Q9: What hyperparameters would you tune for an RBF SVM and what is their effect on the decision boundary?**

**Q10: You train an LDA classifier on data where one class has significantly higher variance than another. What goes wrong, and how do you fix it?**  
*Answer*: LDA assumes equal within-class covariance. Unequal covariances violate this → QDA (quadratic boundary) accounts for per-class covariance matrices.

-----

## How to Explain in an Interview

### “Walk me through how you’d approach a classification problem.”

> “I start by understanding the business problem — specifically, what’s the cost of each type of error. That tells me which metric to optimize. Then I look at class balance, because that determines my resampling strategy and whether accuracy is even a meaningful metric.
> 
> I’d split data with stratification, build a pipeline that includes scaling (mandatory for distance-based models like K-NN or SVM), and apply any oversampling (SMOTE) only inside training folds to avoid leakage.
> 
> I evaluate with a full metric suite — precision, recall, F1, ROC-AUC, and PR-AUC — not just accuracy. Then I tune the decision threshold based on the cost ratio between false positives and false negatives, because 0.5 is almost never the right threshold for imbalanced problems.”

### “How would you explain SVM to a non-technical stakeholder?”

> “SVM finds the thickest possible boundary between your two groups in your data. Think of it as drawing a road between two neighborhoods, making the road as wide as possible — giving you the most margin for error when classifying new cases. The kernel trick lets it find this wide road even when the neighborhoods are mixed together in a complex pattern.”

### “What’s wrong with accuracy for imbalanced data?”

> “Accuracy counts all correct predictions equally. If 99% of your data is negative, a model that predicts ‘negative’ for everything scores 99% accuracy — but it finds zero of your actual positives. In fraud detection, that means catching no fraud. I always look at recall for the minority class and PR-AUC, which tells you the real cost of missing positives.”

-----

## Summary Cheatsheet

### Distance Metrics at a Glance

|Metric     |Formula                  |Best For                               |
|-----------|-------------------------|---------------------------------------|
|Euclidean  |√Σ(aᵢ-bᵢ)²               |Low-dim, same-scale features           |
|Manhattan  |Σ|aᵢ-bᵢ|                 |High-dim, robust to outliers           |
|Mahalanobis|√(a-b)ᵀΣ⁻¹(a-b)          |Correlated / heteroscedastic features  |
|Cosine     |1 - (a·b)/(‖a‖‖b‖)       |Text, embeddings (magnitude irrelevant)|
|Hamming    |Count differing positions|Binary / categorical strings           |

### Metric Selection Matrix

|Situation                    |Use                         |
|-----------------------------|----------------------------|
|Balanced classes             |Accuracy, F1                |
|Imbalanced, FN costly        |Recall, F-beta (β>1), PR-AUC|
|Imbalanced, FP costly        |Precision, F-beta (β<1)     |
|Ranking / threshold-free eval|ROC-AUC                     |
|Heavy imbalance              |PR-AUC > ROC-AUC            |
|Multiple operating points    |Full ROC or PR curve        |

### Algorithm Selector

|Situation                           |Algorithm                          |
|------------------------------------|-----------------------------------|
|Small dataset, non-linear boundary  |K-NN or SVM-RBF                    |
|Large dataset, non-linear           |Gradient Boosting, Random Forest   |
|Linearly separable, high-dim text   |LinearSVC                          |
|Need probabilities + linear         |Logistic Regression                |
|Gaussian classes, equal covariance  |LDA                                |
|Gaussian classes, unequal covariance|QDA                                |
|Diverse models available            |Voting / Stacking                  |
|Few labels, much unlabeled          |Semi-supervised (Label Propagation)|

### Imbalance Handling Quick Reference

|Imbalance Ratio  |Strategy                                |
|-----------------|----------------------------------------|
|< 5:1            |`class_weight='balanced'`               |
|5:1 – 20:1       |SMOTE + `class_weight='balanced'`       |
|> 20:1           |SMOTE-Tomek or ADASYN + threshold tuning|
|Extreme (> 100:1)|Anomaly detection framing               |

### The Golden Rules

```
1. Accuracy ≠ performance on imbalanced data. Ever.
2. SMOTE goes inside the pipeline, never before the split.
3. The decision threshold is a business decision, not a default.
4. Always scale before K-NN or SVM.
5. Use stratified K-fold CV, always.
6. Report the full confusion matrix, not just one metric.
7. For imbalanced data: PR-AUC > ROC-AUC.
8. Support vectors define the SVM boundary — not all training points.
9. K in K-NN is a bias-variance dial: high K = more bias, less variance.
10. LDA is a classifier AND a dimensionality reducer — use both properties.
```

-----

*Module 7 — Classification and Metrics | Machine Learning Curriculum*  
*Next: Module 8 — Ensemble Methods and Boosting*
