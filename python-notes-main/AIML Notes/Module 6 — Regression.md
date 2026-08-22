# Module 6 — Regression
> *"Regression is the art of finding the line (or curve) that best explains how one thing changes when another thing changes."*

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

Before a machine can classify, generate, or recommend — it must learn to **predict numbers**.

Regression is the purest form of supervised learning: given input features, predict a continuous output. Every advanced ML technique you will ever learn builds on this foundation:

- Neural networks are just deeply stacked regression layers
- Gradient boosting is regression on residuals, recursively
- Logistic regression is linear regression passed through a squashing function
- Attention mechanisms are weighted regressions over token relationships

Mastering regression means mastering the **core loop of machine learning**:
```
Make prediction → Measure error → Adjust parameters → Repeat
```

It also introduces the two most important tensions in all of ML:
- **Bias vs. Variance** — are you underfitting or overfitting?
- **Fit vs. Complexity** — is your model learning signal or noise?

---

## ELI5

Imagine you're trying to guess how much a pizza costs based on its size.

You look at 100 past orders and notice: **bigger pizzas cost more**. You draw a straight line through the price-vs-size data that best represents this trend. Now, given a new pizza's size, you read off your line to predict the price.

That line is your **regression model**.

- The **slope** of the line says: "for every extra inch of diameter, the price goes up by $X"
- The **intercept** says: "a pizza of zero size costs $Y" (not physically meaningful here, but mathematically needed)
- The **residuals** are the gaps between your line and the actual prices — your errors
- **Training** the model means choosing the slope and intercept that make those gaps as small as possible

Everything in this module is an extension of this simple idea.

---

## Core Concepts

### 1. What Is a Regression Problem?

A regression problem asks: **"Given some inputs, predict a number."**

| Task | Inputs | Output (number) |
|---|---|---|
| House price prediction | sqft, bedrooms, location | Price ($) |
| Temperature forecasting | date, humidity, pressure | Temperature (°C) |
| Demand forecasting | day of week, promotions | Units sold |
| Medical dosing | weight, age, diagnosis | Drug dose (mg) |

The output is **continuous** (can take any value in a range), unlike classification where the output is a category.

---

### 2. Simple Linear Regression

One input feature, one output. The model is a straight line:

```
ŷ = w₀ + w₁x

where:
  ŷ  = predicted value
  x  = input feature
  w₀ = intercept (where the line crosses y-axis)
  w₁ = slope (how much ŷ changes per unit of x)
```

**The model has only 2 parameters: `w₀` and `w₁`.**  
Training means finding the values of these two numbers that make the line fit the data best.

---

### 3. Multiple Linear Regression

Multiple input features, one output:

```
ŷ = w₀ + w₁x₁ + w₂x₂ + ... + wₙxₙ

Now you have n+1 parameters to learn.
The "line" becomes a hyperplane in (n+1)-dimensional space.
```

**Example — predicting house price:**
```
price = w₀ + w₁×(sqft) + w₂×(bedrooms) + w₃×(distance_to_city)
```
Each `wᵢ` says: *"all else equal, how much does the price change per unit of feature i?"*

---

### 4. Residuals

A **residual** is the difference between the actual value and the predicted value:

```
residual = actual - predicted = y - ŷ
```

Residuals are your model's **honest report card**:
- Small residuals → predictions are close to reality
- Large residuals → the model is missing something
- **Patterns in residuals** → the model is systematically wrong (a solvable problem)

A well-trained model should have residuals that look like **random noise** — no patterns.

---

### 5. The Loss Function

How do we measure "how wrong" the model is overall?  
We use a **loss function** — a single number summarizing total error across all training examples.

The most common loss for regression is **Mean Squared Error (MSE)**:

```
MSE = (1/n) Σ (yᵢ - ŷᵢ)²

Squaring does two things:
  1. Penalizes large errors much more than small ones
  2. Makes all errors positive (no cancelling out)
```

**Training = minimizing the loss function** by adjusting the model's parameters.

---

## Math Intuition

### The Least Squares Idea

Imagine each data point has a rubber band connecting it to the regression line. The rubber bands pull the line toward the points. The line settles where the total **tension** (sum of squared distances) is minimized.

```
Data points:   ×    ×
                  ×     ×
             ×        ×
Line:   ─────────────────────
              ↕ ↕ ↕ ↕ ↕ ↕
              residuals (gaps)

Minimize: sum of (all gaps²)
```

This is **Ordinary Least Squares (OLS)** — the standard algorithm for linear regression.

---

### Why Squared Errors?

You might ask: why square the residuals instead of just taking absolute values?

```
Option 1: Sum of |residuals|  → Mean Absolute Error (MAE)
Option 2: Sum of residuals²   → Mean Squared Error (MSE)

MSE advantages:
  ✓ Smooth, differentiable → easy to optimize with calculus
  ✓ Has a closed-form solution (we can solve exactly, no guessing)
  ✓ Large errors get disproportionately penalized → good for safety-critical tasks

MAE advantages:
  ✓ Robust to outliers (outlier residual counts linearly, not quadratically)
  ✓ More interpretable ("off by X units on average")
  ✓ Better when outliers are real data, not noise
```

