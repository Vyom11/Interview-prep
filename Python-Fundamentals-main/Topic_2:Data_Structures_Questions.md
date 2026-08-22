# 🐍 Phase 2: Core Data Structures — Senior Engineer Interview Master Guide

## Part 1: Dictionaries & Sets

### 1. Dictionaries: Dense/Sparse Implementation
**Question:** In Python 3.6+, dictionaries maintain insertion order and consume significantly less memory than in older versions. Explain how CPython implemented this under the hood and how it impacts time complexity.
**Expected Answer:**
*   Older Python dictionaries used a single sparse hash table array containing the hash, key, and value. This consumed a massive amount of memory because sparse arrays have empty, unused slots. 
*   Python 3.6+ split the dictionary into two arrays:
    1. A **dense array** (stores the actual key, value, and hash sequentially in insertion order).
    2. A **sparse array** of indices (acts as the actual hash table, pointing to the index in the dense array).
*   **Impact:** This drastically reduces memory footprint and inherently maintains insertion order. Average case time complexity remains `O(1)` for lookups, insertions, and deletions. 
**Senior Signal:** Shows an understanding of internal data structure implementations and memory optimization techniques.

### 2. Dictionaries: Memory Efficiency & Key-Sharing (PEP 412)
**Question:** In heavily object-oriented Python code, every object instance historically contained its own dictionary (`__dict__`) for attributes, consuming massive amounts of RAM. How do modern Python dictionaries handle object attributes to prevent memory bloat?
**Expected Answer:**
*   Modern CPython implements **Key-Sharing Dictionaries** (PEP 412).
*   Instead of every instance creating a full hash table containing both keys and values, the **keys are stored on the Class object**. 
*   The instance `__dict__` only stores a highly compact array of **values**, indexed in the exact same order as the shared keys array.
*   If an instance dynamically adds a new attribute that isn't shared by the rest of the class, it "de-shares" and creates its own standalone dictionary.
**Senior Signal:** Demonstrates architectural knowledge. A senior engineer knows that pre-declaring attributes in `__init__` isn't just "good practice"—it physically preserves the key-sharing memory structure.

### 3. Sets: The "Ordered" Integer Illusion
**Question:** Sets are formally unordered collections. However, if you run `print(set([0, 1, 2, 3, 4]))`, it will consistently print in perfect order. Why does this happen, and at what exact point does this ordering break?
**Expected Answer:**
*   **The Illusion:** In CPython, the `hash()` of an integer is just the integer itself. When inserting items into a set, Python determines the memory slot using `hash(item) & mask`. 
*   A new set initializes with a hash table size of 8 (the mask is `8 - 1 = 7`). 
*   The integers 0 through 7 will have hashes 0 through 7. `0 & 7 = 0`, `1 & 7 = 1`, etc. They are placed exactly into indices 0 through 7 in the C array, making them appear perfectly ordered.
*   **When it breaks:** This breaks exactly when you insert an element that triggers a hash collision or a table resize (when the set becomes 2/3 full, i.e., adding a 6th element causes a resize to 32). It also breaks for negative numbers, as `hash(-1)` is internally converted to `-2` (since `-1` is reserved in C to indicate a hashing error).

---

## Part 2: Lists, Tuples, & Mutability

### 4. Lists vs Tuples: Memory Allocation & Freelist
**Question:** Aside from immutability, why is tuple creation generally faster and more memory-efficient than list creation? Explain Python's underlying memory allocation strategies.
**Expected Answer:**
*   **Lists (Dynamic Arrays):** To make `append()` `O(1)` amortized, Python over-allocates memory. If you create a list of 4 items, Python allocates space for ~8. Every time bounds are exceeded, Python requests a larger contiguous block from the OS and copies references over.
*   **Tuples (Fixed-size Arrays):** Because they are immutable, Python allocates the exact memory needed. Furthermore, CPython utilizes a **tuple freelist** (a caching mechanism for small tuples up to 20 items). If a small tuple is destroyed, Python keeps the memory block alive for the next tuple of that size, bypassing OS memory allocation entirely.

