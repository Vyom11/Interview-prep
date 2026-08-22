# Phase 10 — Performance Engineering in Python

## Introduction: The Senior Engineer's Mindset
A junior developer writes code to make things work. A senior developer writes code that works *efficiently at scale*. However, the golden rule of performance engineering is: **Don't guess, measure.** Premature optimization leads to complex, unmaintainable code. 

As a senior engineer, your workflow should always be:
1. **Profile** to identify the exact bottleneck.
2. **Determine the nature** of the bottleneck (CPU-bound, I/O-bound, or Memory-bound).
3. **Apply the appropriate optimization technique** (Caching, Vectorization, C-extensions, or Database tuning).
4. **Measure again** to verify the improvement.

---

## 1. Profiling (Finding the Bottleneck)

Before optimizing, we must know exactly where the application spends its time. 

### Tool: `cProfile`
* **Why we use it:** It is Python’s built-in, deterministic C-extension profiler. It tracks how many times every function is called and how much time is spent inside it.
* **Alternatives:** 
  * `py-spy`: A sampling profiler that runs out-of-process. Excellent for production because it has near-zero overhead and doesn't require modifying your code.
  * `yappi`: Specifically designed for multithreaded and `asyncio` Python applications.

#### Code Example: Using `cProfile`
```python
import cProfile
import pstats
import time

def slow_function():
    # Simulating an I/O bound task (e.g., network request)
    time.sleep(1)

def compute_heavy():
    # Simulating a CPU bound task
    return sum(i * i for i in range(10_000_000))

def main():
    slow_function()
    compute_heavy()

if __name__ == "__main__":
    # cProfile.run() executes the string command and profiles it.
    # We sort by 'cumulative' time to see which functions took the longest from start to finish.
    cProfile.run('main()', sort='cumulative')
```

### Tool: `line_profiler`
* **Why we use it:** `cProfile` only tells you *which function* is slow. `line_profiler` tells you *which exact line* inside that function is the bottleneck.
* **Alternatives:** `scalene` (A modern, AI-powered profiler that profiles CPU, GPU, and memory line-by-line).

#### Code Example: Using `line_profiler`
*Note: Requires installation (`pip install line_profiler`).*

```python
# Save as script.py
# The @profile decorator is injected by the kernprof command-line tool.
@profile
def compute_heavy_line_by_line():
    total = 0
    # Line profiler will show us exactly how much time is spent on this loop
    for i in range(1_000_000):
        total += i
    
    # And how much time is spent doing this operation
    squares = [x**2 for x in range(100_000)]
    return total

if __name__ == "__main__":
    compute_heavy_line_by_line()

# To run: kernprof -l -v script.py
```

---

## 2. Memory Optimization

In Python, everything is an object, and the overhead can be significant. Unmanaged memory leads to high infrastructure costs, Out of Memory (OOM) kills, and slow execution due to Garbage Collection (GC) pauses.

### Tool: `memory_profiler`
* **Why we use it:** It allows line-by-line tracking of memory allocation, helping us identify memory leaks or bloated data structures.
* **Alternatives:** 
  * `tracemalloc`: Built-in Python library, excellent for finding exactly where in the code memory was allocated.
  * **`Memray` (by Bloomberg):** The modern industry standard. It tracks memory at the C-level, making it vastly superior to `memory_profiler` for tracking NumPy/Pandas/C-extension memory leaks.

#### Code Example: Generators vs Lists
```python
# pip install memory_profiler
from memory_profiler import profile

@profile
def create_huge_list():
    # This allocates memory for 10 million integers all at once.
    # Expect a massive spike in RAM usage.
    my_list = [i for i in range(10_000_000)]
    return sum(my_list)

@profile
def use_generator():
    # This yields one item at a time. 
    # Memory usage remains virtually flat regardless of the size.
    my_gen = (i for i in range(10_000_000))
    return sum(my_gen)

if __name__ == "__main__":
    create_huge_list()
    use_generator()

# To run: python -m memory_profiler script.py
```
*Senior Tip:* Using `__slots__` in Python classes prevents the dynamic creation of `__dict__` and `__weakref__` for each object, saving ~40-50% memory when instantiating millions of objects.

---

