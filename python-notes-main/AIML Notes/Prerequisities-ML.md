# 📐 Mathematical Foundations of Machine Learning

### A Beginner-Friendly Guide — Intuition First, Formulas Second

> **Who is this for?** Anyone building intuition for the math behind ML — whether for interviews, GitHub portfolios, or honest self-study. Every concept is explained simply before being made formal.

-----

## 📚 Table of Contents

1. [Linear Algebra](#1-linear-algebra)
- [Vectors](#11-vectors)
- [Matrices](#12-matrices)
- [Systems of Linear Equations](#13-systems-of-linear-equations)
- [Eigenvalues & Eigenvectors](#14-eigenvalues--eigenvectors)
1. [Statistics & Probability](#2-statistics--probability)
- [Probability Basics](#21-probability-basics)
- [Random Variables](#22-random-variables)
- [Distributions](#23-distributions)
- [Expectation & Variance](#24-expectation--variance)
- [Bayes’ Theorem](#25-bayes-theorem)
1. [Gradient Descent](#3-gradient-descent)
- [Optimization & Loss Functions](#31-optimization--loss-functions)
- [Gradients & Partial Derivatives](#32-gradients--partial-derivatives)
- [The Update Rule](#33-the-update-rule)
- [Learning Rate & Convergence](#34-learning-rate--convergence)
- [Batch vs Stochastic Gradient Descent](#35-batch-vs-stochastic-gradient-descent)

-----

# 1. Linear Algebra

> **One-sentence summary:** Linear algebra is the language of data — it gives us tools to represent, transform, and analyze structured information efficiently.

-----

## 1.1 Vectors

### 🧠 Intuition

Imagine you want to describe a house for sale. You might list: 3 bedrooms, 2 bathrooms, 1500 sq ft, priced at $300,000. That list of numbers **is** a vector. A vector is simply an ordered list of numbers that together describe something.

Geometrically, a vector is an arrow pointing from the origin to a point in space. In 2D, the vector `[3, 4]` points 3 units right and 4 units up.

**Row vs Column vectors:**

- Row vector: numbers arranged horizontally → `[3, 4, 5]`
- Column vector: numbers arranged vertically (the default in ML)

### 📐 Mathematical Formulation

A **column vector** with n elements:

```
      ⎡ x₁ ⎤
x  =  ⎢ x₂ ⎥   ∈ ℝⁿ
      ⎢ ⋮  ⎥
      ⎣ xₙ ⎦
```

**Vector Addition** (element-wise):

```
a + b = [a₁ + b₁,  a₂ + b₂,  ...,  aₙ + bₙ]
```

**Scalar Multiplication** (scale every element):

```
c · a = [c·a₁,  c·a₂,  ...,  c·aₙ]
```

**Dot Product** (produces a single number):

```
a · b = a₁b₁ + a₂b₂ + ... + aₙbₙ = Σᵢ aᵢbᵢ
```

**L2 Norm** (Euclidean length of the vector):

```
‖x‖₂ = √(x₁² + x₂² + ... + xₙ²)
```

**L1 Norm** (sum of absolute values):

```
‖x‖₁ = |x₁| + |x₂| + ... + |xₙ|
```

### 🔢 Worked Example

Let `a = [1, 2, 3]` and `b = [4, 0, -1]`.

**Addition:**

```
a + b = [1+4, 2+0, 3+(-1)] = [5, 2, 2]
```

**Scalar multiplication** (c = 2):

```
2 · a = [2×1, 2×2, 2×3] = [2, 4, 6]
```

**Dot product:**

```
a · b = (1×4) + (2×0) + (3×-1)
      = 4 + 0 + (-3)
      = 1
```

**L2 norm of a:**

```
‖a‖₂ = √(1² + 2² + 3²) = √(1 + 4 + 9) = √14 ≈ 3.74
```

**L1 norm of a:**

```
‖a‖₁ = |1| + |2| + |3| = 6
```

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 0, -1])

print(a + b)           # [5, 2, 2]
print(2 * a)           # [2, 4, 6]
print(np.dot(a, b))    # 1
print(np.linalg.norm(a, 2))  # 3.74
print(np.linalg.norm(a, 1))  # 6.0
```

### 🤖 Machine Learning Connection

|Concept                 |Where it’s Used                   |Why it Matters                                                               |
|------------------------|----------------------------------|-----------------------------------------------------------------------------|
|**Vector as data point**|Every ML algorithm                |A single training example (e.g., a customer’s age, income, spend) is a vector|
|**Dot product**         |Linear regression, neural networks|`ŷ = w · x` computes a prediction as a weighted sum of features              |
|**Cosine similarity**   |NLP, recommender systems          |`cos(θ) = (a·b)/(‖a‖‖b‖)` measures how similar two vectors are               |
|**L2 norm**             |Regularization (Ridge)            |Penalizes large weights to prevent overfitting                               |
|**L1 norm**             |Regularization (Lasso)            |Drives some weights to exactly zero (feature selection)                      |

**Concrete example:** In a spam classifier, each email might be represented as a vector where each element counts how often a word appears. The dot product of this vector with a learned weight vector produces a “spam score.”

### ⚠️ Common Pitfalls

1. **Confusing dot product with element-wise multiplication.** `a · b` produces a *scalar*. Element-wise multiplication `a ⊙ b` produces another *vector*. These are very different operations.
1. **Ignoring vector orientation.** In ML, data points are typically column vectors `(n × 1)`. Mixing row and column vectors causes shape errors in code that can be silent and produce wrong results.
1. **Thinking L1 and L2 norms are interchangeable.** L2 is smooth and penalizes large values heavily. L1 is sparse-inducing and more robust to outliers. Choosing the wrong one changes your model’s behavior significantly.

-----

## 1.2 Matrices

### 🧠 Intuition

A matrix is just a table of numbers — like a spreadsheet. If you have 100 customers and each one is described by 5 features, your dataset is naturally a `100 × 5` matrix. Each row is a customer; each column is a feature.

Matrices are also **transformations** — multiplying a vector by a matrix can rotate, scale, or project it into a different space. This is the core of how neural networks work.

### 📐 Mathematical Formulation

A matrix `A` with `m` rows and `n` columns:

```
      ⎡ a₁₁  a₁₂  ···  a₁ₙ ⎤
A  =  ⎢ a₂₁  a₂₂  ···  a₂ₙ ⎥   ∈ ℝᵐˣⁿ
      ⎢  ⋮    ⋮         ⋮  ⎥
      ⎣ aₘ₁  aₘ₂  ···  aₘₙ ⎦
```

**Matrix Addition** (same shape, element-wise):

```
(A + B)ᵢⱼ = Aᵢⱼ + Bᵢⱼ
```

**Matrix Multiplication** (A is m×k, B is k×n → result is m×n):

```
(AB)ᵢⱼ = Σₖ Aᵢₖ · Bₖⱼ
```

The (i,j) entry is the dot product of row i of A with column j of B.

**Transpose** (flip rows and columns):

```
(Aᵀ)ᵢⱼ = Aⱼᵢ
```

**Identity Matrix** (acts like the number 1 for matrices):

```
      ⎡ 1  0  0 ⎤
I₃ =  ⎢ 0  1  0 ⎥     AI = IA = A
      ⎣ 0  0  1 ⎦
```

**Matrix Inverse** (only for square, invertible matrices):

```
A · A⁻¹ = A⁻¹ · A = I
```

### 🔢 Worked Example

Let:

```
A = ⎡ 1  2 ⎤    B = ⎡ 5  6 ⎤
    ⎣ 3  4 ⎦        ⎣ 7  8 ⎦
```

**Matrix Addition:**

```
A + B = ⎡ 1+5  2+6 ⎤ = ⎡  6   8 ⎤
        ⎣ 3+7  4+8 ⎦   ⎣ 10  12 ⎦
```

**Matrix Multiplication (A × B):**

```
(1,1): row 1 of A · col 1 of B = (1×5) + (2×7) = 5 + 14 = 19
(1,2): row 1 of A · col 2 of B = (1×6) + (2×8) = 6 + 16 = 22
(2,1): row 2 of A · col 1 of B = (3×5) + (4×7) = 15 + 28 = 43
(2,2): row 2 of A · col 2 of B = (3×6) + (4×8) = 18 + 32 = 50

A × B = ⎡ 19  22 ⎤
        ⎣ 43  50 ⎦
```

**Transpose:**

```
Aᵀ = ⎡ 1  3 ⎤
     ⎣ 2  4 ⎦
```

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(A + B)          # [[ 6  8], [10 12]]
print(A @ B)          # [[19 22], [43 50]]
print(A.T)            # [[1 3], [2 4]]
print(np.linalg.inv(A))  # inverse of A
```

### 🤖 Machine Learning Connection

|Concept                  |Where it’s Used        |Why it Matters                                               |
|-------------------------|-----------------------|-------------------------------------------------------------|
|**Matrix as dataset**    |All supervised learning|Shape `(n_samples × n_features)` is the universal data format|
|**Matrix multiplication**|Neural networks        |Each layer computes `Z = XW + b` — a matrix multiply         |
|**Transpose**            |Computing gradients    |`XᵀX` appears in the normal equations for linear regression  |
|**Matrix inverse**       |Closed-form solutions  |Ordinary Least Squares solution: `w = (XᵀX)⁻¹ Xᵀy`           |

**Concrete example:** In a neural network forward pass with 32 training examples and 10 input features feeding into a layer of 8 neurons, the weight matrix is `(10 × 8)`, the input is `(32 × 10)`, and `X @ W` is `(32 × 8)` — one output per neuron per example. Matrix multiplication computes all 32 × 8 = 256 values at once.

### ⚠️ Common Pitfalls

1. **Matrix multiplication is NOT commutative.** In general, `AB ≠ BA`. Order matters enormously — check shapes before multiplying.
1. **Not every square matrix is invertible.** If the determinant is zero (singular matrix), the inverse doesn’t exist. This happens when features are perfectly correlated (multicollinearity).
1. **Confusing `A.T @ A` with `A @ A.T`.** These produce matrices of very different shapes and meanings. `XᵀX` is a covariance-like `(features × features)` matrix; `XXᵀ` is a `(samples × samples)` similarity matrix.

-----

## 1.3 Systems of Linear Equations

### 🧠 Intuition

A system of linear equations is a set of constraints that must all be satisfied at once. For example:

- “I bought 2 apples and 3 oranges for $7”
- “I bought 1 apple and 2 oranges for $4”

What is the price of each fruit? That’s a system of 2 equations with 2 unknowns — exactly what matrix algebra is built to solve.

### 📐 Mathematical Formulation

A system of `m` equations with `n` unknowns:

```
a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ = b₁
a₂₁x₁ + a₂₂x₂ + ... + a₂ₙxₙ = b₂
...
aₘ₁x₁ + aₘ₂x₂ + ... + aₘₙxₙ = bₘ
```

Written compactly in matrix form:

```
Ax = b
```

Where `A` is the `(m×n)` coefficient matrix, `x` is the unknown vector, and `b` is the right-hand side.

**Solution** (when A is square and invertible):

```
x = A⁻¹b
```

### 🔢 Worked Example

Using the apple/orange problem:

```
2x + 3y = 7   →   ⎡ 2  3 ⎤ ⎡ x ⎤   ⎡ 7 ⎤
1x + 2y = 4       ⎣ 1  2 ⎦ ⎣ y ⎦ = ⎣ 4 ⎦
```

**Step 1:** Find A⁻¹

```
det(A) = (2×2) - (3×1) = 4 - 3 = 1

A⁻¹ = (1/det) × ⎡  2  -3 ⎤ = ⎡  2  -3 ⎤
                 ⎣ -1   2 ⎦   ⎣ -1   2 ⎦
```

**Step 2:** Solve `x = A⁻¹b`

```
⎡ x ⎤   ⎡  2  -3 ⎤ ⎡ 7 ⎤   ⎡ (2×7) + (-3×4) ⎤   ⎡ 14 - 12 ⎤   ⎡ 2 ⎤
⎣ y ⎦ = ⎣ -1   2 ⎦ ⎣ 4 ⎦ = ⎣ (-1×7) + (2×4) ⎦ = ⎣ -7 + 8  ⎦ = ⎣ 1 ⎦
```

An apple costs **$2** and an orange costs **$1**. ✓

```python
import numpy as np

A = np.array([[2, 3], [1, 2]])
b = np.array([7, 4])
x = np.linalg.solve(A, b)
print(x)  # [2., 1.]
```

### 🤖 Machine Learning Connection

Linear systems are the foundation of **Linear Regression**. Given training data `X` (features) and `y` (targets), finding the weights `w` that best fit the data solves:

```
Xw ≈ y
```

The exact closed-form solution (Normal Equation) is:

```
w = (XᵀX)⁻¹ Xᵀy
```

This is literally solving a system of linear equations. However, when data is large, computing `A⁻¹` is expensive (`O(n³)`), which is why gradient descent is used in practice instead.

### ⚠️ Common Pitfalls

1. **Assuming a unique solution always exists.** A system can have no solution (contradictory constraints) or infinitely many solutions (underdetermined). In ML, with more features than samples, your system is underdetermined.
1. **Using `np.linalg.inv(A) @ b` instead of `np.linalg.solve(A, b)`.** The `solve` function is numerically more stable and faster. Explicitly computing the inverse is almost never necessary.
1. **Ignoring conditioning.** A “nearly singular” matrix (very small determinant) makes the solution highly sensitive to noise. This is the multicollinearity problem in regression.

-----

## 1.4 Eigenvalues & Eigenvectors

### 🧠 Intuition

Imagine pushing a piece of jelly in some direction. Most directions cause the jelly to deform in a complicated way. But there are a few *special directions* — push along those, and the jelly just stretches or shrinks in place. It doesn’t rotate or distort. Those special directions are **eigenvectors**. The amount of stretch is the **eigenvalue**.

More precisely: when you apply a matrix transformation to an eigenvector, you get back the *same vector*, just scaled.

### 📐 Mathematical Formulation

For a square matrix `A`, a non-zero vector `v` is an eigenvector with eigenvalue `λ` if:

```
Av = λv
```

- `A` — the square matrix (the transformation)
- `v` — the eigenvector (a special direction, non-zero)
- `λ` (lambda) — the eigenvalue (the scaling factor)

**Finding eigenvalues:** Solve the characteristic equation:

```
det(A - λI) = 0
```

**Visual intuition:** Imagine `A` as a linear transformation that stretches the x-axis by 3 and the y-axis by 1. The x-axis vector `[1,0]` is an eigenvector with λ=3; the y-axis vector `[0,1]` is an eigenvector with λ=1.

### 🔢 Worked Example

Let:

```
A = ⎡ 3  1 ⎤
    ⎣ 0  2 ⎦
```

**Step 1: Find eigenvalues** via `det(A - λI) = 0`

```
A - λI = ⎡ 3-λ   1  ⎤
         ⎣  0   2-λ  ⎦

det = (3-λ)(2-λ) - (1)(0) = 0
    = λ² - 5λ + 6 = 0
    = (λ - 3)(λ - 2) = 0

λ₁ = 3,  λ₂ = 2
```

**Step 2: Find eigenvector for λ₁ = 3**

```
(A - 3I)v = 0

⎡ 0  1 ⎤ ⎡ v₁ ⎤   ⎡ 0 ⎤
⎣ 0 -1 ⎦ ⎣ v₂ ⎦ = ⎣ 0 ⎦

→ v₂ = 0,  v₁ is free → v₁ = ⎡ 1 ⎤
                               ⎣ 0 ⎦
```

**Verify:**

```
A · v₁ = ⎡ 3  1 ⎤ ⎡ 1 ⎤ = ⎡ 3 ⎤ = 3 · ⎡ 1 ⎤  ✓
         ⎣ 0  2 ⎦ ⎣ 0 ⎦   ⎣ 0 ⎦       ⎣ 0 ⎦
```

```python
import numpy as np

A = np.array([[3, 1], [0, 2]])
eigenvalues, eigenvectors = np.linalg.eig(A)
print("Eigenvalues:", eigenvalues)      # [3. 2.]
print("Eigenvectors:\n", eigenvectors)
```

### 🤖 Machine Learning Connection

**Principal Component Analysis (PCA)** is the most direct application.

PCA finds the directions of *maximum variance* in your data. These directions are exactly the eigenvectors of the data’s covariance matrix. The eigenvalues tell you *how much variance* is explained by each direction.

**Workflow:**

1. Compute the covariance matrix `C = (1/n) XᵀX`
1. Compute eigenvectors and eigenvalues of `C`
1. Sort eigenvectors by their eigenvalues (largest first)
1. Project data onto top-k eigenvectors → dimensionality reduction

**Why this matters:** A 1000-feature dataset might have 95% of its variance explained by just 10 eigenvectors. Keeping only those 10 directions compresses your data 100× with minimal information loss — speeding up training and reducing overfitting.

```python
from sklearn.decomposition import PCA
import numpy as np

X = np.random.randn(100, 20)   # 100 samples, 20 features
pca = PCA(n_components=5)      # Keep top 5 principal components
X_reduced = pca.fit_transform(X)   # Shape: (100, 5)

print(pca.explained_variance_ratio_)  # Fraction of variance per component
```

### ⚠️ Common Pitfalls

1. **Thinking eigenvectors always form a complete basis.** Non-symmetric matrices may have complex eigenvalues or fewer linearly independent eigenvectors than their dimension. PCA works cleanly because covariance matrices are always symmetric and positive semi-definite.
1. **Forgetting to standardize data before PCA.** Features with large scales (e.g., income in dollars vs. age in years) will dominate variance. Always center and scale your data first (`StandardScaler`).
1. **Equating eigenvalue magnitude with “importance” in all contexts.** Eigenvalues represent variance in PCA — but in other contexts (e.g., graph Laplacians) their interpretation is completely different.

-----

# 2. Statistics & Probability

> **One-sentence summary:** Statistics and probability give us the language to reason about uncertainty — essential because ML models make predictions about an inherently uncertain world.

-----

## 2.1 Probability Basics

### 🧠 Intuition

Probability is just a formal way of quantifying how likely something is. If you flip a fair coin, there’s a 50% chance of heads. If it rains 3 out of 10 days in a city, the probability of rain on any given day is roughly 30%.

The key insight for ML: we rarely know things for certain. A model that says “this email is 87% likely spam” is much more useful than one that just says “spam” without any measure of confidence.

### 📐 Mathematical Formulation

**Sample Space (Ω):** The set of all possible outcomes.

```
Coin flip: Ω = {H, T}
Die roll:  Ω = {1, 2, 3, 4, 5, 6}
```

**Event (E):** A subset of the sample space.

```
E = "roll an even number" = {2, 4, 6}
```

**Probability:** A function P: events → [0, 1] satisfying:

```
P(Ω) = 1        (something always happens)
P(∅) = 0        (impossible event has 0 probability)
P(A ∪ B) = P(A) + P(B)  if A and B are mutually exclusive
```

**Conditional Probability** — probability of A *given that* B has occurred:

```
P(A | B) = P(A ∩ B) / P(B)     [provided P(B) > 0]
```

**Independence** — A and B are independent if:

```
P(A ∩ B) = P(A) · P(B)
```

Equivalently: `P(A|B) = P(A)` — knowing B tells you nothing about A.

### 🔢 Worked Example

A bag has 3 red and 2 blue marbles (5 total).

**P(red)** = 3/5 = 0.6

**P(red on 2nd draw | red on 1st draw, no replacement):**

```
After drawing 1 red: 2 red, 2 blue remain (4 total)
P(red | 1st was red) = 2/4 = 0.5
```

**Are 1st and 2nd draws independent?**

```
P(both red) = 3/5 × 2/4 = 6/20 = 0.3
P(red) × P(red) = 0.6 × 0.6 = 0.36
0.3 ≠ 0.36  →  Not independent (draws without replacement are dependent)
```

### 🤖 Machine Learning Connection

- **Classification outputs** are probabilities: `P(spam | email features) = 0.87`
- **Naive Bayes** directly uses conditional probability: `P(class | features)`
- **Dropout regularization** randomly disables neurons with some probability during training
- **Data augmentation** applies transformations with certain probabilities to improve generalization

### ⚠️ Common Pitfalls

1. **Confusing P(A|B) with P(B|A).** “P(disease | positive test)” is very different from “P(positive test | disease).” Mixing these up leads to the classic base rate fallacy.
1. **Assuming independence without justification.** Naive Bayes literally assumes all features are conditionally independent given the class — this is almost never true, yet the model often works well anyway.
1. **Treating 0% and 100% as valid probabilities in practice.** A model that outputs probability exactly 0 or 1 has infinite log-loss on any wrong prediction. Use Laplace smoothing or probability clipping.

-----

## 2.2 Random Variables

### 🧠 Intuition

A random variable is a variable whose value is determined by a random process. It’s a function that maps outcomes to numbers so we can do math with them. For example, “the number of heads in 10 coin flips” is a random variable — it could be 0, 1, 2, …, up to 10.

### 📐 Mathematical Formulation

**Discrete Random Variable:** Takes countable values (integers, categories).

**PMF (Probability Mass Function):** `P(X = x)` — gives the exact probability of each value.

```
Properties:  P(X = x) ≥ 0  for all x
             Σₓ P(X = x) = 1
```

**Continuous Random Variable:** Takes values in a continuous range (e.g., real numbers).

**PDF (Probability Density Function):** `f(x)` — describes the relative likelihood at each point.

```
Properties:  f(x) ≥ 0  for all x
             ∫₋∞^∞ f(x) dx = 1

P(a ≤ X ≤ b) = ∫ₐᵇ f(x) dx   (area under the curve)
```

> ⚠️ For a continuous variable, `P(X = exactly 5.000) = 0`. Probability only has meaning over intervals.

### 🔢 Worked Example

**Discrete:** Rolling a fair die. Let X = outcome.

```
P(X=1) = P(X=2) = ... = P(X=6) = 1/6

P(X ≤ 3) = P(X=1) + P(X=2) + P(X=3) = 3/6 = 0.5
```

**Continuous:** Suppose heights follow a normal distribution. The probability that a randomly selected person is between 165cm and 175cm is the area under the normal PDF curve between those two values — computed via integration or a table.

### 🤖 Machine Learning Connection

- **Model outputs** for classification are discrete PMFs: `[P(cat), P(dog), P(bird)]`
- **Softmax** converts raw scores into a valid PMF (values sum to 1)
- **Sampling** from distributions is used in variational autoencoders (VAEs) and Bayesian networks
- **Continuous PDFs** model feature distributions in Gaussian Mixture Models (GMMs)

### ⚠️ Common Pitfalls

1. **Forgetting that PDFs can exceed 1.** A PDF value of `f(x) = 5` is perfectly valid — it’s not a probability, it’s a density. The area must equal 1, not the height.
1. **Using a PMF where a PDF is needed.** Discretizing continuous features too coarsely (e.g., binning ages into 5 buckets) loses information. Many models work better with the raw continuous values.

-----

## 2.3 Distributions

### 🧠 Intuition

Distributions describe the “shape” of randomness. Some data clusters around a single value with a bell-curve shape (Normal). Some data is binary — either yes or no (Bernoulli). Some counts follow a Binomial pattern. Knowing which distribution fits your data guides your choice of model and loss function.

### 📐 Mathematical Formulation

#### Normal (Gaussian) Distribution — `N(μ, σ²)`

```
f(x) = (1 / (σ√(2π))) · exp(−(x − μ)² / (2σ²))
```

- `μ` (mu) — mean (center of the bell curve)
- `σ` (sigma) — standard deviation (width of the curve)
- `σ²` — variance
- **68-95-99.7 rule:** 68% of data falls within ±1σ, 95% within ±2σ, 99.7% within ±3σ

#### Bernoulli Distribution — `Bern(p)`

```
P(X = 1) = p       (success)
P(X = 0) = 1 − p   (failure)
```

- `p` — probability of success
- Used for **binary outcomes** (yes/no, spam/not spam)

#### Binomial Distribution — `Bin(n, p)`

```
P(X = k) = C(n,k) · pᵏ · (1−p)ⁿ⁻ᵏ
```

- `n` — number of trials
- `k` — number of successes
- `C(n,k)` — “n choose k” = n! / (k!(n-k)!)
- Models: “how many out of n emails are spam?”

### 🔢 Worked Example

**Bernoulli:** Is a coin flip heads? p = 0.5

```
P(X=1) = 0.5,  P(X=0) = 0.5
```

**Binomial:** Flip a fair coin 5 times. What’s P(exactly 3 heads)?

```
P(X = 3) = C(5,3) · (0.5)³ · (0.5)²
         = 10 · 0.125 · 0.25
         = 10 × 0.03125
         = 0.3125
```

(There’s a ~31.25% chance of getting exactly 3 heads in 5 flips.)

```python
from scipy.stats import binom, norm

# Binomial: P(X=3) with n=5, p=0.5
print(binom.pmf(k=3, n=5, p=0.5))   # 0.3125

# Normal: P(165 ≤ X ≤ 175) with μ=170, σ=10
print(norm.cdf(175, loc=170, scale=10) - norm.cdf(165, loc=170, scale=10))  # ~0.383
```

### 🤖 Machine Learning Connection

|Distribution           |ML Application                                                                            |
|-----------------------|------------------------------------------------------------------------------------------|
|**Normal**             |Linear regression assumes normally distributed errors; features are often assumed Gaussian|
|**Bernoulli**          |Logistic regression models binary outcomes as Bernoulli                                   |
|**Binomial**           |Modeling counts; basis for binomial deviance loss                                         |
|**Gaussian assumption**|K-Means clustering, Linear Discriminant Analysis (LDA)                                    |

**Concrete example:** Logistic regression outputs `P(y=1 | x)` — a Bernoulli probability. The binary cross-entropy loss is derived from the likelihood of the Bernoulli distribution. If you change the assumed distribution (e.g., to Poisson for count data), you get a different model and a different loss function.

### ⚠️ Common Pitfalls

1. **Assuming all data is Gaussian.** Real-world data is often skewed, heavy-tailed, or multimodal. Blindly assuming normality can invalidate statistical tests and hurt model performance.
1. **Forgetting the Binomial requires independent trials.** If events influence each other, the Binomial model is inappropriate (e.g., modeling customer purchases in a sequence).

-----

## 2.4 Expectation & Variance

### 🧠 Intuition

The **expectation** is the average value you’d expect if you repeated a random experiment many, many times. The **variance** measures how spread out the results are around that average. These two quantities capture the essence of a distribution: “where is the center, and how uncertain is it?”

### 📐 Mathematical Formulation

**Expectation (Mean):**

```
Discrete:   E[X] = Σₓ x · P(X = x)
Continuous: E[X] = ∫ x · f(x) dx
```

**Variance:**

```
Var(X) = E[(X − μ)²] = E[X²] − (E[X])²
```

- Measures the average squared deviation from the mean
- `σ² = Var(X)` — variance
- `σ = √Var(X)` — standard deviation (same units as X)

**Key properties:**

```
E[aX + b] = a·E[X] + b          (linearity)
Var(aX + b) = a²·Var(X)         (constants shift, don't scale variance)
E[X + Y] = E[X] + E[Y]          (always true)
Var(X + Y) = Var(X) + Var(Y)    (only if X and Y are independent)
```

### 🔢 Worked Example

Roll a fair die. X = outcome, values {1, 2, 3, 4, 5, 6}, each with P = 1/6.

**Expectation:**

```
E[X] = 1·(1/6) + 2·(1/6) + 3·(1/6) + 4·(1/6) + 5·(1/6) + 6·(1/6)
     = (1+2+3+4+5+6) / 6
     = 21/6
     = 3.5
```

**E[X²]:**

```
E[X²] = (1² + 2² + 3² + 4² + 5² + 6²) / 6
      = (1 + 4 + 9 + 16 + 25 + 36) / 6
      = 91/6 ≈ 15.17
```

**Variance:**

```
Var(X) = E[X²] − (E[X])²
       = 91/6 − (3.5)²
       = 15.17 − 12.25
       = 2.92
```

**Standard deviation:** σ = √2.92 ≈ 1.71

### 🤖 Machine Learning Connection

**Loss functions as expectations:** The Mean Squared Error loss is literally an expectation:

```
MSE = E[(y − ŷ)²]   (average squared prediction error)
```

**The Bias-Variance Tradeoff:** The expected test error of any model decomposes as:

```
E[(y − ŷ)²] = Bias² + Variance + Irreducible Noise
```

- **Bias** = how far off your average prediction is from the truth (underfitting)
- **Variance** = how much your predictions change with different training sets (overfitting)

A complex model (many parameters) has low bias but high variance. A simple model has high bias but low variance. The art of ML is finding the sweet spot.

### ⚠️ Common Pitfalls

1. **Confusing variance with standard deviation.** Variance is in *squared units* (hard to interpret). Standard deviation is in the same units as the data. Always report σ for communication.
1. **Thinking low variance = better model.** A model that always predicts the mean has zero variance but very high bias. You need both low bias AND low variance.

-----

## 2.5 Bayes’ Theorem

### 🧠 Intuition

You take a medical test for a rare disease. The test comes back positive. How worried should you be?

Bayes’ theorem tells you how to *update your belief* in light of new evidence. It combines:

- What you believed *before* seeing the evidence (the **prior**)
- How likely the evidence is given your hypothesis (the **likelihood**)
- To give you a new, updated belief (the **posterior**)

This is the foundation of rational reasoning under uncertainty.

### 📐 Mathematical Formulation

```
P(A | B) = [P(B | A) · P(A)] / P(B)
```

- `P(A | B)` — **Posterior**: probability of hypothesis A *given* evidence B
- `P(B | A)` — **Likelihood**: probability of seeing evidence B *if* A is true
- `P(A)` — **Prior**: initial belief in A, before seeing B
- `P(B)` — **Marginal likelihood** (normalizing constant): total probability of evidence B

**Expanding P(B) using total probability:**

```
P(B) = P(B|A)·P(A) + P(B|Aᶜ)·P(Aᶜ)
```

### 🔢 Worked Example

A disease affects 1% of the population. A test is 95% accurate:

- P(positive | disease) = 0.95 (true positive rate)
- P(positive | no disease) = 0.05 (false positive rate)

You test positive. What’s P(disease | positive)?

```
P(disease) = 0.01            (prior — rare disease)
P(no disease) = 0.99

Step 1 — P(positive):
P(pos) = P(pos|disease)·P(disease) + P(pos|no disease)·P(no disease)
       = 0.95 × 0.01  +  0.05 × 0.99
       = 0.0095 + 0.0495
       = 0.059

Step 2 — Apply Bayes:
P(disease | positive) = [P(pos|disease) · P(disease)] / P(pos)
                      = (0.95 × 0.01) / 0.059
                      = 0.0095 / 0.059
                      ≈ 0.161
```

**Only a 16% chance you actually have the disease**, despite the positive test! This is why base rates matter enormously.

### 🤖 Machine Learning Connection

**Naive Bayes Classifier** applies Bayes’ theorem directly to classification:

```
P(class | features) ∝ P(features | class) · P(class)
```

To classify an email as spam/not spam:

1. Compute `P(spam)` from training data (prior)
1. Compute `P(word | spam)` for each word (likelihood)
1. Multiply together (the “naive” independence assumption)
1. Pick the class with highest posterior

Despite the naive assumption, it works remarkably well for text classification, is fast, and handles high-dimensional data gracefully.

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

texts = ["free money now", "meeting at 3pm", "win prize free", "project update"]
labels = [1, 0, 1, 0]  # 1=spam, 0=not spam

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)
print(model.predict(vectorizer.transform(["free win prize"])))  # [1]
```

### ⚠️ Common Pitfalls

1. **Forgetting the prior (base rate neglect).** The most common Bayesian error. A 95%-accurate positive test means very little for a 1-in-10,000 disease. Always include the prior.
1. **Assuming features are truly independent in Naive Bayes.** The “naive” assumption is almost always violated. The model still often works well, but probability *estimates* (not just rankings) can be poorly calibrated.
1. **Confusing posterior with likelihood.** `P(disease|positive)` ≠ `P(positive|disease)`. These are fundamentally different quantities — the prosecutor’s fallacy exploits exactly this confusion.

-----

# 3. Gradient Descent

> **One-sentence summary:** Gradient descent is the engine that trains nearly every ML model — it’s an iterative algorithm that finds the model parameters that minimize prediction error.

-----

## 3.1 Optimization & Loss Functions

### 🧠 Intuition

Imagine you’re blindfolded on a hilly landscape, and your goal is to reach the lowest point (the valley). You can’t see the whole landscape, but you *can* feel which way is downhill beneath your feet. So you take a step in the steepest downhill direction, pause, check the slope again, and repeat.

This is gradient descent. The “landscape” is the **loss function** — a measure of how wrong your model’s predictions are. The “lowest point” is the set of parameters that make the best predictions.

### 📐 Mathematical Formulation

**Parameters:** θ = [θ₁, θ₂, …, θₙ] — the numbers your model learns (weights, biases).

**Loss Function J(θ):** Measures prediction error. Common choices:

```
Mean Squared Error (regression):
J(θ) = (1/n) Σᵢ (yᵢ − ŷᵢ)²      where ŷᵢ = model prediction

Binary Cross-Entropy (classification):
J(θ) = −(1/n) Σᵢ [yᵢ log(ŷᵢ) + (1−yᵢ) log(1−ŷᵢ)]
```

**Goal:** Find θ* that minimizes J(θ):

```
θ* = argmin_θ J(θ)
```

### 🤖 Machine Learning Connection

The loss function is the *objective* — it defines what “better” means for your model. Every learning algorithm is, at its core, an optimizer minimizing some loss. Choosing the right loss function is one of the most important modeling decisions:

- **MSE** penalizes large errors heavily (sensitive to outliers)
- **MAE** (Mean Absolute Error) is more robust to outliers
- **Cross-entropy** is the natural choice when outputs are probabilities

-----

## 3.2 Gradients & Partial Derivatives

### 🧠 Intuition

A **derivative** tells you the slope of a function at a point — how much the output changes when you nudge the input. For a function with multiple inputs (like a loss function with many parameters), a **partial derivative** measures the slope with respect to *one* parameter at a time, holding all others fixed.

The **gradient** collects all partial derivatives into a vector — it points in the direction of *steepest increase* of the function. To go downhill, we move in the *opposite* direction of the gradient.

### 📐 Mathematical Formulation

**Partial derivative** of J with respect to θⱼ:

```
∂J/∂θⱼ = rate of change of J when only θⱼ changes
```

**Gradient** (vector of all partial derivatives):

```
∇J(θ) = ⎡ ∂J/∂θ₁ ⎤
         ⎢ ∂J/∂θ₂ ⎥
         ⎢   ⋮    ⎥
         ⎣ ∂J/∂θₙ ⎦
```

**Visual intuition:** If J(θ₁, θ₂) is a bowl-shaped surface, the gradient at any point is a 2D arrow on the surface pointing uphill. Going downhill means subtracting a scaled version of this arrow.

### 🔢 Worked Example

Let `J(θ) = θ² + 2θ + 1` (a simple 1D parabola, minimum at θ = −1).

```
dJ/dθ = 2θ + 2

At θ = 2:   gradient = 2(2) + 2 = 6   (slope is 6, going up to the right)
At θ = -1:  gradient = 2(-1) + 2 = 0  (at the minimum — flat!)
At θ = -3:  gradient = 2(-3) + 2 = -4 (going down to the right)
```

The gradient is zero at the minimum — this is how we know we’ve converged.

-----

## 3.3 The Update Rule

### 🧠 Intuition

At each step, we measure the slope (gradient) of the loss at our current position, then take a step in the *opposite* direction (downhill). The size of the step is controlled by the **learning rate** η (eta).

### 📐 Mathematical Formulation

**Gradient Descent Update Rule:**

```
θ ← θ − η · ∇J(θ)
```

Breaking it down:

- `θ` — current parameters
- `η` (eta) — learning rate (step size, a positive scalar you choose)
- `∇J(θ)` — gradient of the loss at current parameters
- `θ − η · ∇J(θ)` — new parameters after one step downhill

Repeat until convergence (gradient ≈ 0 or loss stops decreasing).

### 🔢 Worked Example

Using `J(θ) = θ²`, gradient = `2θ`, and learning rate `η = 0.3`. Start at `θ₀ = 4`.

```
Step 0: θ = 4.0,   gradient = 2(4) = 8.0
Step 1: θ = 4.0 − 0.3 × 8.0 = 4.0 − 2.4 = 1.6
        gradient = 2(1.6) = 3.2

Step 2: θ = 1.6 − 0.3 × 3.2 = 1.6 − 0.96 = 0.64
        gradient = 2(0.64) = 1.28

Step 3: θ = 0.64 − 0.3 × 1.28 = 0.64 − 0.384 = 0.256
        ...

Converging toward θ* = 0  (where J(θ) = θ² is minimized)
```

```python
theta = 4.0
eta = 0.3

for i in range(10):
    gradient = 2 * theta           # dJ/dtheta for J = theta^2
    theta = theta - eta * gradient
    print(f"Step {i+1}: theta = {theta:.4f}, J = {theta**2:.4f}")
```

### 🤖 Machine Learning Connection

For **linear regression** with parameters `w` and `b`:

```
J(w, b) = (1/2n) Σᵢ (yᵢ − (wᵀxᵢ + b))²

Gradients:
∂J/∂w = (1/n) Xᵀ(ŷ − y)
∂J/∂b = (1/n) Σᵢ (ŷᵢ − yᵢ)

Updates:
w ← w − η · (1/n) Xᵀ(ŷ − y)
b ← b − η · (1/n) Σᵢ (ŷᵢ − yᵢ)
```

This same logic extends to **logistic regression** and **neural networks** (via backpropagation, which is just the chain rule applied to compute gradients through many layers).

-----

## 3.4 Learning Rate & Convergence

### 🧠 Intuition

The learning rate η controls *how big a step* you take at each iteration.

- **Too large:** You overshoot the minimum, bouncing back and forth or even diverging
- **Too small:** You take tiny steps and convergence takes forever
- **Just right:** You reliably descend toward the minimum at a good pace

Think of it like adjusting a thermostat. Cranking it by 30° every time it’s slightly wrong means it overshoots and oscillates. Adjusting by 0.001° means you wait hours to reach temperature. The right adjustment is somewhere in between.

### 📐 Mathematical Formulation

**Convergence** is typically declared when:

```
‖∇J(θ)‖ < ε       (gradient is nearly zero)
or
|J(θ_new) − J(θ_old)| < ε   (loss barely changes)
```

where ε is a small tolerance (e.g., 1e-6).

**Local vs Global Minima:**

- **Convex functions** (like MSE for linear regression) have one minimum — gradient descent always finds it.
- **Non-convex functions** (like neural network loss surfaces) have many local minima and saddle points. Gradient descent may get stuck, but in practice, local minima in deep networks are often close to the global minimum.

**Visual intuition of local vs global:**

```
        *                        ← starting point
       / \         ___
      /   \       /   \
-----/     \*____/     \*global_min
              local_min
```

If you start near the local minimum, gradient descent converges there and misses the global minimum.

### 🤖 Machine Learning Connection

- **Learning rate schedules** — start with a large η and decrease it over time (e.g., cosine annealing, step decay)
- **Adaptive optimizers** — Adam, RMSProp automatically adjust the effective learning rate per parameter
- **Early stopping** — stop training when validation loss stops improving (prevents overfitting)

```python
import torch.optim as optim

# Adam optimizer - adaptive learning rates
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Learning rate scheduler
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)
```

### ⚠️ Common Pitfalls

1. **Setting η too high and thinking the model is broken.** Loss oscillating wildly or exploding is almost always a learning rate problem — try dividing it by 10.
1. **Not tracking the loss curve.** Always plot training loss vs iterations. A healthy curve decreases smoothly. Spikes, flat regions, or divergence all tell you something specific is wrong.
1. **Declaring convergence too early.** Loss can plateau temporarily before continuing to decrease. Use a patience parameter: only stop if loss hasn’t improved for N steps.

-----

## 3.5 Batch vs Stochastic Gradient Descent

### 🧠 Intuition

When computing the gradient, how many training examples should you use?

- **Batch GD (full batch):** Use *all* examples. Accurate gradient, but very slow for large datasets.
- **Stochastic GD (SGD):** Use *one* random example at a time. Very fast, but the gradient estimate is noisy — the path to the minimum is jagged.
- **Mini-Batch GD:** Use a small random subset (e.g., 32 or 256 examples). The sweet spot — good gradient estimate, efficient computation, works with GPUs.

In practice, “SGD” in most ML frameworks means mini-batch SGD.

### 📐 Mathematical Formulation

Let the dataset have n samples. The full loss is:

```
J(θ) = (1/n) Σᵢ₌₁ⁿ Lᵢ(θ)
```

Where `Lᵢ` is the loss on the i-th example.

**Batch GD:** Gradient over all n examples:

```
θ ← θ − η · (1/n) Σᵢ₌₁ⁿ ∇Lᵢ(θ)
```

**Stochastic GD:** Gradient over one random example:

```
θ ← θ − η · ∇Lᵢ(θ)     (i sampled randomly)
```

**Mini-Batch GD:** Gradient over a batch B of size m:

```
θ ← θ − η · (1/m) Σᵢ∈B ∇Lᵢ(θ)
```

### 🔢 Worked Example

Suppose you have 1,000,000 training examples.

**Batch GD:**

- 1 gradient computation uses all 1M examples
- Very accurate but takes ~1M multiplications per step
- 1000 epochs = 1000 × 1M computations

**Mini-Batch GD** (batch size 256):

- 1 gradient computation uses 256 examples
- ~3906 mini-batches per epoch
- Much faster per step, and often achieves better generalization because noise helps escape shallow minima

```python
# PyTorch mini-batch training loop
from torch.utils.data import DataLoader

loader = DataLoader(dataset, batch_size=256, shuffle=True)

for epoch in range(100):
    for X_batch, y_batch in loader:
        optimizer.zero_grad()
        predictions = model(X_batch)
        loss = loss_fn(predictions, y_batch)
        loss.backward()      # compute gradients
        optimizer.step()     # update parameters
```

### 🤖 Machine Learning Connection

|Method           |Use Case                       |Tradeoff                                    |
|-----------------|-------------------------------|--------------------------------------------|
|**Batch GD**     |Small datasets, convex problems|Exact gradients, but slow & memory-intensive|
|**SGD**          |Online learning, streaming data|Very fast, but noisy and hard to tune       |
|**Mini-Batch GD**|Deep learning (default)        |Best of both — efficient and stable         |

**Why noise can help:** Mini-batch noise acts as a regularizer — the stochastic nature means the optimizer explores more of the loss surface, making it less likely to get permanently stuck in a sharp local minimum. This is one reason SGD often generalizes better than exact second-order methods.

### ⚠️ Common Pitfalls

1. **Not shuffling data between epochs.** If your data is sorted (e.g., all class 0 then all class 1), mini-batches will be unrepresentative. Always shuffle.
1. **Choosing an extreme batch size.** Very large batches (close to full batch) converge to sharp minima that generalize poorly. Very small batches are noisy and slow. Batch sizes of 32–512 are the typical sweet spot.
1. **Forgetting `optimizer.zero_grad()` in PyTorch.** Gradients accumulate by default in PyTorch. Forgetting to zero them means you’re adding new gradients to old ones, corrupting every update.

-----

# 🎯 Summary Cheat Sheet

## Linear Algebra at a Glance

|Concept           |Formula            |ML Use                     |
|------------------|-------------------|---------------------------|
|Dot product       |`a · b = Σ aᵢbᵢ`   |Predictions, similarity    |
|Matrix multiply   |`(AB)ᵢⱼ = Σ AᵢₖBₖⱼ`|Neural network layers      |
|Transpose         |`(Aᵀ)ᵢⱼ = Aⱼᵢ`     |Normal equations, gradients|
|Inverse           |`A⁻¹: AA⁻¹ = I`    |Closed-form regression     |
|Eigendecomposition|`Av = λv`          |PCA, graph algorithms      |
|L2 norm           |`‖x‖₂ = √(Σxᵢ²)`   |Ridge regularization       |
|L1 norm           |`‖x‖₁ = Σ          |xᵢ                         |

## Probability & Statistics at a Glance

|Concept                |Formula                           |ML Use                     |
|-----------------------|----------------------------------|---------------------------|
|Conditional probability|`P(A                              |B) = P(A∩B)/P(B)`          |
|Bayes’ theorem         |`P(A                              |B) = P(B                   |
|Expectation            |`E[X] = Σ x·P(X=x)`               |Loss functions, risk       |
|Variance               |`Var(X) = E[X²] − E[X]²`          |Bias-variance tradeoff     |
|Normal distribution    |`f(x) = (1/σ√2π)·exp(−(x−μ)²/2σ²)`|Feature assumptions, errors|

## Gradient Descent at a Glance

|Concept      |Formula                        |Role                              |
|-------------|-------------------------------|----------------------------------|
|Loss function|`J(θ) = (1/n)Σ(y−ŷ)²`          |Measures model error              |
|Gradient     |`∇J(θ) = [∂J/∂θ₁, ..., ∂J/∂θₙ]`|Direction of steepest increase    |
|Update rule  |`θ ← θ − η∇J(θ)`               |Core learning step                |
|Learning rate|`η` (tune this!)               |Step size — crucial hyperparameter|
|Convergence  |`‖∇J(θ)‖ < ε`                  |When to stop                      |

-----

> **📌 Key Takeaway:** Linear algebra gives you the language, probability gives you the reasoning framework, and gradient descent gives you the learning engine. Together, they are the complete mathematical foundation of virtually every modern machine learning algorithm.

-----

*Document authored for GitHub portfolios, interview prep, and self-study. All examples use small numbers for clarity. NumPy/PyTorch snippets are production-ready.*