### 5. Lists: The Overallocation Equation and `memmove`
**Question:** You have a list of 100,000 items. You run `my_list.pop(0)` in a loop until it's empty. Why is this catastrophically slow ($O(N^2)$), and how exactly does CPython handle list overallocation when you `append()` instead?
**Expected Answer:**
*   **The `pop(0)` disaster:** A Python list is a contiguous array of pointers in C. When you `pop(0)`, CPython uses the C function `memmove()` to shift all 99,999 remaining pointers exactly one slot to the left. Doing this $N$ times results in $O(N^2)$ time complexity. (The correct data structure is `collections.deque`).
*   **Overallocation Pattern:** CPython's growth pattern for `append()` is roughly `new_allocated = (newsize >> 3) + (newsize < 9 ? 3 : 6)`. It allocates roughly 12.5% more memory than strictly needed to prevent the OS from constantly needing to find new memory blocks.

### 6. Mutability vs Immutability: The Tuple Edge Case
**Question:** Tuples are immutable. What happens if you place a mutable object (like a list) inside a tuple, and then attempt to use `+=` on that list? (e.g., `my_tuple[0] += [1]`). How does this affect hashing?
**Expected Answer:**
*   **The `+=` Edge Case:** Python will throw a `TypeError` (because it attempts to reassign the resulting list back to the immutable tuple index). **But**, the list will actually be modified anyway because `+=` invokes `__iadd__` (in-place addition) *before* the assignment fails.
*   **Hashing:** Because the tuple contains an unhashable (mutable) object, the entire tuple becomes unhashable. It cannot be used as a dictionary key or stored in a set.

### 7. Mutability: The `__defaults__` Trap
**Question:** We all know not to use mutable default arguments like `def foo(my_list=[]):`. Under the hood, where does CPython store that empty list, and how could you theoretically access and clear it from outside the function during runtime?
**Expected Answer:**
*   Default arguments are evaluated exactly once, at **function definition (compile) time**.
*   The resulting objects are stored as a tuple in the function object's `__defaults__` dunder attribute.
*   To clear it at runtime without changing the function's code, you can execute: `foo.__defaults__[0].clear()`.
**Senior Signal:** Demonstrates that the candidate views functions as first-class objects in memory with their own stateful attributes.

---

## Part 3: Indexing, Slicing, & Operations

### 8. Slicing: Memory Management & In-Place Replacement
**Question:** Does slicing a list create a copy or a view? How can you use slicing to clear a list entirely, ensuring that other variables referencing the original list still see the changes?
**Expected Answer:**
*   Slicing (`my_list[1:3]`) creates a **shallow copy**, allocating a new list object with references to the same items.
*   However, slicing *on the left side of an assignment* modifies the original list **in-place** without changing its memory address.
*   To clear a list in-place: `my_list[:] = []`. Doing `my_list = []` would merely point the local variable to a new empty list, leaving other references pointing to the old populated list.

### 9. Slicing: Memory Views and Zero-Copy Operations
**Question:** You need to process massive `bytes` or `bytearray` objects. Standard slicing (`data[1000:5000]`) duplicates pointers and wastes RAM. How can you slice this data natively in Python *without* creating a copy?
**Expected Answer:**
*   Use the built-in `memoryview(data)` object. 
*   `memoryview` supports slicing, but instead of creating a new object, it returns a C-level pointer offset to the original buffer. 
*   It utilizes Python's **Buffer Protocol**, allowing true zero-copy data manipulation (essential for high-performance networking, crypto, or NumPy).

### 10. Operations: The Iterator Chunking Idiom
**Question:** Explain exactly what this code does and *why* it works at the memory reference level:
`data = [1, 2, 3, 4, 5, 6]`
`chunked = list(zip(*[iter(data)] * 3))`
**Expected Answer:**
*   **Result:** It chunks the list into tuples of 3: `[(1, 2, 3), (4, 5, 6)]`.
*   **Why it works:** `iter(data)` creates a *single* stateful list iterator object in memory.
*   `[iter(data)] * 3` creates a list containing three references to that **exact same iterator object**.
*   The `*` unpacks these three identical references into `zip()`. `zip()` evaluates left-to-right. It asks the first argument for a value (1), the second for a value (advances the *same* iterator to 2), and the third (advances to 3). Then it zips them.
**Senior Signal:** Masterful understanding of pointers, stateful iterables, and the unpacking operator.