---

### Closed-Form Solution for Linear Regression

For linear regression with MSE loss, there's an **exact mathematical answer** (no iterative optimization needed):

```
w* = (XᵀX)⁻¹ Xᵀy

where:
  X  = data matrix (n rows × d columns, first column all 1s for intercept)
  y  = target vector (n values)
  w* = optimal weights

This is called the Normal Equations.
```

**Intuition:** This formula finds the point where the derivative of the loss equals zero — the bottom of the bowl. It's an exact solution, not an approximation.

**Practical limitation:** Inverting `XᵀX` is expensive for large d (O(d³) operations). For large datasets, **gradient descent** is used instead.

---

### Gradient Descent Intuition

When the dataset is too large for the Normal Equations, we optimize iteratively:

```
Imagine standing on a hilly landscape where:
  - Your position = current parameter values (w₀, w₁, ...)
  - Your altitude  = current loss (how wrong the model is)
  - Your goal      = find the lowest valley

Gradient Descent:
  1. Measure the slope of the hill at your position (gradient)
  2. Take a small step downhill
  3. Repeat until you stop descending

Update rule:
  w ← w - α × ∇L(w)

where α (alpha) is the learning rate — how big each step is.
```

---

### Polynomial Regression and Basis Expansion

What if the true relationship is curved, not straight?

```
y = w₀ + w₁x + w₂x² + w₃x³ + ...

This is still LINEAR REGRESSION — linear in the parameters w.
We just created new input features: x, x², x³, ...
This is called BASIS EXPANSION.
```

```
Original feature: x = [2, 3, 4, 5]

Degree-2 expansion (add x²):
  x  = [2, 3, 4, 5]
  x² = [4, 9, 16, 25]

Now feed both as features to a standard linear model.
The model learns a parabola in x-space,
but it's still a linear model in (x, x²)-space.
```

**Danger:** Higher degree = more flexibility = can overfit the training data perfectly while failing on new data.

---

### Bias-Variance Tradeoff

This is one of the most important ideas in all of machine learning.

**Bias** = how wrong your model is on average, even with infinite data  
**Variance** = how much your model changes when trained on different data samples

```
           UNDERFITTING                 JUST RIGHT              OVERFITTING
           (High Bias)                                          (High Variance)

  y ↑   ●  ●                   y ↑  ●  ●                y ↑  ●  ●
        ●    ●                        ●  ●                     ╰╮ ╭╯
    ──────────────── ŷ              ╱──────╲ ŷ               ╰╯  ╭╯ ŷ
        ●     ●                   ●        ●                  ●     ●
        ●                         ●                           ●
    └──────────────── x       └──────────────── x        └──────────────── x

  Misses the real pattern        Captures the pattern         Memorizes the data
  Bad on train AND test          Good on train AND test        Good on train only

Error decomposition:
  Total Error = Bias² + Variance + Irreducible Noise

The tradeoff:
  Simpler model → Higher Bias, Lower Variance
  Complex model → Lower Bias, Higher Variance
```

---

### Regularization: Fighting Overfitting

Regularization adds a **penalty for complexity** directly into the loss function:

```
Regular loss:       L(w) = MSE(w)
Regularized loss:   L(w) = MSE(w) + λ × penalty(w)

The penalty discourages large coefficients.
λ (lambda) controls the strength: bigger λ = more regularization.
```

**Why does large weight = overfitting?**  
When a model overfits, it assigns huge weights to noise features. If we penalize large weights, we force the model to only use features that are clearly useful.

---

### Ridge vs. Lasso: Two Flavors of Regularization

```
Ridge (L2):   L(w) = MSE + λ Σ wᵢ²     (penalizes squared weights)
Lasso (L1):   L(w) = MSE + λ Σ |wᵢ|    (penalizes absolute weights)

Ridge:
  → Shrinks ALL coefficients toward zero (but rarely exactly zero)
  → Good when many features are somewhat useful
  → Handles multicollinearity by spreading the load

Lasso:
  → Pushes some coefficients to EXACTLY zero (automatic feature selection!)
  → Good when only a few features truly matter
  → Creates sparse models (simpler, more interpretable)
```

**Geometric picture:**

```
Ridge constraint region:    Lasso constraint region:
        ○                           ◇
     ○     ○                     ╱   ╲
   ○    ●    ○                  ╱  ●  ╲
     ○     ○                   ╲     ╱
        ○                        ╲ ╱
                                  ◇
  Circle: solution rarely       Diamond: pointy corners mean
  hits the axis exactly.        solution often hits axis → w=0
```

The **corners** of the Lasso diamond sit on the axes, where one or more weights are exactly zero. This is why Lasso produces sparse solutions.

---

## Key Formulas and Equations

### Regression Model

$$\hat{y} = w_0 + w_1 x_1 + w_2 x_2 + \ldots + w_n x_n = \mathbf{w}^T \mathbf{x}$$

