# 🐼 Simple Beginner's Guide to Python Pandas

> A plain-English guide to pandas — the most popular Python library for working with data.

---

## What is Pandas?

Pandas is like a supercharged spreadsheet inside Python. It lets you load data from files, clean it, filter it, and summarize it — all without writing complex code.

```bash
pip install pandas       # Install it once
import pandas as pd      # Use 'pd' as a shortcut — everyone does this
```

---

## 1. Core Structures: Series and DataFrames

A **Series** is a single column of data (like one column in a spreadsheet).
A **DataFrame** is a full table with rows and columns.

```python
import pandas as pd

# Series — a single list with labels
ages = pd.Series([25, 30, 22], index=["Alice", "Bob", "Carol"])
print(ages["Bob"])  # 30

# DataFrame — a full table
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol"],
    "age":    [25, 30, 22],
    "salary": [70000, 85000, 60000]
})
print(df)
```

> 💡 `df["salary"]` → returns a **Series** (one column)
> 💡 `df[["salary"]]` → returns a **DataFrame** (still a table, just one column)

---

## 2. Reading & Writing Files

```python
# Read a CSV file
df = pd.read_csv("data.csv")

# Read only specific columns (saves memory)
df = pd.read_csv("data.csv", usecols=["name", "salary"])

# Read an Excel file
df = pd.read_excel("report.xlsx", sheet_name="Sheet1")

# Save to CSV — always use index=False to avoid an extra unwanted column
df.to_csv("output.csv", index=False)
```

> ⚠️ Forgetting `index=False` is the most common beginner mistake. It adds a useless `Unnamed: 0` column when you re-open the file.

---

## 3. Inspecting Your Data

Always do this right after loading data — it tells you what you're working with.

```python
df.head()           # First 5 rows
df.tail(3)          # Last 3 rows
df.info()           # Column names, types, and missing value counts
df.describe()       # Stats: mean, min, max, etc. for number columns
df.shape            # (rows, columns) — e.g. (1000, 5)
df["city"].value_counts()  # How often each city appears
```

---

## 4. Selecting Data: `[]`, `.loc`, and `.iloc`

There are three ways to select data:

| Method | Selects by | Example |
|--------|-----------|---------|
| `df["col"]` | Column name | `df["salary"]` |
| `.loc` | Row/column **labels** | `df.loc[0, "name"]` |
| `.iloc` | Row/column **numbers** | `df.iloc[0, 1]` |

```python
# Select a column
df["name"]

# Select multiple columns
df[["name", "salary"]]

# Select a row by label
df.loc[0]            # Row with label 0

# Select a row by position
df.iloc[0]           # First row (position 0)

# Select a specific cell
df.loc[0, "salary"]  # Label-based: row 0, column "salary"
df.iloc[0, 2]        # Position-based: row 0, column 2
```

> ⚠️ After filtering a DataFrame, row labels and positions may no longer match. Use `.loc` when you know the label, `.iloc` when you know the position.

---

## 5. Filtering Rows

Filtering means keeping only the rows that match a condition.

```python
# Simple filter
df[df["salary"] > 70000]

# Two conditions — wrap each in parentheses!
df[(df["salary"] > 70000) & (df["age"] < 35)]

# OR condition
df[(df["age"] < 25) | (df["age"] > 50)]

# Filter by a list of values
df[df["city"].isin(["New York", "London"])]

# Exclude values
df[~df["city"].isin(["Paris", "Tokyo"])]
```

> ⚠️ Always use `&` (AND) and `|` (OR) — never Python's `and`/`or` keywords. And always wrap conditions in `()`.

---

## 6. Handling Missing Data (NaN)

Missing values show up as `NaN`. Here's how to find and fix them.

```python
# Count missing values per column
df.isnull().sum()

# Drop rows with any missing values
df.dropna()

# Drop rows only if a specific column is missing
df.dropna(subset=["salary"])

# Fill missing values with a fixed value
df.fillna(0)

# Fill each column differently
df.fillna({"salary": df["salary"].mean(), "city": "Unknown"})
```

> ⚠️ `df.dropna()` with no arguments can silently delete most of your data on wide tables. Always use `subset=` to target specific columns.

---

## 7. Transforming Data

Add new columns, remove old ones, or rename them.

```python
import numpy as np

# Add a new column
df["bonus"] = df["salary"] * 0.10

# Conditional column (like an if/else for every row)
df["level"] = np.where(df["salary"] > 80000, "Senior", "Junior")

# Remove a column
df = df.drop(columns=["bonus"])

# Rename columns
df = df.rename(columns={"name": "full_name", "salary": "annual_salary"})

# Change a column's data type
df["salary"] = df["salary"].astype("int32")  # Saves memory
df["dept"] = df["dept"].astype("category")   # Great for repeated string values
```

---

## 8. Sorting

```python
# Sort by one column (ascending)
df.sort_values("salary")

# Sort descending
df.sort_values("salary", ascending=False)

# Sort by two columns
df.sort_values(["dept", "salary"], ascending=[True, False])

# Get the top 3 rows by salary (faster than sorting the whole table)
df.nlargest(3, "salary")

# Get the 3 lowest
df.nsmallest(3, "salary")
```