---

## Part 4: Iteration, Comprehensions, & Built-ins

### 11. Iteration & Comprehensions: Scope and Bytecode Overhead
**Question:** In Python 2, `[x for x in range(5)]` would leak the variable `x` into the global scope. In Python 3, it doesn't. How did Python 3 fix this, and what minor performance penalty did this architectural change introduce?
**Expected Answer:**
*   Python 3 fixes this by compiling list comprehensions as **nested, anonymous functions**. 
*   When the interpreter hits a comprehension, it creates a new temporary function scope, executes the loop, returns the list, and discards the scope.
*   **The penalty:** Creating and tearing down a function frame (`MAKE_FUNCTION` bytecode) has a small overhead. For extremely simple loops, a standard `for` loop might be micro-seconds faster on setup (though C-level execution of the comprehension usually catches up).

### 12. Built-ins: `map`/`filter` vs Comprehensions (Memory & Architecture)
**Question:** You need to filter and transform 10 million records. Compare using a list comprehension, a generator expression, and the `map()`/`filter()` built-ins.
**Expected Answer:**
*   **List Comprehension:** Eager evaluation. Fast (loop runs in C), but loads 10M records into RAM at once, potentially causing `MemoryError`.
*   **Generator Expression:** Lazy evaluation. Processes one item at a time (`O(1)` memory). Slight overhead in CPU time due to Python's `yield` context switching.
*   **Map/Filter:** Lazy evaluation (in Py3). Incredibly fast because iteration happens entirely in C. However, performance depends strictly on the function being applied (see next question).

### 13. Built-ins: `map` Bytecode & The Lambda Trap
**Question:** Which is faster: `list(map(str, my_data))` or `[str(x) for x in my_data]`? What happens if you change `str` to a lambda function like `lambda x: str(x)`?
**Expected Answer:**
*   `list(map(str, my_data))` is faster. Because `str` is a built-in C function, the entire process stays within the C execution layer. Comprehensions must execute Python bytecode (`LOAD_FAST`, `CALL_FUNCTION`) for every item.
*   **The Lambda Trap:** `map(lambda x: str(x), my_data)` becomes **significantly slower** than a list comprehension. `map` now has to transition from C back into the Python execution frame to evaluate the lambda function for *every single element*, incurring massive context-switching overhead.

### 14. Built-ins: `zip` & `enumerate` Strictness
**Question:** What happens natively if you `zip()` two iterables of unequal length? How did Python 3.10 address this, and what is the alternative for padding data?
**Expected Answer:**
*   Natively, `zip()` silently truncates to the shortest iterable, historically causing massive data-loss bugs.
*   Python 3.10 introduced `strict=True` (`zip(a, b, strict=True)`). It raises a `ValueError` if lengths mismatch.
*   To pad shorter iterables with `None`, use `itertools.zip_longest()`.

### 15. Built-ins: `any()` and `all()` Vacuous Truths
**Question:** How do `any()` and `all()` handle short-circuiting? Furthermore, what do `any([])` and `all([])` evaluate to, and what is the mathematical logic behind it?
**Expected Answer:**
*   **Short-circuiting:** `any()` returns `True` on the first truthy value; `all()` returns `False` on the first falsy value.
*   `any([])` is **False**. It requires *at least one* truthy element, which it can't find.
*   `all([])` is **True**. This is a mathematical *vacuous truth*. `all` checks if there are *no falsy elements*. Since the iterable is empty, zero falsy elements exist, so it defaults to True.

---

## Part 5: Sorting

### 16. Sorting: Timsort Internals
**Question:** Python uses Timsort. What makes Timsort particularly well-suited for real-world Python data, and what is its space/time complexity?
**Expected Answer:**
*   Timsort is a hybrid of Merge Sort and Insertion Sort. 
*   **Real-world advantage:** It identifies "runs" (subsequences that are already partially ordered). Real-world data is often partially sorted. Timsort merges these runs, meaning its **Best Case Time Complexity is O(n)**.
*   **Average/Worst Case:** `O(n log n)`.
*   **Stability:** It is a *stable* sort. Objects with equal keys remain in their original relative order. This is critical for multi-pass sorting (e.g., sorting users by age, and then sorting that result by last name).