### Loss Functions

$$\text{MSE} = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2$$

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|$$

$$\text{RMSE} = \sqrt{\text{MSE}} = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2}$$

### R² Score (Coefficient of Determination)

$$R^2 = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2} = 1 - \frac{\text{SS}_\text{res}}{\text{SS}_\text{tot}}$$

> **Interpretation:** R² = 0.85 means "the model explains 85% of the variance in the target variable."

$$R^2 = 1 \Rightarrow \text{perfect predictions} \quad R^2 = 0 \Rightarrow \text{no better than predicting the mean}$$

### Normal Equation

$$\mathbf{w}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$

### Gradient Descent Update

$$\mathbf{w} \leftarrow \mathbf{w} - \alpha \cdot \nabla_\mathbf{w} L(\mathbf{w})$$

### Ridge and Lasso Objectives

$$\text{Ridge:} \quad L = \text{MSE} + \lambda \sum_{i=1}^n w_i^2$$

$$\text{Lasso:} \quad L = \text{MSE} + \lambda \sum_{i=1}^n |w_i|$$

### Bias-Variance Decomposition

$$\text{Expected Error} = \text{Bias}^2 + \text{Variance} + \sigma^2_\text{noise}$$

---

## Algorithms Breakdown

### Ordinary Least Squares (OLS) — Step by Step

```
Goal: Find w* that minimizes MSE = (1/n)‖y - Xw‖²

Step 1: Assemble the design matrix X
        - Add a column of 1s for the intercept
        - Shape: (n_samples × n_features+1)

Step 2: Compute XᵀX  and  Xᵀy
        (XᵀX is a (d+1)×(d+1) matrix)

Step 3: Solve the Normal Equations:
        w* = (XᵀX)⁻¹ Xᵀy

Step 4: Predict:  ŷ = Xw*

Step 5: Compute residuals:  e = y - ŷ

COMPLEXITY: O(nd²) to form XᵀX + O(d³) to invert
USE WHEN:   n is moderate, d is small-to-medium
```

---

### Gradient Descent for Regression

```
Goal: Same as OLS — minimize MSE — but done iteratively

Step 1: Initialize weights w randomly (or zeros)
Step 2: Repeat until convergence:
    a. Compute predictions:       ŷ = Xw
    b. Compute residuals:         e = ŷ - y
    c. Compute gradient:          ∇w = (2/n) Xᵀe
    d. Update weights:            w ← w - α × ∇w
Step 3: Return final w

Variants:
  Batch GD:    use all n samples per step (accurate, slow)
  Stochastic:  use 1 sample per step (noisy, fast)
  Mini-batch:  use m samples per step (best of both worlds)

USE WHEN: n or d is large (Normal Equations too expensive)
```

---

### Ridge Regression

```
Adds L2 penalty to OLS:

Closed form: w* = (XᵀX + λI)⁻¹ Xᵀy

Key difference from OLS:
  - Adding λI makes the matrix always invertible (even if XᵀX is singular)
  - This is why Ridge helps with multicollinearity
  - λ = 0 → Ridge = OLS
  - λ → ∞ → all weights → 0 (model predicts the mean)
```

---

### Lasso Regression

```
Adds L1 penalty to OLS:

No closed form! (|w| is not differentiable at w=0)
Use:
  - Coordinate Descent (update one weight at a time)
  - Subgradient methods
  - ADMM (Alternating Direction Method of Multipliers)

sklearn uses coordinate descent — fast and reliable.

KEY BEHAVIOR:
  - For small enough λ, Lasso sets some weights to exactly 0
  - Effectively performs feature selection automatically
  - Resulting model uses a sparse subset of features
```

---

### Multicollinearity: When Features Are Too Similar

```
PROBLEM:
  If x₁ ≈ x₂ (highly correlated), the model struggles:
  "Should I assign the credit to x₁ or x₂?"

  Mathematically: XᵀX becomes nearly singular (hard to invert)
  Result: coefficients are unstable, huge values, opposite signs

SYMPTOMS:
  - Individual p-values are high, but R² is high
  - Coefficients change drastically when you add/remove one feature
  - VIF (Variance Inflation Factor) > 10 for some features

SOLUTIONS:
  1. Remove one of the correlated features
  2. Use Ridge regression (regularization stabilizes coefficients)
  3. Use PCA first, then regress on principal components
  4. Create a combined feature (e.g., average of the two)
```

---

## Visual Mental Models

### The Regression Line as a Moving Average

```
Data:                                 Final line:
  y↑                                    y↑
  │  ●                                  │  ●
  │      ●   ●                          │      ●   ●
  │  ●       ●                          │  ●  ╱    ●
  │    ●   ●                            │    ● ╱ ●
  │  ●                                  │  ●╱
  └──────────────── x                  └──────────────── x

The line is pulled toward clusters of points.
No single point dictates the line — it's a collective average.
```

---

### Residual Diagnostics — What to Look For

