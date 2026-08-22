# Master Python DSA Interview Guide: Intermediate to Senior Engineer

This document evaluates algorithmic thinking, deep understanding of Python's data structure internals, space-time complexity analysis, and the ability to apply correct architectural patterns to solve data-heavy problems.

---

## SECTION 1: Python Built-In Data Structures & Internals

#### 1. How is a Python `list` implemented under the hood? What are the performance implications?
**Answer:**
A Python `list` is **not** a linked list; it is a **dynamic array** implemented in C (an array of pointers to Python objects). 
*   **Time Complexity:** Append operations are amortized $O(1)$. Access by index is $O(1)$. However, inserting or popping from the *beginning* of a list (e.g., `list.insert(0, item)`) is $O(N)$ because every subsequent element must be shifted in memory.
*   **Memory:** It over-allocates memory. When the array is full, Python creates a larger array (usually 1.125x to 2x the size depending on the version) and copies the elements over. 

#### 2. Explain how a Python `dict` works under the hood. Does it maintain order?
**Answer:**
A `dict` is implemented as a **Hash Table**. 
*   **How it works:** It uses the `hash()` of a key to calculate an index in a C-level array. To handle hash collisions, CPython uses **Open Addressing with probing** (not chaining/linked lists).
*   **Complexity:** Lookups, insertions, and deletions are average $O(1)$, worst-case $O(N)$ (if a catastrophic hash collision occurs).
*   **Ordering:** As of Python 3.7 (and CPython 3.6), standard dictionaries **guarantee insertion order**. They maintain a dense array of entries and a sparse array of indices to achieve this compactly.

#### 3. What is the difference between `list.sort()` and `sorted()`? What algorithm do they use?
**Answer:**
*   **Algorithm:** Both use **Timsort** (a hybrid of Merge Sort and Insertion Sort). It is highly optimized for real-world data, heavily exploiting already-sorted sub-arrays (runs). Its worst-case time complexity is $O(N \log N)$ and best-case is $O(N)$. It is a **stable** sort.
*   **`list.sort()`:** Sorts the list **in-place**. It modifies the original object and returns `None`. Uses slightly less memory.
*   **`sorted(iterable)`:** Accepts any iterable (lists, tuples, generators), leaves the original intact, and returns a **brand new list**. 

#### 4. Why should you avoid using a `list` as a Queue in Python? What is the alternative?
**Answer:**
Using a standard list as a Queue (FIFO) by calling `my_list.pop(0)` forces an $O(N)$ memory shift for every element removed. If the queue has 100,000 items, this becomes drastically slow.
*   **Alternative:** Use `collections.deque` (Double-Ended Queue). Under the hood, it is implemented as a block-linked list. Pushing and popping from *either* end (`appendleft`, `popleft`) operates in **$O(1)$** time. 

---

## SECTION 2: Advanced Python Standard Library Structures