## 3. Caching (Redis)

When a computation is expensive or database queries are slow, we cache the result.

### Tool: Redis
* **Why we use it:** Redis is an ultra-fast, in-memory, distributed Key-Value store. It scales horizontally, persists data to disk (unlike pure RAM caches), and supports complex data structures (Sets, Hashes, Sorted Sets).
* **Alternatives:** 
  * `Memcached`: Simpler, multithreaded out-of-the-box, but lacks advanced data structures.
  * `Dragonfly`: A modern, highly multithreaded drop-in replacement for Redis.
  * `functools.lru_cache`: Built-in Python decorator for *local*, in-memory caching (not distributed).

#### Code Example: Redis Caching Pattern
```python
import redis
import json
import time

# Initialize Redis connection pool (best practice for handling multiple connections)
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

def fetch_user_data_from_db(user_id):
    """Simulate a slow database call."""
    time.sleep(2)
    return {"user_id": user_id, "name": "John Doe", "role": "Admin"}

def get_user_data(user_id):
    cache_key = f"user:{user_id}:data"
    
    # 1. Try to fetch from Redis
    cached_data = r.get(cache_key)
    
    if cached_data:
        print("Cache HIT")
        # Redis stores bytes, we must decode and deserialize
        return json.loads(cached_data.decode('utf-8'))
    
    print("Cache MISS")
    # 2. On miss, fetch from DB
    db_data = fetch_user_data_from_db(user_id)
    
    # 3. Store the result in Redis with an expiration time (TTL) of 300 seconds
    # TTL is crucial to prevent stale data and memory exhaustion
    r.setex(cache_key, 300, json.dumps(db_data))
    
    return db_data

# First call takes 2 seconds, second call takes ~1 millisecond.
```

---

## 4. Advanced Optimization & Vectorization (Cython & Numba)

Python's dynamic typing and interpretation make it slow for heavy math/loops. Furthermore, the **Global Interpreter Lock (GIL)** prevents true multithreading for CPU-bound tasks. We bypass this using compilation.