```
GOOD residuals (random, no pattern):    BAD residuals (pattern = problem):
  residual↑                               residual↑
  │  ×   ×                                │         × ×
  │×    ×   ×  ×                          │      × ×
  │  × ×  × ×                             │   × ×                ← Curved
  │×    ×   ×                             │× ×
  └──────────── ŷ                        └──────────── ŷ

GOOD: points scatter randomly            BAD: pattern suggests polynomial
around zero → model is correct           term is missing

Other bad patterns:
  
  residual↑                               residual↑
  │          × ×                          │×
  │      × ×                              │  ×
  │    ×    ×                             │    ×
  │× ×    ×                               │      ×  ← One huge outlier
  └──────────── ŷ                        └──────────── ŷ

  Trumpet/funnel shape                    Outlier
  → Heteroscedasticity                   → Investigate this point
  (variance grows with ŷ)
  → Use log(y) or weighted regression
```

---

### Bias-Variance as Model Complexity Changes

```
Error
  │
  │ ╲                          Total Error
  │   ╲                    ╭───────────────
  │    ╲           ╭───────╯
  │     ╲   ╭──────╯       Training Error
  │      ╲──╯
  │       ●  ← Sweet spot
  └──────────────────────────────────────── Model Complexity →
           Low       Medium       High
        (underfit)  (just right)  (overfit)

  Bias²  dominates ←──────── ──────────→ Variance dominates
  Model too simple              Model too complex
```

---

### Regularization Effect on Coefficients

```
Without regularization (OLS):
  Feature:  sqft  beds  bath  age   noise1  noise2
  Weight:   0.8   1.2   0.3   -0.4  2.1     -1.8    ← Large noise weights!

With Ridge (λ=1):
  Weight:   0.7   1.0   0.3   -0.3  0.4     -0.3    ← Shrunk, but nonzero

With Lasso (λ=1):
  Weight:   0.7   0.9   0.2   -0.3  0.0      0.0    ← Noise features zeroed out!

Lasso tells you: "sqft, beds, bath, age matter. The rest: irrelevant."
```

---

### R² Intuition

```
Baseline model (predict mean ȳ):              Your regression model:
  y↑  ●                                         y↑  ●
  │ ●   ●                                        │ ●   ●
ȳ ├──────────── ← every prediction = ȳ          │  ╱──── ← model line
  │   ●   ●                                      │ ●   ●
  └──────────── x                               └──────────── x

SS_total = total variation in y               SS_residual = leftover variation

R² = 1 - SS_residual / SS_total
   = fraction of variation EXPLAINED by the model

R² = 0.0 → model no better than "always predict ȳ"
R² = 1.0 → model predicts perfectly
R² < 0   → model is WORSE than predicting the mean (something is wrong)
```

---

## Real-World Applications

### California Housing Dataset Case Study

This classic dataset predicts **median house values** for California census blocks.

**Features:**
- `MedInc` — Median household income
- `HouseAge` — Median house age
- `AveRooms` — Average rooms per household
- `AveBedrms` — Average bedrooms per household
- `Population` — Block population
- `AveOccup` — Average household occupancy
- `Latitude`, `Longitude` — Geographic coordinates

**Target:** `MedHouseVal` — Median house value (hundreds of thousands $)

**Key insights this dataset teaches:**
1. **Income is king** — `MedInc` has by far the highest correlation with price
2. **Geography matters** — latitude/longitude are nonlinear (need polynomial or tree models)
3. **Multicollinearity exists** — `AveRooms` and `AveBedrms` are correlated
4. **Outliers matter** — values are capped at 5.0 (censoring bias)

---

### Other Application Domains

| Domain | Problem | Key Insight |
|---|---|---|
| Finance | Stock return prediction | Residuals must be checked for autocorrelation |
| Healthcare | Patient length-of-stay | Skewed target → use log transform |
| Retail | Sales forecasting | Seasonality requires feature engineering |
| Engineering | Material strength | Physical constraints need bounded predictions |
| HR | Salary modeling | Ridge prevents overfitting on many job categories |

---

## Engineering Insights

### When to Use Which Method

```
┌────────────────────────────────────────────────────────────────┐
│                    CHOOSING YOUR REGRESSION METHOD             │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  n >> d AND features uncorrelated?                             │
│    → OLS (fast, exact, interpretable)                          │
│                                                                │
│  Many correlated features?                                     │
│    → Ridge (stable, shrinks all coefficients)                  │
│                                                                │
│  Suspect many irrelevant features?                             │
│    → Lasso (automatic feature selection)                       │
│                                                                │
│  Want both?                                                    │
│    → ElasticNet = α×Lasso + (1-α)×Ridge                        │
│                                                                │
│  Nonlinear relationship?                                       │
│    → Polynomial features + Ridge (prevent overfitting)         │
│    → Or: Decision Trees, Random Forest, XGBoost               │
│                                                                │
│  Very large dataset (n > 1M)?                                  │
│    → SGD (stochastic gradient descent)                         │
│    → sklearn.linear_model.SGDRegressor                         │
└────────────────────────────────────────────────────────────────┘
```

