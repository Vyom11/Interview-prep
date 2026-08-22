# Foundations of Data Preparation
## A Complete Guide to EDA, Preprocessing & Feature Engineering

> **Who this guide is for:** Beginners who know NumPy and Pandas basics but are new to the full data preparation workflow.
> **Dataset used throughout:** A simulated housing prices dataset — the same data is used in every single section so you can see how each step connects to the next.

---

## Table of Contents

1. [The Big Picture: End-to-End ML Workflow](#1-the-big-picture)
2. [Our Dataset](#2-our-dataset)
3. [Exploratory Data Analysis (EDA)](#3-exploratory-data-analysis)
4. [Data Preprocessing](#4-data-preprocessing)
5. [Feature Engineering](#5-feature-engineering)
6. [Scikit-Learn Pipelines](#6-scikit-learn-pipelines)
7. [Quick Reference Cheat Sheet](#7-quick-reference-cheat-sheet)

---

## 1. The Big Picture

### 1.1 What Does the Full ML Workflow Look Like?

Before writing a single line of code, it helps to understand the journey. Think of building an ML model like preparing a dish in a restaurant kitchen:

- **Raw ingredients arrive** → this is your raw data
- **The chef inspects them** → this is EDA
- **Bad ingredients are removed, others are washed and chopped** → this is Preprocessing
- **Ingredients are combined cleverly** → this is Feature Engineering
- **The dish is cooked** → this is Model Training
- **A taster judges it** → this is Model Evaluation

Here is the full pipeline laid out as steps:

```
Raw Data
   ↓
[ EDA ] ← Understand what you have. Find problems.
   ↓
[ Preprocessing ] ← Fix problems. Clean and transform data.
   ↓
[ Feature Engineering ] ← Create better inputs for the model.
   ↓
[ Model Training ] ← Teach the model on your prepared data.
   ↓
[ Evaluation ] ← Test how well the model performs.
   ↓
[ Deployment ] ← Use the model in the real world.
```

This guide covers the first three stages deeply.

---

### 1.2 The Role of Each Tool

| Tool | What it is | What it does in this workflow |
|---|---|---|
| **NumPy** | Numerical computing library | Handles arrays and mathematical operations under the hood |
| **Pandas** | Data manipulation library | Lets you load, inspect, filter, and transform tabular data |
| **scikit-learn** | Machine learning library | Provides preprocessing tools (scalers, encoders) and ML models |
| **Matplotlib / Seaborn** | Visualization libraries | Used during EDA to plot charts and find patterns |

---

### 1.3 How EDA, Preprocessing, and Feature Engineering Connect

This is the most important conceptual relationship to understand:

```
EDA reveals problems and patterns
       ↓
Preprocessing fixes those problems
       ↓
Feature Engineering builds on clean data to create smarter inputs
```

**Concrete example using our housing dataset:**

- **EDA** tells you: "The `age` column has some extreme outlier values, and `neighbourhood` is a text column."
- **Preprocessing** fixes it: Remove or cap the outliers. Convert the text neighbourhood into numbers a model can read.
- **Feature Engineering** improves it: Create a new column called `price_per_sqft` by dividing `price` by `area` — this gives the model a more meaningful signal.

Each step depends on the one before it. You cannot preprocess wisely without doing EDA first. You cannot engineer features on dirty data. The order matters.

---

## 2. Our Dataset

We will simulate a realistic housing prices dataset and use it for every single example in this guide.

### What the Dataset Represents

Imagine a real estate company collected data on 1,000 houses. Each row is one house. The columns are:

| Column | Type | Description |
|---|---|---|
| `price` | Numeric (float) | Sale price of the house (target variable) |
| `area_sqft` | Numeric (int) | Total floor area in square feet |
| `num_bedrooms` | Numeric (int) | Number of bedrooms |
| `num_bathrooms` | Numeric (float) | Number of bathrooms |
| `house_age` | Numeric (int) | Age of the house in years |
| `neighbourhood` | Categorical (text) | Area: 'Urban', 'Suburban', or 'Rural' |
| `condition` | Categorical (text) | House condition: 'Poor', 'Fair', 'Good', 'Excellent' |
| `has_garage` | Categorical (text) | Whether house has a garage: 'Yes' or 'No' |
| `sale_date` | DateTime | Date the house was sold |

### Creating the Dataset

```python
# ─────────────────────────────────────────────────────────────────────────────
# SETUP: Import all libraries we will use throughout this guide
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np               # For numerical operations
import pandas as pd              # For data manipulation
import matplotlib.pyplot as plt  # For basic plots
import seaborn as sns            # For prettier statistical plots
from sklearn.preprocessing import (
    StandardScaler,              # Scales features to mean=0, std=1
    MinMaxScaler,                # Scales features to [0, 1] range
    OneHotEncoder,               # Converts nominal categories to binary columns
    OrdinalEncoder               # Converts ordered categories to integers
)
from sklearn.impute import SimpleImputer         # Fills in missing values
from sklearn.pipeline import Pipeline           # Chains steps together
from sklearn.compose import ColumnTransformer   # Applies different steps to different columns

# Set a random seed so the simulated data is the same every time you run this
np.random.seed(42)

# Number of houses in our dataset
n = 1000

# ─────────────────────────────────────────────────────────────────────────────
# CREATE EACH COLUMN INDIVIDUALLY
# ─────────────────────────────────────────────────────────────────────────────

# Area in square feet: randomly drawn from normal distribution
# Most houses between ~800 and ~3200 sqft (mean=2000, std=500)
area_sqft = np.random.normal(loc=2000, scale=500, size=n).astype(int)
area_sqft = np.clip(area_sqft, 500, 5000)  # No house smaller than 500 or larger than 5000 sqft

# Number of bedrooms: integer between 1 and 6
num_bedrooms = np.random.randint(1, 7, size=n)

# Number of bathrooms: 1.0, 1.5, 2.0, 2.5, 3.0
num_bathrooms = np.random.choice([1.0, 1.5, 2.0, 2.5, 3.0], size=n)

# House age in years: between 0 (brand new) and 80 (old house)
house_age = np.random.randint(0, 81, size=n)

# Neighbourhood: choose randomly from 3 types
neighbourhood = np.random.choice(['Urban', 'Suburban', 'Rural'], size=n, p=[0.4, 0.4, 0.2])

# Condition: ordered from Poor to Excellent
condition = np.random.choice(['Poor', 'Fair', 'Good', 'Excellent'], size=n, p=[0.1, 0.2, 0.5, 0.2])

# Garage: Yes or No
has_garage = np.random.choice(['Yes', 'No'], size=n, p=[0.65, 0.35])

# Price: built using a realistic formula
# Larger area → higher price
# More bedrooms → higher price
# Older house → lower price
# Urban → premium, Rural → discount
neighbourhood_map = {'Urban': 50000, 'Suburban': 20000, 'Rural': -10000}
neighbourhood_bonus = np.array([neighbourhood_map[n_] for n_ in neighbourhood])

price = (
    area_sqft * 150           # Base: $150 per sqft
    + num_bedrooms * 8000      # Each bedroom adds $8,000
    + num_bathrooms * 5000     # Each bathroom adds $5,000
    - house_age * 500          # Each year of age reduces price by $500
    + neighbourhood_bonus      # Location premium/discount
    + np.random.normal(0, 20000, size=n)  # Random noise (real world isn't perfect)
).round(-3)                    # Round to nearest thousand

# Sale dates: spread over 2 years
sale_date = pd.date_range(start='2022-01-01', periods=n, freq='17H')

# ─────────────────────────────────────────────────────────────────────────────
# INTRODUCE REALISTIC PROBLEMS (so we have something to fix during preprocessing)
# ─────────────────────────────────────────────────────────────────────────────

# 1. Add missing values (~8% of some columns will be missing)
missing_indices_area = np.random.choice(n, size=int(n * 0.08), replace=False)
area_sqft = area_sqft.astype(float)  # Convert to float to allow NaN
area_sqft[missing_indices_area] = np.nan  # NaN = "Not a Number" = missing value

missing_indices_bath = np.random.choice(n, size=int(n * 0.05), replace=False)
num_bathrooms = num_bathrooms.astype(float)
num_bathrooms[missing_indices_bath] = np.nan

missing_indices_cond = np.random.choice(n, size=int(n * 0.06), replace=False)
condition = list(condition)
for i in missing_indices_cond:
    condition[i] = np.nan  # Make some condition values missing

# 2. Add a few extreme outliers in price (data entry errors, unusual houses)
outlier_indices = np.random.choice(n, size=5, replace=False)
price[outlier_indices] = price[outlier_indices] * 10  # These prices are 10x too high

# 3. Add a few duplicate rows (common in real-world data)
duplicate_rows = np.random.choice(n, size=10, replace=False)

# ─────────────────────────────────────────────────────────────────────────────
# ASSEMBLE INTO A DATAFRAME
# ─────────────────────────────────────────────────────────────────────────────

df = pd.DataFrame({
    'price': price,
    'area_sqft': area_sqft,
    'num_bedrooms': num_bedrooms,
    'num_bathrooms': num_bathrooms,
    'house_age': house_age,
    'neighbourhood': neighbourhood,
    'condition': condition,
    'has_garage': has_garage,
    'sale_date': sale_date
})

# Add duplicate rows at the end of the dataframe
df = pd.concat([df, df.iloc[duplicate_rows]], ignore_index=True)

print("Dataset created successfully!")
print(f"Shape: {df.shape}")  # (rows, columns)
print(df.head())             # Show first 5 rows
```

---

## 3. Exploratory Data Analysis

### What is EDA?

**EDA (Exploratory Data Analysis)** means: *look at your data carefully before doing anything else*.

Think of it like a doctor examining a patient before prescribing medicine. You do not guess — you examine, ask questions, and look for symptoms.

EDA is not about fixing problems yet. It is about **understanding** what you have:
- What does the data look like?
- Are there any missing values?
- Are there outliers?
- How are variables distributed?
- Are there relationships between variables?

The insights from EDA directly tell you **what to fix in preprocessing** and **what to create in feature engineering**.

---

### 3.1 Initial Inspection

#### Step 1: Shape and Columns

```python
# ─────────────────────────────────────────────────────────────────────────────
# INITIAL INSPECTION: The first things to check in any new dataset
# ─────────────────────────────────────────────────────────────────────────────

# .shape returns a tuple: (number of rows, number of columns)
print("Dataset shape:", df.shape)
# If this says (1010, 9), it means 1010 rows and 9 columns

# .columns lists all column names
print("\nColumn names:", df.columns.tolist())

# .dtypes tells you what type each column is:
# int64   → whole numbers
# float64 → decimal numbers
# object  → text / mixed data (usually categorical)
# datetime64 → dates and times
print("\nData types:\n", df.dtypes)
```

**Why does this matter?**
- If a numeric column shows as `object`, it likely has hidden text (like "£300,000" instead of 300000) — you need to fix it.
- Knowing which columns are text (object) tells you which ones need encoding before modelling.
- Knowing column names up front prevents surprises later.

---

#### Step 2: First and Last Rows

```python
# .head(n) shows the first n rows (default is 5)
print("First 5 rows:")
print(df.head())

# .tail(n) shows the last n rows
# Useful to check if duplicates were added at the end
print("\nLast 5 rows:")
print(df.tail())

# .sample(n) shows n random rows — good for a random spot check
print("\n5 random rows:")
print(df.sample(5))
```

---

#### Step 3: Summary Statistics

```python
# .describe() gives key statistics for every numeric column:
# count  → how many non-missing values exist
# mean   → average value
# std    → standard deviation (how spread out the values are)
# min    → smallest value
# 25%    → value below which 25% of data falls (1st quartile)
# 50%    → median (middle value — half above, half below)
# 75%    → value below which 75% of data falls (3rd quartile)
# max    → largest value

print("Summary statistics for numeric columns:")
print(df.describe())

# To include object (text) columns too, use include='all'
print("\nSummary including categorical columns:")
print(df.describe(include='all'))
```

**Reading the output — what to look for:**

| Signal | What it means |
|---|---|
| `count` is less than total rows | Missing values exist in that column |
| `min` or `max` looks extreme | Possible outlier |
| `mean` is very different from `50%` (median) | Distribution is skewed (pulled by extremes) |
| `std` is very large relative to `mean` | High variability |

---

#### Step 4: Missing Values

```python
# .isnull() returns True/False for each cell (True = missing)
# .sum() counts the True values per column
missing_counts = df.isnull().sum()
print("Missing value count per column:")
print(missing_counts)

# Express missing values as a percentage of total rows
missing_percentage = (df.isnull().sum() / len(df)) * 100
print("\nMissing value percentage per column:")
print(missing_percentage.round(2))

# Only show columns that actually have missing values
print("\nColumns with missing values:")
print(missing_percentage[missing_percentage > 0])
```

---

#### Step 5: Duplicates

```python
# .duplicated() returns True for rows that are exact copies of an earlier row
num_duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {num_duplicates}")

# View the actual duplicate rows
print("\nDuplicate rows:")
print(df[df.duplicated()])
```

---

#### Step 6: Unique Values in Categorical Columns

```python
# For categorical columns, check what unique values exist
# This tells you if there are unexpected categories (like typos: 'urbn' instead of 'Urban')

categorical_columns = ['neighbourhood', 'condition', 'has_garage']

for col in categorical_columns:
    print(f"\n--- Column: {col} ---")
    print(f"Unique values: {df[col].unique()}")      # What categories exist
    print(f"Value counts:\n{df[col].value_counts()}")  # How many of each
```

---

### 3.2 Visual EDA

Numbers tell part of the story. **Visualizations reveal what numbers hide** — such as the *shape* of a distribution, where outliers sit, and whether two variables move together.

#### Understanding Two Key Plot Types First

**Histogram** → Shows how values are distributed (spread across ranges)
- X-axis: value ranges (called "bins")
- Y-axis: how many rows fall into each bin
- Tells you: Is the data symmetric? Skewed? Are there unusual gaps?

**Boxplot** → Shows the 5-number summary and outliers visually
```
|──── whisker ────[  Q1 | median | Q3  ]──── whisker ────| ●  ●
                        The Box                              Outliers
```
- The box covers the middle 50% of data (Q1 to Q3)
- The line inside the box is the median
- Whiskers extend to 1.5× the IQR (explained in detail in Section 4)
- Points beyond the whiskers are flagged as outliers

---

#### Univariate Analysis (one variable at a time)

```python
# ─────────────────────────────────────────────────────────────────────────────
# UNIVARIATE ANALYSIS: Study each variable by itself
# Goal: Understand the distribution and spot problems
# ─────────────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 3, figsize=(15, 8))  # 2 rows, 3 columns of subplots
fig.suptitle("Univariate Analysis: Distribution of Numeric Features", fontsize=14)

# List of numeric columns to examine
numeric_cols = ['price', 'area_sqft', 'num_bedrooms', 'num_bathrooms', 'house_age']

for i, col in enumerate(numeric_cols):
    row = i // 3  # Which row: 0 or 1
    col_idx = i % 3  # Which column: 0, 1, or 2

    ax = axes[row][col_idx]

    # Plot a histogram with a KDE (kernel density estimate) curve overlaid
    # KDE = a smooth curve that estimates the probability distribution
    sns.histplot(df[col].dropna(), kde=True, ax=ax, color='steelblue')
    ax.set_title(f'Distribution of {col}')
    ax.set_xlabel(col)
    ax.set_ylabel('Count')

# Hide the last empty subplot (we have 5 columns but 6 spaces)
axes[1][2].set_visible(False)

plt.tight_layout()
plt.savefig('univariate_analysis.png', dpi=120, bbox_inches='tight')
plt.show()
```

**What to look for in histograms:**

| Pattern | What it means | What to do |
|---|---|---|
| Bell curve (symmetric) | Normally distributed — ideal for most models | No transformation needed |
| Long tail to the right | Right-skewed — a few very high values | Consider log transformation |
| Long tail to the left | Left-skewed | Consider square transformation |
| Two humps (bimodal) | Likely two distinct groups in data | Investigate why |
| Spike at one value | Most data is that one value | May not be useful as a feature |

```python
# ─────────────────────────────────────────────────────────────────────────────
# BOXPLOT: Great for visualizing outliers
# ─────────────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Boxplots: Spotting Outliers in Key Numeric Columns", fontsize=14)

# Box plot for price — we expect outliers here because we added extreme ones
sns.boxplot(y=df['price'], ax=axes[0], color='salmon')
axes[0].set_title('Price')

# Box plot for area
sns.boxplot(y=df['area_sqft'], ax=axes[1], color='lightgreen')
axes[1].set_title('Area (sqft)')

# Box plot for house age
sns.boxplot(y=df['house_age'], ax=axes[2], color='lightyellow')
axes[2].set_title('House Age')

plt.tight_layout()
plt.savefig('boxplots.png', dpi=120, bbox_inches='tight')
plt.show()

# KEY INSIGHT FROM THIS PLOT:
# The 'price' boxplot will show a few dots far above the whisker → those are our outliers
# This tells us: "We need to handle outliers in price during preprocessing"
```

```python
# ─────────────────────────────────────────────────────────────────────────────
# BAR CHART: Count of categorical variables
# ─────────────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
fig.suptitle("Distribution of Categorical Features", fontsize=14)

categorical_cols = ['neighbourhood', 'condition', 'has_garage']

for i, col in enumerate(categorical_cols):
    # value_counts() counts occurrences of each category
    counts = df[col].value_counts()
    axes[i].bar(counts.index, counts.values, color='mediumpurple', edgecolor='white')
    axes[i].set_title(f'Distribution of {col}')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('Count')

plt.tight_layout()
plt.savefig('categorical_distributions.png', dpi=120, bbox_inches='tight')
plt.show()

# KEY INSIGHT:
# If one category has very few rows, it might cause problems during encoding
# If categories are roughly balanced, the model will have enough examples of each
```

---

#### Bivariate Analysis (two variables together)

```python
# ─────────────────────────────────────────────────────────────────────────────
# BIVARIATE ANALYSIS: Study how two variables relate to each other
# Especially: how does each feature relate to our TARGET variable (price)?
# ─────────────────────────────────────────────────────────────────────────────

# --- Scatter Plot: Numeric vs Numeric ---
# Goal: Do larger houses cost more? (we'd expect yes)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Area vs Price
axes[0].scatter(df['area_sqft'], df['price'], alpha=0.4, color='steelblue')
axes[0].set_xlabel('Area (sqft)')
axes[0].set_ylabel('Price')
axes[0].set_title('Area vs Price')

# House Age vs Price
axes[1].scatter(df['house_age'], df['price'], alpha=0.4, color='salmon')
axes[1].set_xlabel('House Age (years)')
axes[1].set_ylabel('Price')
axes[1].set_title('House Age vs Price')

plt.tight_layout()
plt.savefig('scatter_plots.png', dpi=120, bbox_inches='tight')
plt.show()

# KEY INSIGHT:
# If you see a clear upward trend in area vs price → strong positive correlation → area is a useful feature
# Outlier prices will appear as isolated dots far above the cluster → confirms we need to handle them
```

```python
# ─────────────────────────────────────────────────────────────────────────────
# BOX PLOT: Categorical vs Numeric
# Goal: Does neighbourhood affect price?
# ─────────────────────────────────────────────────────────────────────────────

plt.figure(figsize=(10, 5))
sns.boxplot(x='neighbourhood', y='price', data=df, palette='Set2')
plt.title('Price Distribution by Neighbourhood')
plt.xlabel('Neighbourhood')
plt.ylabel('Price')
plt.savefig('price_by_neighbourhood.png', dpi=120, bbox_inches='tight')
plt.show()

# KEY INSIGHT:
# If Urban median price is clearly higher than Rural → neighbourhood is a meaningful feature
# This justifies encoding it and including it in the model
```

```python
# ─────────────────────────────────────────────────────────────────────────────
# CORRELATION HEATMAP: All numeric variables at once
# ─────────────────────────────────────────────────────────────────────────────

# What is correlation?
# Correlation measures how two numeric variables move together.
# Range: -1 to +1
#  +1 = perfect positive relationship (as X goes up, Y goes up)
#  -1 = perfect negative relationship (as X goes up, Y goes down)
#   0 = no relationship

# .corr() computes the correlation between every pair of numeric columns
correlation_matrix = df[['price', 'area_sqft', 'num_bedrooms', 'num_bathrooms', 'house_age']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(
    correlation_matrix,
    annot=True,        # Show numbers inside each cell
    fmt='.2f',         # Round to 2 decimal places
    cmap='coolwarm',   # Red = positive correlation, Blue = negative
    vmin=-1, vmax=1,   # Fix scale from -1 to 1
    linewidths=0.5
)
plt.title('Correlation Heatmap of Numeric Features')
plt.savefig('correlation_heatmap.png', dpi=120, bbox_inches='tight')
plt.show()

# KEY INSIGHTS FROM THE HEATMAP:
# - area_sqft and price: should be ~0.8 (strong positive correlation → useful feature)
# - house_age and price: should be negative (older = cheaper → useful feature)
# - num_bedrooms and area_sqft: likely correlated (bigger house = more bedrooms)
#   → Be careful: two highly correlated INPUT features can cause multicollinearity in some models
```

---

### 3.3 EDA Summary: What Did We Learn?

After EDA, you should have a checklist of **problems found** and **actions to take**:

| Problem Found in EDA | Action in Preprocessing |
|---|---|
| `area_sqft` has ~8% missing values | Impute with median |
| `num_bathrooms` has ~5% missing values | Impute with median |
| `condition` has ~6% missing values | Impute with mode (most common value) |
| `price` has extreme outliers (10x normal values) | Cap or remove outliers using IQR rule |
| 10 duplicate rows found | Drop duplicate rows |
| `neighbourhood` is categorical (text) | Apply OneHotEncoder |
| `condition` is ordered categorical (Poor→Excellent) | Apply OrdinalEncoder |
| `has_garage` is binary Yes/No | Apply OneHotEncoder |
| `area_sqft` and `price` have very different scales | Apply StandardScaler |
| `sale_date` is a datetime column | Extract month, day-of-week as features |

**This table is the direct link between EDA and Preprocessing. EDA does not fix things — it creates your to-do list.**

---

## 4. Data Preprocessing

### What is Data Preprocessing?

Preprocessing means: **taking the problems found in EDA and fixing them** so that the data is:
1. **Complete** (no missing values — most models cannot handle them)
2. **Consistent** (no outliers that would mislead the model)
3. **In the right format** (numbers, not text — models need numbers)
4. **On a comparable scale** (so no single feature dominates unfairly)

---

### 4.1 Handling Missing Values

#### What are Missing Values?

A **missing value** is when a cell in your dataset is empty — there is no data for that particular row and column.

In Python/Pandas, missing values are represented as `NaN` (Not a Number).

**Why do missing values happen?**
- Survey respondent skipped a question
- Sensor malfunctioned and did not record data
- Data entry error
- Information was not available at the time of collection

**Why is this a problem?**
Most ML models simply cannot work with missing values. They will either crash or silently produce wrong results. You must handle them before modelling.

---

#### Option 1: Dropping Rows or Columns

**What it does:** Removes any row that has at least one missing value.

**When to use it:**
- Very few rows are missing (less than 1-2% of your data)
- The missing pattern is random (not systematic)

**When NOT to use it:**
- Many rows have missing values → you'd lose too much data
- The fact that a value is missing is itself informative (e.g., "question skipped" means something)

```python
# ─────────────────────────────────────────────────────────────────────────────
# OPTION 1: DROPPING ROWS WITH MISSING VALUES
# ─────────────────────────────────────────────────────────────────────────────

# Make a copy so we don't destroy the original dataset
df_dropped = df.copy()

# .dropna() removes any row that has at least one NaN
df_dropped_rows = df_dropped.dropna()

print(f"Original shape: {df.shape}")
print(f"After dropping rows with NaN: {df_dropped_rows.shape}")
# Notice: we lose many rows — this is why dropping is not always good

# Alternatively, drop a column if it has too many missing values (e.g., >50%)
# axis=1 means "drop columns" (axis=0 means "drop rows")
threshold = 0.5  # 50% missing
df_dropped_cols = df.dropna(axis=1, thresh=int(len(df) * (1 - threshold)))
print(f"After dropping columns with >50% missing: {df_dropped_cols.shape}")
```

---

#### Option 2: Imputation (Filling Missing Values)

**What is imputation?**
Imputation means **filling in missing values with a reasonable estimate** rather than losing the entire row.

**Types of imputation:**

| Strategy | Formula | Use when |
|---|---|---|
| **Mean imputation** | Fill with column average | Data is normally distributed, no outliers |
| **Median imputation** | Fill with column middle value | Data has outliers (median is not affected by extremes) |
| **Mode imputation** | Fill with most frequent value | Categorical columns |

**Why median over mean?**
If you have house prices: [200k, 210k, 195k, 205k, 2000k], the mean is ~560k — pulled up by the outlier. The median is 205k — a much better estimate for a typical house. When outliers exist, median is safer.

```python
# ─────────────────────────────────────────────────────────────────────────────
# OPTION 2: IMPUTATION USING scikit-learn's SimpleImputer
# ─────────────────────────────────────────────────────────────────────────────

# What is SimpleImputer?
# It is a scikit-learn "transformer" (more on transformers in Section 6)
# It learns the fill value FROM the training data, then applies it

# --- Numeric columns: use median ---

# Step 1: Create the imputer object
# strategy='median' means: fill missing values with the column's median
numeric_imputer = SimpleImputer(strategy='median')

# Step 2: .fit_transform() does two things at once:
# - .fit()      → Learns the median of each column
# - .transform() → Fills in the missing values using that learned median
# We pass only the numeric columns that have missing values
df_imputed = df.copy()
df_imputed[['area_sqft', 'num_bathrooms']] = numeric_imputer.fit_transform(
    df_imputed[['area_sqft', 'num_bathrooms']]
)

# Verify: missing values should now be 0
print("Missing values after numeric imputation:")
print(df_imputed[['area_sqft', 'num_bathrooms']].isnull().sum())

# --- Categorical columns: use mode (most frequent value) ---

# strategy='most_frequent' fills missing values with the most common category
categorical_imputer = SimpleImputer(strategy='most_frequent')

df_imputed[['condition']] = categorical_imputer.fit_transform(
    df_imputed[['condition']]
)

print("\nMissing values in 'condition' after imputation:")
print(df_imputed['condition'].isnull().sum())
```

---

### 4.2 Handling Outliers

#### What is an Outlier?

An **outlier** is a data point that is very different from the majority of data — it is far from the "normal" range.

**Example:** If 999 houses are priced between $100,000 and $800,000, and one house is priced at $8,000,000 — that $8M price is an outlier.

**Why do outliers matter?**
- They can distort the mean (as we saw with imputation)
- They can mislead ML models, causing them to try to fit those extreme points and ignore the majority
- They can represent data entry errors (someone typed an extra zero)

**Types of outliers:**
1. **Genuine outliers** — A billionaire's mansion really does cost $8M. It's real but unusual.
2. **Error outliers** — Someone entered 8,000,000 instead of 800,000 by mistake.

The *treatment* differs: genuine outliers might be kept or capped; error outliers should be corrected or removed.

---

#### The IQR Rule — From Scratch

**IQR (Interquartile Range)** is the most common statistical rule for detecting outliers. Let's build up the concept step by step.

**Step 1: What is a Quartile?**

Imagine you line up all your values from smallest to largest:

```
[100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
  ↑                    ↑                              ↑
 Min                Median (Q2)                      Max
         ↑                          ↑
         Q1 (25th percentile)      Q3 (75th percentile)
```

- **Q1 (1st quartile / 25th percentile):** 25% of values are below this point
- **Q2 (2nd quartile / 50th percentile):** This is the median — 50% of values below
- **Q3 (3rd quartile / 75th percentile):** 75% of values are below this point

**Step 2: What is the IQR?**

`IQR = Q3 − Q1`

The IQR captures the **middle 50% of your data** — the typical range. It is not affected by extreme values because it only looks at the middle half.

**Step 3: The Outlier Fences**

Any value outside these two "fences" is flagged as an outlier:
```
Lower Fence = Q1 - (1.5 × IQR)
Upper Fence = Q3 + (1.5 × IQR)
```

The factor **1.5** is a widely accepted convention in statistics (proposed by statistician John Tukey). Using 1.5 means you flag only genuinely extreme values — about 0.7% of a perfectly normal distribution.

Why 1.5? It is a balance — small enough to catch real outliers, large enough not to flag normal variation. You can use 3.0 for more conservative outlier detection.

```python
# ─────────────────────────────────────────────────────────────────────────────
# THE IQR RULE: DETECTING AND HANDLING OUTLIERS
# ─────────────────────────────────────────────────────────────────────────────

df_clean = df_imputed.copy()  # Start from the imputed dataframe

def detect_outliers_iqr(df, column):
    """
    Detect outliers in a column using the IQR rule.
    Returns: (lower_fence, upper_fence, number_of_outliers)
    """
    Q1 = df[column].quantile(0.25)   # 25th percentile
    Q3 = df[column].quantile(0.75)   # 75th percentile
    IQR = Q3 - Q1                    # Interquartile range

    lower_fence = Q1 - 1.5 * IQR    # Anything below this is an outlier
    upper_fence = Q3 + 1.5 * IQR    # Anything above this is an outlier

    # Boolean mask: True where value is an outlier
    outlier_mask = (df[column] < lower_fence) | (df[column] > upper_fence)
    num_outliers = outlier_mask.sum()

    return lower_fence, upper_fence, num_outliers, outlier_mask

# Check outliers in 'price'
lower, upper, count, mask = detect_outliers_iqr(df_clean, 'price')
print(f"Price IQR Analysis:")
print(f"  Q1: {df_clean['price'].quantile(0.25):,.0f}")
print(f"  Q3: {df_clean['price'].quantile(0.75):,.0f}")
print(f"  IQR: {df_clean['price'].quantile(0.75) - df_clean['price'].quantile(0.25):,.0f}")
print(f"  Lower fence: {lower:,.0f}")
print(f"  Upper fence: {upper:,.0f}")
print(f"  Number of outliers detected: {count}")
print(f"\nOutlier rows:")
print(df_clean[mask][['price', 'area_sqft', 'neighbourhood']].head(10))
```

#### Handling Outliers: Options

Once you detect outliers, you have three choices:

**Option A: Remove them** — If they are clearly errors
```python
# Remove rows where price is an outlier
# ~ means "NOT" — keep rows where the outlier mask is False
df_clean = df_clean[~mask]
print(f"Rows after removing price outliers: {len(df_clean)}")
```

**Option B: Cap them (Winsorization)** — If they might be genuine but extreme
```python
# Capping: Replace any value above upper_fence with upper_fence
# Replace any value below lower_fence with lower_fence
# .clip(lower, upper) does this in one step

df_capped = df_imputed.copy()
lower, upper, _, _ = detect_outliers_iqr(df_capped, 'price')

df_capped['price'] = df_capped['price'].clip(lower=lower, upper=upper)
print(f"Max price before capping: {df_imputed['price'].max():,.0f}")
print(f"Max price after capping: {df_capped['price'].max():,.0f}")
# The outlier values are now brought down to the upper fence
```

**Option C: Transform them** — Log transformation (covered in Feature Engineering)

**For this guide, we will use capping (Option B)** and continue with `df_clean`.

```python
# Let's use the capped version going forward
df_clean = df_capped.copy()
```

---

### 4.3 Handling Duplicates

```python
# ─────────────────────────────────────────────────────────────────────────────
# REMOVING DUPLICATE ROWS
# ─────────────────────────────────────────────────────────────────────────────

print(f"Rows before removing duplicates: {len(df_clean)}")

# .drop_duplicates() removes rows that are identical to an earlier row
# keep='first' means: keep the first occurrence, remove the later ones
df_clean = df_clean.drop_duplicates(keep='first')

print(f"Rows after removing duplicates: {len(df_clean)}")

# Verify
print(f"Remaining duplicates: {df_clean.duplicated().sum()}")
```

---

### 4.4 Categorical Encoding

#### What is Categorical Data?

**Categorical data** is data that represents groups or categories rather than continuous numbers.

Examples in our dataset:
- `neighbourhood`: 'Urban', 'Suburban', 'Rural'
- `condition`: 'Poor', 'Fair', 'Good', 'Excellent'
- `has_garage`: 'Yes', 'No'

#### Why Can't Models Use Text Directly?

ML models are mathematical functions. They perform operations like multiplication, addition, and distance calculation. You cannot multiply "Urban" by 150 — it is meaningless. You must convert categories into numbers.

But **how** you convert them matters — and doing it wrong can introduce incorrect assumptions into your model.

---

#### OneHotEncoder — For Nominal Categories

**Nominal** means the categories have **no natural order**. 'Urban' is not "greater than" or "less than" 'Rural' — they are just different.

**What OneHotEncoder does:**
It creates **one new binary column for each category**:

```
Before:                    After:
neighbourhood              neighbourhood_Urban  neighbourhood_Suburban  neighbourhood_Rural
Urban          →           1                    0                       0
Suburban       →           0                    1                       0
Rural          →           0                    0                       1
Urban          →           1                    0                       0
```

Each house gets a 1 in the column that matches its neighbourhood, and 0 everywhere else.

**Why not just assign numbers (Urban=1, Suburban=2, Rural=3)?**
Because then the model would think Rural (3) is three times Urban (1), and Suburban (2) is in between — which is completely wrong. There is no such ordering or magnitude. OneHotEncoder avoids this fake ordering problem.

**The "dummy variable trap":**
If you create three columns (Urban, Suburban, Rural), you actually only need two. If Urban=0 and Suburban=0, you already know it's Rural. Having all three creates *redundancy* (called multicollinearity). This is why many implementations use `drop='first'` — it drops one column.

```python
# ─────────────────────────────────────────────────────────────────────────────
# ONEHOT ENCODING: For nominal categories (no order)
# Applied to: 'neighbourhood', 'has_garage'
# ─────────────────────────────────────────────────────────────────────────────

# Make a working copy
df_encoded = df_clean.copy()

# Create the encoder
# sparse_output=False → return a regular numpy array (not a sparse matrix)
# drop='first' → drop one column per feature to avoid the dummy variable trap
# handle_unknown='ignore' → if a new category appears, output all zeros (safe for deployment)
ohe = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore')

# Columns we want to one-hot encode
nominal_cols = ['neighbourhood', 'has_garage']

# .fit_transform() learns the categories and creates the binary columns
encoded_array = ohe.fit_transform(df_encoded[nominal_cols])

# Get the names for the new columns
# get_feature_names_out() returns names like 'neighbourhood_Suburban', 'has_garage_Yes'
encoded_col_names = ohe.get_feature_names_out(nominal_cols)

# Convert the numpy array back to a DataFrame
encoded_df = pd.DataFrame(encoded_array, columns=encoded_col_names, index=df_encoded.index)

# Add the new columns to our main dataframe
df_encoded = pd.concat([df_encoded, encoded_df], axis=1)

# Remove the original text columns (we no longer need them)
df_encoded = df_encoded.drop(columns=nominal_cols)

print("Columns after OneHotEncoding:")
print(df_encoded.columns.tolist())
print("\nSample of new encoded columns:")
print(df_encoded[encoded_col_names].head())
```

---

#### OrdinalEncoder — For Ordinal Categories

**Ordinal** means the categories **have a meaningful order**.

In our dataset, `condition` has a clear order: Poor < Fair < Good < Excellent

Here, it makes sense to encode them as: Poor=0, Fair=1, Good=2, Excellent=3

The model can now understand that Good (2) is better than Fair (1), which is correct and useful.

**Key difference from OneHotEncoder:**
- OneHotEncoder: No order → creates separate binary columns
- OrdinalEncoder: Has order → creates one column with integers

```python
# ─────────────────────────────────────────────────────────────────────────────
# ORDINAL ENCODING: For ordered categories
# Applied to: 'condition'
# ─────────────────────────────────────────────────────────────────────────────

# Define the order explicitly — from least to greatest
# IMPORTANT: You must always define the order yourself. OrdinalEncoder does not guess.
condition_order = [['Poor', 'Fair', 'Good', 'Excellent']]
# This maps: Poor→0, Fair→1, Good→2, Excellent→3

# Create the encoder with the specified order
ordinal_encoder = OrdinalEncoder(
    categories=condition_order,
    handle_unknown='use_encoded_value',  # If unknown category appears, use -1
    unknown_value=-1
)

# Encode the condition column
# Note: OrdinalEncoder expects a 2D array, so we use [['condition']] (double brackets)
df_encoded[['condition']] = ordinal_encoder.fit_transform(df_encoded[['condition']])

print("Condition encoding result:")
print(df_encoded[['condition']].value_counts().sort_index())
# You should see: 0=Poor, 1=Fair, 2=Good, 3=Excellent
```

---

#### Quick Decision Guide: Which Encoder to Use?

```
Is the categorical column ordered?
    │
    ├─ YES (Poor < Fair < Good) → Use OrdinalEncoder
    │    Define the order yourself!
    │
    └─ NO (Urban, Suburban, Rural — no ranking) → Use OneHotEncoder
         Be aware: creates many columns if you have many categories
         For very high cardinality (100+ categories), consider Target Encoding instead
```

---

### 4.5 Feature Scaling

#### What is Feature Scaling?

**Feature scaling** means transforming numeric columns so they are all on a similar scale.

#### Why is Scaling Needed?

Consider two features in our dataset:
- `area_sqft`: values range from 500 to 5,000
- `num_bedrooms`: values range from 1 to 6

To a model that uses distance calculations or gradient descent, `area_sqft` will appear 1,000 times more important than `num_bedrooms` — not because it is actually more informative, but simply because its numbers are larger.

**Analogy:** Imagine comparing salaries in rupees vs dollars. If someone earns ₹50,000/month and another earns $700/month, the rupee number looks much bigger — but they might be equivalent. Scaling converts everything to the same "currency."

#### When is Scaling Required?

| Model Type | Needs Scaling? | Why |
|---|---|---|
| Linear Regression | Yes | Coefficients are sensitive to scale |
| Logistic Regression | Yes | Same reason |
| Support Vector Machines | Yes | Distance-based: scale matters a lot |
| K-Nearest Neighbours | Yes | Distance-based |
| Neural Networks | Yes | Gradient descent is scale-sensitive |
| Decision Trees | **No** | Splits are based on thresholds, not distances |
| Random Forest | **No** | Same reason as decision trees |
| Gradient Boosting (XGBoost) | **No** | Same reason |

**Rule of thumb:** Scale when using distance-based or gradient-based algorithms. Skip for tree-based algorithms.

---

#### StandardScaler

**What it does:**
Transforms each value so the column has **mean = 0 and standard deviation = 1**.

**Formula:**
```
z = (x − mean) / std
```

Where `x` is the original value, `mean` is the column's average, and `std` is the standard deviation.

**After scaling:**
- Values centered around 0
- Most values will fall between −3 and +3
- The column's shape (distribution) does not change, only its centre and spread

**When to use:** When data is approximately normally distributed (bell-shaped). Most general-purpose situations.

**When NOT to use:** When you need values in a specific range (e.g., between 0 and 1 for image pixels).

```python
# ─────────────────────────────────────────────────────────────────────────────
# STANDARDSCALER: Scale to mean=0, std=1
# ─────────────────────────────────────────────────────────────────────────────

df_scaled = df_encoded.copy()

# Columns to scale: numeric features (not the ones we already encoded)
numeric_features = ['area_sqft', 'num_bedrooms', 'num_bathrooms', 'house_age']

# Create the scaler
standard_scaler = StandardScaler()

# .fit_transform() learns the mean and std, then applies the formula
df_scaled[numeric_features] = standard_scaler.fit_transform(df_scaled[numeric_features])

print("Before scaling:")
print(df_encoded[numeric_features].describe().loc[['mean', 'std', 'min', 'max']].round(2))

print("\nAfter StandardScaling:")
print(df_scaled[numeric_features].describe().loc[['mean', 'std', 'min', 'max']].round(2))
# mean should be ≈ 0, std should be ≈ 1 for all columns
```

---

#### MinMaxScaler

**What it does:**
Scales each value to a fixed range, typically **[0, 1]**.

**Formula:**
```
x_scaled = (x − min) / (max − min)
```

The smallest value becomes 0. The largest value becomes 1. Everything else falls between.

**When to use:**
- When you need values bounded in [0, 1] (e.g., neural networks with sigmoid activation)
- When the algorithm assumes input is in a specific range

**When NOT to use:**
- When your data has extreme outliers — the outlier becomes 1 (or 0) and squishes all other values into a tiny range
- StandardScaler handles outliers more gracefully

```python
# ─────────────────────────────────────────────────────────────────────────────
# MINMAXSCALER: Scale to [0, 1] range
# ─────────────────────────────────────────────────────────────────────────────

df_minmax = df_encoded.copy()

min_max_scaler = MinMaxScaler()

df_minmax[numeric_features] = min_max_scaler.fit_transform(df_minmax[numeric_features])

print("After MinMaxScaling:")
print(df_minmax[numeric_features].describe().loc[['mean', 'std', 'min', 'max']].round(4))
# min should be 0, max should be 1 for all columns
```

#### Quick Decision Guide: StandardScaler vs MinMaxScaler

| Situation | Use |
|---|---|
| General purpose, normally distributed data | StandardScaler |
| Neural networks, need [0,1] range | MinMaxScaler |
| Data has significant outliers | StandardScaler (more robust) |
| Comparing features across models | StandardScaler |

---

## 5. Feature Engineering

### What is Feature Engineering?

**Feature engineering** is the art of creating new, more informative columns from existing ones.

A raw dataset contains the data that was collected. But sometimes the *raw* form is not the most useful form for a model to learn from. Feature engineering asks: **"Can I combine, transform, or extract information from existing columns to give the model a clearer signal?"**

**Example intuition:**
- Raw: a house has `area_sqft = 2000` and `price = 400,000`
- Engineered: `price_per_sqft = 400,000 / 2,000 = 200` — this is a direct signal about value per unit area that the model can more easily learn from

---

### 5.1 Interaction Features (Ratios and Combinations)

```python
# ─────────────────────────────────────────────────────────────────────────────
# INTERACTION FEATURES: Combine two columns into a more meaningful one
# ─────────────────────────────────────────────────────────────────────────────

# Start from the clean (but not yet encoded/scaled) dataframe for clarity
df_fe = df_clean.copy()

# --- Feature 1: Price per Square Foot ---
# WHY: A 2000 sqft house at $300k is a better deal than a 1000 sqft house at $300k
# price_per_sqft directly captures "value density"
df_fe['price_per_sqft'] = df_fe['price'] / df_fe['area_sqft']

# --- Feature 2: Bedroom-to-Bathroom Ratio ---
# WHY: A house with 4 bedrooms and 1 bathroom might be uncomfortable
# This ratio captures the balance between sleeping and bathroom capacity
df_fe['bed_bath_ratio'] = df_fe['num_bedrooms'] / df_fe['num_bathrooms']

# --- Feature 3: Total Room Count ---
# WHY: A simple addition that captures overall house size in terms of rooms
df_fe['total_rooms'] = df_fe['num_bedrooms'] + df_fe['num_bathrooms']

print("New interaction features:")
print(df_fe[['price_per_sqft', 'bed_bath_ratio', 'total_rooms']].head())

# WHEN NOT TO USE:
# Avoid creating interaction features blindly — every feature you add increases complexity
# Only create features that have logical meaning
# After creation, use correlation analysis to check if they're actually useful
```

---

### 5.2 Log Transformation

#### What is a Log Transformation?

A **log transformation** replaces a value `x` with its logarithm: `log(x)`.

**Why?**
Many real-world variables — like house prices, income, population — are **right-skewed**. There are many average-priced houses and a few very expensive ones. This creates a long right tail.

Problems with skewed data:
1. Outliers have a disproportionate effect on models
2. The relationship between variables may be multiplicative, not additive (a 10% increase in area leads to a 10% increase in price, not a fixed amount increase)
3. Many models assume data is approximately normally distributed

Log transformation **compresses** large values and **spreads out** small values — turning a skewed distribution into something more symmetric.

```
Original prices:   100k, 200k, 300k, 1000k, 2000k
                   (the 2000k value is far from the cluster)

Log(prices):       5.0, 5.3, 5.5, 6.0, 6.3
                   (much more evenly spread)
```

```python
# ─────────────────────────────────────────────────────────────────────────────
# LOG TRANSFORMATION: Compress skewed distributions
# ─────────────────────────────────────────────────────────────────────────────

# np.log1p(x) computes log(1 + x)
# We use log1p instead of log because log(0) = negative infinity (undefined)
# log1p handles zero values safely: log1p(0) = log(1) = 0

df_fe['log_price'] = np.log1p(df_fe['price'])
df_fe['log_area'] = np.log1p(df_fe['area_sqft'])

# Visualize the effect
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Original price distribution
axes[0][0].hist(df_fe['price'].dropna(), bins=50, color='salmon', edgecolor='white')
axes[0][0].set_title('Price (Original) — Notice the right skew')
axes[0][0].set_xlabel('Price')

# Log-transformed price distribution
axes[0][1].hist(df_fe['log_price'].dropna(), bins=50, color='steelblue', edgecolor='white')
axes[0][1].set_title('Log(Price) — More symmetric')
axes[0][1].set_xlabel('log(Price)')

# Original area distribution
axes[1][0].hist(df_fe['area_sqft'].dropna(), bins=50, color='lightgreen', edgecolor='white')
axes[1][0].set_title('Area (Original)')
axes[1][0].set_xlabel('Area (sqft)')

# Log-transformed area
axes[1][1].hist(df_fe['log_area'].dropna(), bins=50, color='mediumpurple', edgecolor='white')
axes[1][1].set_title('Log(Area) — More symmetric')
axes[1][1].set_xlabel('log(Area)')

plt.tight_layout()
plt.savefig('log_transformation.png', dpi=120, bbox_inches='tight')
plt.show()

# WHEN TO USE LOG TRANSFORMATION:
# ✓ When distribution is right-skewed (long tail on the right)
# ✓ When the variable represents something that compounds (prices, population)
# ✓ Before applying LinearRegression if target variable is skewed

# WHEN NOT TO USE:
# ✗ When values include 0 or negatives (use log1p for zeros)
# ✗ When data is already symmetric
# ✗ For tree-based models (they don't care about distribution shape)
```

---

### 5.3 Binning (Grouping Continuous Values)

#### What is Binning?

Binning means converting a continuous numeric variable into **discrete groups** (bins or buckets).

**Why?**
- Sometimes the exact value matters less than the group it falls in
- A model predicting family housing might care whether a house is "new" (0-5 years), "moderate" (6-20), "old" (21-50), or "very old" (50+) — not the exact year
- Reduces the impact of small variations
- Captures non-linear relationships (old houses might drop sharply in value, not linearly)

```python
# ─────────────────────────────────────────────────────────────────────────────
# BINNING WITH pd.cut(): Group house_age into categories
# ─────────────────────────────────────────────────────────────────────────────

# pd.cut() divides a column into bins you define
# bins: the boundary points of each bin
# labels: what to call each bin
# include_lowest=True: ensures the minimum value is included in the first bin

df_fe['age_group'] = pd.cut(
    df_fe['house_age'],
    bins=[0, 5, 20, 50, 100],           # Boundaries: 0-5, 6-20, 21-50, 51-100
    labels=['New', 'Moderate', 'Old', 'Very Old'],  # Names for each group
    include_lowest=True                  # Include houses with age = 0
)

print("House age distribution by group:")
print(df_fe['age_group'].value_counts().sort_index())

print("\nSample of binning result:")
print(df_fe[['house_age', 'age_group']].head(10))

# Note: After binning, 'age_group' is a categorical column
# You will need to encode it (with OrdinalEncoder if order matters, which it does here)
age_order = [['New', 'Moderate', 'Old', 'Very Old']]
age_ordinal = OrdinalEncoder(categories=age_order)
df_fe['age_group_encoded'] = age_ordinal.fit_transform(df_fe[['age_group']].astype(str))

# WHEN TO USE BINNING:
# ✓ When relationship with target is non-linear within ranges
# ✓ When you want to reduce the effect of outliers
# ✓ When domain knowledge says grouping makes sense (e.g., age groups)

# WHEN NOT TO USE:
# ✗ When the precise value matters (e.g., temperature in scientific experiments)
# ✗ When it destroys meaningful variation (binning can lose information)
```

---

### 5.4 Time-Based Features

#### What are Time-Based Features?

When your dataset contains a date/time column, you should extract meaningful components from it rather than using the raw date (which models cannot interpret directly).

**Why?**
A house sold in December might sell for a different price than one sold in June (seasonal effects). A house sold on a weekday vs weekend might differ. These patterns can only be captured if you extract the month, day of week, quarter, etc.

```python
# ─────────────────────────────────────────────────────────────────────────────
# TIME-BASED FEATURES: Extract useful information from datetime columns
# ─────────────────────────────────────────────────────────────────────────────

# First, ensure the column is in datetime format
df_fe['sale_date'] = pd.to_datetime(df_fe['sale_date'])

# Extract month: January=1, February=2, ..., December=12
df_fe['sale_month'] = df_fe['sale_date'].dt.month

# Extract day of week: Monday=0, Tuesday=1, ..., Sunday=6
df_fe['sale_dayofweek'] = df_fe['sale_date'].dt.dayofweek

# Extract quarter: Q1=1, Q2=2, Q3=3, Q4=4
df_fe['sale_quarter'] = df_fe['sale_date'].dt.quarter

# Extract year — useful if data spans multiple years and there's a year-over-year trend
df_fe['sale_year'] = df_fe['sale_date'].dt.year

# Create a binary "is_weekend" feature (True if Saturday or Sunday)
df_fe['is_weekend'] = df_fe['sale_dayofweek'].isin([5, 6]).astype(int)

print("Extracted time features:")
print(df_fe[['sale_date', 'sale_month', 'sale_dayofweek', 'sale_quarter', 'is_weekend']].head())

# Drop the original date column — models can't use raw dates
df_fe = df_fe.drop(columns=['sale_date'])

# WHEN TO USE TIME FEATURES:
# ✓ Seasonal patterns exist (retail sales, housing demand)
# ✓ Day-of-week effects (traffic, transactions)
# ✓ Year-over-year trends (inflation, growth)

# WHEN NOT TO USE:
# ✗ When time is irrelevant to what you're predicting
# ✗ When your dataset covers only a short time range with no seasonal variation
```

---

## 6. Scikit-Learn Pipelines

### 6.1 What is a Transformer? (From Scratch)

Before learning about Pipelines, you need to understand **transformers**.

A **transformer** is any object that takes in data and outputs a modified version of that data.

In scikit-learn, transformers always follow this pattern:

1. **`.fit(data)`** — The transformer "learns" from the data.
   - `SimpleImputer` learns the median value of each column
   - `StandardScaler` learns the mean and standard deviation
   - `OneHotEncoder` learns what categories exist

2. **`.transform(data)`** — The transformer uses what it learned to modify the data.
   - `SimpleImputer` replaces NaN with the median it learned
   - `StandardScaler` subtracts the mean and divides by std it learned
   - `OneHotEncoder` creates binary columns based on the categories it learned

3. **`.fit_transform(data)`** — Does both steps at once (shortcut for convenience).

**The critical rule:** You `.fit()` on training data only. You use `.transform()` on both training and test data using the values learned from training. **Never fit on test data.**

---

### 6.2 What is Data Leakage? (The Most Important Concept in this Section)

**Data leakage** is one of the most dangerous and common mistakes in ML. It means: **information from the test/future data accidentally influences the training process**.

This makes your model seem more accurate than it actually is — it's cheating, and you won't discover it until the model fails in production.

#### A Concrete Example:

You have 1000 houses. You split them 800 for training, 200 for testing.

**Wrong approach:**
```
Apply StandardScaler on ALL 1000 houses
          ↓
Then split into 800 train / 200 test
```

**Why is this wrong?**
When you calculated the mean and std across all 1000 houses, those statistics were influenced by your 200 test houses. The test data should be completely "unseen" — but its information already leaked into the scaler's parameters. Your model has indirectly "seen" the test data.

**Correct approach:**
```
Split into 800 train / 200 test FIRST
          ↓
Fit StandardScaler ONLY on the 800 training houses
          ↓
Transform the training data using learned parameters
Transform the test data using the SAME learned parameters
```

The test set is now truly unseen. Any statistics came purely from the training data.

**Pipelines prevent leakage automatically** — they enforce the correct order.

---

### 6.3 What is a Pipeline?

A **Pipeline** is a scikit-learn object that **chains multiple transformers and a model together into one unit**.

Without a pipeline, you'd have to manually apply each step in order, every time. You'd need to remember: "Did I scale before encoding? Did I fit the scaler on test data by mistake?"

With a pipeline:
- All steps are applied in the right order automatically
- `.fit()` on the pipeline trains all steps on training data
- `.transform()` (or `.predict()`) applies all steps to new data using training-learned parameters
- No leakage is possible

```
Pipeline = [Step 1: Imputer] → [Step 2: Scaler] → [Step 3: Encoder] → [Model]
```

---

### 6.4 What is a ColumnTransformer?

In our dataset, different columns need different treatments:
- Numeric columns: Impute → Scale
- Nominal columns: Impute → OneHotEncode
- Ordinal columns: Impute → OrdinalEncode

**ColumnTransformer** lets you apply different pipelines to different subsets of columns — simultaneously — and then combines the results into one dataframe.

```
ColumnTransformer:
    ├── numeric_pipeline     → applied to ['area_sqft', 'num_bedrooms', ...]
    ├── nominal_pipeline     → applied to ['neighbourhood', 'has_garage']
    └── ordinal_pipeline     → applied to ['condition']
```

---

### 6.5 Complete Pipeline — All Steps Combined

```python
# ─────────────────────────────────────────────────────────────────────────────
# COMPLETE SCIKIT-LEARN PIPELINE
# Handles: missing values, encoding, and scaling in one clean object
# Prevents: data leakage by design
# ─────────────────────────────────────────────────────────────────────────────

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# ── Step 0: Prepare the Dataset ──────────────────────────────────────────────

# Start fresh from the clean dataframe (with extracted time features)
df_pipeline = df_fe.copy()

# Drop columns we engineered for illustration that would cause leakage
# (price_per_sqft uses 'price' which is the target — don't use target to create features
#  unless you're very careful about how you handle it)
df_pipeline = df_pipeline.drop(columns=['price_per_sqft', 'log_price', 'log_area',
                                         'bed_bath_ratio', 'total_rooms', 'age_group',
                                         'age_group_encoded'], errors='ignore')

# Separate features (X) from target variable (y)
# 'price' is what we want to predict — it must NOT be an input to the model
X = df_pipeline.drop(columns=['price'])  # All columns except price
y = df_pipeline['price']                 # The target column

print("Features (X) shape:", X.shape)
print("Target (y) shape:", y.shape)
print("Feature columns:", X.columns.tolist())

# ── Step 1: Split into Training and Test Sets FIRST ───────────────────────────

# train_test_split randomly divides data
# test_size=0.2 → 20% for testing, 80% for training
# random_state=42 → makes the split reproducible
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set size: {len(X_train)} rows")
print(f"Test set size: {len(X_test)} rows")

# ── Step 2: Define Which Columns Go to Which Pipeline ─────────────────────────

# Numeric features: will be imputed and scaled
numeric_features = ['area_sqft', 'num_bedrooms', 'num_bathrooms', 'house_age',
                    'sale_month', 'sale_dayofweek', 'sale_quarter', 'sale_year', 'is_weekend']

# Nominal categorical features: no order, will be one-hot encoded
nominal_features = ['neighbourhood', 'has_garage']

# Ordinal categorical features: have order, will be ordinal encoded
ordinal_features = ['condition']

# ── Step 3: Build Each Sub-Pipeline ──────────────────────────────────────────

# --- Numeric Pipeline ---
# Step 1: Impute missing values with median (robust to outliers)
# Step 2: Scale to mean=0, std=1
numeric_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),   # Fill missing with median
    ('scaler', StandardScaler())                      # Scale to z-score
])

# --- Nominal Pipeline ---
# Step 1: Impute missing values with most frequent category
# Step 2: OneHotEncode (create binary columns)
nominal_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # Fill missing with mode
    ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))
])

# --- Ordinal Pipeline ---
# Step 1: Impute missing values with most frequent value
# Step 2: OrdinalEncode with known order
ordinal_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OrdinalEncoder(
        categories=[['Poor', 'Fair', 'Good', 'Excellent']],
        handle_unknown='use_encoded_value',
        unknown_value=-1
    ))
])

# ── Step 4: Combine with ColumnTransformer ────────────────────────────────────

# ColumnTransformer applies each pipeline to its designated columns
# remainder='drop' → any columns not listed are dropped (safe default)
preprocessor = ColumnTransformer(transformers=[
    ('numeric', numeric_pipeline, numeric_features),
    ('nominal', nominal_pipeline, nominal_features),
    ('ordinal', ordinal_pipeline, ordinal_features)
], remainder='drop')

# ── Step 5: Fit on Training Data, Transform Both Sets ────────────────────────

# .fit_transform(X_train):
# - ALL imputers learn from X_train only
# - ALL scalers learn mean/std from X_train only
# - ALL encoders learn categories from X_train only
# Then transforms X_train using those learned values
X_train_processed = preprocessor.fit_transform(X_train)

# .transform(X_test):
# - Uses parameters learned from X_train (not from X_test)
# - No leakage: test data is transformed with training statistics
X_test_processed = preprocessor.transform(X_test)

print(f"\nProcessed training set shape: {X_train_processed.shape}")
print(f"Processed test set shape: {X_test_processed.shape}")
print("\n✅ Pipeline complete! Data is ready for model training.")
print("✅ No data leakage: all transformers were fit on training data only.")

# ── Optional: Convert back to DataFrame for inspection ────────────────────────

# Get column names from each transformer
ohe_col_names = preprocessor.named_transformers_['nominal']['encoder'].get_feature_names_out(nominal_features)
all_col_names = numeric_features + list(ohe_col_names) + ordinal_features

# Convert to DataFrame
X_train_df = pd.DataFrame(X_train_processed, columns=all_col_names)
print("\nSample of processed training data:")
print(X_train_df.head())
```

---

### 6.6 What Happens If You Add a Model to the Pipeline?

The Pipeline can also include an ML model as the final step. This makes everything even cleaner:

```python
# ─────────────────────────────────────────────────────────────────────────────
# FULL PIPELINE WITH MODEL INCLUDED
# ─────────────────────────────────────────────────────────────────────────────

from sklearn.linear_model import LinearRegression

# Build the full pipeline: preprocessing + model
full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),    # All the transformation steps
    ('model', LinearRegression())      # The ML model
])

# .fit() on the full pipeline:
# - Fits all preprocessors on X_train
# - Trains the LinearRegression model on the preprocessed X_train
full_pipeline.fit(X_train, y_train)

# .predict() on new data:
# - Applies all preprocessing steps using training-learned parameters
# - Then runs the model to produce predictions
y_pred = full_pipeline.predict(X_test)

print("Sample predictions vs actual prices:")
comparison = pd.DataFrame({
    'Actual Price': y_test.values[:5],
    'Predicted Price': y_pred[:5].round(0)
})
print(comparison)

# BENEFITS OF FULL PIPELINE:
# 1. One .fit() call trains everything
# 2. One .predict() call handles all transformations + prediction
# 3. Easy to save and deploy — save the entire pipeline, not separate pieces
# 4. Leakage-proof by design
# 5. Easy to swap models — just change 'LinearRegression()' to another model
```

---

## 7. Quick Reference Cheat Sheet

### Preprocessing Decision Tree

```
Is data missing?
├── Yes
│   ├── < 5% rows affected → Drop rows
│   ├── Numeric column → Impute with median (if outliers) or mean
│   └── Categorical column → Impute with mode (most frequent)
│
└── No → Continue

Are there outliers?
├── Detect with IQR rule: flag values outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
├── If data entry error → Remove or correct
└── If genuine but extreme → Cap with .clip()

Is a column categorical?
├── No natural order (Urban, Suburban, Rural) → OneHotEncoder
└── Has natural order (Poor → Excellent) → OrdinalEncoder

Are features on different scales?
├── Using distance/gradient-based model → Scale (StandardScaler usually)
└── Using tree-based model → No scaling needed
```

### Feature Engineering Quick Reference

| Technique | When to Use | Example |
|---|---|---|
| Interaction features | When the combination is meaningful | price_per_sqft = price / area |
| Log transformation | When distribution is right-skewed | log(price) |
| Binning | When groups matter more than exact values | house_age → New/Old/Very Old |
| Time extraction | When date column exists | sale_month, is_weekend |
| Ratio features | When relative values matter | bed_bath_ratio |

### Scaler Comparison

| Scaler | Formula | Output Range | Best For |
|---|---|---|---|
| StandardScaler | (x − mean) / std | Usually −3 to 3 | General use, linear models |
| MinMaxScaler | (x − min) / (max − min) | 0 to 1 | Neural networks |

### Encoder Comparison

| Encoder | When | Example |
|---|---|---|
| OneHotEncoder | No order between categories | Colour: Red, Blue, Green |
| OrdinalEncoder | Natural ordering exists | Size: S < M < L < XL |

### The Key Sequence

```
Raw Data
   ↓
EDA → Understand data, find problems, create action plan
   ↓
Preprocessing → Fix missing values, outliers, encode categories, scale features
   ↓
Feature Engineering → Create new meaningful features from existing ones
   ↓
Train-Test Split → Split BEFORE fitting any transformer
   ↓
Pipeline → Fit preprocessors on train only, transform both train and test
   ↓
Model Training → Ready for ML!
```

---

> **Final Thought:** Every decision in this guide — whether to impute or drop, which encoder to use, whether to scale — should be driven by understanding your data (from EDA) and understanding your model. The goal is not to blindly apply all these tools, but to ask: *"What does my data need, and why?"*
>
> A strong data preparation process is often more impactful than choosing the "best" model. A well-prepared dataset with a simple model frequently outperforms a poorly prepared dataset with a complex one.

---

*Guide prepared for AIML internship evaluation preparation — covering EDA, Preprocessing, and Feature Engineering with a consistent housing prices dataset throughout.*
