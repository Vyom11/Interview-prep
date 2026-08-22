# 🤖 ML Fundamentals: A Foundational Guide to Classical Machine Learning

> **This document serves as a foundational guide for learners understanding Machine Learning.**
> Designed for beginners with an EDA background — every concept is explained from intuition to code.

-----

## 📋 Table of Contents

1. [🔁 ML Workflow](#-ml-workflow)
- [Train / Test / Validation Splits](#1a-traintestvaliodation-splits)
- [Feature Scaling](#1b-feature-scaling)
- [One-Hot Encoding](#1c-one-hot-encoding)
- [Pipelines](#1d-pipelines)
1. [📈 Supervised Learning](#-supervised-learning)
- [Linear Regression & Gradient Descent](#2a-linear-regression--gradient-descent)
- [Logistic Regression](#2b-logistic-regression)
- [Decision Trees & Random Forest](#2c-decision-trees--random-forest)
- [Gradient Boosting](#2d-gradient-boosting)
1. [🔍 Unsupervised Learning](#-unsupervised-learning)
- [K-Means Clustering](#3a-k-means-clustering)
- [PCA (Principal Component Analysis)](#3b-pca-principal-component-analysis)
1. [📊 Model Evaluation](#-model-evaluation)
- [Accuracy, Precision, Recall, F1](#4a-accuracy-precision-recall-f1)
- [ROC-AUC & Confusion Matrix](#4b-roc-auc--confusion-matrix)
- [K-Fold Cross-Validation](#4c-k-fold-cross-validation)
1. [⚖️ Core Theory: Bias-Variance Trade-off](#️-core-theory-bias-variance-trade-off)

-----

## 🔁 ML Workflow

-----

### 1A. Train/Test/Validation Splits

#### 🧠 Phase 1: The Intuition

Imagine you are a student preparing for a final exam.

- You study from your **textbook** — this is your **training set**. The model learns patterns from this data.
- Partway through studying, you take a **practice quiz** to check how you’re doing and adjust your study strategy — this is your **validation set**. You use it to tune your learning approach.
- On exam day, you face **completely unseen questions** — this is your **test set**. This is the true measure of how well you’ve learned.

**Why do we split?** If you only practiced on the exact questions in the exam, you’d score 100% — but you haven’t actually *learned* anything. A model that only memorises training data is similarly useless in the real world. This phenomenon is called **overfitting** (explained in depth later).

**Key Terms:**

- **Split**: Dividing your dataset into separate, non-overlapping portions.
- **Training Set**: The data the model sees and learns from (~60–80% of data).
- **Validation Set**: Used during development to tune model settings (called **hyperparameters**) (~10–20%).
- **Test Set**: Held back entirely until the very end to give an honest performance estimate (~10–20%).
- **Data Leakage**: The critical mistake of accidentally letting test/validation data influence training. Like a student seeing exam answers before the test — results are inflated and meaningless.

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

Statistically, we need to estimate how our model will perform on **new, unseen data** (called the **generalisation error**). If we evaluate on the training data, we get an optimistic, misleading estimate.

- **Validation set** allows us to tune **hyperparameters** (e.g., “how deep should my decision tree be?”) without contaminating the test set.
- **Test set** gives a final unbiased estimate. It should be touched exactly **once**.
- A common mistake is using the test set iteratively — each peek makes it less trustworthy.
- **Stratified splitting** ensures that the class balance (e.g., 70% Class A, 30% Class B) is preserved in each split. This is critical for imbalanced datasets.

**Bias-Variance Note:** Using too little training data can increase **bias** (underfitting). Using the entire dataset for training and nothing for validation removes our ability to detect **variance** (overfitting).

**Preprocessing Note:** Fit all scalers and encoders *only on training data*. Then use those fitted objects to transform validation and test data. If you fit on the full dataset, you introduce **data leakage**.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: Train / Test / Validation Splits
# Dataset: Iris (Classic multi-class classification dataset)
# ============================================================

# --- Import Libraries ---
from sklearn.datasets import load_iris          # Built-in dataset: 150 flower samples, 3 species
from sklearn.model_selection import train_test_split  # Function to split arrays into subsets
import pandas as pd                             # For readable display of shapes

# --- Load the Dataset ---
iris = load_iris()           # Load the full Iris dataset object
X = iris.data                # X = Features (sepal length, sepal width, petal length, petal width)
y = iris.target              # y = Labels (0=Setosa, 1=Versicolor, 2=Virginica) — what we want to predict

print(f"Full dataset size: {X.shape}")  # Shape = (rows, columns) → (150, 4)

# --- Step 1: Split off the Test Set (20% of total data) ---
# random_state=42 seeds the random number generator for reproducibility
# stratify=y ensures class proportions are preserved in both halves
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y,
    test_size=0.20,       # Reserve 20% as the final test set
    random_state=42,      # Reproducibility: same split every run
    stratify=y            # Keep class balance: proportional representation of each species
)

# --- Step 2: Split the remaining 80% into Train (75%) and Validation (25%) ---
# 0.25 of the remaining 80% = 20% of total → gives us 60/20/20 split overall
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp,
    test_size=0.25,       # 25% of remaining = 20% of total data
    random_state=42,
    stratify=y_temp       # Preserve class balance in training and validation sets
)

# --- Verify the Splits ---
print(f"\nTraining set size:   {X_train.shape[0]} samples ({X_train.shape[0]/len(X)*100:.0f}%)")
print(f"Validation set size: {X_val.shape[0]} samples ({X_val.shape[0]/len(X)*100:.0f}%)")
print(f"Test set size:       {X_test.shape[0]} samples ({X_test.shape[0]/len(X)*100:.0f}%)")

# Expected output:
# Training set size:   90 samples (60%)
# Validation set size: 30 samples (20%)
# Test set size:       30 samples (20%)
```

-----

### 1B. Feature Scaling

#### 🧠 Phase 1: The Intuition

Imagine comparing two athletes: one’s height is measured in centimetres (e.g., 180 cm) and another’s weight in kilograms (e.g., 75 kg). If a machine learning algorithm treats these numbers directly, it would think height is *more than twice as important* simply because its numbers are larger. This is unfair and mathematically misleading.

**Feature Scaling** brings all features onto a common numerical scale so that no single feature dominates due to its unit of measurement.

**Two common methods:**

1. **Standardisation (Z-score Scaling):** Transforms data to have a **mean of 0** and a **standard deviation of 1**.
- Formula: `z = (x - mean) / std`
- *Analogy:* Converting exam scores to “how many standard deviations above or below average you scored.” A score of 0 means exactly average.
1. **Normalisation (Min-Max Scaling):** Squeezes all values into a fixed range, usually **[0, 1]**.
- Formula: `x_norm = (x - min) / (max - min)`
- *Analogy:* Rescaling all values on a 0–100% spectrum. The lowest value becomes 0%, the highest becomes 100%.

**Key Terms:**

- **Mean**: The average value of a feature.
- **Standard Deviation (std)**: How spread out values are from the mean.
- **Feature**: A single column/variable in your dataset (e.g., “age”, “salary”).

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

**When is scaling MANDATORY?**

|Algorithm                     |Needs Scaling?|Why?                                                   |
|------------------------------|--------------|-------------------------------------------------------|
|Linear/Logistic Regression    |✅ Yes         |Gradient descent converges faster with uniform scales  |
|K-Nearest Neighbours (KNN)    |✅ Yes         |Distance calculations are distorted by different scales|
|SVM                           |✅ Yes         |Maximising margin is affected by feature magnitudes    |
|K-Means Clustering            |✅ Yes         |Uses Euclidean distance — large-scale features dominate|
|Decision Trees / Random Forest|❌ No          |Splits are based on thresholds, not distances          |
|Gradient Boosting             |❌ No          |Tree-based; unaffected by monotonic transformations    |

**Standardisation vs. Normalisation:**

- Use **Standardisation** when your data has **outliers** or when the algorithm assumes a Gaussian (bell-curve) distribution (e.g., Logistic Regression, SVM).
- Use **Normalisation** when you need values bounded in [0,1] and are certain there are no extreme outliers (e.g., neural network inputs, image pixel values).

**Critical Rule:** Always fit the scaler on **training data only**, then apply (transform) it to all sets. If you fit on the full dataset, you leak information about the test distribution into training — a form of data leakage.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: Feature Scaling
# Dataset: California Housing (regression dataset with varied feature scales)
# ============================================================

from sklearn.datasets import fetch_california_housing  # Real estate dataset with 8 features
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler  # Two scaling transformers
import numpy as np

# --- Load Dataset ---
housing = fetch_california_housing()  # 20,640 California housing blocks, target = median house price
X = housing.data                      # Features: MedInc, HouseAge, AveRooms, etc.
y = housing.target                    # Target: Median house value (in $100,000s)

# --- Split Data ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,    # 80% train, 20% test
    random_state=42   # Reproducibility
)

# --- Print raw unscaled statistics ---
print("=== BEFORE SCALING (first 3 features, training set) ===")
print(f"Feature means:  {X_train[:, :3].mean(axis=0).round(2)}")   # axis=0 = mean down each column
print(f"Feature stds:   {X_train[:, :3].std(axis=0).round(2)}")    # Wildly different magnitudes

# ============================================================
# METHOD 1: StandardScaler (Standardisation / Z-score)
# Result: mean=0, std=1 for each feature
# ============================================================

scaler_std = StandardScaler()   # Instantiate the scaler object (no fitting yet)

# fit() computes the mean and std FROM THE TRAINING DATA ONLY
# This is critical — never fit on test data (data leakage!)
X_train_std = scaler_std.fit_transform(X_train)  # fit + transform in one step on training set
X_test_std  = scaler_std.transform(X_test)       # ONLY transform test set using training statistics

print("\n=== AFTER StandardScaler (first 3 features) ===")
print(f"Training means (should ≈ 0): {X_train_std[:, :3].mean(axis=0).round(4)}")
print(f"Training stds  (should ≈ 1): {X_train_std[:, :3].std(axis=0).round(4)}")

# ============================================================
# METHOD 2: MinMaxScaler (Normalisation)
# Result: all values compressed to range [0, 1]
# ============================================================

scaler_minmax = MinMaxScaler()  # Default range is [0, 1]; can set feature_range=(a, b)

X_train_mm = scaler_minmax.fit_transform(X_train)  # Fit on train, transform train
X_test_mm  = scaler_minmax.transform(X_test)       # Transform test using train min/max

print("\n=== AFTER MinMaxScaler (first 3 features) ===")
print(f"Training min (should ≈ 0): {X_train_mm[:, :3].min(axis=0).round(4)}")
print(f"Training max (should ≈ 1): {X_train_mm[:, :3].max(axis=0).round(4)}")

# Note: test set min/max may slightly exceed [0,1] — this is expected and correct.
# It just means a test sample has a value outside the training range.
```

-----

### 1C. One-Hot Encoding

#### 🧠 Phase 1: The Intuition

Imagine you have a “Color” column with values: `Red`, `Blue`, `Green`. If you naively convert these to numbers — Red=1, Blue=2, Green=3 — the model *wrongly* infers that Green (3) is “greater than” Red (1), and Blue is exactly halfway between them. But colors have no numerical order — this is a **categorical variable**.

**One-Hot Encoding** solves this by creating a **new binary column for each category**:

|Color|is_Red|is_Blue|is_Green|
|-----|------|-------|--------|
|Red  |1     |0      |0       |
|Blue |0     |1      |0       |
|Green|0     |0      |1       |

Now the model sees independent yes/no signals with no false ordering.

**Key Terms:**

- **Categorical Variable**: A feature with discrete labels (e.g., “City”, “Gender”, “Product Category”). No mathematical order.
- **Ordinal Variable**: A categorical variable *with* meaningful order (e.g., “Low/Medium/High”). Can be label-encoded as 1/2/3.
- **Dummy Variable Trap**: If you include all one-hot columns, they become **perfectly multicollinear** (if not Red and not Blue, it must be Green — redundant). Drop one column with `drop='first'` to avoid this. Many models handle this automatically, but it’s best practice to drop.
- **Sparse Matrix**: When many categories exist, the one-hot matrix has mostly zeros. This is called “sparse” — memory-efficient formats exist to store it.

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

Most ML algorithms require **numerical input**. They perform mathematical operations (multiplication, distance computation) that are undefined on text.

- **Label Encoding** (mapping categories to integers) introduces a false ordinal relationship. Only use it for truly ordinal features.
- **One-Hot Encoding** is the safest default for **nominal** (unordered) categorical variables.
- **High-cardinality** features (e.g., “City” with 1000 unique values) create 1000 new columns. Alternatives: **Target Encoding**, **Embedding**, or **Frequency Encoding**.
- Scaling is NOT needed after one-hot encoding (values are already 0 or 1).

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: One-Hot Encoding
# Dataset: Titanic (manually constructed sample for clarity)
# ============================================================

import pandas as pd
from sklearn.preprocessing import OneHotEncoder  # Scikit-learn's one-hot encoder
from sklearn.compose import ColumnTransformer    # Apply different transformers to different columns

# --- Create a small Titanic-like dataset ---
data = pd.DataFrame({
    'Pclass':    [1, 2, 3, 1, 3],           # Ticket class (ordinal: 1st, 2nd, 3rd)
    'Sex':       ['male', 'female', 'male', 'female', 'male'],  # Nominal: no order
    'Embarked':  ['S', 'C', 'Q', 'S', 'C'], # Port of embarkation (Nominal: Southampton/Cherbourg/Queenstown)
    'Age':       [22, 38, 26, 35, 28],       # Numerical feature (no encoding needed)
    'Survived':  [0, 1, 1, 1, 0]            # Target label (0=died, 1=survived)
})

print("=== Original Data ===")
print(data)

# --- Separate features and target ---
X = data[['Pclass', 'Sex', 'Embarked', 'Age']]  # Feature matrix
y = data['Survived']                              # Target vector

# ============================================================
# METHOD 1: pandas get_dummies (quick exploration)
# ============================================================

X_dummies = pd.get_dummies(
    X,
    columns=['Sex', 'Embarked'],  # Only one-hot encode nominal columns
    drop_first=True               # Drop first category to avoid dummy variable trap
                                  # 'Sex' keeps only 'Sex_male'; 'Embarked' drops 'Embarked_C'
)
print("\n=== After pd.get_dummies ===")
print(X_dummies)

# ============================================================
# METHOD 2: sklearn OneHotEncoder via ColumnTransformer (production-ready)
# Use this in real pipelines — integrates cleanly with train/test splits
# ============================================================

# ColumnTransformer applies different transformations to different column subsets
preprocessor = ColumnTransformer(
    transformers=[
        # Format: ('name', transformer_object, [list of columns to apply to])
        ('onehot',         # Arbitrary name for this step
         OneHotEncoder(    # The transformer to apply
             drop='first',       # Drop first category (avoids dummy variable trap)
             sparse_output=False, # Return dense numpy array instead of sparse matrix
             handle_unknown='ignore'  # Silently ignore categories not seen in training
         ),
         ['Sex', 'Embarked']    # Apply only to these nominal columns
        ),
    ],
    remainder='passthrough'  # Keep all other columns (Pclass, Age) unchanged
)

# fit_transform: learns the categories from X, then applies the transformation
X_encoded = preprocessor.fit_transform(X)

# Get meaningful column names for the output
ohe_feature_names = preprocessor.named_transformers_['onehot'].get_feature_names_out(['Sex', 'Embarked'])
all_feature_names = list(ohe_feature_names) + ['Pclass', 'Age']

print("\n=== After ColumnTransformer OneHotEncoder ===")
print(pd.DataFrame(X_encoded, columns=all_feature_names).round(2))
```

-----

### 1D. Pipelines

#### 🧠 Phase 1: The Intuition

Imagine a car manufacturing assembly line: every car goes through the same sequence of steps — first the frame is built, then the engine is installed, then it’s painted, then it’s tested. Each step is standardised and applies to every car in order.

An **ML Pipeline** is exactly this assembly line for data. You chain together multiple preprocessing steps and a final model into a single, unified object. When new data arrives, it automatically flows through each step in sequence.

**Why is this powerful?**

- Without a pipeline, you must manually remember to scale before predicting — easy to forget and causes bugs.
- Pipelines **prevent data leakage** by ensuring that fit operations only happen on training data when you call `pipeline.fit(X_train, y_train)`.
- Enables clean **cross-validation** and **hyperparameter tuning** on the entire workflow at once.

**Key Terms:**

- **Step**: One transformation or model within the pipeline.
- **Transformer**: Any object with `fit()` and `transform()` methods (e.g., scalers, encoders).
- **Estimator**: The final model in the pipeline (e.g., Logistic Regression). Has `fit()` and `predict()`.

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

Without a pipeline, a common data leakage bug looks like this:

```
❌ WRONG (leakage):
scaler.fit(X_all)         # Fitted on ALL data — test info leaks into scaler
X_train_s = scaler.transform(X_train)
X_test_s  = scaler.transform(X_test)

✅ CORRECT (via Pipeline):
pipeline.fit(X_train, y_train)   # fit() only touches training data internally
pipeline.predict(X_test)          # Applies learned transformations, then predicts
```

Pipelines also enable `GridSearchCV` — automated hyperparameter search — to tune both preprocessing and model parameters together, which ensures each fold in cross-validation is treated correctly.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: ML Pipelines
# Dataset: Titanic-like (mixed numerical + categorical features)
# ============================================================

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline                         # The Pipeline class — chains steps sequentially
from sklearn.compose import ColumnTransformer                 # Apply different transforms to different columns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer                      # Fills in missing (NaN) values
from sklearn.linear_model import LogisticRegression           # Our final classifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- Build a sample dataset with missing values (realistic) ---
np.random.seed(42)
n = 200  # number of samples

data = pd.DataFrame({
    'Age':       np.random.normal(35, 12, n),                       # Numerical, has distribution
    'Fare':      np.random.exponential(30, n),                       # Numerical, right-skewed
    'Sex':       np.random.choice(['male', 'female'], n),            # Categorical
    'Embarked':  np.random.choice(['S', 'C', 'Q', None], n, p=[0.7, 0.2, 0.09, 0.01]),  # Categorical w/ NaN
    'Survived':  np.random.randint(0, 2, n)                          # Target
})

# Introduce some missing values in Age (realistic — Titanic data had this)
data.loc[np.random.choice(data.index, 20, replace=False), 'Age'] = np.nan

print(f"Missing values:\n{data.isnull().sum()}\n")

# --- Separate features and target ---
X = data.drop('Survived', axis=1)  # All columns except the target
y = data['Survived']               # The target column

# --- Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ============================================================
# Define column groups — which columns need which treatment
# ============================================================
numerical_cols   = ['Age', 'Fare']           # Need imputation + scaling
categorical_cols = ['Sex', 'Embarked']       # Need imputation + one-hot encoding

# ============================================================
# Build sub-pipelines for each column type
# ============================================================

# Pipeline for NUMERICAL columns:
# Step 1: Impute (fill) missing values with the median (robust to outliers)
# Step 2: Scale with StandardScaler (mean=0, std=1)
numerical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),  # Replace NaN with column median
    ('scaler',  StandardScaler())                   # Standardise: (x - mean) / std
])

# Pipeline for CATEGORICAL columns:
# Step 1: Impute missing values with the most frequent category
# Step 2: One-hot encode
categorical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # Replace NaN with mode
    ('encoder', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
])

# ============================================================
# Combine both sub-pipelines using ColumnTransformer
# ============================================================
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_pipeline,   numerical_cols),    # Apply numerical pipeline to num cols
        ('cat', categorical_pipeline, categorical_cols),  # Apply categorical pipeline to cat cols
    ]
)

# ============================================================
# Build the FULL end-to-end pipeline
# ============================================================
full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),                      # Step 1: All preprocessing
    ('classifier',   LogisticRegression(random_state=42, max_iter=1000))  # Step 2: Final model
])

# ============================================================
# Fit the pipeline — ONLY on training data
# Internally: preprocessor.fit(X_train) → model.fit(preprocessed_X_train, y_train)
# ============================================================
full_pipeline.fit(X_train, y_train)

# ============================================================
# Predict — pipeline automatically preprocesses test data
# Internally: preprocessor.transform(X_test) → model.predict(preprocessed_X_test)
# No manual scaling or encoding needed!
# ============================================================
y_pred = full_pipeline.predict(X_test)

# --- Evaluate ---
print(f"Pipeline Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nThe pipeline handled missing values, encoding, scaling, and prediction — all in one object!")
```

-----

## 📈 Supervised Learning

> **Supervised Learning**: The model learns from **labelled data** — input-output pairs where the correct answer is already known. Goal: learn a mapping from inputs (X) to outputs (y).

-----

### 2A. Linear Regression & Gradient Descent

#### 🧠 Phase 1: The Intuition

Imagine you want to predict a house’s price based on its size (in sq ft). You plot all your data points on a graph — size on the x-axis, price on the y-axis. **Linear Regression** finds the single *best straight line* through those dots.

This line is your model. Given a new house size you’ve never seen, you find where it lands on the line — that’s your price prediction.

The line is described by the equation: **ŷ = β₀ + β₁·x**

- **ŷ** (pronounced “y-hat”): The predicted price.
- **β₀** (beta-zero): The **intercept** — where the line crosses the y-axis (price when size = 0).
- **β₁** (beta-one): The **coefficient** (or **slope**) — how much price increases per 1 sq ft increase.
- The model’s job: find the values of β₀ and β₁ that make the line fit the data best.

**What does “best fit” mean?** The line that minimises the total error — the sum of squared distances between each real point and the line’s prediction. This is called the **Mean Squared Error (MSE)**.

**Gradient Descent** is how the model *learns* those best β values:

Imagine you’re blindfolded on a hilly landscape, and you want to reach the lowest valley (minimum error). Each step, you feel which direction slopes downward and take a step that way. Repeat until you’re at the bottom. That’s gradient descent — iteratively adjusting β values in the direction that reduces error most.

**Key Terms:**

- **Coefficient**: The weight assigned to a feature; how much that feature influences the prediction.
- **Intercept**: The baseline prediction when all features are zero.
- **Loss Function**: A mathematical measure of how wrong predictions are. For regression, this is MSE.
- **Gradient**: The slope of the loss surface — points in the direction of steepest increase.
- **Learning Rate (α)**: The size of each step in gradient descent. Too large = overshoot the minimum. Too small = painfully slow convergence.
- **Epoch**: One full pass through the training data during gradient descent.

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

**The Maths of Gradient Descent:**

The MSE loss for Linear Regression is:

`L(β) = (1/n) · Σ(yᵢ - ŷᵢ)²`

Gradient Descent updates β as:

`β_new = β_old - α · ∂L/∂β`

Where `∂L/∂β` is the partial derivative of the loss with respect to β — pointing in the direction of steepest ascent. We move *against* the gradient (downhill).

**Variants of Gradient Descent:**

- **Batch GD**: Uses all training samples to compute gradient — stable but slow for large data.
- **Stochastic GD (SGD)**: Uses one sample at a time — fast but noisy.
- **Mini-Batch GD**: Uses small batches (e.g., 32 samples) — best of both worlds. Most commonly used in practice.

**Bias-Variance Trade-off for Linear Regression:**

- Linear Regression is a **high-bias, low-variance** model. It assumes a linear relationship, which may be overly simple (underfitting) for complex datasets.
- Adding polynomial features (`x²`, `x³`) reduces bias but can increase variance.
- **Regularisation** (Ridge/Lasso) controls variance by penalising large coefficients.

**Why Scaling is MANDATORY here:**
If feature A ranges from 0 to 1 and feature B ranges from 0 to 1,000,000, gradient descent takes enormous steps along B’s axis and tiny steps along A’s, making the loss surface extremely elongated and hard to navigate. Scaling makes the loss surface spherical — gradient descent converges much faster.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: Linear Regression + Gradient Descent
# Dataset: California Housing (predicting house prices)
# ============================================================

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for file saving
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.metrics import mean_squared_error, r2_score

# --- Load Dataset ---
housing = fetch_california_housing()
X = housing.data    # 8 numerical features
y = housing.target  # Median house value in $100,000s

# --- Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Scale Features (MANDATORY for gradient descent-based models) ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit on train, transform train
X_test_scaled  = scaler.transform(X_test)       # Only transform test (no fitting!)

# ============================================================
# METHOD 1: Ordinary Least Squares (OLS) — Closed-form solution
# sklearn's LinearRegression uses matrix algebra (Normal Equation)
# directly solves for the optimal β without iteration
# Best for small/medium datasets where exact solution is feasible
# ============================================================
ols_model = LinearRegression()          # Instantiate; no hyperparameters needed for OLS
ols_model.fit(X_train_scaled, y_train)  # Solve for β using the Normal Equation: β = (XᵀX)⁻¹Xᵀy

# Predict on test set
y_pred_ols = ols_model.predict(X_test_scaled)  # ŷ = β₀ + β₁x₁ + β₂x₂ + ... + β₈x₈

# Evaluate
mse_ols = mean_squared_error(y_test, y_pred_ols)  # Mean of (actual - predicted)²
r2_ols  = r2_score(y_test, y_pred_ols)            # R²: proportion of variance explained (1.0 = perfect)

print("=== OLS Linear Regression ===")
print(f"MSE:  {mse_ols:.4f}")           # Lower is better
print(f"RMSE: {np.sqrt(mse_ols):.4f}") # Root MSE — in same units as target
print(f"R²:   {r2_ols:.4f}")           # ~0.60 means model explains 60% of price variance

# Show the learned coefficients
print(f"\nIntercept (β₀): {ols_model.intercept_:.4f}")
print("Feature Coefficients (β₁ to β₈):")
for name, coef in zip(housing.feature_names, ols_model.coef_):
    print(f"  {name:15s}: {coef:.4f}")  # Larger |coef| = stronger influence on price

# ============================================================
# METHOD 2: SGD Regressor — Gradient Descent iterative solution
# Useful for large datasets where OLS is computationally expensive
# Implements Mini-Batch Stochastic Gradient Descent
# ============================================================
sgd_model = SGDRegressor(
    loss='squared_error',   # Optimise MSE loss function
    learning_rate='optimal',# Adaptive learning rate schedule (decreases over time)
    max_iter=1000,          # Maximum number of epochs (full passes through training data)
    tol=1e-4,               # Convergence tolerance: stop if loss improvement < tol
    random_state=42
)
sgd_model.fit(X_train_scaled, y_train)  # Iteratively update β via gradient descent

y_pred_sgd = sgd_model.predict(X_test_scaled)

print("\n=== SGD Regressor ===")
print(f"MSE:  {mean_squared_error(y_test, y_pred_sgd):.4f}")
print(f"R²:   {r2_score(y_test, y_pred_sgd):.4f}")
# Should be close to OLS — both optimise the same objective, just different methods

# ============================================================
# MANUAL Gradient Descent — Educational implementation
# Shows exactly how gradient descent works step-by-step
# ============================================================
print("\n=== Manual Gradient Descent (Educational) ===")

# Use just 1 feature (MedInc = Median Income) for easy visualisation
X_simple_train = X_train_scaled[:, 0:1]  # Slice first feature only, keep 2D shape
X_simple_test  = X_test_scaled[:, 0:1]

n = len(X_simple_train)                  # Number of training samples

# Initialise parameters randomly
np.random.seed(42)
beta_0 = 0.0   # Intercept — start at zero
beta_1 = 0.0   # Coefficient — start at zero

alpha = 0.01   # Learning rate — step size for each gradient descent update
epochs = 500   # Number of full passes through training data
loss_history = []  # Track loss at each epoch to monitor convergence

for epoch in range(epochs):
    # --- Forward Pass: Compute predictions ---
    y_hat = beta_0 + beta_1 * X_simple_train.flatten()  # ŷ = β₀ + β₁·x

    # --- Compute Loss (MSE) ---
    errors = y_hat - y_simple_train if epoch > 0 else y_hat - y_train  # residuals
    errors = y_hat - y_train         # residuals = predicted - actual
    mse    = np.mean(errors ** 2)    # Mean Squared Error
    loss_history.append(mse)

    # --- Compute Gradients (partial derivatives of MSE w.r.t. each parameter) ---
    # ∂MSE/∂β₀ = (2/n) · Σ(ŷᵢ - yᵢ)      ← gradient for intercept
    # ∂MSE/∂β₁ = (2/n) · Σ(ŷᵢ - yᵢ)·xᵢ  ← gradient for slope
    grad_beta_0 = (2/n) * np.sum(errors)                           # Gradient of intercept
    grad_beta_1 = (2/n) * np.sum(errors * X_simple_train.flatten()) # Gradient of coefficient

    # --- Gradient Descent Update Step ---
    # Move AGAINST the gradient (downhill on the loss surface)
    beta_0 = beta_0 - alpha * grad_beta_0  # Update intercept
    beta_1 = beta_1 - alpha * grad_beta_1  # Update coefficient

# Final results from manual gradient descent
print(f"Learned Intercept (β₀): {beta_0:.4f}")
print(f"Learned Coefficient (β₁ for MedInc): {beta_1:.4f}")
print(f"Final Training MSE: {loss_history[-1]:.4f}")

# Plot the loss curve — should decrease and flatten (converge)
plt.figure(figsize=(8, 4))
plt.plot(loss_history, color='steelblue', linewidth=2)           # Loss over epochs
plt.xlabel('Epoch')
plt.ylabel('MSE Loss')
plt.title('Gradient Descent: Loss Convergence')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('gradient_descent_loss.png', dpi=100)
plt.close()
print("\nLoss convergence plot saved to 'gradient_descent_loss.png'")
```

-----

### 2B. Logistic Regression

#### 🧠 Phase 1: The Intuition

Despite its name, **Logistic Regression** is a **classification** algorithm, not a regression one. It predicts *categories* (e.g., spam or not spam, survived or died).

Imagine a doctor looking at a patient’s test results to decide: *“Does this patient have diabetes?”* The answer is binary — Yes or No. Logistic Regression estimates the **probability** of belonging to a class, then uses a threshold (usually 0.5) to make the final decision.

The core trick is the **Sigmoid Function**, which squashes any number into a probability between 0 and 1:

```
P(y=1 | X) = 1 / (1 + e^(-z))
```

Where `z = β₀ + β₁x₁ + ... + βₙxₙ` — the same linear combination as Linear Regression, but passed through the sigmoid “squasher.”

*Analogy:* Imagine a dimmer switch. Linear Regression is like setting the raw voltage. The sigmoid is the dimmer — no matter what voltage you input, the light brightness (probability) stays between 0% and 100%.

**Key Terms:**

- **Binary Classification**: Predicting one of two classes (0 or 1, Yes or No).
- **Probability**: A number between 0 and 1 representing likelihood of an outcome.
- **Sigmoid / Logistic Function**: The S-shaped curve that converts any real number to a probability.
- **Decision Boundary**: The threshold (default 0.5) above which we predict class 1, below which class 0.
- **Log-Odds (Logit)**: The natural log of the odds ratio: `log(p / (1-p))`. Logistic regression models this as linear in X.

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

Why not just use Linear Regression for classification?

Linear Regression can predict values outside [0, 1], which are meaningless as probabilities. It also assumes a linear relationship in output values, but class probabilities saturate (a very healthy patient has near-0 probability of disease, a very sick patient has near-1).

**Loss Function**: Logistic Regression uses **Binary Cross-Entropy** (Log Loss) instead of MSE:

`L = -[y·log(p) + (1-y)·log(1-p)]`

This penalises confident wrong predictions very heavily (if the model says 99% probability of class 0 but the answer is class 1, the loss is enormous).

**Bias-Variance Trade-off:**

- Logistic Regression is a **linear model** — it draws a straight line (or hyperplane in higher dimensions) as the decision boundary.
- If the true boundary is curved, LR underfits (**high bias**).
- Adding polynomial features or using **regularisation** (C parameter in sklearn) balances this. Smaller C = stronger regularisation = simpler model = higher bias, lower variance.

**Why Scaling is MANDATORY:**
Same as Linear Regression — gradient descent on the log-loss is scale-sensitive. Unscaled features cause uneven gradient steps.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: Logistic Regression (Binary Classification)
# Dataset: Breast Cancer Wisconsin (malignant vs. benign tumours)
# ============================================================

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                              confusion_matrix, roc_auc_score)
import numpy as np

# --- Load Dataset ---
cancer = load_breast_cancer()
X = cancer.data    # 30 numerical features (tumour measurements)
y = cancer.target  # 0 = malignant (cancerous), 1 = benign (non-cancerous)

print(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features")
print(f"Classes: {cancer.target_names}")  # ['malignant', 'benign']
print(f"Class balance: {np.bincount(y)}")  # [212 malignant, 357 benign]

# --- Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y  # Preserve 37/63% malignant/benign ratio in both sets
)

# --- Feature Scaling (MANDATORY for logistic regression) ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit on train only
X_test_scaled  = scaler.transform(X_test)       # Transform test using training stats

# --- Train Logistic Regression Model ---
# C: Inverse of regularisation strength. Smaller C = stronger regularisation.
# Regularisation prevents overfitting by penalising large coefficients.
# solver='lbfgs': Optimisation algorithm (good default for small/medium datasets)
# max_iter: Maximum iterations for the optimiser to converge
logistic_model = LogisticRegression(
    C=1.0,          # Default regularisation strength (try 0.01 or 100 to see effect)
    solver='lbfgs', # Limited-memory BFGS — efficient quasi-Newton optimiser
    max_iter=1000,  # Allow enough iterations for convergence
    random_state=42
)

logistic_model.fit(X_train_scaled, y_train)  # Learn coefficients by minimising log-loss

# --- Predict ---
y_pred       = logistic_model.predict(X_test_scaled)        # Hard predictions: 0 or 1
y_pred_proba = logistic_model.predict_proba(X_test_scaled)  # Soft predictions: [P(class0), P(class1)]

print("\n=== Logistic Regression Results ===")
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
# ROC-AUC: Area Under the Receiver Operating Characteristic curve
# Measures the model's ability to distinguish between classes (1.0 = perfect, 0.5 = random)
print(f"ROC-AUC:   {roc_auc_score(y_test, y_pred_proba[:, 1]):.4f}")  # Use P(class=1)

# Full classification report: precision, recall, F1 for each class
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=cancer.target_names))

# Show probability predictions for first 5 test samples
print("=== Probability Predictions (first 5 samples) ===")
print("P(malignant)  P(benign)  True Label  Prediction")
for i in range(5):
    print(f"  {y_pred_proba[i, 0]:.4f}      {y_pred_proba[i, 1]:.4f}"
          f"     {cancer.target_names[y_test[i]]:10s}  {cancer.target_names[y_pred[i]]}")

# Show most influential features (largest |coefficient| = strongest predictor)
print("\n=== Top 5 Most Influential Features ===")
feature_importance = sorted(
    zip(cancer.feature_names, logistic_model.coef_[0]),  # coef_[0] = coefficients for class 1
    key=lambda x: abs(x[1]),  # Sort by absolute value of coefficient
    reverse=True
)
for feature, coef in feature_importance[:5]:
    direction = "↑ increases" if coef > 0 else "↓ decreases"
    print(f"  {feature:35s}: {coef:+.4f}  ({direction} P(benign))")
```

-----

### 2C. Decision Trees & Random Forest

#### 🧠 Phase 1: The Intuition

**Decision Tree:**

Think of the children’s game “20 Questions.” You’re thinking of an animal:

- *“Does it have fur?”* → Yes → *“Does it bark?”* → Yes → *It’s a dog!*

A Decision Tree works exactly this way — it asks a series of yes/no questions about the features to classify data. Each question is a **split node**, each possible answer is a **branch**, and the final answers are **leaf nodes** (the predicted class).

**Random Forest:**

One doctor’s opinion is good. But what if you got second opinions from 500 doctors, each trained slightly differently, and took the majority vote? That’s far more reliable!

A Random Forest builds **hundreds of Decision Trees**, each trained on a slightly different random subset of the data and features, then combines their predictions by **majority vote** (classification) or **averaging** (regression). This is called **ensemble learning**.

**Key Terms:**

- **Node**: A decision point in the tree (a question about a feature).
- **Split**: Dividing data at a node based on a feature threshold (e.g., “Age > 30?”).
- **Leaf Node**: The terminal node — contains the final prediction.
- **Depth**: How many questions deep the tree goes. Deeper = more complex = more prone to overfitting.
- **Gini Impurity**: A measure of how “mixed” the classes are at a node (0 = pure node, all same class).
- **Bootstrap Sample**: A random sample drawn *with replacement* from the training set. Each tree in a Random Forest is trained on a different bootstrap sample.
- **Feature Subsampling**: At each split, each tree only considers a random subset of features. This ensures trees are diverse (different from each other).

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

**How a Decision Tree Splits:**

At each node, the algorithm tries all possible feature-threshold combinations and picks the split that most reduces **impurity** (measured by Gini Impurity or Entropy):

`Gini = 1 - Σpᵢ²`

Where `pᵢ` is the proportion of class i at that node. A pure node (all one class) has Gini = 0.

**Bias-Variance Trade-off — The Core Problem with Trees:**

- A **fully grown tree** (no depth limit) will memorise every training sample, achieving 0 training error but failing badly on new data. This is **high variance / overfitting**.
- A **very shallow tree** (depth=1 is called a “stump”) is too simple and underfits — **high bias**.

**How Random Forest fixes this:**

By averaging hundreds of high-variance trees, Random Forest dramatically **reduces variance** while keeping **bias low**. The randomness (bootstrap sampling + feature subsampling) ensures trees make **uncorrelated errors** — their mistakes cancel out in the majority vote. This principle is called the **Bias-Variance trade-off via ensemble averaging**.

**Scaling:** Decision Trees and Random Forests are **scale-invariant**. They only care about the *relative ordering* of feature values to set thresholds, not the actual magnitudes. No scaling required.

**Feature Importance:** Random Forest naturally provides feature importance scores — how much each feature reduces impurity across all trees. Very useful for feature selection.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: Decision Trees & Random Forest
# Dataset: Iris (multi-class classification with 3 flower species)
# ============================================================

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text  # Decision tree + text visualiser
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# --- Load Dataset ---
iris = load_iris()
X = iris.data    # 4 features: sepal/petal length & width
y = iris.target  # 3 classes: Setosa (0), Versicolor (1), Virginica (2)

# --- Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================
# Part 1: Decision Tree
# ============================================================

# --- Overfitting Example: Fully Grown Tree ---
dt_overfit = DecisionTreeClassifier(
    random_state=42  # No max_depth = tree grows until pure leaves (overfitting!)
)
dt_overfit.fit(X_train, y_train)

print("=== Decision Tree (No Depth Limit — Overfitting) ===")
print(f"  Train Accuracy: {dt_overfit.score(X_train, y_train):.4f}")  # Likely 1.00 (memorised training set)
print(f"  Test  Accuracy: {dt_overfit.score(X_test,  y_test):.4f}")   # Lower — poor generalisation

# --- Well-Tuned Tree: Limit depth to prevent overfitting ---
dt_tuned = DecisionTreeClassifier(
    max_depth=3,           # Maximum 3 levels of questions — prevents memorisation
    min_samples_split=5,   # A node must have ≥5 samples to be split (prevents tiny, noisy splits)
    min_samples_leaf=2,    # Each leaf must have ≥2 samples (prevents single-sample leaf nodes)
    criterion='gini',      # Use Gini Impurity to measure split quality (alternative: 'entropy')
    random_state=42
)
dt_tuned.fit(X_train, y_train)

print("\n=== Decision Tree (Depth=3 — Well Tuned) ===")
print(f"  Train Accuracy: {dt_tuned.score(X_train, y_train):.4f}")
print(f"  Test  Accuracy: {dt_tuned.score(X_test,  y_test):.4f}")

# Visualise the tree structure as text — see exactly what questions it asks
print("\nDecision Tree Structure:")
print(export_text(dt_tuned, feature_names=iris.feature_names))

# ============================================================
# Part 2: Random Forest
# ============================================================

# n_estimators: Number of trees in the forest (more = better, but slower)
# max_features: At each split, consider only sqrt(n_features) random features
#               This is what ensures trees are diverse and uncorrelated
# max_depth: Optionally limit tree depth; None = fully grown trees
# n_jobs=-1: Use all available CPU cores (parallelise tree building)
rf_model = RandomForestClassifier(
    n_estimators=200,   # Build 200 independent decision trees
    max_depth=None,     # Let trees grow fully; variance reduced by averaging
    max_features='sqrt',# Each split considers sqrt(4) ≈ 2 random features
    min_samples_split=2,# Default: split as soon as ≥2 samples
    min_samples_leaf=1, # Default: leaves can have 1 sample (OK because we're averaging)
    bootstrap=True,     # Each tree uses a bootstrap sample (random with replacement)
    random_state=42,
    n_jobs=-1           # Parallel processing — speeds up training on multi-core machines
)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)  # Majority vote across all 200 trees

print("\n=== Random Forest (200 Trees) ===")
print(f"  Train Accuracy: {rf_model.score(X_train, y_train):.4f}")
print(f"  Test  Accuracy: {rf_model.score(X_test,  y_test):.4f}")
print(f"\n{classification_report(y_test, y_pred_rf, target_names=iris.target_names)}")

# --- Feature Importance: Which features matter most? ---
# Computed as the mean decrease in Gini impurity across all trees and splits
print("=== Feature Importances (mean decrease in Gini impurity) ===")
importance_pairs = sorted(
    zip(iris.feature_names, rf_model.feature_importances_),
    key=lambda x: x[1],   # Sort by importance
    reverse=True           # Most important first
)
for feature, importance in importance_pairs:
    bar = "█" * int(importance * 50)  # Visual bar chart in terminal
    print(f"  {feature:25s}: {importance:.4f}  {bar}")

# Petal features should dominate — they are the most discriminative for Iris classification
```

-----

### 2D. Gradient Boosting

#### 🧠 Phase 1: The Intuition

Where Random Forest builds trees **in parallel** (independently), Gradient Boosting builds trees **sequentially** — each new tree learns from the *mistakes* of the previous ones.

*Analogy:* Imagine a student taking a series of practice tests. After the first test, the teacher identifies every question they got wrong and focuses the next lesson *entirely* on those weak areas. After the second test, the teacher focuses on the remaining errors. Each lesson specifically targets the previous mistakes.

In Gradient Boosting:

1. Start with a simple prediction (e.g., the mean of all targets).
1. Calculate the **residuals** — how wrong was that prediction?
1. Train a small tree to predict those residuals.
1. Add this tree to the model (scaled by a small **learning rate**).
1. Recalculate residuals. Repeat.

The final model is the *sum* of all these small trees — a committee of specialists, each correcting the previous committee’s errors.

**Key Terms:**

- **Residuals**: The errors of the current model — what’s left unexplained (actual minus predicted).
- **Weak Learner**: A simple model (typically a shallow tree, depth 3–8) that performs only slightly better than chance.
- **Ensemble**: A combination of many models whose predictions are aggregated.
- **Learning Rate (shrinkage)**: Scales each tree’s contribution. Smaller = slower learning but better generalisation.
- **XGBoost / LightGBM / CatBoost**: Production-grade implementations of gradient boosting with performance optimisations.

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

**The “Gradient” in Gradient Boosting:**

At each step, we fit a tree to the **negative gradient of the loss function** with respect to the current predictions. For MSE loss, the gradient is simply the residual — but the framework generalises to any differentiable loss.

**Bias-Variance Trade-off:**

- Each tree is a high-bias, low-variance learner (shallow).
- By combining them sequentially, we **reduce bias** — each addition fixes systematic errors.
- Risk: too many trees can cause **overfitting** (high variance). Control with:
  - `n_estimators`: Number of trees.
  - `learning_rate`: Shrinkage per tree — smaller rate requires more trees.
  - `max_depth`: Depth of individual trees.
  - `subsample`: Fraction of samples used per tree (adds randomness, reduces overfitting).

**Gradient Boosting vs. Random Forest:**

|Property           |Random Forest|Gradient Boosting               |
|-------------------|-------------|--------------------------------|
|Tree building      |Parallel     |Sequential                      |
|Variance control   |Averaging    |Learning rate + depth control   |
|Bias               |Low          |Very Low                        |
|Overfitting risk   |Low          |Medium (needs careful tuning)   |
|Speed              |Faster       |Slower (XGBoost is fast)        |
|Typical performance|Very good    |State-of-the-art on tabular data|

**Scaling:** Not required — tree-based.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: Gradient Boosting
# Dataset: California Housing (regression)
# ============================================================

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# --- Load Dataset ---
housing = fetch_california_housing()
X = housing.data
y = housing.target

# --- Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- No scaling needed for tree-based methods ---

# ============================================================
# METHOD 1: sklearn GradientBoostingRegressor (educational, slower)
# ============================================================

gb_model = GradientBoostingRegressor(
    n_estimators=300,       # Build 300 sequential trees
    learning_rate=0.05,     # Each tree contributes only 5% — conservative but more accurate
                            # Rule of thumb: smaller learning_rate needs more n_estimators
    max_depth=4,            # Each tree is shallow — weak learner (high bias, low variance)
    subsample=0.8,          # Each tree trains on 80% of data (random sampling)
                            # Adds stochasticity — reduces overfitting, like Random Forest
    min_samples_split=10,   # A node needs ≥10 samples to split — prevents tiny useless splits
    loss='squared_error',   # Minimise MSE (standard for regression)
    random_state=42
)

print("Training Gradient Boosting... (may take a moment)")
gb_model.fit(X_train, y_train)  # Sequential: each tree fits residuals of previous model

y_pred_gb = gb_model.predict(X_test)

print("=== Gradient Boosting Regressor ===")
print(f"  Train R²: {r2_score(y_train, gb_model.predict(X_train)):.4f}")
print(f"  Test  R²: {r2_score(y_test,  y_pred_gb):.4f}")
print(f"  Test RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_gb)):.4f}")

# ============================================================
# METHOD 2: HistGradientBoostingRegressor (faster, production-grade)
# Uses histogram-based algorithm (similar to LightGBM)
# Handles missing values natively, faster on large datasets
# ============================================================

hist_gb = HistGradientBoostingRegressor(
    max_iter=300,           # Number of boosting iterations (trees)
    learning_rate=0.05,     # Shrinkage factor per iteration
    max_depth=4,            # Maximum depth of individual trees
    l2_regularization=0.1,  # L2 penalty on leaf values — prevents overfitting
    early_stopping=True,    # Stop if validation score stops improving
    validation_fraction=0.1,# 10% of training data used for early stopping validation
    n_iter_no_change=20,    # Stop after 20 consecutive iterations with no improvement
    random_state=42
)

hist_gb.fit(X_train, y_train)

y_pred_hist = hist_gb.predict(X_test)

print("\n=== Histogram Gradient Boosting (Faster) ===")
print(f"  Actual iterations used: {hist_gb.n_iter_}")  # May stop early
print(f"  Train R²:  {r2_score(y_train, hist_gb.predict(X_train)):.4f}")
print(f"  Test  R²:  {r2_score(y_test,  y_pred_hist):.4f}")
print(f"  Test RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_hist)):.4f}")

# ============================================================
# Insight: How predictions improve with more trees
# ============================================================
staged_r2 = []
# staged_predict: yields prediction after each of the 300 boosting stages
for i, y_staged in enumerate(gb_model.staged_predict(X_test)):
    if (i+1) % 50 == 0:  # Print every 50 trees
        r2 = r2_score(y_test, y_staged)
        staged_r2.append(r2)
        print(f"  After {i+1:3d} trees — Test R²: {r2:.4f}")
# You'll see R² increase as more trees are added, then plateau (early stopping helps here)
```

-----

## 🔍 Unsupervised Learning

> **Unsupervised Learning**: No labels. The model finds hidden structure, patterns, or groupings in data on its own.

-----

### 3A. K-Means Clustering

#### 🧠 Phase 1: The Intuition

Imagine you’re a supermarket manager looking at customer purchase data. You have no predefined customer categories — but you want to identify natural groups (budget shoppers, premium buyers, bargain hunters) to tailor promotions.

**K-Means** finds K natural groups (**clusters**) in your data by:

1. Randomly place K **centroids** (imaginary cluster centres) in the data space.
1. Assign each data point to the nearest centroid — forming K clusters.
1. Recalculate each centroid as the **mean** (average position) of all points assigned to it.
1. Repeat steps 2–3 until the centroids stop moving (convergence).

*Analogy:* Imagine K magnets dropped onto a map of cities. Each city attaches to its nearest magnet. Then each magnet moves to the geographic centre of its assigned cities. Repeat until no city needs to change magnets.

**Key Terms:**

- **K**: The number of clusters — **you must choose this beforehand** (a critical limitation).
- **Centroid**: The mean position of all data points in a cluster. Not necessarily an actual data point.
- **Cluster**: A group of data points that are more similar to each other than to points in other clusters.
- **Inertia (Within-Cluster Sum of Squares, WCSS)**: Total distance of all points from their centroids. Lower = tighter, better-defined clusters.
- **Elbow Method**: A technique to choose K — plot inertia vs. K and look for where the curve bends like an elbow.

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

**K-Means Objective Function:**

Minimise: `J = Σᵢ Σ(x ∈ Cᵢ) ||x - μᵢ||²`

Where μᵢ is the centroid of cluster i. This is not globally optimal — K-Means finds a local minimum, which is why:

- `n_init=10`: sklearn runs K-Means 10 times with different random starts, picks the best.
- `init='k-means++'`: Smart initialisation that spreads initial centroids, reduces bad local minima.

**Bias-Variance in Clustering:**

- Very small K: Few broad clusters — high bias (underfitting, ignoring true structure).
- Very large K: Tiny clusters — high variance (overfitting, splitting noise).
- K-Means assumes **spherical, equally-sized clusters**. Fails on elongated or oddly-shaped clusters (use DBSCAN instead).

**Why Scaling is MANDATORY:**
K-Means uses **Euclidean distance**. If “salary” ranges 30,000–150,000 and “age” ranges 20–65, distance will be almost entirely dominated by salary. After standardisation, each feature contributes equally to the distance calculation.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: K-Means Clustering
# Dataset: Iris (we remove labels to simulate unsupervised scenario)
# ============================================================

from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Load Dataset (ignore labels — unsupervised!) ---
iris = load_iris()
X = iris.data    # 4 features
y_true = iris.target  # Keep true labels only for evaluation, NOT for training

# --- Feature Scaling (MANDATORY for distance-based algorithms) ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Standardise: all features get mean=0, std=1

# ============================================================
# Step 1: Find optimal K using the Elbow Method
# Plot inertia (within-cluster sum of squares) vs. number of clusters
# ============================================================

inertias = []          # Store WCSS for each value of K
silhouette_scores = [] # Store silhouette score for each K (alternative metric)
K_range = range(2, 9)  # Test K from 2 to 8

for k in K_range:
    # n_init: Run K-Means k times with different random centroids, keep best result
    # init='k-means++': Smart centroid initialisation to avoid bad local minima
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    km.fit(X_scaled)

    inertias.append(km.inertia_)  # WCSS: sum of squared distances to centroids

    # Silhouette score: measures cohesion vs. separation (-1 to 1, higher = better)
    sil = silhouette_score(X_scaled, km.labels_)
    silhouette_scores.append(sil)

    print(f"K={k}: Inertia={km.inertia_:.2f}, Silhouette={sil:.4f}")

# Plot Elbow Curve
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)  # Blue circles connected by line
axes[0].set_xlabel('Number of Clusters K')
axes[0].set_ylabel('Inertia (WCSS)')
axes[0].set_title('Elbow Method: Find Optimal K')
axes[0].axvline(x=3, color='red', linestyle='--', label='Elbow at K=3')  # Expected elbow
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(K_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
axes[1].set_xlabel('Number of Clusters K')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Score vs. K')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('kmeans_elbow.png', dpi=100)
plt.close()
print("\nElbow method plot saved to 'kmeans_elbow.png'")

# ============================================================
# Step 2: Fit final K-Means with K=3 (we know Iris has 3 species)
# ============================================================

kmeans_final = KMeans(
    n_clusters=3,       # K=3: we expect 3 natural groups (matching 3 Iris species)
    init='k-means++',   # Smart initialisation: first centroid random, others chosen proportional to distance
    n_init=10,          # Run 10 times, keep result with lowest inertia
    max_iter=300,       # Maximum iterations per run for convergence
    random_state=42
)

cluster_labels = kmeans_final.fit_predict(X_scaled)  # fit + return cluster assignments

# --- Evaluate Cluster Quality ---
final_silhouette = silhouette_score(X_scaled, cluster_labels)

# Adjusted Rand Index (ARI): compares clustering to true labels (1=perfect, 0=random)
# Only usable when ground truth is known — not normally available in unsupervised learning
ari = adjusted_rand_score(y_true, cluster_labels)

print("\n=== Final K-Means Model (K=3) ===")
print(f"  Final Inertia:         {kmeans_final.inertia_:.4f}")
print(f"  Silhouette Score:      {final_silhouette:.4f}  (range -1 to 1, higher is better)")
print(f"  Adjusted Rand Index:   {ari:.4f}          (1.0 = perfect match with true labels)")

# --- Inspect Cluster Centroids ---
# Centroids are in scaled space — inverse_transform back to original scale for interpretation
centroids_original = scaler.inverse_transform(kmeans_final.cluster_centers_)
print("\n=== Cluster Centroids (original scale) ===")
print(f"{'Feature':20s}  {'Cluster 0':>10} {'Cluster 1':>10} {'Cluster 2':>10}")
for i, feature in enumerate(iris.feature_names):
    print(f"  {feature:20s}  {centroids_original[0, i]:>10.2f} "
          f"{centroids_original[1, i]:>10.2f} {centroids_original[2, i]:>10.2f}")

# Cluster size distribution
unique, counts = np.unique(cluster_labels, return_counts=True)
print("\n=== Cluster Sizes ===")
for cluster, count in zip(unique, counts):
    print(f"  Cluster {cluster}: {count} samples")
```

-----

### 3B. PCA (Principal Component Analysis)

#### 🧠 Phase 1: The Intuition

Imagine taking a 3D sculpture and photographing it from a perfect angle that captures the most detail in 2D. You’re reducing dimensions while preserving as much information as possible.

**PCA** does exactly this for data. If you have 100 features but many are correlated (e.g., “height” and “wingspan” both capture “size”), PCA finds new **artificial axes** (called **Principal Components**) that capture the maximum variation in fewer dimensions.

*Analogy:* You’re watching shadows of dancers on a wall. The wall is 2D, the dancers are 3D. If the spotlight is positioned perfectly, the 2D shadow captures almost all the meaningful motion. PCA is finding that perfect spotlight angle.

**Key Terms:**

- **Principal Component (PC)**: A new artificial feature — a linear combination of original features that captures maximum variance.
- **Variance**: How spread out the data is. More variance = more information. PCA maximises captured variance.
- **Explained Variance Ratio**: The % of total variance each PC captures. PC1 captures the most, PC2 the second most, etc.
- **Dimensionality Reduction**: Reducing the number of features while preserving maximum information.
- **Eigenvalue / Eigenvector**: Mathematical objects that define the direction (eigenvector) and magnitude (eigenvalue) of each Principal Component.
- **Loading**: How much each original feature contributes to a Principal Component.

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

**How PCA Works:**

1. **Standardise** the data (PCA is extremely sensitive to scale).
1. Compute the **covariance matrix** — captures how features vary together.
1. Find the **eigenvectors** of the covariance matrix — these are the Principal Component directions.
1. Sort eigenvectors by their **eigenvalues** (largest = most variance captured).
1. Project data onto the top K eigenvectors.

**When to use PCA:**

- **Curse of Dimensionality**: Many ML algorithms degrade with too many features. PCA compresses features.
- **Visualisation**: Reduce to 2–3 PCs for plotting.
- **Noise Reduction**: Low-variance components often encode noise. Dropping them can improve model generalisation.
- **Multicollinearity**: PCs are orthogonal (uncorrelated) by construction, solving correlated feature issues for linear models.

**Limitations:**

- PCA components are **not interpretable** (each PC is a blend of all original features).
- Loses information — the discarded variance is gone permanently.
- Linear only — for nonlinear structure, use Kernel PCA or UMAP.

**Why Scaling is MANDATORY:**
PCA maximises variance. Without scaling, a feature with large values (e.g., salary: $50,000) would dominate purely due to scale, not because it’s more informative.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: PCA (Principal Component Analysis)
# Dataset: Breast Cancer (30 features → 2 for visualisation)
# ============================================================

from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Load Dataset ---
cancer = load_breast_cancer()
X = cancer.data   # 30 features (many are correlated — PCA ideal here)
y = cancer.target # Labels (0=malignant, 1=benign) — used only for visualisation

print(f"Original shape: {X.shape}")  # (569, 30) — 569 samples, 30 features

# --- Step 1: Scale (MANDATORY — PCA is variance-maximising, scale-sensitive) ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Mean=0, Std=1 for each feature

# ============================================================
# Step 2: Full PCA — keep all 30 components to analyse variance
# ============================================================

pca_full = PCA()              # No n_components specified → compute all 30
pca_full.fit(X_scaled)        # Compute eigenvectors/values of the covariance matrix

# explained_variance_ratio_: proportion of total variance each PC captures
cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)  # Running total

print("\n=== Variance Explained by Each Principal Component ===")
for i, (var, cum) in enumerate(
    zip(pca_full.explained_variance_ratio_[:10], cumulative_variance[:10])
):
    bar = "█" * int(var * 200)
    print(f"  PC{i+1:2d}: {var:.4f} ({var*100:5.1f}%)  Cumulative: {cum*100:.1f}%  {bar}")

# Find how many PCs needed for 95% variance
n_95 = np.argmax(cumulative_variance >= 0.95) + 1  # +1 for 1-indexed count
print(f"\n→ {n_95} PCs needed to explain 95% of variance (out of 30 original features)")

# Plot explained variance
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].bar(range(1, 11), pca_full.explained_variance_ratio_[:10] * 100,
            color='steelblue', alpha=0.8)
axes[0].set_xlabel('Principal Component')
axes[0].set_ylabel('Explained Variance (%)')
axes[0].set_title('Variance per Principal Component')
axes[0].grid(True, alpha=0.3, axis='y')

axes[1].plot(range(1, 31), cumulative_variance * 100, 'bo-', linewidth=2)
axes[1].axhline(y=95, color='red', linestyle='--', label='95% threshold')
axes[1].axvline(x=n_95, color='orange', linestyle='--', label=f'{n_95} PCs needed')
axes[1].set_xlabel('Number of Principal Components')
axes[1].set_ylabel('Cumulative Explained Variance (%)')
axes[1].set_title('Scree Plot (Cumulative Variance)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('pca_variance.png', dpi=100)
plt.close()
print("Scree plot saved to 'pca_variance.png'")

# ============================================================
# Step 3: PCA with 2 Components — for 2D visualisation
# ============================================================

pca_2d = PCA(n_components=2)         # Reduce 30 features → 2 PCs
X_pca_2d = pca_2d.fit_transform(X_scaled)  # Project data onto top 2 PCs

print(f"\n=== 2D PCA Projection ===")
print(f"  Shape after PCA: {X_pca_2d.shape}")  # (569, 2)
print(f"  Variance explained by PC1: {pca_2d.explained_variance_ratio_[0]*100:.1f}%")
print(f"  Variance explained by PC2: {pca_2d.explained_variance_ratio_[1]*100:.1f}%")
print(f"  Total captured:            {sum(pca_2d.explained_variance_ratio_)*100:.1f}%")

# Visualise — if PCA worked, clusters should be visible without any labels used in training
fig, ax = plt.subplots(figsize=(8, 6))
colours = ['crimson', 'steelblue']
labels  = ['Malignant', 'Benign']
for class_idx, (colour, label) in enumerate(zip(colours, labels)):
    mask = y == class_idx  # Boolean mask for this class
    ax.scatter(
        X_pca_2d[mask, 0],   # PC1 coordinates for this class
        X_pca_2d[mask, 1],   # PC2 coordinates for this class
        c=colour, label=label, alpha=0.6, edgecolors='white', linewidths=0.5, s=50
    )
ax.set_xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}% variance)')
ax.set_ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}% variance)')
ax.set_title('PCA: Breast Cancer Data — 2D Projection')
ax.legend()
ax.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig('pca_2d_scatter.png', dpi=100)
plt.close()
print("2D scatter plot saved to 'pca_2d_scatter.png'")

# ============================================================
# Step 4: PCA for Dimensionality Reduction before ML
# ============================================================

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

results = {}
for n_comp in [2, 5, 10, 20, 30]:  # Test different levels of dimensionality reduction
    pca = PCA(n_components=n_comp)
    X_train_pca = pca.fit_transform(X_train)  # Fit PCA on training data only
    X_test_pca  = pca.transform(X_test)       # Apply to test data

    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train_pca, y_train)
    acc = accuracy_score(y_test, lr.predict(X_test_pca))
    var_explained = pca.explained_variance_ratio_.sum() * 100
    results[n_comp] = (acc, var_explained)
    print(f"  PCA({n_comp:2d} components): Acc={acc:.4f}  Variance kept={var_explained:.1f}%")

print("\n→ Notice how accuracy peaks before needing all 30 features!")
```

-----

## 📊 Model Evaluation

> Knowing *how* to measure model quality is as important as building the model itself.

-----

### 4A. Accuracy, Precision, Recall, F1

#### 🧠 Phase 1: The Intuition

Imagine a doctor screening patients for a rare, serious disease. The disease affects 1% of patients.

- A model that predicts “Healthy” for **everyone** would be **99% accurate** — but completely useless!

This shows why **accuracy alone is misleading** for imbalanced classes. We need more nuanced metrics.

Think of it like a **fishing net**:

- **Precision**: Of all the fish you caught in the net — what fraction are actually the fish you wanted? (No bycatch)
  - *“When my model says YES, how often is it right?”*
- **Recall (Sensitivity)**: Of all the fish you wanted in the ocean — what fraction did your net actually catch?
  - *“Of all the actual YES cases, how many did I catch?”*
- **F1 Score**: The harmonic mean of Precision and Recall — a single balanced metric. Use when you care about both equally.
- **Accuracy**: Of all predictions — what fraction were correct? Only reliable when classes are balanced.

**The Precision-Recall Trade-off:** Lowering the decision threshold catches more positives (higher recall) but introduces more false positives (lower precision). You cannot maximise both simultaneously without a better model.

**Key Terms (The Confusion Matrix):**

- **True Positive (TP)**: Model predicted Positive, and it actually is. ✅
- **True Negative (TN)**: Model predicted Negative, and it actually is. ✅
- **False Positive (FP)**: Model predicted Positive, but it’s actually Negative. ❌ (*Type I Error*)
- **False Negative (FN)**: Model predicted Negative, but it’s actually Positive. ❌ (*Type II Error*)

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

**Formulas:**

```
Accuracy  = (TP + TN) / (TP + TN + FP + FN)

Precision = TP / (TP + FP)    ← "Of what I flagged, how much was correct?"

Recall    = TP / (TP + FN)    ← "Of all real positives, how many did I find?"

F1 Score  = 2 · (Precision × Recall) / (Precision + Recall)
```

**When to use which metric:**

|Scenario        |Priority Metric|Reason                                    |
|----------------|---------------|------------------------------------------|
|Cancer detection|Recall         |Missing a cancer (FN) is catastrophic     |
|Spam filtering  |Precision      |Blocking real emails (FP) is annoying     |
|Fraud detection |F1 or ROC-AUC  |Balance both — fraud is rare but important|
|Balanced classes|Accuracy       |Fair and simple                           |

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: Accuracy, Precision, Recall, F1, Confusion Matrix
# Dataset: Breast Cancer (binary classification)
# ============================================================

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,          # Overall fraction correct
    precision_score,         # TP / (TP + FP)
    recall_score,            # TP / (TP + FN)
    f1_score,                # Harmonic mean of precision and recall
    confusion_matrix,        # 2x2 matrix of TP/TN/FP/FN
    classification_report    # All metrics for each class in one table
)
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns  # For a beautiful confusion matrix heatmap

# --- Prepare Data ---
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target  # 0=malignant, 1=benign

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# Train model
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_s, y_train)

# Hard predictions (0 or 1 using default threshold of 0.5)
y_pred = model.predict(X_test_s)

# Soft predictions (probability of class 1 = benign)
y_prob = model.predict_proba(X_test_s)[:, 1]

# ============================================================
# Compute Individual Metrics
# pos_label=0: we define 'malignant' (class 0) as our "Positive" class
# because in medical context, detecting malignant is the critical case
# ============================================================

accuracy  = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label=0)  # pos_label=0: malignant is positive
recall    = recall_score(y_test, y_pred, pos_label=0)     # How many malignant did we catch?
f1        = f1_score(y_test, y_pred, pos_label=0)

print("=== Model Evaluation Metrics ===")
print(f"  Accuracy:  {accuracy:.4f}  → {accuracy*100:.1f}% of all predictions are correct")
print(f"  Precision: {precision:.4f}  → When we flag malignant, {precision*100:.1f}% are actually malignant")
print(f"  Recall:    {recall:.4f}  → We catch {recall*100:.1f}% of all actual malignant cases")
print(f"  F1 Score:  {f1:.4f}  → Balanced precision-recall score")

# Full report for all classes
print(f"\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=['Malignant', 'Benign']))

# ============================================================
# Confusion Matrix — the full picture
# ============================================================

cm = confusion_matrix(y_test, y_pred)  # Returns [[TN FP], [FN TP]] for binary case
print("=== Confusion Matrix ===")
print(f"  True Negatives  (TN): {cm[1,1]}  — Benign correctly identified")
print(f"  True Positives  (TP): {cm[0,0]}  — Malignant correctly identified")
print(f"  False Positives (FP): {cm[1,0]}  — Benign incorrectly flagged as Malignant (Type I Error)")
print(f"  False Negatives (FN): {cm[0,1]}  — Malignant missed (Type II Error — the dangerous one!)")

# Visualise confusion matrix as heatmap
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,       # Show numbers in each cell
    fmt='d',          # Display as integers
    cmap='Blues',     # Blue colour scheme
    xticklabels=['Malignant', 'Benign'],   # Predicted class labels
    yticklabels=['Malignant', 'Benign'],   # Actual class labels
    ax=ax
)
ax.set_xlabel('Predicted Label', fontsize=12)
ax.set_ylabel('True Label', fontsize=12)
ax.set_title('Confusion Matrix — Logistic Regression\n(Breast Cancer Classification)', fontsize=12)
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=100)
plt.close()
print("\nConfusion matrix saved to 'confusion_matrix.png'")

# ============================================================
# Effect of Threshold on Precision-Recall Trade-off
# ============================================================
print("\n=== Precision-Recall Trade-off at Different Thresholds ===")
print(f"{'Threshold':>10}  {'Precision':>10}  {'Recall':>8}  {'F1':>8}")

# y_prob is P(benign); for malignant detection, a lower threshold means more aggressive detection
for threshold in [0.3, 0.4, 0.5, 0.6, 0.7]:
    # Apply custom threshold: classify as benign (1) only if P(benign) >= threshold
    y_custom = (y_prob >= threshold).astype(int)  # 1 if benign probability exceeds threshold
    p = precision_score(y_test, y_custom, pos_label=0, zero_division=0)
    r = recall_score(y_test, y_custom, pos_label=0)
    f = f1_score(y_test, y_custom, pos_label=0, zero_division=0)
    print(f"  {threshold:>9.1f}  {p:>10.4f}  {r:>8.4f}  {f:>8.4f}")
```

-----

### 4B. ROC-AUC & Confusion Matrix

#### 🧠 Phase 1: The Intuition

The **ROC Curve** (Receiver Operating Characteristic) visualises model performance across **all possible thresholds** at once. Instead of asking “how good is my model at threshold 0.5?”, we ask “how good is my model at every possible threshold simultaneously?”

*Analogy:* Imagine you’re adjusting a metal detector’s sensitivity at an airport. Too sensitive (low threshold) → it flags every innocent traveller (many false positives, high recall). Too lenient (high threshold) → it misses real threats (high false negatives, low recall). The ROC curve shows the entire sensitivity-specificity trade-off spectrum.

**The AUC (Area Under the Curve)** summarises the entire ROC curve in one number:

- **AUC = 1.0**: Perfect model — always distinguishes classes correctly.
- **AUC = 0.5**: Random guessing — the model has no discriminative power.
- **AUC = 0.8+**: Generally considered a good model.

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

**ROC Curve axes:**

- **X-axis**: False Positive Rate (FPR) = FP / (FP + TN) — fraction of negatives incorrectly flagged.
- **Y-axis**: True Positive Rate (TPR) = TP / (TP + FN) — same as Recall.

A random model’s ROC is the diagonal line (AUC=0.5). Any model above this line does better than chance.

**Why AUC is preferred over accuracy for imbalanced data:**

- AUC measures the model’s ability to *rank* positives above negatives, regardless of class balance.
- It is threshold-independent — evaluates the model’s discriminative ability across all operating points.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: ROC Curve & AUC
# Builds on the previous logistic regression model
# ============================================================

from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, auc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Reuse y_test and y_prob from the previous code section
# y_prob = model.predict_proba(X_test_s)[:, 1]  — P(benign)

# ============================================================
# ROC Curve
# roc_curve returns three arrays:
#   fpr: False Positive Rate at each threshold
#   tpr: True Positive Rate (Recall) at each threshold
#   thresholds: The probability thresholds used
# ============================================================

fpr, tpr, thresholds_roc = roc_curve(
    y_test,   # True binary labels
    y_prob,   # Predicted probabilities for the positive class (benign=1)
    pos_label=1  # Define which class is "positive" for this curve
)

auc_score = roc_auc_score(y_test, y_prob)  # Single number summary of the ROC curve

print(f"ROC-AUC Score: {auc_score:.4f}")
print(f"Interpretation: The model correctly ranks a random benign case")
print(f"above a random malignant case {auc_score*100:.1f}% of the time.")

# ============================================================
# Precision-Recall Curve (better for highly imbalanced datasets)
# Shows precision and recall across all thresholds
# ============================================================

precision_curve, recall_curve, thresholds_pr = precision_recall_curve(
    y_test,
    1 - y_prob,    # Probabilities for malignant (class 0) = 1 - P(benign)
    pos_label=0    # Define malignant as the positive class
)

pr_auc = auc(recall_curve, precision_curve)  # Area under Precision-Recall curve

# ============================================================
# Plot both curves
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# --- ROC Curve ---
axes[0].plot(fpr, tpr, color='steelblue', linewidth=2.5,
             label=f'ROC Curve (AUC = {auc_score:.3f})')
axes[0].plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier (AUC = 0.5)')  # Diagonal
axes[0].fill_between(fpr, tpr, alpha=0.1, color='steelblue')  # Shade under curve
axes[0].set_xlabel('False Positive Rate (FPR)')
axes[0].set_ylabel('True Positive Rate / Recall (TPR)')
axes[0].set_title('ROC Curve')
axes[0].legend(loc='lower right')
axes[0].grid(True, alpha=0.3)

# --- Precision-Recall Curve ---
axes[1].plot(recall_curve, precision_curve, color='coral', linewidth=2.5,
             label=f'PR Curve (AUC = {pr_auc:.3f})')
axes[1].axhline(y=sum(y_test==0)/len(y_test), color='k', linestyle='--', linewidth=1,
                label=f'Baseline (class prevalence = {sum(y_test==0)/len(y_test):.2f})')
axes[1].set_xlabel('Recall')
axes[1].set_ylabel('Precision')
axes[1].set_title('Precision-Recall Curve')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('ROC-AUC and Precision-Recall Analysis', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('roc_pr_curves.png', dpi=100)
plt.close()
print("ROC and PR curves saved to 'roc_pr_curves.png'")

# ============================================================
# Find optimal threshold (maximise F1 score)
# ============================================================
print("\n=== Finding Optimal Decision Threshold ===")
best_threshold = 0.5
best_f1 = 0

for thresh in np.arange(0.1, 0.9, 0.05):
    y_thresh_pred = (y_prob >= thresh).astype(int)
    f = f1_score(y_test, y_thresh_pred, pos_label=0, zero_division=0)
    if f > best_f1:
        best_f1 = f
        best_threshold = thresh

print(f"Optimal threshold for malignant detection: {best_threshold:.2f}")
print(f"Best F1 at this threshold: {best_f1:.4f}")
print("(In medical contexts, we'd lower this threshold to prioritise recall — catching all cancers)")
```

-----

### 4C. K-Fold Cross-Validation

#### 🧠 Phase 1: The Intuition

Imagine you want to evaluate a chef’s skill, but you only have 10 dishes for them to cook. If you ask them to cook 8 and you taste 2, your judgment depends heavily on which 2 you chose — maybe both were the hardest or easiest dishes.

**K-Fold Cross-Validation** is fairer: divide the 10 dishes into 5 pairs. Have the chef cook 8 dishes (4 pairs) and taste 2 (1 pair). Record the score. Then rotate — a different pair becomes the test. Repeat 5 times until every dish has been tasted exactly once. Average all 5 scores.

This way, **every data point** contributes to both training and validation, giving a much more reliable performance estimate.

**Key Terms:**

- **Fold**: One of K equally-sized subsets of the data.
- **K**: Number of folds (typically 5 or 10). Each fold takes a turn as the validation set.
- **Cross-Validation Score**: The average performance across all K folds.
- **Standard Deviation of CV Scores**: Tells you how *stable* the model is across different data subsets. High std = high variance.

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

**Why not just use a single train/test split?**

A single split can be misleadingly optimistic or pessimistic depending on random chance. Cross-validation provides:

1. A more **statistically reliable** performance estimate.
1. Information about **variance** — if scores vary wildly across folds, the model is unstable.
1. **Efficient use of data** — especially valuable with small datasets.

**Variants:**

- **Stratified K-Fold**: Preserves class balance in each fold (recommended for classification).
- **Leave-One-Out (LOO)**: K = N (each sample is its own test fold). Very expensive but unbiased.
- **Time-Series Split**: For temporal data — only past data can train, never future.

**Important:** When using Pipelines with cross-validation, the entire pipeline (including scaling/encoding) is re-fitted in each fold. This is the correct way to avoid data leakage.

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: K-Fold Cross-Validation
# Dataset: Iris (multi-class classification)
# ============================================================

from sklearn.datasets import load_iris
from sklearn.model_selection import (
    cross_val_score,        # Convenience function for K-Fold CV
    StratifiedKFold,        # Class-balanced K-Fold splitter
    cross_validate          # Extended version: returns multiple metrics and timing
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# --- Load Dataset ---
iris = load_iris()
X = iris.data
y = iris.target

# ============================================================
# METHOD 1: Simple cross_val_score
# Automatically performs K-Fold CV and returns scores
# ============================================================

# Build pipeline (ensures scaling is re-fitted inside each fold — no leakage)
pipeline = Pipeline([
    ('scaler', StandardScaler()),            # Step 1: Scale features
    ('model',  LogisticRegression(max_iter=1000, random_state=42))  # Step 2: Classify
])

# cv=5: 5-Fold Cross-Validation
# scoring='accuracy': Use accuracy as the evaluation metric
# Note: cv can also accept a StratifiedKFold object for more control
cv_scores = cross_val_score(
    pipeline,           # The model/pipeline to evaluate
    X, y,              # Full dataset (not pre-split — CV handles this internally)
    cv=5,              # Number of folds
    scoring='accuracy' # Metric to compute in each fold
)

print("=== 5-Fold Cross-Validation (Logistic Regression) ===")
print(f"  Scores per fold: {cv_scores.round(4)}")
print(f"  Mean accuracy:   {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print(f"  Interpretation: Model achieves {cv_scores.mean()*100:.1f}% accuracy on average,")
print(f"  with ±{cv_scores.std()*100:.1f}% variation — {'stable' if cv_scores.std() < 0.02 else 'unstable'}")

# ============================================================
# METHOD 2: Stratified K-Fold (explicitly specified — best practice)
# Ensures each fold has the same class proportions as the full dataset
# ============================================================

skf = StratifiedKFold(
    n_splits=10,     # 10 folds — more reliable estimate (more data seen in each test)
    shuffle=True,    # Shuffle data before splitting — reduces ordering bias
    random_state=42  # Reproducibility
)

# Multiple scoring metrics at once
cv_results = cross_validate(
    pipeline,
    X, y,
    cv=skf,                  # Use our stratified splitter
    scoring=['accuracy', 'f1_macro', 'precision_macro', 'recall_macro'],  # Multiple metrics
    return_train_score=True  # Also return training scores (useful for bias-variance analysis)
)

print("\n=== 10-Fold Stratified CV (Multiple Metrics) ===")
for metric in ['accuracy', 'f1_macro', 'precision_macro', 'recall_macro']:
    test_scores  = cv_results[f'test_{metric}']
    train_scores = cv_results[f'train_{metric}']
    print(f"  {metric:18s}: Test={test_scores.mean():.4f}±{test_scores.std():.4f}  "
          f"Train={train_scores.mean():.4f}  Gap={train_scores.mean()-test_scores.mean():.4f}")
# If Train >> Test: large gap → overfitting. If both low → underfitting.

# ============================================================
# METHOD 3: Compare models using CV — the right way to model selection
# ============================================================

models = {
    'Logistic Regression': Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(max_iter=1000, random_state=42))
    ]),
    'Random Forest': Pipeline([
        # Random Forest doesn't need scaling, but it's fine to include (no harm)
        ('scaler', StandardScaler()),
        ('model', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
}

print("\n=== Model Comparison via 10-Fold Stratified CV ===")
print(f"{'Model':25s}  {'Mean Acc':>10}  {'Std':>8}  {'95% CI':>20}")

for name, pipe in models.items():
    scores = cross_val_score(pipe, X, y, cv=skf, scoring='accuracy')
    # 95% Confidence Interval: mean ± 2 standard deviations
    ci_low  = scores.mean() - 2 * scores.std()
    ci_high = scores.mean() + 2 * scores.std()
    print(f"  {name:23s}  {scores.mean():>10.4f}  {scores.std():>8.4f}  "
          f"[{ci_low:.4f}, {ci_high:.4f}]")

print("\nConclusion: Use CV mean ± std for fair model comparison. Avoid comparing single test-set scores.")
```

-----

## ⚖️ Core Theory: Bias-Variance Trade-off

-----

#### 🧠 Phase 1: The Intuition

Consider two archery students:

- **Student A (High Bias)**: Always shoots far left of centre — their arrows cluster tightly, but in the wrong place. This is **underfitting**: the model is too simple to capture the true pattern.
- **Student B (High Variance)**: Shoots all over the target — sometimes near centre, sometimes at the edge. Their mean aim is correct but the spread is huge. This is **overfitting**: the model is too sensitive to the specific training data and fails on new data.
- **The Goal**: Tight clustering *at* the centre — **low bias AND low variance**.

**Overfitting** happens when a model is too complex: it memorises the training data (including its noise and quirks) and fails to generalise.

**Underfitting** happens when a model is too simple: it doesn’t have enough capacity to capture the true patterns in the data.

**Key Terms:**

- **Bias**: Error from wrong assumptions. High-bias models are too simple, miss real patterns. (Underfitting)
- **Variance**: Error from sensitivity to fluctuations in training data. High-variance models are too complex, memorise noise. (Overfitting)
- **Noise**: Random, irreducible error that cannot be modelled (inherent randomness in data).
- **Generalisation**: How well a model performs on *new, unseen* data.
- **Regularisation**: Techniques to constrain model complexity, reducing variance (e.g., L1/L2 penalty, dropout, tree depth limits).

#### ⚙️ Phase 2: The Technical ‘Why’ & Logic

The **Total Expected Error** of any model can be mathematically decomposed as:

```
Total Error = Bias² + Variance + Irreducible Noise
```

- **Bias²**: How far off the average prediction is from the truth. A straight line fit to a quadratic curve — systematically wrong.
- **Variance**: How much predictions change when you train on different samples of data.
- **Irreducible Noise**: The floor — inherent randomness that no model can eliminate.

**The Trade-off:**

|Model Complexity     |Bias    |Variance|Training Error|Test Error|
|---------------------|--------|--------|--------------|----------|
|Too Simple (underfit)|High ⬆️  |Low ⬇️   |High          |High      |
|Just Right           |Balanced|Balanced|Medium-Low    |Lowest    |
|Too Complex (overfit)|Low ⬇️   |High ⬆️  |Very Low      |High      |

**Algorithm-Specific Summary:**

|Algorithm           |Bias|Variance|Typical Issue                       |
|--------------------|----|--------|------------------------------------|
|Linear Regression   |High|Low     |Underfitting on nonlinear data      |
|Logistic Regression |High|Low     |Underfitting on nonlinear boundaries|
|Decision Tree (deep)|Low |High    |Overfitting                         |
|Random Forest       |Low |Low     |Balanced (ensemble reduces variance)|
|Gradient Boosting   |Low |Medium  |Can overfit without tuning          |
|K-Means (large K)   |Low |High    |Overfitting noise clusters          |

**How to Fix Each Problem:**

|Problem                    |Symptoms                           |Solutions                                                           |
|---------------------------|-----------------------------------|--------------------------------------------------------------------|
|Underfitting (High Bias)   |High training AND test error       |Add features, increase model complexity, reduce regularisation      |
|Overfitting (High Variance)|Low training error, high test error|More data, regularisation, reduce model complexity, cross-validation|

#### 💻 Phase 3: Hands-On Code

```python
# ============================================================
# TOPIC: Bias-Variance Trade-off
# Visualised through Decision Tree depth vs. performance
# Dataset: Iris
# ============================================================

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, train_test_split
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Load Dataset ---
iris = load_iris()
X = iris.data
y = iris.target

# --- Single Train/Test Split for learning curves ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# ============================================================
# Experiment: Vary Decision Tree depth from 1 to 20
# At each depth, record TRAINING and TEST accuracy
# This directly demonstrates the bias-variance trade-off
# ============================================================

depths = range(1, 21)   # Tree depths from 1 (stump) to 20 (very deep)
train_scores = []       # Training accuracy at each depth
test_scores  = []       # Test accuracy at each depth
cv_scores    = []       # Cross-validation accuracy (more reliable estimate)
cv_stds      = []       # CV standard deviation (proxy for model variance)

for depth in depths:
    # Instantiate tree with current depth
    dt = DecisionTreeClassifier(max_depth=depth, random_state=42)

    # --- Train accuracy ---
    dt.fit(X_train, y_train)
    train_scores.append(dt.score(X_train, y_train))  # Score on data it was trained on
    test_scores.append(dt.score(X_test, y_test))     # Score on unseen data

    # --- Cross-Validation (5-fold) ---
    cv = cross_val_score(dt, X, y, cv=5, scoring='accuracy')
    cv_scores.append(cv.mean())   # Average CV accuracy
    cv_stds.append(cv.std())      # Spread of CV scores (high std = high variance model)

# ============================================================
# Plot the Bias-Variance Trade-off curves
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# --- Plot 1: Train vs Test Score ---
axes[0].plot(depths, train_scores, 'b-o', linewidth=2, markersize=6,
             label='Training Accuracy')   # Usually increases with depth
axes[0].plot(depths, test_scores,  'r-o', linewidth=2, markersize=6,
             label='Test Accuracy')       # Peaks then may decline
axes[0].axvline(x=np.argmax(test_scores)+1, color='green', linestyle='--', linewidth=2,
                label=f'Optimal depth = {np.argmax(test_scores)+1}')
axes[0].set_xlabel('Decision Tree Depth (Model Complexity →)')
axes[0].set_ylabel('Accuracy')
axes[0].set_title('Bias-Variance Trade-off\n(Training vs Test Accuracy)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Annotate regions
axes[0].annotate('← HIGH BIAS\n(Underfitting)',
                 xy=(1, train_scores[0]), xytext=(2, train_scores[0]-0.08),
                 fontsize=9, color='blue',
                 arrowprops=dict(arrowstyle='->', color='blue'))
axes[0].annotate('HIGH VARIANCE →\n(Overfitting)',
                 xy=(15, train_scores[14]), xytext=(12, train_scores[14]-0.12),
                 fontsize=9, color='red',
                 arrowprops=dict(arrowstyle='->', color='red'))

# --- Plot 2: CV Score and its Variance (std) ---
axes[1].plot(depths, cv_scores, 'g-o', linewidth=2, markersize=6,
             label='CV Mean Accuracy')
axes[1].fill_between(
    depths,
    np.array(cv_scores) - np.array(cv_stds),   # Lower bound: mean - std
    np.array(cv_scores) + np.array(cv_stds),   # Upper bound: mean + std
    alpha=0.2, color='green',                  # Shaded band = model uncertainty
    label='±1 Std Dev (Model Variance)'
)
axes[1].set_xlabel('Decision Tree Depth (Model Complexity →)')
axes[1].set_ylabel('Cross-Validation Accuracy')
axes[1].set_title('CV Accuracy with Variance Band\n(Width = Model Variance)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('The Bias-Variance Trade-off', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('bias_variance_tradeoff.png', dpi=100)
plt.close()
print("Bias-variance plot saved to 'bias_variance_tradeoff.png'")

# ============================================================
# Print the key insight numerically
# ============================================================

print("\n=== Numerical Bias-Variance Analysis ===")
print(f"{'Depth':>6}  {'Train':>8}  {'Test':>8}  {'CV Mean':>9}  {'CV Std':>8}  {'Diagnosis':>20}")
print("-" * 70)

for i, depth in enumerate(depths):
    gap = train_scores[i] - test_scores[i]  # High gap = overfitting signal
    if depth <= 2:
        diagnosis = "UNDERFITTING"
    elif gap > 0.05:
        diagnosis = "OVERFITTING"
    else:
        diagnosis = "WELL BALANCED"

    print(f"  {depth:>4}  {train_scores[i]:>8.4f}  {test_scores[i]:>8.4f}"
          f"  {cv_scores[i]:>9.4f}  {cv_stds[i]:>8.4f}  {diagnosis:>20}")

optimal_depth = np.argmax(cv_scores) + 1
print(f"\n→ Optimal depth by CV: {optimal_depth}")
print(f"→ At depth {optimal_depth}: Train={train_scores[optimal_depth-1]:.4f}, "
      f"Test={test_scores[optimal_depth-1]:.4f}, "
      f"Gap={train_scores[optimal_depth-1]-test_scores[optimal_depth-1]:.4f}")
print("\nKey Insight: The optimal model sits at the 'sweet spot' where")
print("complexity is sufficient to capture patterns (low bias) but not")
print("so high that it memorises noise (low variance).")

# ============================================================
# Regularisation Demo: L2 (Ridge) Regularisation on Logistic Regression
# Shows how regularisation controls the bias-variance trade-off
# ============================================================

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

print("\n=== Regularisation: Effect of C on Logistic Regression ===")
print("(C = inverse regularisation strength: smaller C = stronger regularisation)")
print(f"{'C':>12}  {'Train':>8}  {'Test':>8}  {'CV Mean':>9}  {'Bias-Variance Regime':>25}")
print("-" * 75)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

C_values = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]

for C in C_values:
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(C=C, max_iter=5000, random_state=42))
    ])
    pipe.fit(X_train, y_train)
    tr = pipe.score(X_train, y_train)
    te = pipe.score(X_test,  y_test)
    cv = cross_val_score(pipe, X, y, cv=5).mean()

    if C <= 0.01:
        regime = "HIGH REGULARISATION → High Bias"
    elif C >= 100:
        regime = "LOW REGULARISATION → High Variance"
    else:
        regime = "Balanced"

    print(f"  C={C:>10}  {tr:>8.4f}  {te:>8.4f}  {cv:>9.4f}  {regime:>25}")

print("\nObservation: Very small C (strong regularisation) → underfitting.")
print("Very large C (weak regularisation) → potential overfitting on noisy data.")
```

-----

## 📚 Quick Reference Summary

|Algorithm          |Type                       |Scaling?|Interpretable?|Best For                               |
|-------------------|---------------------------|--------|--------------|---------------------------------------|
|Linear Regression  |Supervised (Regression)    |✅ Yes   |✅ Yes         |Continuous output, linear relationships|
|Logistic Regression|Supervised (Classification)|✅ Yes   |✅ Yes         |Binary/multi-class, probability outputs|
|Decision Tree      |Supervised (Both)          |❌ No    |✅ Yes         |Explainable decisions, quick baseline  |
|Random Forest      |Supervised (Both)          |❌ No    |Partial       |Robust general-purpose model           |
|Gradient Boosting  |Supervised (Both)          |❌ No    |Partial       |State-of-the-art tabular performance   |
|K-Means            |Unsupervised               |✅ Yes   |✅ Yes         |Customer segmentation, grouping        |
|PCA                |Unsupervised               |✅ Yes   |❌ No          |Dimensionality reduction, visualisation|

-----

## 🔬 Key ML Workflow Checklist

```
✅ Understand the problem (regression vs. classification? balanced or imbalanced?)
✅ Explore the data (EDA — distributions, correlations, missing values)
✅ Split data FIRST (train/val/test) before any preprocessing
✅ Handle missing values (imputation)
✅ Encode categorical variables (One-Hot for nominal, Ordinal for ordinal)
✅ Scale features (StandardScaler for most models, not needed for trees)
✅ Wrap everything in a Pipeline to prevent data leakage
✅ Train multiple models
✅ Evaluate using cross-validation (not just single test score)
✅ Select the right metric (not always accuracy!)
✅ Diagnose overfitting/underfitting (bias-variance)
✅ Tune hyperparameters (GridSearchCV / RandomizedSearchCV)
✅ Final evaluation on the test set — exactly once
```

-----

## 📖 Recommended Next Steps

|Topic              |What to Learn Next                                       |
|-------------------|---------------------------------------------------------|
|After Linear Models|Ridge, Lasso, ElasticNet Regularisation                  |
|After Tree Models  |XGBoost, LightGBM (production gradient boosting)         |
|After Evaluation   |GridSearchCV & RandomizedSearchCV (hyperparameter tuning)|
|After Unsupervised |DBSCAN, Hierarchical Clustering, t-SNE, UMAP             |
|After Classical ML |Neural Networks → Deep Learning (PyTorch / TensorFlow)   |
|General Practice   |Kaggle competitions, real-world datasets                 |

-----

> **💡 Remember:** Machine Learning is empirical. There is no single “best” algorithm. Always experiment, validate rigorously, and let the data guide your decisions.

-----

*Document created for foundational ML education. All code examples use Python 3.8+ and scikit-learn 1.x.*