---

### Feature Scaling Matters (A Lot)

```python
# Without scaling:
# Feature A: income (range 0 – 200,000)
# Feature B: age    (range 0 – 100)

# After OLS fit:
# w_income ≈ 0.0003   (tiny because income is huge numerically)
# w_age    ≈ 500      (huge because age is small numerically)
# → Coefficients not comparable, gradient descent is slow

# With StandardScaler:
# w_income ≈ 2.1   (directly comparable)
# w_age    ≈ 0.8
# → Gradient descent converges faster, coefficients interpretable
```

**Rule:** Always scale features before:
- Regularized regression (Ridge, Lasso) — penalty treats all weights equally
- Gradient descent — convergence is much faster with scaled features
- Coefficient interpretation — only valid when features are on same scale

---

### Log-Transforming Skewed Targets

Many real-world targets (prices, incomes, populations) are right-skewed:

```
Raw house prices:         Log(house prices):
  │  ██                      │     ██████
  │  ████                    │   ████████
  │  ████████                │  ██████████
  │  ████████████████        │  ████████████
  └────────────────── $      └────────────────── log($)
  Right-skewed               Approximately normal

After predicting log(y), transform back:  ŷ_price = exp(ŷ_log)
This also ensures predictions are always positive.
```

---

## Production Notes

```
┌─────────────────────────────────────────────────────────────────┐
│  PRODUCTION CHECKLIST                                           │
├─────────────────────────────────────────────────────────────────┤
│ ✅ Fit scaler on TRAIN data only, apply to test                 │
│ ✅ Cross-validate λ (Ridge/Lasso alpha) with CV                 │
│ ✅ Monitor for distribution shift in features over time         │
│ ✅ Log predictions and residuals in production                  │
│ ✅ Set up alerts when residual distribution changes             │
│ ✅ Use sklearn Pipeline (scaler → model) to prevent leakage     │
│ ✅ Save the entire fitted pipeline, not just model weights      │
│ ✅ Document feature names and expected ranges                   │
│ ✅ Cap/clip predictions if domain has hard limits               │
│ ✅ Retrain on schedule or trigger-based as new data arrives     │
└─────────────────────────────────────────────────────────────────┘
```

### The Golden Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score

pipe = Pipeline([
    ('poly',   PolynomialFeatures(degree=2, include_bias=False)),
    ('scaler', StandardScaler()),
    ('ridge',  Ridge(alpha=1.0))
])

# Cross-validate on training data
cv_scores = cross_val_score(pipe, X_train, y_train,
                            scoring='r2', cv=5)
print(f"CV R²: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# Final fit and evaluate
pipe.fit(X_train, y_train)
print(f"Test R²: {pipe.score(X_test, y_test):.3f}")
```

---

## Common Mistakes

### ❌ Mistake 1: Not checking residual plots

```
Just because R² = 0.85 doesn't mean the model is correct.
If residuals show a pattern, you're systematically wrong.

Fix: ALWAYS plot residuals vs. fitted values before trusting a model.
```

---

### ❌ Mistake 2: Interpreting R² as absolute quality

```
R² = 0.3 might be excellent for predicting stock returns.
R² = 0.99 might be suspicious for noisy data (possible overfitting).

Context matters. Compare against a sensible baseline.
```

---

### ❌ Mistake 3: Forgetting to scale before Ridge/Lasso

```
Ridge penalizes: λ(w₁² + w₂² + w₃²)
If w₁ corresponds to income (scale 10,000s) and w₂ to age (scale 1-100),
the penalty hits them very differently — unfair!

Fix: StandardScaler before any regularized regression.
```

---

### ❌ Mistake 4: Using R² for comparing models across different datasets

```
R² depends on the variance of y in the dataset.
A model with R²=0.9 on dataset A is not necessarily better than
a model with R²=0.7 on dataset B — the targets have different scales.

Fix: Use RMSE for cross-dataset comparisons.
```

---

### ❌ Mistake 5: Overfitting with high-degree polynomial

```python
# ❌ This memorizes training data perfectly
PolynomialFeatures(degree=15)  # 15th degree polynomial!

# ✅ Always pair high-degree polynomial with regularization
Pipeline([
    ('poly',  PolynomialFeatures(degree=5)),
    ('scaler', StandardScaler()),
    ('ridge', Ridge(alpha=10.0))   # regularization saves you
])
```

---

### ❌ Mistake 6: Ignoring multicollinearity

```
Symptom: R² is high but individual coefficients are huge and opposite in sign.
Example:
  w_sqft = +50,000   and   w_sqft_per_room = -48,000
  These cancel out — the model is unstable.

Fix: Check VIF scores. Use Ridge or drop one of the correlated features.
```

---

## Best Practices

### Residual Diagnostic Workflow

```
After fitting any regression model, run ALL of these:

1. Residuals vs. Fitted values
   → Looking for: random scatter around zero
   → Bad sign: curved pattern (need polynomial terms)

2. Q-Q Plot of residuals
   → Looking for: points on the diagonal line (normality)
   → Bad sign: heavy tails (outliers, or wrong model)

3. Residuals vs. each input feature
   → Looking for: no pattern
   → Bad sign: U-shape means that feature needs a polynomial term

4. Scale-Location plot (√|residuals| vs fitted)
   → Looking for: horizontal band
   → Bad sign: funnel shape = heteroscedasticity

5. Influence plot (Cook's distance)
   → Looking for: no single point dominating the fit
   → Bad sign: one point with huge Cook's distance
```

---

### Choosing λ (Regularization Strength)

```python
from sklearn.linear_model import RidgeCV, LassoCV

# Ridge: automatically cross-validates over these alpha values
ridge_cv = RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0, 100.0], cv=5)
ridge_cv.fit(X_train_scaled, y_train)
print(f"Best alpha: {ridge_cv.alpha_}")