> ⚠️ `sort_values()` doesn't change `df` — you need to reassign: `df = df.sort_values("salary")`

---

## 9. Grouping & Aggregating

Group rows by a category and compute summaries — like "average salary per department."

```python
# Average salary per department
df.groupby("dept")["salary"].mean()

# Multiple stats at once
df.groupby("dept").agg(
    avg_salary=("salary", "mean"),
    headcount=("salary", "count"),
    max_salary=("salary", "max")
)

# Pivot table — rows are dept, columns are gender, values are avg salary
pd.pivot_table(df, values="salary", index="dept", columns="gender", aggfunc="mean")
```

> 💡 Use `transform("mean")` instead of `agg` when you want to add the group average back as a column on the original DataFrame.

---

## 10. String Operations

Clean and manipulate text columns using `.str`.

```python
# Clean whitespace and fix casing
df["name"] = df["name"].str.strip().str.title()

# Replace text
df["phone"] = df["phone"].str.replace("-", "", regex=False)

# Check if a column contains a word
df[df["email"].str.contains("@gmail.com", na=False)]

# Split into two columns
df[["first", "last"]] = df["name"].str.split(" ", expand=True)

# Get the length of each string
df["name_length"] = df["name"].str.len()
```

> 💡 Chain `.str` operations: `df["col"].str.strip().str.lower()` — clean and readable.

---

## 11. apply() and map()

Use these when built-in operations aren't enough.

```python
# apply() — run a custom function on each value in a column
def classify(salary):
    return "High" if salary >= 100000 else "Low"

df["tier"] = df["salary"].apply(classify)

# Or use a quick lambda
df["salary_k"] = df["salary"].apply(lambda x: f"${x//1000}k")

# map() — perfect for substituting values using a dictionary
dept_names = {"Eng": "Engineering", "Mkt": "Marketing"}
df["dept_full"] = df["dept"].map(dept_names)

# apply() row-wise (uses multiple columns per row)
def get_bonus(row):
    return row["salary"] * 0.15 if row["dept"] == "Eng" else row["salary"] * 0.10

df["bonus"] = df.apply(get_bonus, axis=1)
```

> ⚠️ `apply()` is essentially a loop — it's slow on large data. Prefer vectorized operations like `np.where` when possible.

---

## 12. Combining DataFrames

```python
# merge() — like SQL JOIN, combine on a shared column
pd.merge(employees, departments, on="dept_id", how="left")
# how options: "inner" (only matches), "left" (all from left), "outer" (all rows)

# concat() — stack DataFrames on top of each other
full_year = pd.concat([q1_df, q2_df], ignore_index=True)

# concat() side by side (add columns)
combined = pd.concat([names_df, scores_df], axis=1)
```

> ⚠️ After a `concat`, always use `ignore_index=True` to get a clean 0, 1, 2... index.

---

## 13. Working with Dates

```python
# Convert a string column to proper dates
df["order_date"] = pd.to_datetime(df["order_date"])

# Extract parts of a date
df["year"]     = df["order_date"].dt.year
df["month"]    = df["order_date"].dt.month
df["day_name"] = df["order_date"].dt.day_name()  # "Monday", "Tuesday", etc.

# Filter by date range
df[df["order_date"].between("2024-01-01", "2024-06-30")]

# Add days
df["due_date"] = df["order_date"] + pd.DateOffset(days=30)
```

> 💡 Use `parse_dates=["order_date"]` in `read_csv()` to auto-convert date columns at load time.

---

## 14. Finding & Removing Duplicates

```python
# Count duplicates
df.duplicated().sum()

# See which rows are duplicated
df[df.duplicated(keep=False)]

# Remove duplicates (keep first occurrence)
df = df.drop_duplicates()

# Remove duplicates based on a specific column only
df = df.drop_duplicates(subset=["order_id"], keep="last")
```

> 💡 Always inspect duplicates before dropping them — sometimes they reveal a real data problem (like two different orders sharing the same ID).

---

## 15. Best Practices

**Never use `inplace=True`** — it looks like it saves memory but doesn't, prevents chaining, and is being removed in future pandas versions. Always reassign instead:

```python
# ❌ Avoid
df.drop(columns=["temp"], inplace=True)

# ✅ Do this
df = df.drop(columns=["temp"])
```

**Use method chaining for clean code:**

```python
df = (
    pd.read_csv("data.csv")
    .dropna(subset=["salary"])
    .rename(columns={"sal": "salary"})
    .sort_values("salary")
    .reset_index(drop=True)
)
```

**Load only what you need:**

```python
df = pd.read_csv("data.csv",
    usecols=["name", "dept", "salary"],       # Skip unused columns
    dtype={"dept": "category"},               # Efficient types from the start
    parse_dates=["hire_date"]
)
```

**Use `.query()` for readable filters:**

```python
# Instead of this:
df[(df["salary"] > 70000) & (df["dept"] == "Eng")]

# Write this:
df.query("salary > 70000 and dept == 'Eng'")
```

---

*Start by loading a dataset you care about and try one section at a time. Pandas clicks into place through practice. Happy wrangling! 🐼*
