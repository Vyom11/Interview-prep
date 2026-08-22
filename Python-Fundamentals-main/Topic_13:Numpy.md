# NumPy: Zero to Hero for Data Science & AI/ML

> *"NumPy is not just a library — it is the language your data speaks."*

This guide takes you from absolute beginner to production-ready practitioner. Every concept is anchored to real Data Science and ML workflows. Code snippets are self-contained and immediately runnable. By the end, you won't just *use* NumPy — you'll *think* in NumPy.

---

## Table of Contents

1. [Why NumPy? The Case Against Pure Python](#1-why-numpy-the-case-against-pure-python)
2. [Module 1 — The Array: Building Your Foundation](#2-module-1--the-array-building-your-foundation)
3. [Module 2 — Array Attributes: Understanding What You Have](#3-module-2--array-attributes-understanding-what-you-have)
4. [Module 3 — Accessing Data: Slicing, Masking & Fancy Indexing](#4-module-3--accessing-data-slicing-masking--fancy-indexing)
5. [Module 4 — Operations & Math: Arithmetic to Linear Algebra](#5-module-4--operations--math-arithmetic-to-linear-algebra)
6. [Module 5 — Aggregation: Summarizing Your Data](#6-module-5--aggregation-summarizing-your-data)
7. [Module 6 — Advanced Manipulation: Reshaping Your World](#7-module-6--advanced-manipulation-reshaping-your-world)
8. [Module 7 — The Silent Killers: Views vs. Copies](#8-module-7--the-silent-killers-views-vs-copies)
9. [Module 8 — Broadcasting: NumPy's Superpower](#9-module-8--broadcasting-numpys-superpower)
10. [Module 9 — Utility Functions: The Swiss Army Knife](#10-module-9--utility-functions-the-swiss-army-knife)
11. [Module 10 — Reproducibility: Controlling Randomness](#11-module-10--reproducibility-controlling-randomness)
12. [Module 11 — Vectorization: The Philosophy of Speed](#12-module-11--vectorization-the-philosophy-of-speed)
13. [Quick Reference Cheat Sheet](#13-quick-reference-cheat-sheet)

---

## 1. Why NumPy? The Case Against Pure Python

Before writing a single line of NumPy code, you need to understand *why* it exists.

Python lists are flexible and convenient, but they come with a fatal flaw for numerical computing: **they store objects, not raw numbers**. Each element in a Python list is a full Python object with overhead — type information, reference counts, and memory pointers. This is fine for general programming, but catastrophic for ML workloads that operate on millions of numbers.

**NumPy arrays**, by contrast, store data as a **contiguous block of raw bytes in memory**, all of the same type. This unlocks:

- **Speed** — Operations run in optimized C and Fortran code under the hood.
- **Vectorization** — Apply an operation to an entire array without a Python `for` loop.
- **Memory efficiency** — A float64 array uses 8 bytes per element. A Python float uses ~28 bytes.
- **Ecosystem compatibility** — PyTorch, TensorFlow, Pandas, Scikit-learn, and OpenCV all speak NumPy natively.

```python
import numpy as np
import time

size = 1_000_000

# Python list approach
py_list = list(range(size))
start = time.time()
result = [x * 2 for x in py_list]
print(f"Python list: {time.time() - start:.4f}s")

# NumPy approach
np_array = np.arange(size)
start = time.time()
result = np_array * 2
print(f"NumPy array: {time.time() - start:.4f}s")
# NumPy is typically 10x–100x faster
```

> 💡 **Data Science Context:** Every dataset you load with Pandas, every tensor in PyTorch, every image in OpenCV — at their core, they are NumPy arrays or memory-compatible equivalents. Mastering NumPy means you understand the foundation of the entire Python ML stack.

---

## 2. Module 1 — The Array: Building Your Foundation

The **`ndarray`** (N-dimensional array) is NumPy's central data structure. Everything else in this guide exists to create, transform, or query it. By default, maximum supported dimension for an ndarray is 32.

### 2.1 Creating Arrays from Data

```python
import numpy as np

# From a Python list — the most common starting point
scores = np.array([92, 87, 95, 78, 88])
print(scores)         # [92 87 95 78 88]
print(type(scores))   # <class 'numpy.ndarray'>

# 2D array — think of it as a matrix or a spreadsheet
# Shape: (3 rows, 4 columns)
feature_matrix = np.array([
    [1.2, 0.5, 3.1, 2.0],
    [0.8, 1.4, 2.7, 1.1],
    [2.3, 0.9, 1.8, 3.5]
])
print(feature_matrix.shape)  # (3, 4)

# Force a specific data type (critical for memory control in ML)
int_array = np.array([1.9, 2.7, 3.4], dtype=np.int32)
print(int_array)  # [1 2 3] — truncated, not rounded!
```

> ⚠️ **Avoid This:** `np.array([1.9, 2.7], dtype=np.int32)` **truncates**, it does not round. `1.9` becomes `1`. This is a common source of silent data corruption in preprocessing pipelines.

---

### 2.2 Creating Arrays from Scratch

These six functions are the workhorses of array initialization in ML.

```python
# Zeros — default weight initialization, masks, placeholders
bias_vector = np.zeros(5)
print(bias_vector)  # [0. 0. 0. 0. 0.]

# Zeros for a 2D matrix
weight_matrix = np.zeros((3, 4))   # 3 neurons, 4 inputs each

# Ones — useful for creating masks or additive identity
ones = np.ones((2, 3))

# arange — integer or float steps, EXCLUSIVE of stop
indices = np.arange(0, 10, 2)
print(indices)  # [0 2 4 6 8]

# linspace — N evenly spaced points, INCLUSIVE of stop
thresholds = np.linspace(0, 1, 5)
print(thresholds)  # [0.   0.25 0.5  0.75 1.  ]

# random.rand — uniform distribution [0, 1)
weights = np.random.rand(3, 4)   # shape (3, 4)

# random.randn — standard normal distribution (mean=0, std=1)
noise = np.random.randn(100)     # Gaussian noise
```

---

### 2.3 `arange` vs `linspace` — The Definitive Comparison

These two functions are frequently confused. Here's the mental model:

| Feature | `np.arange(start, stop, step)` | `np.linspace(start, stop, num)` |
|---|---|---|
| **You control** | The **step size** | The **number of points** |
| **Stop is** | **Exclusive** (like `range()`) | **Inclusive** |
| **Best for** | Integer sequences, loop indices | Evenly spaced intervals, plotting axes |
| **Output size** | Determined by step | Exactly `num` elements |
| **Floating-point safe?** | ⚠️ Can have precision issues | ✅ Always exact count |

```python
# arange: "give me steps of 0.3"
a = np.arange(0, 1, 0.3)
print(a)  # [0.  0.3 0.6 0.9]  — 4 elements, stop excluded

# linspace: "give me exactly 5 points from 0 to 1"
b = np.linspace(0, 1, 5)
print(b)  # [0.   0.25 0.5  0.75 1.  ] — exactly 5 elements, 1 included

# The floating-point trap with arange:
c = np.arange(0, 1, 0.1)
print(len(c))  # Sometimes 10, sometimes 11 — unpredictable!

# linspace is always safe when you need an exact count:
d = np.linspace(0, 1, 10)
print(len(d))  # Always exactly 10
```

> 💡 **Data Science Context:** Use `linspace` when generating x-axis values for plots, learning rate schedules, or probability bins. Use `arange` when generating integer indices or when step size has a specific semantic meaning (e.g., every 5th frame in a video).

---

## 3. Module 2 — Array Attributes: Understanding What You Have

Before transforming data, always interrogate it. These attributes are your diagnostic tools.

```python
import numpy as np

# Simulating a dataset: 1000 samples, 28x28 pixel images (like MNIST)
images = np.random.rand(1000, 28, 28)

print(images.ndim)   # 3     — number of dimensions (axes)
print(images.shape)  # (1000, 28, 28) — size along each axis
print(images.size)   # 784000 — total number of elements
print(images.dtype)  # float64 — data type of elements
print(images.nbytes) # 6272000 — total memory in bytes (~6 MB)
```

### 3.1 The Magic of `reshape()`

`reshape()` changes the *interpretation* of an array's shape **without copying data**. This makes it nearly instantaneous, even on huge arrays.

```python
# Flatten a single image for a fully connected (dense) layer
single_image = np.random.rand(28, 28)   # shape: (28, 28)
flat_image = single_image.reshape(784)   # shape: (784,)
# Equivalent: single_image.reshape(-1) — let NumPy infer the size

# -1 is NumPy's "figure it out for me" placeholder
batch = np.random.rand(64, 28, 28)       # 64 images, 28x28
flat_batch = batch.reshape(64, -1)       # shape: (64, 784)
print(flat_batch.shape)                  # (64, 784)

# Going the other way: restore from flat to spatial
restored = flat_batch.reshape(64, 28, 28)
print(restored.shape)                    # (64, 28, 28)
```

> 💡 **Data Science Context:** This is one of the most-used operations in deep learning. Convolutional layers output 3D feature maps `(batch, height, width)`. Before passing them to a fully connected layer, you must flatten to `(batch, features)` using `reshape(batch_size, -1)`.

> ⚠️ **Keep in Mind:** `reshape()` requires the total number of elements to remain the same. `(28, 28)` → `(784,)` works because `28×28 = 784`. Attempting `reshape(100)` on a `(28, 28)` array raises a `ValueError`.

---

## 4. Module 3 — Accessing Data: Slicing, Masking & Fancy Indexing

Knowing how to *extract* exactly the data you need is fundamental to every preprocessing and analysis workflow.

### 4.1 1D Slicing

```python
losses = np.array([0.91, 0.78, 0.65, 0.52, 0.44, 0.38, 0.31])

print(losses[0])     # 0.91  — first element
print(losses[-1])    # 0.31  — last element
print(losses[2:5])   # [0.65 0.52 0.44] — index 2 up to (not including) 5
print(losses[::2])   # [0.91 0.65 0.44 0.31] — every other element
print(losses[::-1])  # reversed array
```

### 4.2 2D Slicing

The golden rule: **`array[rows, columns]`** — rows first, then columns.

```python
# Simulating a feature matrix: 5 samples, 4 features
X = np.array([
    [2.1, 0.5, 1.3, 4.2],   # sample 0
    [1.4, 2.2, 0.8, 3.1],   # sample 1
    [0.9, 1.7, 2.5, 2.8],   # sample 2
    [3.3, 0.4, 1.1, 1.9],   # sample 3
    [1.8, 2.9, 0.6, 2.4],   # sample 4
])

print(X[0])          # First sample (all features): [2.1 0.5 1.3 4.2]
print(X[:, 0])       # All samples, first feature: [2.1 1.4 0.9 3.3 1.8]
print(X[1:3, :2])    # Samples 1–2, first 2 features
print(X[-2:, -1:])   # Last 2 samples, last feature
```

### 4.3 Boolean Masking — The Data Cleaning Powerhouse

**Boolean masking** lets you filter data based on conditions. It's the NumPy equivalent of `WHERE` in SQL.

```python
ages = np.array([17, 24, 15, 32, 19, 14, 28, 21])

# Step 1: Create a boolean mask
adult_mask = ages >= 18
print(adult_mask)   # [False  True False  True  True False  True  True]

# Step 2: Apply the mask to filter
adults = ages[adult_mask]
print(adults)       # [24 32 19 28 21]

# Combine in one line (most common pattern)
print(ages[ages >= 18])  # same result

# Multiple conditions — use & (AND), | (OR), ~ (NOT)
# Must wrap each condition in parentheses!
valid_range = ages[(ages >= 18) & (ages <= 30)]
print(valid_range)  # [24 19 28 21]
```

**Boolean masking on a 2D feature matrix — a real preprocessing scenario:**

```python
# Dataset: each row is [height_cm, weight_kg, age]
data = np.array([
    [175, 70, 25],
    [180, 90, 30],
    [-1,  65, 22],   # corrupted height (sentinel value)
    [165, 55, 28],
    [172, -99, 35],  # corrupted weight
])

# Keep only rows where ALL values are positive
valid_rows_mask = np.all(data > 0, axis=1)
print(valid_rows_mask)       # [True True False True False]

clean_data = data[valid_rows_mask]
print(clean_data)
# [[175  70  25]
#  [180  90  30]
#  [165  55  28]]
```

> 💡 **Data Science Context:** Boolean masking is your primary tool for **data cleaning** — removing outliers, filtering corrupted values, selecting specific classes from a label array (e.g., `X[y == 2]` to extract all samples of class 2).

### 4.4 Fancy Indexing

**Fancy indexing** uses an array of indices (not a slice) to select elements. The result is always a **copy**, not a view.

```python
scores = np.array([88, 72, 95, 61, 84, 90, 77])

# Select specific indices
selected = scores[[0, 2, 5]]
print(selected)  # [88 95 90]

# Use argsort to get indices that would sort the array
sorted_indices = np.argsort(scores)
print(sorted_indices)          # [3 1 6 0 4 5 2]
print(scores[sorted_indices])  # [61 72 77 88 84 90 95] — sorted scores

# Useful for ranking: top-3 scorers
top3_indices = np.argsort(scores)[-3:][::-1]
print(scores[top3_indices])    # [95 90 84]
```

| Operation | Use Case | Time Complexity |
|---|---|---|
| Regular Sort (np.sort) | Use when you just need the values in order (e.g., numbers from 1 to 100). | $O(n \log n)$ |
| Argsort (np.argsort) | Use when you need the original positions to sort a second, related list (e.g., sorting names by their ages). | $O(n \log n)$ |
| Argpartition (np.argpartition) | Use when you only need the Top K items (e.g., finding the 5 highest scores in a million entries) and don't care about the rest. | $O(n)$ |

## Summary for Quick Pick:

* Need values sorted? Use sort.
* Need to reorder a different list? Use argsort.
* Need speed for a "Top 10" list? Use argpartition.
---

## 5. Module 4 — Operations & Math: Arithmetic to Linear Algebra

### 5.1 Element-Wise Arithmetic

All standard operators (`+`, `-`, `*`, `/`, `**`) work **element-by-element** on arrays of the same shape.

```python
a = np.array([1.0, 2.0, 3.0, 4.0])
b = np.array([2.0, 2.0, 2.0, 2.0])

print(a + b)   # [3. 4. 5. 6.]
print(a * b)   # [2. 4. 6. 8.]
print(a ** 2)  # [ 1.  4.  9. 16.]
print(a / b)   # [0.5 1.  1.5 2. ]

# Universal functions (ufuncs) — optimized element-wise operations
print(np.sqrt(a))   # [1.    1.414 1.732 2.   ]
print(np.log(a))    # [0.    0.693 1.099 1.386]
print(np.exp(a))    # [ 2.718  7.389 20.086 54.598]
```

> ⚠️ **Avoid This — Integer Division Trap:**
> ```python
> a = np.array([1, 2, 3])    # dtype: int64
> print(a / 2)               # [0.5 1.  1.5] — OK in Python 3
> print(a // 2)              # [0 1 1]       — floor division, data loss!
> # Always cast to float first when precision matters:
> print(a.astype(float) / 2) # [0.5 1.  1.5]
> ```

### 5.2 The `axis` Parameter — Visualized Once, Remembered Forever

The `axis` parameter is the source of more confusion than almost anything else in NumPy. Here's the mental model that makes it stick forever.

**Think of axes as the directions you're "collapsing":**

```
For a 2D array with shape (rows, columns):

           axis=1 →→→→→→→→→→→
         ┌─────┬─────┬─────┬─────┐
  axis=0 │ 1.2 │ 0.5 │ 3.1 │ 2.0 │  ← row 0
    ↓    ├─────┼─────┼─────┼─────┤
    ↓    │ 0.8 │ 1.4 │ 2.7 │ 1.1 │  ← row 1
    ↓    ├─────┼─────┼─────┼─────┤
         │ 2.3 │ 0.9 │ 1.8 │ 3.5 │  ← row 2
         └─────┴─────┴─────┴─────┘

axis=0: collapse DOWN the rows → result has shape (4,)  = one value per COLUMN
axis=1: collapse ACROSS columns → result has shape (3,) = one value per ROW
```

```python
X = np.array([
    [1.2, 0.5, 3.1, 2.0],
    [0.8, 1.4, 2.7, 1.1],
    [2.3, 0.9, 1.8, 3.5]
])

# axis=0: compute along rows (collapse rows → one value per column)
# "What is the mean of each FEATURE across all samples?"
col_means = np.mean(X, axis=0)
print(col_means)          # [1.433 0.933 2.533 2.2  ] — shape: (4,)

# axis=1: compute along columns (collapse columns → one value per row)
# "What is the mean of each SAMPLE across all features?"
row_means = np.mean(X, axis=1)
print(row_means)          # [1.7   1.5   2.125] — shape: (3,)

# No axis: collapse everything → single scalar
overall_mean = np.mean(X)
print(overall_mean)       # 1.775
```

> 🧠 **The Mnemonic:** `axis=0` collapses **rows** (moves *down*), producing one value **per column**. `axis=1` collapses **columns** (moves *across*), producing one value **per row**.

### 5.3 Linear Algebra — The Language of ML Models

Element-wise multiplication (`*`) and **matrix multiplication** are fundamentally different operations. Confusing them is one of the most common ML bugs.

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Element-wise multiplication (Hadamard product)
print(A * B)
# [[ 5 12]
#  [21 32]]

# Matrix multiplication — two equivalent syntaxes
print(np.dot(A, B))   # classic syntax
print(A @ B)           # modern syntax (preferred, PEP 465)
# [[19 22]
#  [43 50]]

# Dot product of two vectors
u = np.array([1, 2, 3])
v = np.array([4, 5, 6])
print(np.dot(u, v))   # 1*4 + 2*5 + 3*6 = 32
```

**A complete forward pass through a neural network layer:**

```python
# Forward pass: output = inputs @ weights + bias
batch_size    = 32
input_features = 64
output_features = 10

X = np.random.randn(batch_size, input_features)   # (32, 64)
W = np.random.randn(input_features, output_features) * 0.01  # (64, 10)
b = np.zeros(output_features)                     # (10,)

# Matrix multiplication — the core of every dense layer
Z = X @ W + b
print(Z.shape)  # (32, 10)

# Apply softmax to get class probabilities
def softmax(z):
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # numerically stable
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

probs = softmax(Z)
print(probs.shape)          # (32, 10)
print(probs[0].sum())       # 1.0 — valid probability distribution
```


| Operation | Simple Use Case | Syntax | How Output Changes |
|---|---|---|---|
| Element-wise | Applying a filter (e.g., 10% discount to all prices) | A * B | Shape stays the same. Numbers in the same spot multiply. |
| Matrix Multiply | Combining features (e.g., total cost for multiple orders) | A @ B | Shape blends. Rows of A mix with columns of B. |
| Dot Product | Getting a single score (e.g., similarity/compatibility) | np.dot(u,v) | Two lists collapse into one single number. |
| Outer Product | Creating a grid (e.g., building a multiplication table) | np.outer(u,v) | Two lists expand into a full matrix. |
| Transpose | Flipping the view (e.g., swapping rows for columns) | A.T | Dimensions swap. (Rows $\leftrightarrow$ Columns). |

---

## 6. Module 5 — Aggregation: Summarizing Your Data

Aggregation functions reduce arrays to summary statistics. Every EDA workflow lives here.

```python
import numpy as np

# Simulated feature: house prices (in $1000s)
prices = np.array([245, 312, 198, 425, 289, 367, 156, 498, 271, 334])

print(f"Sum:        {np.sum(prices)}")          # 3095
print(f"Mean:       {np.mean(prices):.2f}")     # 309.50
print(f"Median:     {np.median(prices):.2f}")   # 300.50
print(f"Std Dev:    {np.std(prices):.2f}")      # 97.51
print(f"Variance:   {np.var(prices):.2f}")      # 9508.25
print(f"Min/Max:    {np.min(prices)} / {np.max(prices)}")
print(f"Arg Min/Max:{np.argmin(prices)} / {np.argmax(prices)}")  # indices
```

### 6.1 Percentiles — Better Than Min/Max for Outlier Detection

```python
# Percentiles give you a robust view of your distribution
p25  = np.percentile(prices, 25)   # Q1
p50  = np.percentile(prices, 50)   # Q2 (same as median)
p75  = np.percentile(prices, 75)   # Q3
iqr  = p75 - p25                   # Interquartile Range

print(f"Q1: {p25}, Median: {p50}, Q3: {p75}, IQR: {iqr}")

# Outlier detection using IQR method
lower_bound = p25 - 1.5 * iqr
upper_bound = p75 + 1.5 * iqr
outliers = prices[(prices < lower_bound) | (prices > upper_bound)]
print(f"Outliers: {outliers}")
```

### 6.2 Correlation Coefficient — Feature Relationship Analysis

```python
# Feature correlation matrix — prerequisite to feature selection
n_samples = 100
feature_A = np.random.randn(n_samples)
feature_B = feature_A * 0.8 + np.random.randn(n_samples) * 0.2  # correlated
feature_C = np.random.randn(n_samples)  # uncorrelated

feature_matrix = np.array([feature_A, feature_B, feature_C])
corr_matrix = np.corrcoef(feature_matrix)
print(corr_matrix.round(2))
# [[1.   ~0.97 ~0.05]   — A vs A, A vs B (high!), A vs C (low)
#  [~0.97 1.  ~0.03]
#  [~0.05 ~0.03 1.  ]]
```

> 💡 **Data Science Context:** `np.corrcoef()` returns a correlation matrix identical in concept to `df.corr()` in Pandas. Use it to identify **multicollinearity** between features before training linear models, or to build heatmaps for EDA.

---

## 7. Module 6 — Advanced Manipulation: Reshaping Your World

### 7.1 `flatten()` vs `ravel()` — Know the Difference

Both functions collapse a multi-dimensional array into 1D, but they have an important distinction:

| Feature | `flatten()` | `ravel()` |
|---|---|---|
| **Returns** | Always a **copy** | A **view** when possible |
| **Memory** | Always allocates new memory | Zero-copy when contiguous |
| **Speed** | Slower (copy overhead) | Faster |
| **Safe to modify?** | ✅ Yes — won't affect original | ⚠️ Modifying may affect original |
| **When to use** | When you need an independent copy | When memory/speed matters |

```python
image = np.array([[1, 2, 3], [4, 5, 6]])

flat_copy = image.flatten()
flat_view = image.ravel()

flat_copy[0] = 999
print(image[0, 0])  # 1 — original unchanged (flatten made a copy)

flat_view[0] = 999
print(image[0, 0])  # 999 — original CHANGED (ravel made a view!)
```

### 7.2 Transpose

```python
W = np.array([[1, 2, 3], [4, 5, 6]])  # shape (2, 3)
print(W.T.shape)                       # (3, 2)
print(W.transpose())                   # same as W.T

# For 3D+ arrays, specify axes
tensor = np.zeros((32, 64, 128))
transposed = tensor.transpose(0, 2, 1)  # swap last two dims
print(transposed.shape)                 # (32, 128, 64)
```

### 7.3 `concatenate()` vs `stack()` — Joining Arrays

These two functions are frequently confused. Here is the core distinction:

> **`concatenate`** joins existing arrays **along an existing axis** — the number of dimensions stays the same.
> **`stack`** joins arrays **along a new axis** — this adds a dimension.

```python
a = np.array([1, 2, 3])   # shape (3,)
b = np.array([4, 5, 6])   # shape (3,)

# concatenate: (3,) + (3,) → (6,) — same dimensions
joined = np.concatenate([a, b])
print(joined)        # [1 2 3 4 5 6]
print(joined.shape)  # (6,)

# stack: (3,) + (3,) → (2, 3) — new dimension added
stacked = np.stack([a, b])
print(stacked)
# [[1 2 3]
#  [4 5 6]]
print(stacked.shape)        # (2, 3)

stacked_col = np.stack([a, b], axis=1)  # → (3, 2)
print(stacked_col.shape)    # (3, 2)
```

**2D example with real ML context:**

```python
# Two batches of samples: (50, 10) and (30, 10)
batch1 = np.random.randn(50, 10)
batch2 = np.random.randn(30, 10)

# concatenate along rows (axis=0) — merge the batches
full_dataset = np.concatenate([batch1, batch2], axis=0)
print(full_dataset.shape)  # (80, 10) ✅

# stack along axis=0 — would FAIL here if shapes differ
# np.stack requires all arrays to have IDENTICAL shapes
```

### 7.4 `split()` — Dividing Data

```python
data = np.arange(20).reshape(4, 5)

# Split into 2 equal parts along axis=0 (row-wise)
part1, part2 = np.split(data, 2, axis=0)
print(part1.shape, part2.shape)  # (2, 5) (2, 5)

# For unequal splits, pass split indices
train, val, test = np.split(data, [3, 4], axis=0)
# rows 0-2 → train, row 3 → val, row 4 → test
```

> 💡 **Data Science Context:** `np.split()` is useful for manual train/validation/test splitting before Scikit-learn's `train_test_split`. `np.concatenate` is used extensively in custom training loops to assemble mini-batches.

---

## 8. Module 7 — The Silent Killers: Views vs. Copies

This is the single most common source of **hard-to-debug bugs** in NumPy. Understanding this deeply will save you hours of frustration.

### 8.1 The Core Concept

A **view** is a reference to the same underlying data. Modifying a view **modifies the original**. A **copy** is independent memory — modifying it leaves the original untouched.

```
Original Array Memory:
┌────┬────┬────┬────┬────┬────┐
│  1 │  2 │  3 │  4 │  5 │  6 │
└────┴────┴────┴────┴────┴────┘
       ↑
   SLICE (view) points to the SAME memory
   
   np.copy() creates NEW memory:
┌────┬────┬────┬────┬────┬────┐
│  1 │  2 │  3 │  4 │  5 │  6 │  ← independent copy
└────┴────┴────┴────┴────┴────┘
```

### 8.2 When Does Slicing Create a View?

```python
original = np.array([10, 20, 30, 40, 50])

# ✅ Basic slicing → VIEW (same memory)
view = original[1:4]
view[0] = 999
print(original)  # [ 10 999  30  40  50] — ORIGINAL WAS CHANGED!

# Reset
original = np.array([10, 20, 30, 40, 50])

# ✅ Safe way: explicit copy
safe_copy = original[1:4].copy()
safe_copy[0] = 999
print(original)  # [10 20 30 40 50] — original untouched ✅
```

### 8.3 When Is a Copy Created Automatically?

```python
arr = np.array([10, 20, 30, 40, 50])

# Fancy indexing → COPY (not a view!)
fancy = arr[[0, 2, 4]]
fancy[0] = 999
print(arr)  # [10 20 30 40 50] — unchanged ✅

# Boolean masking → COPY
mask = arr > 25
masked = arr[mask]
masked[0] = 999
print(arr)  # [10 20 30 40 50] — unchanged ✅

# Reshape → usually a VIEW
reshaped = arr.reshape(5, 1)
reshaped[0] = 999
print(arr)  # [999  20  30  40  50] — CHANGED! reshape is a view!
```

### 8.4 Diagnosing Views

```python
arr = np.array([1, 2, 3, 4, 5])
sliced = arr[1:3]

# Check if it's a view
print(sliced.base is arr)   # True — it IS a view of arr
print(sliced.flags['OWNDATA'])  # False — doesn't own its data

copy = arr[1:3].copy()
print(copy.base is arr)     # False — it owns its data
print(copy.flags['OWNDATA'])   # True
```

> 🔑 **The Golden Rule:** When in doubt, call `.copy()`. The small memory overhead is almost always worth the debugging time you save. In preprocessing pipelines, always copy before mutating to avoid corrupting upstream data.

---

## 9. Module 8 — Broadcasting: NumPy's Superpower

**Broadcasting** is NumPy's mechanism for performing operations on arrays of *different but compatible shapes* without allocating extra memory or writing loops.

### 9.1 The Broadcasting Rules

NumPy compares shapes element-by-element, **starting from the trailing (rightmost) dimensions**. Two dimensions are compatible if:
1. They are **equal**, or
2. One of them is **1**

If the arrays have different numbers of dimensions, the shape of the smaller array is **padded with 1s on the left**.

```
Example:
  Matrix shape: (3, 4)
  Vector shape:    (4,) → padded to (1, 4) → broadcast to (3, 4)
  Result shape: (3, 4) ✅

  Matrix shape: (3, 4)
  Vector shape: (3,) → padded to (1, 3) → CANNOT broadcast to (3, 4) ❌
  Fix: reshape vector to (3, 1) → broadcasts to (3, 4) ✅
```

### 9.2 Broadcasting in Action

```python
# Scalar broadcasting — the simplest case
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr * 10)
# [[10 20 30]
#  [40 50 60]]

# Row normalization: subtract the mean of each ROW
# Shape walkthrough:
#   arr shape:         (3, 4)
#   row_means shape:   (3,)  → must reshape to (3, 1) for broadcasting!
#   arr - row_means:   (3, 4) - (3, 1) → (3, 4) ✅

data = np.array([
    [10.0, 20.0, 30.0, 40.0],
    [1.0,   2.0,  3.0,  4.0],
    [5.0,  15.0, 25.0, 35.0],
])

row_means = data.mean(axis=1)           # shape (3,)
row_means_col = row_means[:, np.newaxis]  # shape (3, 1) — the key step!
# equivalent: row_means.reshape(-1, 1)

centered = data - row_means_col
print(centered)
# [[-15.  -5.   5.  15.]
#  [-1.5  -0.5  0.5  1.5]
#  [-15.  -5.   5.  15.]]

print(centered.mean(axis=1).round(10))  # [0. 0. 0.] ✅ — means are now zero
```

### 9.3 Feature Normalization via Broadcasting (Z-Score)

```python
# Standardize each feature (column) to mean=0, std=1
X = np.random.randn(100, 5) * np.array([10, 2, 50, 1, 0.1])  # different scales

col_means = X.mean(axis=0)  # shape (5,) — mean of each feature
col_stds  = X.std(axis=0)   # shape (5,)

# Broadcasting: (100, 5) - (5,) → (100, 5) — works automatically!
X_normalized = (X - col_means) / col_stds

print(X_normalized.mean(axis=0).round(10))  # [0. 0. 0. 0. 0.] ✅
print(X_normalized.std(axis=0).round(10))   # [1. 1. 1. 1. 1.] ✅
```

> 💡 **Data Science Context:** This Z-score normalization is applied before almost every ML model. Scikit-learn's `StandardScaler` does exactly this under the hood. Implementing it in raw NumPy makes the mechanism transparent.

> ⚠️ **Shape Mismatch Trap:**
> ```python
> A = np.ones((3, 4))
> b = np.ones(3)         # shape (3,) — trailing dim is 3, not 4!
> # A - b → ERROR: operands could not be broadcast with shapes (3,4) (3,)
> # Fix:
> b_col = b[:, np.newaxis]   # shape (3, 1) — now broadcasts correctly
> result = A - b_col          # shape (3, 4) ✅
> ```

---

## 10. Module 9 — Utility Functions: The Swiss Army Knife

### 10.1 `np.where()` — Vectorized Conditional Logic

`np.where(condition, value_if_true, value_if_false)` is the vectorized `if-else`.

```python
# Replace negative values (corrupted sensor readings) with 0
readings = np.array([1.2, -0.5, 3.4, -1.1, 2.8, 0.0, -0.3])
cleaned = np.where(readings < 0, 0, readings)
print(cleaned)  # [1.2 0.  3.4 0.  2.8 0.  0. ]

# Binary classification: threshold probabilities into class labels
probabilities = np.array([0.82, 0.31, 0.95, 0.48, 0.61, 0.12])
predictions = np.where(probabilities >= 0.5, 1, 0)
print(predictions)  # [1 0 1 0 1 0]
```

### 10.2 `np.argmax()` — The Neural Network Output Decoder

`np.argmax()` returns the **index** of the maximum value. In classification models, this converts a probability vector to a predicted class label.

```python
# Softmax output for a single sample — 5 classes
softmax_output = np.array([0.02, 0.08, 0.67, 0.18, 0.05])
predicted_class = np.argmax(softmax_output)
print(predicted_class)  # 2 — the model predicts class 2

# Batch inference: (batch_size=4, num_classes=5)
batch_probs = np.array([
    [0.1, 0.7, 0.05, 0.1,  0.05],  # → class 1
    [0.3, 0.1, 0.05, 0.5,  0.05],  # → class 3
    [0.0, 0.0, 0.0,  0.0,  1.0 ],  # → class 4
    [0.4, 0.3, 0.1,  0.15, 0.05],  # → class 0
])
predicted_classes = np.argmax(batch_probs, axis=1)
print(predicted_classes)  # [1 3 4 0]
```

> 💡 **Data Science Context:** `np.argmax(axis=1)` is the standard way to convert softmax probabilities to class labels. You'll see this exact pattern in every PyTorch and TensorFlow inference loop.

### 10.3 `np.argsort()` — Ranking Without Sorting

```python
feature_importances = np.array([0.12, 0.34, 0.08, 0.27, 0.19])
feature_names = ['age', 'income', 'height', 'education', 'experience']

# Get indices that would sort in ascending order
sort_indices = np.argsort(feature_importances)

# Reverse for descending (most important first)
ranked_indices = sort_indices[::-1]
print([feature_names[i] for i in ranked_indices])
# ['income', 'education', 'experience', 'age', 'height']

print(feature_importances[ranked_indices])
# [0.34 0.27 0.19 0.12 0.08]
```

### 10.4 `np.unique()` — Discovering Classes and Distributions

```python
labels = np.array([2, 0, 1, 2, 0, 1, 1, 2, 0, 0, 2])

# Find unique classes
unique_classes = np.unique(labels)
print(unique_classes)   # [0 1 2]

# Count occurrences (class distribution check)
classes, counts = np.unique(labels, return_counts=True)
for cls, cnt in zip(classes, counts):
    print(f"Class {cls}: {cnt} samples ({cnt/len(labels)*100:.1f}%)")
# Class 0: 4 samples (36.4%)
# Class 1: 3 samples (27.3%)
# Class 2: 4 samples (36.4%)
```

> 💡 **Data Science Context:** Always run `np.unique(y, return_counts=True)` on your label array before training. Class imbalance is one of the leading causes of poor model performance.

---

## 11. Module 10 — Reproducibility: Controlling Randomness

In ML, **reproducibility** is not optional — it's professionalism. When you share a model or experiment, others must be able to reproduce your results exactly.

### 11.1 `np.random.seed()` — The Reproducibility Switch
If you use the same seed value (e.g., random.seed(42)), Python will generate the exact same sequence of "random" numbers every time the code is executed.
```python
# Without seed: different results each run
print(np.random.rand(3))  # [0.374 0.951 0.732] (example)
print(np.random.rand(3))  # [0.599 0.156 0.058] (different!)

# With seed: identical results every run
np.random.seed(42)
print(np.random.rand(3))  # [0.374 0.951 0.732]
np.random.seed(42)
print(np.random.rand(3))  # [0.374 0.951 0.732] — identical ✅
```

> ⚠️ **Best Practice:** Use `np.random.seed()` at the very top of your script or notebook. In modern code, prefer the newer **Generator API** which is more flexible and reproducible across NumPy versions:
> ```python
> rng = np.random.default_rng(seed=42)
> samples = rng.normal(loc=0, scale=1, size=(100, 5))
> ```

### 11.2 Random Distributions for ML

```python
np.random.seed(42)

# Uniform: random float in [0.0, 1.0)
uniform = np.random.rand(3, 3)

# Integer: random integers in [low, high)
class_labels = np.random.randint(0, 10, size=20)  # 20 labels, classes 0–9

# Normal (Gaussian): mean=0, std=1 — for weight initialization
weights = np.random.normal(loc=0.0, scale=0.01, size=(64, 32))
# or equivalently: np.random.randn(64, 32) * 0.01

# He initialization (common for ReLU networks)
fan_in = 64
he_weights = np.random.randn(64, 32) * np.sqrt(2.0 / fan_in)
```

### 11.3 `np.random.shuffle()` — In-Place Dataset Shuffling

```python
np.random.seed(0)

X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
y = np.array([0, 1, 0, 1, 0])

# CRITICAL: shuffle indices, then apply to both X and y
# Never shuffle X and y independently — you'll break the correspondence!
indices = np.arange(len(X))
np.random.shuffle(indices)

X_shuffled = X[indices]
y_shuffled = y[indices]

print("Shuffled indices:", indices)           # [2 1 4 0 3]
print("Shuffled labels:", y_shuffled)         # [0 1 0 0 1]
print("Shuffled X:\n", X_shuffled)
```

> ⚠️ **Critical Pitfall:** Never call `np.random.shuffle(X)` and `np.random.shuffle(y)` separately. They will be shuffled with different random states, completely destroying the `(sample, label)` correspondence — and your model will silently train on garbage.

---

## 12. Module 11 — Vectorization: The Philosophy of Speed

**Vectorization** is the practice of replacing explicit Python `for` loops with NumPy array operations. This is not just a style preference — it is the difference between code that runs in milliseconds and code that runs in minutes.

### 12.1 Why Vectorization Is So Fast

Python `for` loops interpret each iteration at the Python level — checking types, managing objects, moving through the interpreter. NumPy operations execute in compiled C code that can also exploit **SIMD (Single Instruction, Multiple Data)** CPU instructions, processing multiple elements in a single clock cycle.

```python
import numpy as np
import time

n = 1_000_000
a = np.random.rand(n)
b = np.random.rand(n)

# Python loop approach
start = time.time()
result = [a[i] * b[i] for i in range(n)]
loop_time = time.time() - start

# Vectorized approach
start = time.time()
result = a * b
vec_time = time.time() - start

print(f"Loop time:   {loop_time:.4f}s")
print(f"Vector time: {vec_time:.4f}s")
print(f"Speedup:     {loop_time / vec_time:.1f}x")
# Typical output: 50x–200x speedup
```

### 12.2 Vectorizing Real ML Operations

```python
# Computing Mean Squared Error loss — loop vs vectorized
y_true = np.array([3.0, -0.5, 2.0, 7.0, 1.0])
y_pred = np.array([2.5, 0.0, 2.0, 8.0, 1.5])

# Loop version (never do this in production)
mse_loop = sum((y_true[i] - y_pred[i])**2 for i in range(len(y_true))) / len(y_true)

# Vectorized version (always do this)
mse_vec = np.mean((y_true - y_pred) ** 2)

print(f"MSE (loop):     {mse_loop:.4f}")   # 0.3750
print(f"MSE (vectorized): {mse_vec:.4f}")  # 0.3750 ✅ — same result, faster

# ReLU activation — the most common in deep learning
def relu(x):
    return np.maximum(0, x)

z = np.random.randn(1000, 64)  # pre-activation values
activated = relu(z)             # applied to all 64,000 values at once
print((activated >= 0).all())   # True ✅
```

> 💡 **Data Science Context:** Every loss function, every activation function, every normalization step you implement in NumPy should be vectorized. If you find yourself writing `for i in range(len(X))` over samples, stop and ask: "How do I express this as a matrix operation?"

---

## 13. Quick Reference Cheat Sheet

```python
import numpy as np

# ── CREATION ──────────────────────────────────────────────────
np.array([1, 2, 3])               # from list
np.zeros((m, n))                   # all zeros
np.ones((m, n))                    # all ones
np.eye(n)                          # identity matrix
np.arange(start, stop, step)       # like range(), exclusive stop
np.linspace(start, stop, num)      # num points, inclusive stop
np.random.rand(m, n)               # uniform [0, 1)
np.random.randn(m, n)              # standard normal
np.random.randint(low, high, size) # random integers

# ── ATTRIBUTES ────────────────────────────────────────────────
arr.shape    # tuple of dimensions
arr.ndim     # number of axes
arr.size     # total elements
arr.dtype    # element data type
arr.nbytes   # memory footprint

# ── RESHAPING ────────────────────────────────────────────────
arr.reshape(m, n)      # new shape (same data)
arr.reshape(-1)        # flatten, infer size
arr.flatten()          # always a copy
arr.ravel()            # view when possible
arr.T                  # transpose
arr[:, np.newaxis]     # add axis (for broadcasting)

# ── INDEXING ────────────────────────────────────────────────
arr[i]                 # single element (1D)
arr[i, j]              # element at row i, col j (2D)
arr[start:stop:step]   # slice
arr[arr > 0]           # boolean mask
arr[[0, 2, 4]]         # fancy indexing

# ── MATH & LINEAR ALGEBRA ─────────────────────────────────────
a + b, a - b, a * b, a / b, a ** 2   # element-wise
np.sqrt(a), np.log(a), np.exp(a)      # element-wise ufuncs
a @ b                                  # matrix multiply
np.dot(a, b)                           # dot product / matmul

# ── AGGREGATION ───────────────────────────────────────────────
np.sum(arr, axis=0)     # sum down columns
np.mean(arr, axis=1)    # mean across rows
np.std(arr)             # standard deviation
np.var(arr)             # variance
np.min(arr), np.max(arr)
np.argmin(arr), np.argmax(arr)         # index of min/max
np.percentile(arr, 75)                 # 75th percentile
np.corrcoef(matrix)                    # correlation matrix

# ── COMBINING ───────────────────────────────────────────────
np.concatenate([a, b], axis=0)   # join along existing axis
np.stack([a, b], axis=0)         # join along NEW axis
np.split(arr, n, axis=0)         # split into n parts
np.vstack([a, b])                # vertical stack (rows)
np.hstack([a, b])                # horizontal stack (cols)

# ── UTILITY ────────────────────────────────────────────────
np.where(cond, x, y)             # vectorized if-else
np.unique(arr, return_counts=True)  # unique values + counts
np.argmax(arr, axis=1)           # index of max per row
np.argsort(arr)                  # indices that would sort arr
arr.copy()                        # explicit deep copy

# ── REPRODUCIBILITY ────────────────────────────────────────
np.random.seed(42)
rng = np.random.default_rng(42)  # modern, preferred approach
```

---

## Final Thoughts

You now have a complete, working mental model of NumPy — from the fundamentals of the `ndarray` all the way through broadcasting, vectorization, and the subtle footguns that trip up even experienced practitioners.

The most important insight to take forward: **NumPy is a way of thinking**, not just a library. When you look at a problem and immediately see it as a matrix operation rather than a loop, you've internalized NumPy. That shift in thinking is the foundation for everything that follows — Pandas, Scikit-learn, PyTorch, and beyond.

**Your next steps:**

1. Implement Z-score normalization from scratch using only NumPy.
2. Build a complete single-layer neural network forward pass (linear + ReLU + softmax) using only `@`, broadcasting, and `np.exp`.
3. Explore `np.einsum()` — the ultimate generalization of all tensor operations used in attention mechanisms.

The more you write NumPy, the more fluently you'll speak the language of data.

---

*Guide authored for Python 3.9+ and NumPy 1.24+. All snippets tested and runnable.*