# Lasso: uses cross-validation with coordinate descent
lasso_cv = LassoCV(cv=5, random_state=42)
lasso_cv.fit(X_train_scaled, y_train)
print(f"Best alpha: {lasso_cv.alpha_}")
# Also shows which features were zeroed out:
print(f"Features used: {(lasso_cv.coef_ != 0).sum()} / {len(lasso_cv.coef_)}")
```

---

## Minimal Practical Workflow

```python
# ─── COMPLETE REGRESSION WORKFLOW ─────────────────────────────────────

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, RidgeCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ─── 1. Load Data ─────────────────────────────────────────────────────
data = fetch_california_housing(as_frame=True)
X, y = data.data, data.target
print(X.describe())

# ─── 2. Split ─────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ─── 3. Baseline: Predict the Mean ────────────────────────────────────
y_pred_baseline = np.full_like(y_test, fill_value=y_train.mean())
print(f"Baseline RMSE: {mean_squared_error(y_test, y_pred_baseline, squared=False):.4f}")
print(f"Baseline R²:   {r2_score(y_test, y_pred_baseline):.4f}")  # Should be ~0

# ─── 4. Linear Regression ─────────────────────────────────────────────
pipe_lr = Pipeline([
    ('scaler', StandardScaler()),
    ('model',  LinearRegression())
])
pipe_lr.fit(X_train, y_train)
y_pred_lr = pipe_lr.predict(X_test)

print(f"\nLinear Regression:")
print(f"  MAE:  {mean_absolute_error(y_test, y_pred_lr):.4f}")
print(f"  RMSE: {mean_squared_error(y_test, y_pred_lr, squared=False):.4f}")
print(f"  R²:   {r2_score(y_test, y_pred_lr):.4f}")

# ─── 5. Residual Analysis ─────────────────────────────────────────────
residuals = y_test - y_pred_lr

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Residuals vs Fitted
axes[0].scatter(y_pred_lr, residuals, alpha=0.3, s=5)
axes[0].axhline(0, color='red', linewidth=1)
axes[0].set_xlabel("Predicted"); axes[0].set_ylabel("Residual")
axes[0].set_title("Residuals vs Fitted")

# Residual distribution
axes[1].hist(residuals, bins=50, edgecolor='k')
axes[1].set_xlabel("Residual"); axes[1].set_title("Residual Distribution")

# Actual vs Predicted
axes[2].scatter(y_test, y_pred_lr, alpha=0.3, s=5)
axes[2].plot([y_test.min(), y_test.max()],
             [y_test.min(), y_test.max()], 'r--')
axes[2].set_xlabel("Actual"); axes[2].set_ylabel("Predicted")
axes[2].set_title("Actual vs Predicted")

plt.tight_layout(); plt.show()

# ─── 6. Ridge with Cross-Validated Alpha ──────────────────────────────
pipe_ridge = Pipeline([
    ('scaler', StandardScaler()),
    ('model',  RidgeCV(alphas=np.logspace(-3, 3, 50), cv=5))
])
pipe_ridge.fit(X_train, y_train)
y_pred_ridge = pipe_ridge.predict(X_test)
best_alpha = pipe_ridge.named_steps['model'].alpha_

print(f"\nRidge (best α={best_alpha:.4f}):")
print(f"  RMSE: {mean_squared_error(y_test, y_pred_ridge, squared=False):.4f}")
print(f"  R²:   {r2_score(y_test, y_pred_ridge):.4f}")

# ─── 7. Coefficient Analysis ──────────────────────────────────────────
scaler = StandardScaler().fit(X_train)
feature_names = X.columns.tolist()
lr_coefs = pipe_lr.named_steps['model'].coef_
ridge_coefs = pipe_ridge.named_steps['model'].coef_

coef_df = pd.DataFrame({
    'Feature':    feature_names,
    'Linear_Reg': lr_coefs,
    'Ridge':      ridge_coefs
}).sort_values('Linear_Reg', key=abs, ascending=False)
print("\nCoefficients:\n", coef_df.to_string(index=False))