#### 5. When and why would you use the `heapq` module? 
**Answer:**
`heapq` provides functions to implement a **Min-Heap** on a standard Python list.
*   **Use cases:** Real-time priority queues, finding the $K^{th}$ largest/smallest element, or scheduling algorithms (like Dijkstra's).
*   **Performance:** `heappush` and `heappop` are $O(\log N)$. `heapify` (converting an unsorted list into a heap) is $O(N)$.
*   **Max-Heap workaround:** Python only natively supports Min-Heaps. To create a Max-Heap of numbers, you multiply the numbers by `-1` before pushing, and multiply by `-1` again when popping.

#### 6. What is the `bisect` module and when is it useful?
**Answer:**
`bisect` provides a way to perform **Binary Search** and insert elements into an already *sorted* list without having to re-sort it.
*   `bisect.bisect_left(arr, x)` finds the index where `x` should be inserted to maintain order in **$O(\log N)$** time. 
*   `bisect.insort(arr, x)` finds the index and inserts it. *(Note: While finding the index is $O(\log N)$, the actual insertion in a list is still $O(N)$).*

#### 7. Compare `defaultdict`, `Counter`, and standard `dict`.
**Answer:**
All are hash maps, but the `collections` module provides specialized subclasses:
*   **`defaultdict(type)`:** Never raises a `KeyError`. If a key doesn't exist, it uses the provided factory function (like `int` or `list`) to create a default value. Perfect for building adjacency lists for graphs (e.g., `graph = defaultdict(list)`).
*   **`Counter`:** A dictionary specifically designed for counting hashable objects. It has a highly optimized `most_common(k)` method which uses a Heap under the hood to return the top $K$ elements in $O(N \log K)$ time.

---

## SECTION 3: Algorithmic Paradigms & Pythonic Implementation

#### 8. Explain the Sliding Window pattern. What time complexity does it typically optimize?
**Answer:**
Sliding window is used on arrays/strings to track a contiguous subset of elements. Instead of using nested loops to evaluate every possible sub-array (which is $O(N^2)$), you maintain a "window" using two pointers (left and right). 
*   As the right pointer expands the window, if a condition is violated, the left pointer shrinks it. 
*   **Optimization:** It reduces $O(N^2)$ brute-force solutions down to **$O(N)$** time complexity.

#### 9. Dynamic Programming (DP): How do you implement Memoization natively in Python?
**Answer:**
Memoization is top-down DP, caching the results of expensive function calls.
*   **Pythonic Way:** Use the `functools` module decorators, specifically `@lru_cache(maxsize=None)` or (in Python 3.9+) simply `@cache`.
*   **Under the hood:** It wraps the function in a dictionary. When the function is called, it checks if the arguments `*args` (which must be hashable) exist as a key. If so, it returns the $O(1)$ cached result instead of executing the recursion tree.

#### 10. Breadth-First Search (BFS) vs. Depth-First Search (DFS). Which data structures back them?
**Answer:**
*   **BFS:** Explores layer by layer. Perfect for finding the **shortest path** in an unweighted graph. It is backed by a **Queue** (using `collections.deque` in Python).
*   **DFS:** Explores as deep as possible along a branch before backtracking. Perfect for topological sorting, cycle detection, or exhausting all possibilities (Backtracking). It is backed by a **Stack** (using the Call Stack via Recursion, or a standard Python `list` via `.append()` and `.pop()`).

---

## SECTION 4: Real-World Scenarios & Whiteboarding

#### 11. Whiteboard Scenario: The LRU Cache
**Question:** *"Design a Least Recently Used (LRU) cache with O(1) get and put operations."*
**Answer:**
*   **Algorithmic approach:** Requires a combination of a **Hash Map** (for $O(1)$ lookups) and a **Doubly Linked List** (for $O(1)$ eviction and moving items to the "recently used" end).
*   **Senior Pythonic approach:** A senior developer should point out that this exact structure already exists in Python via `collections.OrderedDict`. You can achieve this trivially:
    ```python
    from collections import OrderedDict

    class LRUCache(OrderedDict):
        def __init__(self, capacity):
            self.capacity = capacity

        def get(self, key):
            if key not in self: return -1
            self.move_to_end(key) # Marks as recently used
            return self[key]

        def put(self, key, value):
            if key in self: self.move_to_end(key)
            self[key] = value
            if len(self) > self.capacity:
                self.popitem(last=False) # Evicts LRU (FIFO)
    ```

#### 12. Whiteboard Scenario: Implementing a Trie (Prefix Tree)
**Question:** *"How would you design an autocomplete engine in Python that efficiently searches prefixes?"*
**Answer:**
The candidate should implement a **Trie**. In Python, this is most elegantly done using nested dictionaries.
*   **Structure:**
    ```python
    class TrieNode:
        def __init__(self):
            self.children = {} # Maps char -> TrieNode
            self.is_end_of_word = False
    ```
*   **Complexity:** Inserting or searching for a word of length $L$ takes exactly $O(L)$ time, regardless of how many millions of words are in the dictionary. It is vastly superior to searching through a flat list or standard hash map for partial string matches.

#### 13. System-Level Scenario: Handling Massive Datasets
**Question:** *"You need to process a 50GB log file and count the frequency of unique IPs. Your server only has 8GB of RAM. How do you do this in Python?"*
**Answer:**
A test of memory management and stream processing. 
*   **Anti-pattern:** `file.readlines()` or loading the file into a giant list. This will trigger an Out Of Memory (OOM) killer.
*   **Pythonic Solution:** Use **Generators**. Iterating over a file line-by-line (`for line in open('file.log'):`) acts as a generator, keeping only one line in memory at a time.
*   **Data Structure:** As you stream the file, hash the IP addresses into a `collections.Counter`. While the file is 50GB, the number of *unique* IP addresses is likely small enough that the resulting Hash Map will easily fit into the 8GB of RAM. 

#### 14. Algorithmic Scenario: Finding Top K Elements
**Question:** *"Given an infinite stream of real-time data, how do you continuously keep track of the Top 10 highest scores?"*
**Answer:**
*   **Anti-pattern:** Appending to a list and calling `.sort()` every time new data arrives (which is $O(N \log N)$ every tick).
*   **Optimal Solution:** Maintain a **Min-Heap** of size $K$ (where $K=10$). 
    *   When a new score arrives, if the heap is $< 10$, push it.
    *   If the heap is full and the new score is *greater* than the root (the minimum of the top 10), use `heapq.heappushpop()` to push the new score and pop the lowest score in a single, hyper-efficient $O(\log K)$ operation. Space complexity is perfectly capped at $O(K)$.