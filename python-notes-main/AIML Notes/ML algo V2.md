# 🎓 Classical Machine Learning: A Complete Foundational Guide

### Your Senior AI-ML Mentor's Master Reference

> **How to use this guide:** Read each section in order. Every concept builds on the previous one. The code blocks are fully self-contained — you can run each one independently.

---

# 📋 TABLE OF CONTENTS

1. [The ML Workflow](#ml-workflow)
2. [Supervised Learning](#supervised-learning)
3. [Unsupervised Learning](#unsupervised-learning)
4. [Model Evaluation](#model-evaluation)
5. [Core Theory: Bias-Variance Trade-off](#bias-variance)

---

<a name="ml-workflow"></a>
# 🔷 PART 1: The ML Workflow

---

## 1.1 Train / Validation / Test Splits

### 🟡 Phase 1: The Intuition

Imagine you're a **student preparing for a final exam**.

- You study from your **textbook** → this is your **Training Set** (the data your model *learns* from)
- You take **practice tests** to tune your studying strategy → this is your **Validation Set** (used to tune and improve the model *while building it*)
- You sit the **actual final exam** → this is your **Test Set** (used *only once*, at the very end, to measure true performance)

**Why not just use all data for training?**
If you only ever studied and never tested yourself, you'd memorize the textbook but fail on new questions. In ML, this is called **overfitting** — the model memorizes instead of learning generalizable patterns.

> **Key Terms:**
> - **Split:** To divide your dataset into separate portions
> - **Training Set:** The portion the model sees and learns patterns from
> - **Validation Set:** A held-out portion used during development to tune the model
> - **Test Set:** A completely untouched portion used only for final evaluation
> - **Data Leakage:** When information from your test set accidentally influences training — like peeking at the exam answers

---

### 🔵 Phase 2: The Technical 'Why' & Logic

Scikit-learn's `train_test_split` shuffles and splits data randomly. The typical ratios are:

| Split | Typical Size | Purpose |
|---|---|---|
| Train | 60–80% | Model learns parameters |
| Validation | 10–20% | Hyperparameter tuning |
| Test | 10–20% | Final unbiased evaluation |

**Why shuffle?** Real-world datasets are often ordered (e.g., all class A samples first). Without shuffling, your test set might contain only one class — making evaluation meaningless.

**`random_state`** is a seed for the random number generator. Setting it ensures your split is reproducible — you get the same split every time you run the code.

---

### 🟢 Phase 3: Hands-on Code

```python
# ============================================================
# TRAIN / VALIDATION / TEST SPLIT
# Dataset: Iris (150 samples, 3 flower species)
# ============================================================

from sklearn.datasets import load_iris          # Built-in toy dataset
from sklearn.model_selection import train_test_split  # The splitting utility
import pandas as pd

# --- Load the dataset ---
iris = load_iris()                              # Returns a Bunch object (like a dict)
X = iris.data                                   # Features: sepal/petal length & width (shape: 150 x 4)
y = iris.target                                 # Labels: 0=setosa, 1=versicolor, 2=virginica (shape: 150,)

print(f"Total samples: {len(X)}")              # Should print 150

# --- Step 1: Split off the TEST set first (20% of total data) ---
# We do this FIRST and then set it aside — never touch it until the very end
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y,
    test_size=0.20,          # 20% goes to test set → 30 samples
    random_state=42,         # Seed for reproducibility — same split every run
    stratify=y               # Ensures each split has proportional class representation
                             # Without this, one split might accidentally have no class 2 samples
)

# --- Step 2: Split the remaining 80% into Train (75% of 80% = 60%) and Validation (25% of 80% = 20%) ---
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp,
    test_size=0.25,          # 25% of the 80% temp = 20% of original data → 30 samples for validation
    random_state=42,
    stratify=y_temp          # Again stratify to preserve class balance
)

# --- Confirm the sizes ---
print(f"Training set:   {X_train.shape}")      # (90, 4) — 90 samples, 4 features
print(f"Validation set: {X_val.shape}")        # (30, 4)
print(f"Test set:       {X_test.shape}")       # (30, 4)

# --- Why stratify? Let's verify class distribution is preserved ---
import numpy as np
print("\nClass distribution in Training set:", np.bincount(y_train))
print("Class distribution in Val set:     ", np.bincount(y_val))
print("Class distribution in Test set:    ", np.bincount(y_test))
# You should see roughly equal numbers of each class in all splits
```

---

## 1.2 Feature Scaling

### 🟡 Phase 1: The Intuition

Imagine you're comparing houses using two features:
- **Number of bedrooms:** ranges from 1 to 10
- **Price:** ranges from $50,000 to $5,000,000

If a machine learning algorithm looks at these raw numbers, it will think **price is astronomically more important** than bedrooms, simply because it's a bigger number. But that's just a unit problem — like comparing kilometers and millimeters.

**Feature Scaling** standardizes all features to the same numerical range so every feature gets a fair say.

> **Key Terms:**
> - **Feature:** A column in your dataset (an input variable)
> - **StandardScaler (Z-score Normalization):** Transforms data so it has **mean = 0** and **standard deviation = 1**. Formula: `z = (x - mean) / std`
> - **MinMaxScaler:** Squeezes all values into a range of [0, 1]. Formula: `x_scaled = (x - min) / (max - min)`
> - **Mean:** The average value
> - **Standard Deviation:** How spread out the values are from the mean

---

### 🔵 Phase 2: The Technical 'Why' & Logic

**When is scaling MANDATORY?**

| Algorithm | Needs Scaling? | Why |
|---|---|---|
| Linear/Logistic Regression | ✅ Yes | Coefficients are affected by scale |
| K-Nearest Neighbors | ✅ Yes | Uses distance — scale dominates |
| SVM | ✅ Yes | Maximizes margin — scale matters |
| Neural Networks | ✅ Yes | Gradient descent converges faster |
| Decision Trees / Random Forest | ❌ No | Uses rule splits, not distances |
| Gradient Boosting | ❌ No | Same reason as trees |

**Critical Rule — Fit on Train, Transform on All:**
You must **only fit** (calculate mean/std) **on the training set**. Then apply those same parameters to validation and test sets. If you fit on the whole dataset, you leak test information into training — the model "knows" something about the test data before ever seeing it.

---

### 🟢 Phase 3: Hands-on Code

```python
# ============================================================
# FEATURE SCALING: StandardScaler and MinMaxScaler
# ============================================================

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import numpy as np

# --- Load and split data ---
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---- STANDARD SCALER (Z-score) ----
# Best for: Linear models, Logistic Regression, SVM, Neural Networks
# Result: Each feature will have mean ≈ 0 and std ≈ 1

scaler = StandardScaler()     # Create the scaler object (no computation yet)

# FIT: Calculate mean and std from TRAINING DATA ONLY
# Think of this as the scaler "studying" the training data's statistics
scaler.fit(X_train)

# TRANSFORM: Apply those learned statistics to scale the data
# This converts raw values to z-scores: z = (x - mean) / std
X_train_scaled = scaler.transform(X_train)   # Scale training features
X_test_scaled  = scaler.transform(X_test)    # Use SAME scaler (from training) on test!
                                              # DO NOT call scaler.fit(X_test) — that would be data leakage

# Shortcut: fit_transform() does fit() + transform() in one step
# ONLY use fit_transform() on training data!
X_train_scaled = scaler.fit_transform(X_train)   # Fit AND transform in one step (training only)
X_test_scaled  = scaler.transform(X_test)         # Only transform (no refitting) on test

# --- Verify scaling worked ---
print("BEFORE scaling:")
print(f"  Feature 0 mean: {X_train[:, 0].mean():.2f}, std: {X_train[:, 0].std():.2f}")

print("\nAFTER StandardScaler:")
print(f"  Feature 0 mean: {X_train_scaled[:, 0].mean():.2f}, std: {X_train_scaled[:, 0].std():.2f}")
# Mean ≈ 0.00, Std ≈ 1.00 ✓

# ---- MIN-MAX SCALER ----
# Best for: When you need values strictly between 0 and 1 (e.g., image pixel values, neural net inputs)
# Sensitive to outliers — one extreme value compresses everything else

mm_scaler = MinMaxScaler()                         # Default range is [0, 1]
X_train_mm = mm_scaler.fit_transform(X_train)      # Fit on train, transform train
X_test_mm  = mm_scaler.transform(X_test)           # Only transform test

print("\nAFTER MinMaxScaler:")
print(f"  Feature 0 min: {X_train_mm[:, 0].min():.2f}, max: {X_train_mm[:, 0].max():.2f}")
# Min ≈ 0.00, Max ≈ 1.00 ✓
```

---

## 1.3 One-Hot Encoding

### 🟡 Phase 1: The Intuition

Most ML algorithms speak **numbers**, not **words**. So what do we do when a feature is a category like `Color = ["Red", "Blue", "Green"]`?

**Bad approach:** Assign numbers: Red=1, Blue=2, Green=3. But this implies Red < Blue < Green — an **ordering that doesn't exist**. The algorithm will incorrectly think Blue is "between" Red and Green.

**Good approach — One-Hot Encoding:** Create a new binary column (0 or 1) for each category.

| Color | is_Red | is_Blue | is_Green |
|---|---|---|---|
| Red | 1 | 0 | 0 |
| Blue | 0 | 1 | 0 |
| Green | 0 | 0 | 1 |

Now there's no false ordering. Each category is independent.

> **Key Terms:**
> - **Categorical Feature:** A feature with discrete labels/groups (e.g., Gender, City, Color)
> - **Ordinal Feature:** A categorical feature WITH a natural order (e.g., Low < Medium < High) — use Label Encoding for these
> - **Dummy Variable Trap:** Having redundant columns. If `is_Red=0` and `is_Blue=0`, we *know* it's Green. So you can drop one column (`drop='first'`).

---

### 🔵 Phase 2: The Technical 'Why' & Logic

One-Hot Encoding is preprocessing, not a model. It transforms your raw data before it ever touches an algorithm.

**When to use it:**
- **Nominal categories** (no order): Cities, Colors, Product Types → One-Hot Encode
- **Ordinal categories** (has order): Rating (Low/Med/High) → Label/Ordinal Encode
- **High cardinality** (many unique values like ZIP codes with 10,000 unique values): One-Hot creates too many columns — use Target Encoding or Embedding instead

---

### 🟢 Phase 3: Hands-on Code

```python
# ============================================================
# ONE-HOT ENCODING
# We'll create a small synthetic DataFrame to show this clearly
# ============================================================

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# --- Create a small sample dataset with categorical features ---
data = {
    'City':   ['New York', 'London', 'Paris', 'London', 'New York'],  # Nominal — no order
    'Rating': ['High', 'Low', 'Medium', 'High', 'Low'],               # Ordinal — has order
    'Age':    [25, 30, 22, 35, 28]                                     # Numerical — no encoding needed
}
df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)

# ---- METHOD 1: pandas get_dummies (quick, great for exploration) ----
# Creates binary columns for each unique category value
df_encoded = pd.get_dummies(
    df,
    columns=['City'],       # Which columns to encode (we'll leave Rating for ordinal example)
    drop_first=True         # Drop first category (New York) to avoid dummy variable trap
                            # This prevents perfect multicollinearity in linear models
)
print("\nAfter get_dummies (drop_first=True):")
print(df_encoded)
# You'll see City_London and City_Paris — New York is implied when both are 0

# ---- METHOD 2: sklearn OneHotEncoder (preferred inside Pipelines) ----
encoder = OneHotEncoder(
    drop='first',           # Equivalent to drop_first=True in get_dummies
    sparse_output=False     # Return a regular numpy array instead of sparse matrix
)

city_column = df[['City']]                         # Must pass a 2D array (DataFrame, not Series)
encoded_array = encoder.fit_transform(city_column) # Fit and transform in one step

# See what category names were created
print("\nEncoded feature names:", encoder.get_feature_names_out(['City']))
print("Encoded array:\n", encoded_array)
```

---

## 1.4 Pipelines

### 🟡 Phase 1: The Intuition

Imagine assembling a car on a **factory assembly line**:
1. First station: weld the frame
2. Second station: install the engine
3. Third station: paint the body

Each step happens in order, and you can't skip or swap them. An ML **Pipeline** works the same way — it chains your preprocessing steps and your model into a single, unified object.

**Why bother?**
Without a pipeline, you have to manually apply each transformation step every time you use the model. This is error-prone — you might forget to scale the test data, or apply the wrong scaler. A pipeline automates this.

> **Key Term:**
> - **Pipeline:** A sequential chain of transformers and a final estimator (model), executed in order

---

### 🔵 Phase 2: The Technical 'Why' & Logic

Pipelines solve two critical real-world problems:

**1. Preventing Data Leakage:** When you call `pipeline.fit(X_train, y_train)`, the scaler inside the pipeline only fits on training data. When you call `pipeline.predict(X_test)`, the pipeline automatically scales X_test using the *training statistics* — correctly, every time.

**2. Deployment Readiness:** In production, you receive a single new data point. With a pipeline, you call `.predict(new_sample)` and all preprocessing happens automatically. You'd never have to remember to scale manually.

---

### 🟢 Phase 3: Hands-on Code

```python
# ============================================================
# SCIKIT-LEARN PIPELINES
# Combines: Scaling → Model in one clean object
# Dataset: Iris
# ============================================================

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression   # We'll cover this model in detail later
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- Prepare data ---
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Build the Pipeline ---
# A Pipeline is a list of (name, object) tuples
# 'name' can be anything you choose — it's used for referencing steps later
# Every step except the last must be a Transformer (has .fit() and .transform())
# The last step must be an Estimator (has .fit() and .predict())

pipeline = Pipeline(steps=[
    ('scaler', StandardScaler()),             # Step 1: Scale features (Transformer)
    ('model', LogisticRegression(max_iter=200))  # Step 2: Train model (Estimator)
    # max_iter: number of optimization iterations — 200 ensures it converges for Iris
])

# --- Train the entire pipeline in one call ---
# Under the hood:
#   1. scaler.fit_transform(X_train) is called
#   2. model.fit(X_train_scaled, y_train) is called
pipeline.fit(X_train, y_train)

# --- Predict using the pipeline ---
# Under the hood:
#   1. scaler.transform(X_test) is called using TRAINING statistics (no leakage!)
#   2. model.predict(X_test_scaled) is called
y_pred = pipeline.predict(X_test)

# --- Evaluate ---
print(f"Pipeline Accuracy: {accuracy_score(y_test, y_pred):.4f}")   # Should be ~0.97

# --- Predict on a SINGLE new flower sample ---
import numpy as np
new_flower = np.array([[5.1, 3.5, 1.4, 0.2]])  # One new sample (must be 2D)
prediction = pipeline.predict(new_flower)        # Scaling + prediction handled automatically!
print(f"\nPrediction for new flower: {iris.target_names[prediction[0]]}")  # e.g., 'setosa'

# --- Inspect pipeline steps ---
print("\nPipeline steps:")
for name, step in pipeline.named_steps.items():
    print(f"  {name}: {step}")
```

---
---

<a name="supervised-learning"></a>
# 🔷 PART 2: Supervised Learning

> **What is Supervised Learning?** You train on **labeled data** — each sample has a known correct answer (label). The model learns to map inputs → outputs. Like a student learning from a textbook that has an answer key.

---

## 2.1 Linear Regression & Gradient Descent

### 🟡 Phase 1: The Intuition

You want to predict a **house price** based on its size (sq ft). You plot all your data points on a graph and draw the **best-fit straight line** through them. That line is Linear Regression.

The line has the formula:
> **Price = (Weight × Size) + Bias**

Or more formally: **ŷ = w₁x₁ + w₂x₂ + ... + b**

- **ŷ (y-hat):** The *predicted* value
- **w (weight/coefficient):** How much each feature influences the prediction. A weight of 200 on "size" means: for every 1 sq ft increase, price increases by $200.
- **b (bias/intercept):** The baseline value when all features are zero
- **Residual:** The error — the vertical gap between the actual point and the predicted line

**Gradient Descent — The learning algorithm:**
Imagine you're blindfolded on a hilly landscape and must find the lowest valley (minimum error). You feel the slope under your feet and take a small step downhill. You repeat this until you're in the valley. That's Gradient Descent — it iteratively adjusts the weights to minimize error.

> **Key Terms:**
> - **Loss Function (MSE):** A measure of how wrong the predictions are. Mean Squared Error = average of (actual - predicted)²
> - **Learning Rate:** The size of each step in Gradient Descent. Too large → overshoot the valley. Too small → takes forever.
> - **Epoch/Iteration:** One complete pass of Gradient Descent

---

### 🔵 Phase 2: The Technical 'Why' & Logic

**How it works under the hood:**

1. Start with random weights (w, b)
2. Make predictions: ŷ = Xw + b
3. Calculate the Loss: MSE = (1/n) × Σ(yᵢ - ŷᵢ)²
4. Calculate the **gradient** (slope of the loss curve with respect to each weight)
5. Update weights: **w = w - learning_rate × gradient**
6. Repeat steps 2–5 until the loss stops decreasing

**Bias-Variance for Linear Regression:**
- Linear Regression is a **high-bias** model — it assumes the relationship is a straight line. If the true relationship is curved, it will underfit.
- It has **low variance** — the line doesn't change much with different training samples.
- **Fix for underfitting:** Add polynomial features (e.g., x², x³) to capture curves → Polynomial Regression.

**Why Scaling is Mandatory Here:**
The gradient descent update uses the same learning rate for all weights. If feature A has range [0, 1] and feature B has range [0, 1,000,000], the gradients are on completely different scales. The optimizer will zigzag and converge extremely slowly or not at all.

---

### 🟢 Phase 3: Hands-on Code

```python
# ============================================================
# LINEAR REGRESSION + GRADIENT DESCENT VISUALIZATION
# Dataset: California Housing (predict house prices)
# ============================================================

from sklearn.datasets import fetch_california_housing  # ~20,000 housing samples
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
import numpy as np
import matplotlib.pyplot as plt

# --- Load dataset ---
housing = fetch_california_housing()
X, y