### Tool 1: Numba
* **Why we use it:** Numba is a Just-In-Time (JIT) compiler based on LLVM. With a simple `@jit` decorator, it translates Python and NumPy code into fast machine code at runtime. It's the lowest-effort, highest-reward tool for pure math loops.
* **Alternatives:** `Taichi` (great for computer graphics/GPU), `JAX` (Google's tool for ML/auto-differentiation).

#### Code Example: Numba JIT
```python
from numba import jit
import math

# nopython=True forces Numba to compile entirely without the Python interpreter.
# nogil=True releases the GIL, allowing this function to run concurrently in threads!
@jit(nopython=True, nogil=True)
def monte_carlo_pi(nsamples):
    acc = 0
    for i in range(nsamples):
        x = math.random()
        y = math.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples
```

### Tool 2: Cython
* **Why we use it:** Cython is an Ahead-Of-Time (AOT) compiler. It allows you to write Python with C-like static typing. It compiles down to C code, which is then compiled into a shared object (`.so`) file. It is deeply integrated with C/C++ libraries.
* **Alternatives:** `pybind11` (Better if you already have existing C++ code and just want to wrap it for Python), `Mojo` (A new language designed to be a fast Python superset).

#### Code Example: Cython (`.pyx` file)
```cython
# save as math_ops.pyx
# We use 'cdef' to define C variables. This bypasses Python object overhead.

cpdef double compute_sum(int n):
    cdef int i
    cdef double total = 0.0
    
    # Because 'i' and 'total' are typed, this loop runs at raw C speed
    for i in range(n):
        total += i * 0.5
        
    return total
```
*Note: Cython code requires a `setup.py` file to compile it into a C extension before importing.*

---

## 5. Database Optimization

Databases are almost always the bottleneck in modern web apps. Python code speed rarely matters if your SQL queries are poorly optimized.

**Core Techniques:**
1. **Indexing:** Use B-Tree indexes for standard lookups and Hash indexes for exact matches.
2. **Connection Pooling:** Opening a DB connection is expensive. Use tools like `PgBouncer` or SQLAlchemy's `QueuePool`.
3. **The N+1 Problem:** The most common ORM mistake.

#### Code Example: Fixing the N+1 Problem (SQLAlchemy)
The N+1 problem occurs when you query a list of items (1 query), and then loop through them, querying a related table for *each* item (N queries).

```python
from sqlalchemy.orm import joinedload

# BAD: N+1 Problem
# Query 1: SELECT * FROM users;
users = session.query(User).all()

for user in users:
    # Query 2 to N: SELECT * FROM addresses WHERE user_id = ?
    print(user.name, user.address.city) 


# GOOD: Eager Loading
# One Query: SELECT * FROM users JOIN addresses ON ...
# We use joinedload to fetch everything in a single trip to the database.
users = session.query(User).options(joinedload(User.address)).all()

for user in users:
    # No extra database hit happens here!
    print(user.name, user.address.city)
```
---

## 6. Senior-Level Interview Questions on Performance Engineering

If you are interviewing for a Senior Backend/Python role, expect these questions:

### Q1: You have a Python API running in production. Over a period of 4 days, the container runs out of memory (OOM) and crashes. How do you debug and fix this?
**Expected Answer:**
This is a classic memory leak. Since Python uses garbage collection, a leak usually means objects are lingering in memory because references to them are still alive. 
1. I would attach `Memray` or use Python's built-in `tracemalloc` module in a staging environment under load-testing, or briefly in production if safe.
2. I would take snapshots of memory allocation at T=0 and T=1 hour and compare them using `tracemalloc.take_snapshot().compare_to()`.
3. Common culprits I'd look for: Unbounded global caches (e.g., storing data in a standard `dict` instead of an `lru_cache`), circular references overriding `__del__`, or unclosed database/network connections.

### Q2: What is the Global Interpreter Lock (GIL) and how do you bypass it to utilize all CPU cores?
**Expected Answer:**
The GIL is a mutex in CPython that allows only one thread to execute Python bytecodes at a time. This makes standard threading useless for CPU-bound tasks.
To bypass it, I can:
1. Use `multiprocessing` to spawn separate processes, each with its own memory space and GIL.
2. Use C-extensions (like Cython) and explicitly release the GIL using `with nogil:`.
3. Use Numba with `@jit(nogil=True)`.
*(Note: I would also mention PEP 703—Python 3.13+ is actively working towards optionally removing the GIL).*

### Q3: We have an endpoint that queries a database and is currently very slow. Adding Redis caching didn't solve the problem entirely because the data is highly dynamic. What else would you look at?
**Expected Answer:**
If caching isn't viable, the database itself must be optimized. 
1. **Explain Plan:** I would run `EXPLAIN ANALYZE` on the generated SQL query to check if we are doing Full Table Scans.
2. **Indexes:** Check if the queried columns are properly indexed. I'd consider compound indexes if filtering by multiple columns.
3. **N+1 Problem:** Check the ORM logs to ensure we aren't firing hundreds of queries in a loop. I would use Eager Loading (`joinedload` or `selectinload`).
4. **Data Transfer:** Ensure we aren't doing `SELECT *` and pulling gigabytes of unused data over the network into Python's memory. Select only needed columns.

### Q4: Explain the difference between Vectorization and JIT Compilation. When would you use which?
**Expected Answer:**
* **Vectorization (NumPy):** Involves pushing loops down to the C-level by operating on entire arrays at once using SIMD (Single Instruction, Multiple Data) CPU capabilities. I use this when my logic can be expressed as linear algebra or broadcasted array operations.
* **JIT Compilation (Numba):** Compiles standard Python loops into machine code just before execution. I use this when the algorithm requires complex branching (`if/else` inside loops), custom heuristics, or stateful iterations that are notoriously difficult or impossible to vectorize cleanly with NumPy.

### Q5: If Redis runs out of memory, what happens? How do you prevent it from crashing your system?
**Expected Answer:**
By default, Redis will return an OOM error on write commands if `maxmemory` is reached. To prevent system crashes:
1. **Eviction Policies:** I would configure an eviction policy like `allkeys-lru` (Least Recently Used) or `volatile-lru` (evicts keys with an expiration set). This turns Redis into an actual cache rather than just a store.
2. **TTL (Time to Live):** Ensure that every cached item is written with a sensible TTL so stale data naturally falls out of memory.
3. **Monitoring:** Set up alerting on Redis memory usage thresholds via Prometheus/Grafana.

### Q6: You need to optimize a monolithic Python application. How do you decide between using `cProfile` and `line_profiler`, and how do you avoid falling into the trap of "profiler overhead" distorting your results?
**Expected Answer:**
I use a top-down approach. I start with macroscopic APM tools (like Datadog or New Relic) to find the slow endpoint. Then, I run `cProfile` locally to identify which *function* is taking the longest cumulative time. Once I isolate the function, I apply `@profile` from `line_profiler` to see exactly which *line of code* inside that function is the culprit.
To avoid profiler overhead (where the act of measuring slows down the code and skews results), I rely on deterministic profilers only in development. For production profiling, I use statistical/sampling profilers like `py-spy`, which read the call stack from outside the Python process, introducing virtually zero overhead.

### Q7: Explain how Python handles memory management. If you write a script to process a 50GB CSV file on a machine with 4GB of RAM, how do you architect it to avoid OOM errors?
**Expected Answer:**
Python handles memory via Reference Counting (objects are deallocated when their ref count hits zero) and a Generational Garbage Collector (to detect and clean up circular references).
To process a 50GB file on a 4GB machine, I cannot load the whole file into memory at once. I would use lazy evaluation/generators. 
I would read the file line-by-line using a generator (`yield`), or process it in chunks using Pandas (`pd.read_csv('file.csv', chunksize=10000)`). The key is to process a chunk, save/aggregate the result, and let the previous chunk's variables go out of scope so Python's GC reclaims the memory before loading the next chunk.

### Q8: What is a "Cache Stampede" (or Thundering Herd) in Redis, and how would you prevent it in a highly concurrent distributed system?
**Expected Answer:**
A Cache Stampede happens when a highly requested, computationally expensive cache key suddenly expires. At that exact millisecond, thousands of concurrent requests miss the cache and hit the database simultaneously, potentially taking down the DB.
To prevent it, I would use one of the following strategies:
1. **Mutex Locks:** When a cache miss occurs, the thread must acquire a distributed Redis lock (`SETNX`) before querying the DB. Other threads fail to get the lock and either wait/retry or return a stale value.
2. **Probabilistic Early Expiration (Cache Warming):** A background worker or the application probabilistically decides to recompute and update the cache *before* it actually expires.
3. **Stale-While-Revalidate:** Serve the stale cached data to the user immediately, but kick off an asynchronous background task (e.g., via Celery) to update the cache for future requests.

### Q9: When migrating a performance-critical module to Cython, what are the common pitfalls that might cause the Cython code to run just as slow as the original Python code?
**Expected Answer:**
The most common pitfall is forgetting to add static C types (`cdef`). If variables aren't typed, Cython falls back to using standard Python objects and C-API calls, which yields zero performance gain. (I would check this using `cython -a` to look for "yellow" lines, which indicate Python interaction).
Other pitfalls include:
1. **Bounds Checking:** Forgetting to disable array bounds checking (`@cython.boundscheck(False)`) when iterating through arrays.
2. **Wraparound:** Forgetting to disable negative indexing support (`@cython.wraparound(False)`).
3. **GIL:** Failing to use `nogil` when writing pure C-level loops, missing out on multithreading opportunities.

### Q10: A database query with `OFFSET 500000 LIMIT 50` is taking multiple seconds to execute, despite having indexes. Why is this happening and how do you optimize it?
**Expected Answer:**
Standard `OFFSET` pagination is extremely inefficient because the database still has to scan, compute, and then throw away the first 500,000 rows before returning the 50 rows you asked for. This makes the query $O(N)$ based on the offset size.
To optimize this, I would switch to **Cursor-based Pagination** (also known as Keyset Pagination). Instead of `OFFSET`, the client passes the ID of the last item they saw. The query becomes: `SELECT * FROM users WHERE id > last_seen_id ORDER BY id ASC LIMIT 50`. Because `id` is indexed, the database performs an $O(1)$ index seek directly to that ID and grabs the next 50 rows, completing in milliseconds regardless of how deep into the data the user scrolls.