# ─── 8. Compare All Methods ───────────────────────────────────────────
from sklearn.linear_model import Lasso

results = {}
for name, pipe in [
    ('OLS',   Pipeline([('s', StandardScaler()), ('m', LinearRegression())])),
    ('Ridge', Pipeline([('s', StandardScaler()), ('m', Ridge(alpha=best_alpha))])),
    ('Lasso', Pipeline([('s', StandardScaler()), ('m', Lasso(alpha=0.01))])),
]:
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    results[name] = {
        'MAE':  round(mean_absolute_error(y_test, y_pred), 4),
        'RMSE': round(mean_squared_error(y_test, y_pred, squared=False), 4),
        'R²':   round(r2_score(y_test, y_pred), 4)
    }

print("\n── Model Comparison ──")
print(pd.DataFrame(results).T.to_string())
```

---

## Python Ecosystem

| Library | Use Case | Key Classes / Functions |
|---|---|---|
| `sklearn.linear_model.LinearRegression` | OLS regression | `.fit()`, `.coef_`, `.intercept_` |
| `sklearn.linear_model.Ridge` | L2 regularized | `alpha` parameter |
| `sklearn.linear_model.RidgeCV` | Ridge with built-in CV | `.alpha_` (best found) |
| `sklearn.linear_model.Lasso` | L1, feature selection | `.coef_` (sparse) |
| `sklearn.linear_model.LassoCV` | Lasso with built-in CV | |
| `sklearn.linear_model.ElasticNet` | L1 + L2 combined | `l1_ratio` parameter |
| `sklearn.linear_model.SGDRegressor` | Gradient descent, large data | `loss='squared_error'` |
| `sklearn.preprocessing.PolynomialFeatures` | Basis expansion | `degree`, `include_bias` |
| `sklearn.preprocessing.StandardScaler` | Feature standardization | `.fit_transform()` |
| `sklearn.metrics` | Evaluation | `mean_absolute_error`, `mean_squared_error`, `r2_score` |
| `sklearn.pipeline.Pipeline` | Reproducible pipelines | chained transforms |
| `statsmodels.formula.api.ols` | Statistical inference | p-values, confidence intervals, VIF |
| `yellowbrick.regressor` | Residual visualizations | `ResidualsPlot`, `PredictionError` |

---

## Interview Questions

**Q1: What is the difference between MAE, MSE, and RMSE? When would you use each?**

> **MAE** averages absolute errors — robust to outliers, directly interpretable in the same units as the target. Use when outliers are legitimate data and you care about average case performance.
> **MSE** squares errors — heavily penalizes large mistakes. Use when large errors are especially bad (e.g., safety-critical prediction).
> **RMSE** is `√MSE` — same unit scale as the target, still penalizes large errors. Most commonly reported because it's interpretable *and* sensitive to large errors.

---

**Q2: What does R² actually mean? Can it be negative?**

> R² measures the fraction of variance in the target explained by the model. R² = 0.8 means 80% of the variability in `y` is captured by your features. R² = 0 means the model is no better than predicting the training mean. Yes, R² can be negative — this happens when your model performs worse than the trivial mean baseline, often because you evaluated on test data using a poorly fitted model, or if you forgot to fit an intercept.

---

**Q3: Explain the bias-variance tradeoff in plain language.**

> Bias is how systematically wrong your model is — a simple model that can't capture the true pattern has high bias. Variance is how much the model would change if you trained it on a different sample — a complex model that memorizes training data has high variance. Total error is the sum of both. Increasing model complexity reduces bias but increases variance; the sweet spot minimizes total error on unseen data.

---

**Q4: Why does Ridge regression help with multicollinearity?**

> When two features are highly correlated, the Normal Equations system becomes nearly singular — tiny changes in the data lead to wildly different coefficient values. Ridge adds `λI` to the `XᵀX` matrix before inverting it. Even if `XᵀX` is singular, `XᵀX + λI` is always invertible. The regularization stabilizes the coefficients by spreading the "credit" across correlated features instead of assigning extreme values to compensate for each other.

---

**Q5: What's the difference between Ridge and Lasso? Why does Lasso produce sparse solutions?**

> Both penalize large coefficients, but Ridge uses the squared penalty (L2) and Lasso uses the absolute value penalty (L1). Geometrically, Ridge's constraint region is a smooth sphere — the optimal solution rarely lands exactly on an axis. Lasso's constraint region is a diamond with corners sitting on the axes. The loss function's elliptical contours often touch the diamond at a corner, where one or more weights are exactly zero. This is why Lasso performs automatic feature selection.

---

**Q6: How would you detect and handle overfitting in a regression model?**

> Symptoms: training RMSE is much lower than test RMSE; residual plots show patterns on training data but not test data; very large coefficient values. Solutions: collect more data; reduce model complexity (use simpler features or lower polynomial degree); add regularization (Ridge or Lasso); use cross-validation to tune hyperparameters.

---

**Q7: What assumptions does linear regression make? How do you check them?**

> The main assumptions are: (1) **Linearity** — the mean of `y` is a linear function of `x`. Check with residuals-vs-fitted plot. (2) **Independence** — residuals are uncorrelated. Check with Durbin-Watson test for time series. (3) **Homoscedasticity** — residual variance is constant. Check scale-location plot. (4) **Normality** of residuals. Check Q-Q plot. (5) **No perfect multicollinearity**. Check VIF scores.

---

## How to Explain in an Interview

### "Explain linear regression in 60 seconds"

> *"Linear regression models the relationship between input features and a continuous target as a weighted sum: each feature gets a coefficient, and you add them up to get a prediction. Training means finding the coefficients that minimize the Mean Squared Error — the average squared gap between predictions and actual values. There's a clean closed-form solution: the Normal Equations. The result is a hyperplane in feature space that best fits the data in the least-squares sense."*

---

### "How does regularization prevent overfitting?"

> *"Without regularization, the model is free to assign any weight to any feature — including fitting random noise with large coefficients. Regularization adds a penalty term to the loss for large weights. Ridge penalizes squared weights, Lasso penalizes absolute weights. The model now faces a tradeoff: reduce the prediction error versus reduce the weight magnitudes. This pressure toward small weights prevents the model from over-committing to noisy features. The hyperparameter lambda controls how hard this pressure is."*

---

### "Walk me through how you'd build a regression model in production"

> *"First, exploratory analysis: understand the target distribution, feature correlations, and outliers. Then split into train/test. Build a sklearn Pipeline: scaler, optional polynomial features, then model. Start with OLS as baseline. If features are correlated, switch to Ridge; if feature selection is needed, use Lasso. Tune lambda with cross-validation. Evaluate with RMSE and R², check residual plots for patterns. If residuals show structure — heteroscedasticity, nonlinearity — address it before deploying. Finally, monitor prediction distributions in production and retrain on schedule."*

---

## Summary Cheatsheet

```
╔════════════════════════════════════════════════════════════════════════╗
║                  MODULE 6 — REGRESSION CHEATSHEET                    ║
╠════════════════════════════════════════════════════════════════════════╣
║  MODEL TYPES                                                          ║
║  Simple Linear:  ŷ = w₀ + w₁x                                        ║
║  Multiple:       ŷ = w₀ + w₁x₁ + ... + wₙxₙ = wᵀx                  ║
║  Polynomial:     add x², x³, ... as new features                     ║
║  Ridge:          MSE + λΣwᵢ²    → shrinks all, none exactly 0        ║
║  Lasso:          MSE + λΣ|wᵢ|   → sets some to exactly 0             ║
║  ElasticNet:     αLasso + (1-α)Ridge                                  ║
╠════════════════════════════════════════════════════════════════════════╣
║  METRICS                                                              ║
║  MAE  = (1/n)Σ|y - ŷ|           ← robust, same units as y           ║
║  MSE  = (1/n)Σ(y - ŷ)²          ← penalizes large errors            ║
║  RMSE = √MSE                    ← most commonly reported              ║
║  R²   = 1 - SS_res/SS_tot       ← fraction of variance explained     ║
║         [0,1] for sensible models; can be negative                   ║
╠════════════════════════════════════════════════════════════════════════╣
║  BIAS-VARIANCE                                                        ║
║  Total Error = Bias² + Variance + Noise                               ║
║  Simple model → High Bias (underfitting)                              ║
║  Complex model → High Variance (overfitting)                          ║
║  Fix underfitting: more features, polynomial, complex model           ║
║  Fix overfitting: regularize, get more data, reduce complexity        ║
╠════════════════════════════════════════════════════════════════════════╣
║  RESIDUAL DIAGNOSTICS                                                 ║
║  Residuals vs. Fitted  → no pattern = good                           ║
║  Q-Q Plot              → straight line = normality                   ║
║  Scale-Location        → flat band = equal variance                  ║
║  Cook's Distance       → no dominant outliers                        ║
╠════════════════════════════════════════════════════════════════════════╣
║  PRODUCTION RULES                                                     ║
║  ① Always StandardScaler before regularized regression               ║
║  ② Fit transforms on TRAIN only                                       ║
║  ③ Cross-validate λ (use RidgeCV / LassoCV)                          ║
║  ④ Use sklearn Pipeline — prevents leakage                            ║
║  ⑤ Plot residuals before trusting any model                          ║
║  ⑥ Log-transform skewed targets                                       ║
║  ⑦ Check VIF > 10 for multicollinearity                              ║
╠════════════════════════════════════════════════════════════════════════╣
║  QUICK DECISION GUIDE                                                 ║
║  Small, clean dataset        → OLS                                   ║
║  Correlated features         → Ridge                                  ║
║  Need feature selection      → Lasso                                  ║
║  Nonlinear relationships     → Polynomial + Ridge                     ║
║  Very large dataset          → SGDRegressor                           ║
║  Need p-values / inference   → statsmodels OLS                       ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

> **Next Module:** Classification — Logistic Regression, Decision Boundaries, and Beyond.
