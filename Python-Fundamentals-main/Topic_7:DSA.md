# Phase 7 — Data Structures & Algorithms
### Goal: Become strong at problem solving

> **How to use these notes:** Read each section top-to-bottom. Every concept is explained plainly first, then backed by a well-commented code example. Complexity analysis is included for every major operation. Alternatives are discussed so you understand *why* a particular structure/algorithm is chosen over others.

---

## Table of Contents

1. [Data Structures](#data-structures)
   - [Arrays](#1-arrays)
   - [Linked Lists](#2-linked-lists)
   - [Stacks](#3-stacks)
   - [Queues](#4-queues)
   - [Trees](#5-trees)
   - [Heaps](#6-heaps)
   - [Graphs](#7-graphs)
   - [Hash Tables](#8-hash-tables)
2. [Algorithms](#algorithms)
   - [Sorting](#1-sorting)
   - [Searching](#2-searching)
   - [Recursion](#3-recursion)
   - [Greedy Algorithms](#4-greedy-algorithms)
   - [Dynamic Programming](#5-dynamic-programming)
   - [Graph Traversal](#6-graph-traversal)
3. [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)

---

# Data Structures

A **data structure** is a way of organizing data in memory so that it can be accessed and modified efficiently. Choosing the right data structure is often 80% of solving a problem well.

---

## 1. Arrays

### What is it?
An array is a **contiguous block of memory** where each element sits right next to the other. You access any element instantly using its index.

Think of it like a row of numbered parking spots — if you know the spot number, you can drive straight to it.

### Why do we use Arrays?
- **O(1) random access** — fastest possible read by index
- Simple, cache-friendly (CPU loves contiguous memory)
- Foundation of almost every other data structure

### When NOT to use Arrays?
- When you need frequent insertions/deletions in the middle (shifting elements is O(n))
- When the size changes dramatically and unpredictably

### Alternatives
| Alternative | Why not always use it? |
|---|---|
| Linked List | No random access, O(n) to reach index i |
| Dynamic Array (ArrayList/vector) | Same concept, just auto-resizes. Fine to use, but carries overhead |
| Hash Table | Good for key-based lookup, not index-based |

### Complexity
| Operation | Time | Notes |
|---|---|---|
| Access by index | O(1) | Direct memory address calculation |
| Search (unsorted) | O(n) | Must scan every element |
| Search (sorted) | O(log n) | Binary search possible |
| Insert at end | O(1) amortized | Dynamic arrays double capacity |
| Insert at middle | O(n) | Must shift elements right |
| Delete at middle | O(n) | Must shift elements left |

### Code Example

```javascript
// ─────────────────────────────────────────────
// Arrays — Core Operations Explained
// ─────────────────────────────────────────────

const fruits = ["apple", "banana", "cherry", "date"];

// O(1) — Direct access by index (fastest possible)
console.log(fruits[2]); // "cherry"

// O(n) — Linear search: we check each element one by one
function linearSearch(arr, target) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === target) return i; // return the index where found
  }
  return -1; // not found
}

// O(n) — Insert in the middle: everything after index must shift right
function insertAt(arr, index, value) {
  // We push a dummy element to make space, then shift from the right
  arr.push(null);
  for (let i = arr.length - 1; i > index; i--) {
    arr[i] = arr[i - 1]; // shift element one position to the right
  }
  arr[index] = value; // place our new value
  return arr;
}

// O(n) — Delete in the middle: everything after must shift left
function deleteAt(arr, index) {
  for (let i = index; i < arr.length - 1; i++) {
    arr[i] = arr[i + 1]; // shift element one position to the left
  }
  arr.pop(); // remove the now-duplicate last element
  return arr;
}

// Example usage
console.log(insertAt([1, 2, 4, 5], 2, 3)); // [1, 2, 3, 4, 5]
console.log(deleteAt([1, 2, 3, 4, 5], 2));  // [1, 2, 4, 5]
```

---

## 2. Linked Lists

### What is it?
A linked list is a **chain of nodes**. Each node holds:
1. A **value** (the data)
2. A **pointer** to the next node

Unlike arrays, nodes are scattered anywhere in memory — they are connected only through pointers.

Think of it like a treasure hunt: each clue (node) tells you where the next clue is.

### Why do we use Linked Lists?
- **O(1) insert/delete at head** — no shifting needed, just update pointers
- Dynamic size — grows and shrinks naturally without reallocation
- Used as the backbone for Stacks, Queues, and Adjacency Lists in Graphs

### Variants
- **Singly Linked List** — each node points only forward
- **Doubly Linked List** — each node points forward AND backward (allows O(1) delete given a node reference)
- **Circular Linked List** — last node points back to head (used in round-robin scheduling)

### Alternatives
| Alternative | Why not always use it? |
|---|---|
| Array | Faster random access O(1), but O(n) insert/delete in middle |
| Dynamic Array | Wastes memory on reallocation, shifting cost on insert |

### Complexity
| Operation | Singly | Doubly |
|---|---|---|
| Access by index | O(n) | O(n) |
| Search | O(n) | O(n) |
| Insert at head | O(1) | O(1) |
| Insert at tail | O(n) / O(1) with tail pointer | O(1) |
| Delete at head | O(1) | O(1) |
| Delete given node | O(n) | O(1) |

### Code Example

```javascript
// ─────────────────────────────────────────────
// Singly Linked List Implementation
// ─────────────────────────────────────────────

// Each node is a tiny object holding data + a reference to the next node
class Node {
  constructor(value) {
    this.value = value;
    this.next = null; // initially points to nothing
  }
}

class LinkedList {
  constructor() {
    this.head = null; // the list starts empty
    this.size = 0;
  }

  // O(1) — Insert at the beginning (just redirect the head pointer)
  prepend(value) {
    const newNode = new Node(value);
    newNode.next = this.head; // new node points to old head
    this.head = newNode;      // head is now the new node
    this.size++;
  }

  // O(n) — Insert at the end (must walk to the last node)
  append(value) {
    const newNode = new Node(value);
    if (!this.head) {
      this.head = newNode; // empty list: new node IS the head
      this.size++;
      return;
    }
    let current = this.head;
    while (current.next !== null) {
      current = current.next; // keep walking until we reach the last node
    }
    current.next = newNode; // last node now points to new node
    this.size++;
  }

  // O(n) — Delete by value (find the node just before the target)
  delete(value) {
    if (!this.head) return;

    // Special case: the head itself is the target
    if (this.head.value === value) {
      this.head = this.head.next; // head jumps over the deleted node
      this.size--;
      return;
    }

    let current = this.head;
    while (current.next !== null) {
      if (current.next.value === value) {
        // Found it — skip over the target node by relinking
        current.next = current.next.next;
        this.size--;
        return;
      }
      current = current.next;
    }
  }

  // O(n) — Print list as a readable string
  print() {
    const values = [];
    let current = this.head;
    while (current !== null) {
      values.push(current.value);
      current = current.next;
    }
    console.log(values.join(" -> "));
  }
}

// Usage
const list = new LinkedList();
list.append(1);
list.append(2);
list.append(3);
list.prepend(0);
list.print();   // 0 -> 1 -> 2 -> 3
list.delete(2);
list.print();   // 0 -> 1 -> 3
```

---

## 3. Stacks

### What is it?
A stack is a **LIFO** (Last In, First Out) structure. The last item you put in is the first one you take out.

Think of a stack of plates — you always add to the top, and remove from the top.

### Why do we use Stacks?
- **Function call management** — every programming language uses a call stack. When you call a function, it's pushed; when it returns, it's popped.
- **Undo/redo** — text editors use stacks to track changes
- **Expression parsing** — compilers use stacks to parse brackets and operators
- **DFS graph traversal** (iterative version)

### Core Operations
| Operation | Description | Time |
|---|---|---|
| push(x) | Add x to the top | O(1) |
| pop() | Remove and return top element | O(1) |
| peek() | Look at top without removing | O(1) |
| isEmpty() | Check if stack is empty | O(1) |

### Alternatives
| Alternative | Why not? |
|---|---|
| Array with random access | Stacks intentionally restrict access to top only. Using an array with unrestricted access defeats the purpose of enforcing LIFO discipline. |
| Queue | FIFO, opposite behavior |

### Code Example

```javascript
// ─────────────────────────────────────────────
// Stack — Built using an array (array tail = stack top)
// ─────────────────────────────────────────────

class Stack {
  constructor() {
    this.items = []; // internal storage
  }

  // O(1) — Push: add element to the top (end of array)
  push(value) {
    this.items.push(value);
  }

  // O(1) — Pop: remove and return the top element
  pop() {
    if (this.isEmpty()) throw new Error("Stack underflow — nothing to pop!");
    return this.items.pop();
  }

  // O(1) — Peek: see what's on top without removing it
  peek() {
    if (this.isEmpty()) throw new Error("Stack is empty");
    return this.items[this.items.length - 1];
  }

  isEmpty() {
    return this.items.length === 0;
  }
}

// ─────────────────────────────────────────────
// Real-world use: Check balanced brackets
// Input: "(a + [b * {c}])" → should return true
// Input: "(a + [b)"         → should return false
// ─────────────────────────────────────────────

function isBalanced(str) {
  const stack = new Stack();
  const open  = "({[";
  const close = ")}]";
  // Map each closing bracket to its matching opener
  const match = { ")": "(", "}": "{", "]": "[" };

  for (const char of str) {
    if (open.includes(char)) {
      stack.push(char);         // opening bracket: push onto stack
    } else if (close.includes(char)) {
      if (stack.isEmpty()) return false;       // no opener to match
      if (stack.pop() !== match[char]) return false; // wrong type
    }
  }

  return stack.isEmpty(); // if stack is empty, all brackets matched
}

console.log(isBalanced("(a + [b * {c}])")); // true
console.log(isBalanced("(a + [b)"));         // false
```

---

## 4. Queues

### What is it?
A queue is a **FIFO** (First In, First Out) structure. The first item added is the first one removed.

Think of a checkout line at a grocery store — first person in line gets served first.

### Why do we use Queues?
- **Task scheduling** — OS process schedulers use queues
- **BFS graph traversal** — level-by-level exploration
- **Message queues** — Kafka, RabbitMQ are built on this concept
- **Printer spooling**, web server request handling

### Variants
- **Simple Queue** — basic FIFO
- **Circular Queue** — wraps around to reuse space (used in fixed-size buffers)
- **Priority Queue** — elements have priority; highest priority exits first (backed by a Heap)
- **Deque (Double-Ended Queue)** — can insert/remove from both ends

### Core Operations
| Operation | Description | Time |
|---|---|---|
| enqueue(x) | Add x to the back | O(1) |
| dequeue() | Remove and return front element | O(1) |
| peek() | See front without removing | O(1) |

### Alternatives
| Alternative | Why not? |
|---|---|
| Stack | LIFO, gives you the wrong order |
| Array (shifting) | dequeue with `array.shift()` is O(n) due to element shifting — avoid for large queues |

### Code Example

```javascript
// ─────────────────────────────────────────────
// Queue — Efficient implementation using two pointers
// (Avoids the O(n) cost of array.shift())
// ─────────────────────────────────────────────

class Queue {
  constructor() {
    this.items = {};  // we use an object as a hash map for O(1) operations
    this.head = 0;    // index of the front element
    this.tail = 0;    // index where the next element will be inserted
  }

  // O(1) — Enqueue: add to the back
  enqueue(value) {
    this.items[this.tail] = value;
    this.tail++; // advance tail pointer
  }

  // O(1) — Dequeue: remove from the front
  dequeue() {
    if (this.isEmpty()) throw new Error("Queue is empty");
    const value = this.items[this.head];
    delete this.items[this.head]; // clean up memory
    this.head++; // advance head pointer
    return value;
  }

  peek() {
    return this.items[this.head];
  }

  isEmpty() {
    return this.head === this.tail;
  }

  size() {
    return this.tail - this.head;
  }
}

// Usage: Simulating a print queue
const printQueue = new Queue();
printQueue.enqueue("Document A");
printQueue.enqueue("Document B");
printQueue.enqueue("Document C");

console.log("Printing:", printQueue.dequeue()); // Document A — first in, first out
console.log("Printing:", printQueue.dequeue()); // Document B
console.log("Next up:", printQueue.peek());      // Document C — just peeking, not removing
```

---

## 5. Trees

### What is it?
A tree is a **hierarchical** data structure made of nodes. Each node has:
- A **value**
- Zero or more **child nodes**

There is always one **root** node at the top. Nodes with no children are called **leaves**.

Think of a company org chart — CEO at the top, managers below, employees below that.

### Why do we use Trees?
- **Hierarchical data** — file systems, DOM (HTML), JSON
- **Fast search** — Binary Search Trees give O(log n) search
- **Decision making** — decision trees in ML
- **Priority management** — Heaps (special trees) for priority queues
- **Routing** — Tries for autocomplete/IP routing

### Key Types
| Type | Description | Use Case |
|---|---|---|
| Binary Tree | Each node has at most 2 children | Foundation for BSTs and Heaps |
| Binary Search Tree (BST) | Left child < parent < right child | Sorted data, fast lookup |
| AVL Tree | Self-balancing BST | Guaranteed O(log n) even after inserts |
| Trie | Each node is a character | Autocomplete, dictionary search |
| N-ary Tree | Each node can have N children | File systems, DOM |

### BST Complexity
| Operation | Average | Worst (unbalanced) |
|---|---|---|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |

> **Why worst case is O(n)?** If you insert sorted data into a BST (1,2,3,4,5...), it degrades into a linked list. This is why self-balancing trees (AVL, Red-Black) exist.

### Code Example

```javascript
// ─────────────────────────────────────────────
// Binary Search Tree (BST) Implementation
// Property: left subtree values < node value < right subtree values
// ─────────────────────────────────────────────

class TreeNode {
  constructor(value) {
    this.value = value;
    this.left = null;  // left child
    this.right = null; // right child
  }
}

class BinarySearchTree {
  constructor() {
    this.root = null;
  }

  // O(log n) average — Insert: walk left if smaller, right if larger
  insert(value) {
    const newNode = new TreeNode(value);
    if (!this.root) {
      this.root = newNode;
      return;
    }
    let current = this.root;
    while (true) {
      if (value < current.value) {
        // Go left
        if (!current.left) { current.left = newNode; return; }
        current = current.left;
      } else {
        // Go right
        if (!current.right) { current.right = newNode; return; }
        current = current.right;
      }
    }
  }

  // O(log n) average — Search: same walk as insert
  search(value) {
    let current = this.root;
    while (current) {
      if (value === current.value) return true;      // found it!
      if (value < current.value) current = current.left;  // go left
      else current = current.right;                        // go right
    }
    return false; // not found
  }

  // In-order traversal: visits nodes in SORTED order (left → root → right)
  inOrder(node = this.root, result = []) {
    if (node) {
      this.inOrder(node.left, result);   // visit left subtree first
      result.push(node.value);           // visit root
      this.inOrder(node.right, result);  // visit right subtree
    }
    return result;
  }
}

// Usage
const bst = new BinarySearchTree();
[5, 3, 7, 1, 4, 6, 8].forEach(v => bst.insert(v));

console.log(bst.search(4));       // true
console.log(bst.search(9));       // false
console.log(bst.inOrder());       // [1, 3, 4, 5, 6, 7, 8] — sorted!

/*
      Tree structure:
            5
           / \
          3   7
         / \ / \
        1  4 6  8
*/
```

---

## 6. Heaps

### What is it?
A heap is a **complete binary tree** (all levels filled, last level filled left to right) that satisfies the **heap property**:

- **Max-Heap**: Parent is always **greater than or equal to** its children → root is the maximum
- **Min-Heap**: Parent is always **less than or equal to** its children → root is the minimum

The brilliant trick: even though it's a tree conceptually, **it's stored as an array**. For a node at index `i`:
- Left child → `2i + 1`
- Right child → `2i + 2`
- Parent → `Math.floor((i - 1) / 2)`

### Why do we use Heaps?
- **Priority Queue** — always get the highest/lowest priority element in O(1)
- **Heap Sort** — O(n log n) in-place sorting
- **Graph algorithms** — Dijkstra's shortest path uses a min-heap
- **Top K elements** — find the K largest/smallest elements efficiently

### Why not use a sorted array instead?
A sorted array gives you O(1) access to the min/max but O(n) insert. A heap gives you O(log n) insert AND O(1) min/max access — much better for dynamic data.

### Complexity
| Operation | Time |
|---|---|
| Get min/max (peek) | O(1) |
| Insert | O(log n) |
| Remove min/max | O(log n) |
| Build heap from array | O(n) |

### Code Example

```javascript
// ─────────────────────────────────────────────
// Min-Heap Implementation
// Root always holds the SMALLEST value
// ─────────────────────────────────────────────

class MinHeap {
  constructor() {
    this.heap = []; // array representation of the heap
  }

  // Helper: swap two elements in the array
  swap(i, j) {
    [this.heap[i], this.heap[j]] = [this.heap[j], this.heap[i]];
  }

  parent(i)     { return Math.floor((i - 1) / 2); }
  leftChild(i)  { return 2 * i + 1; }
  rightChild(i) { return 2 * i + 2; }

  // O(1) — The minimum is always at the root (index 0)
  peek() {
    return this.heap[0];
  }

  // O(log n) — Insert: add at end, then "bubble up" to restore heap property
  insert(value) {
    this.heap.push(value); // step 1: add to the end
    this.bubbleUp(this.heap.length - 1); // step 2: fix the heap
  }

  bubbleUp(index) {
    // Keep swapping with parent as long as we're smaller than our parent
    while (index > 0) {
      const parentIdx = this.parent(index);
      if (this.heap[parentIdx] > this.heap[index]) {
        this.swap(parentIdx, index); // parent is larger: swap to fix
        index = parentIdx;           // continue from parent's position
      } else {
        break; // heap property restored, stop
      }
    }
  }

  // O(log n) — Remove min: take root, put last element at root, "sink down"
  removeMin() {
    if (this.heap.length === 0) return null;
    const min = this.heap[0];                    // save the minimum
    const last = this.heap.pop();                // remove last element
    if (this.heap.length > 0) {
      this.heap[0] = last;                       // put last at root
      this.sinkDown(0);                          // restore heap property
    }
    return min;
  }

  sinkDown(index) {
    const length = this.heap.length;
    // Keep swapping with the smallest child until heap property holds
    while (true) {
      let smallest = index;
      const left  = this.leftChild(index);
      const right = this.rightChild(index);

      if (left < length && this.heap[left] < this.heap[smallest])
        smallest = left;
      if (right < length && this.heap[right] < this.heap[smallest])
        smallest = right;

      if (smallest !== index) {
        this.swap(smallest, index);
        index = smallest; // continue sinking down
      } else {
        break; // heap property restored
      }
    }
  }
}

// Usage: Always extract the smallest task priority
const taskQueue = new MinHeap();
taskQueue.insert(5);  // priority 5
taskQueue.insert(2);  // priority 2 (most urgent)
taskQueue.insert(8);
taskQueue.insert(1);  // priority 1 (most urgent!)

console.log(taskQueue.peek());        // 1 — smallest always at top
console.log(taskQueue.removeMin());   // 1 — removes and returns smallest
console.log(taskQueue.removeMin());   // 2 — next smallest
```

---

## 7. Graphs

### What is it?
A graph is a collection of **nodes (vertices)** connected by **edges**. Unlike trees, graphs can have cycles, and there's no concept of a "root".

Think of a city map — intersections are nodes, roads are edges.

### Types of Graphs
| Type | Description | Example |
|---|---|---|
| Undirected | Edges have no direction (bidirectional) | Social friends (if A is friends with B, B is friends with A) |
| Directed (Digraph) | Edges have direction | Twitter following (A follows B doesn't mean B follows A) |
| Weighted | Edges have a cost/weight | GPS maps (road has a distance) |
| Cyclic | Contains cycles | Most real-world graphs |
| Acyclic | No cycles | DAGs (Directed Acyclic Graphs) used in task scheduling |

### Representations
#### Adjacency List (most common)
```
Graph:  A -- B -- C
              |
              D
Adjacency List:
{ A: [B], B: [A, C, D], C: [B], D: [B] }
```
**Use when:** Sparse graphs (few edges relative to nodes). Space: O(V + E)

#### Adjacency Matrix
```
    A  B  C  D
A [ 0, 1, 0, 0 ]
B [ 1, 0, 1, 1 ]
C [ 0, 1, 0, 0 ]
D [ 0, 1, 0, 0 ]
```
**Use when:** Dense graphs, or when you need O(1) edge lookup. Space: O(V²)

### Why do we use Graphs?
Graphs model virtually any real-world relationship:
- Social networks (Facebook, LinkedIn)
- Navigation (Google Maps uses weighted graphs)
- Internet (web pages linked together)
- Dependency resolution (package managers like npm)
- Recommendation engines

### Code Example

```javascript
// ─────────────────────────────────────────────
// Graph using Adjacency List (undirected)
// ─────────────────────────────────────────────

class Graph {
  constructor() {
    // adjacencyList: { node: [neighbor1, neighbor2, ...] }
    this.adjacencyList = {};
  }

  // Add a new vertex to the graph
  addVertex(vertex) {
    if (!this.adjacencyList[vertex]) {
      this.adjacencyList[vertex] = []; // starts with no connections
    }
  }

  // Add an undirected edge: both nodes point to each other
  addEdge(vertex1, vertex2) {
    this.adjacencyList[vertex1].push(vertex2);
    this.adjacencyList[vertex2].push(vertex1);
  }

  // Remove an edge between two vertices
  removeEdge(vertex1, vertex2) {
    // Filter out the other vertex from each neighbor list
    this.adjacencyList[vertex1] = this.adjacencyList[vertex1].filter(v => v !== vertex2);
    this.adjacencyList[vertex2] = this.adjacencyList[vertex2].filter(v => v !== vertex1);
  }

  // Get all neighbors of a vertex
  getNeighbors(vertex) {
    return this.adjacencyList[vertex] || [];
  }
}

// Build a simple social network graph
const network = new Graph();
["Alice", "Bob", "Carol", "Dave"].forEach(p => network.addVertex(p));
network.addEdge("Alice", "Bob");
network.addEdge("Bob", "Carol");
network.addEdge("Carol", "Dave");
network.addEdge("Alice", "Dave");

console.log(network.getNeighbors("Alice")); // ["Bob", "Dave"]
console.log(network.getNeighbors("Bob"));   // ["Alice", "Carol"]

/*
  Alice --- Bob
   |          |
  Dave --- Carol
*/
```

---

## 8. Hash Tables

### What is it?
A hash table stores **key-value pairs**. It uses a **hash function** to convert a key into an array index, allowing near-instant lookup.

Think of it like a massive filing cabinet where the label on the folder tells you exactly which drawer it's in — you go directly there, no searching.

### Why do we use Hash Tables?
- **O(1) average** for insert, delete, and lookup — fastest possible for key-based access
- Used in databases for indexing, caches (Redis), symbol tables in compilers, frequency counting

### The Hash Function
A hash function converts a key (e.g., a string) into a number (array index):
```
hash("name") → 42 → items[42] = "Alice"
```
A good hash function distributes keys evenly to minimize **collisions** (two keys mapping to the same index).

### Collision Handling
| Method | How it works |
|---|---|
| Chaining | Each slot holds a linked list; collisions just append to the list |
| Open Addressing | On collision, probe to the next available slot |

### Why not use a BST instead?
A BST gives O(log n) — hash tables give O(1) average. However, BSTs keep keys sorted (useful for range queries), hash tables do not.

### Complexity
| Operation | Average | Worst Case (many collisions) |
|---|---|---|
| Insert | O(1) | O(n) |
| Search | O(1) | O(n) |
| Delete | O(1) | O(n) |

### Code Example

```javascript
// ─────────────────────────────────────────────
// Hash Table with Chaining for collision resolution
// ─────────────────────────────────────────────

class HashTable {
  constructor(size = 53) {
    // Internal array; prime size reduces clustering of collisions
    this.table = new Array(size);
    this.size = size;
  }

  // Hash function: convert key string to an array index
  _hash(key) {
    let hash = 0;
    const PRIME = 31; // prime multiplier helps distribute values evenly
    for (let i = 0; i < Math.min(key.length, 100); i++) {
      hash = (hash * PRIME + key.charCodeAt(i)) % this.size;
    }
    return hash;
  }

  // O(1) average — Set: store a key-value pair
  set(key, value) {
    const index = this._hash(key);
    if (!this.table[index]) {
      this.table[index] = []; // create a bucket (array) for chaining
    }
    // Check if key already exists (update it)
    const bucket = this.table[index];
    const existing = bucket.find(pair => pair[0] === key);
    if (existing) {
      existing[1] = value; // update existing key
    } else {
      bucket.push([key, value]); // add new key-value pair
    }
  }

  // O(1) average — Get: retrieve value by key
  get(key) {
    const index = this._hash(key);
    const bucket = this.table[index];
    if (!bucket) return undefined;
    const pair = bucket.find(pair => pair[0] === key);
    return pair ? pair[1] : undefined;
  }

  // O(1) average — Delete: remove a key-value pair
  delete(key) {
    const index = this._hash(key);
    if (!this.table[index]) return false;
    this.table[index] = this.table[index].filter(pair => pair[0] !== key);
    return true;
  }
}

// Real-world use: count word frequencies in a sentence
function wordCount(sentence) {
  const map = new HashTable();
  const words = sentence.toLowerCase().split(/\s+/);
  for (const word of words) {
    const count = map.get(word) || 0;
    map.set(word, count + 1); // increment count for this word
  }
  return map;
}

const freq = wordCount("the cat sat on the mat the cat");
console.log(freq.get("the"));  // 3
console.log(freq.get("cat"));  // 2
console.log(freq.get("mat"));  // 1

// In practice, JavaScript's built-in Map gives you the same O(1) behavior:
const map = new Map();
map.set("key", "value");
console.log(map.get("key")); // "value"
```

---

# Algorithms

An **algorithm** is a step-by-step procedure to solve a problem. The goal is to solve it *correctly* first, then *efficiently*.

---

## 1. Sorting

### What is it?
Sorting rearranges elements in a defined order (ascending/descending). This is one of the most studied problems in CS.

### Why sorting matters
- Binary search requires sorted data
- Many problems become trivially easy on sorted data (finding duplicates, medians, etc.)
- Database queries use sorting internally (ORDER BY)

### Major Sorting Algorithms Compared

| Algorithm | Best | Average | Worst | Space | Stable? | Use When |
|---|---|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes | Teaching only, never in production |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No | Never — always worse options exist |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes | Small arrays or nearly-sorted data |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | When stability required, linked lists |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No | General purpose, usually fastest in practice |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No | When O(1) extra space needed |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes | Integer data with small range |

> **What does "stable" mean?** A stable sort preserves the original order of equal elements. If you're sorting people by last name, a stable sort keeps people with the same last name in their original relative order.

### Code Example

```javascript
// ─────────────────────────────────────────────
// Merge Sort — O(n log n) guaranteed, stable
// Strategy: Divide array in half, sort each half, merge them back
// ─────────────────────────────────────────────

function mergeSort(arr) {
  // Base case: arrays of 0 or 1 element are already sorted
  if (arr.length <= 1) return arr;

  // Step 1: Find the middle and split into two halves
  const mid = Math.floor(arr.length / 2);
  const left  = mergeSort(arr.slice(0, mid));  // recursively sort left half
  const right = mergeSort(arr.slice(mid));      // recursively sort right half

  // Step 2: Merge the two sorted halves into one sorted array
  return merge(left, right);
}

function merge(left, right) {
  const result = [];
  let i = 0, j = 0;

  // Compare elements from both halves, always pick the smaller one
  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) {
      result.push(left[i++]); // left element is smaller (or equal), take it
    } else {
      result.push(right[j++]); // right element is smaller, take it
    }
  }

  // One array is exhausted — append whatever remains from the other
  return result.concat(left.slice(i)).concat(right.slice(j));
}

// ─────────────────────────────────────────────
// Quick Sort — O(n log n) average, O(n²) worst
// Strategy: Pick a pivot, put smaller elements left, larger right, repeat
// ─────────────────────────────────────────────

function quickSort(arr, low = 0, high = arr.length - 1) {
  if (low < high) {
    // Partition: place pivot in its correct sorted position
    const pivotIndex = partition(arr, low, high);
    quickSort(arr, low, pivotIndex - 1);  // sort left of pivot
    quickSort(arr, pivotIndex + 1, high); // sort right of pivot
  }
  return arr;
}

function partition(arr, low, high) {
  const pivot = arr[high]; // we use the last element as pivot
  let i = low - 1;         // i tracks the boundary of the "smaller" region

  for (let j = low; j < high; j++) {
    if (arr[j] <= pivot) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]]; // swap smaller element into left region
    }
  }

  // Place pivot in its correct position
  [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
  return i + 1; // return pivot's final index
}

// Tests
console.log(mergeSort([5, 2, 8, 1, 9, 3])); // [1, 2, 3, 5, 8, 9]
console.log(quickSort([5, 2, 8, 1, 9, 3])); // [1, 2, 3, 5, 8, 9]
```

---

## 2. Searching

### What is it?
Searching finds whether an element exists (and where) in a data structure.

### Linear Search vs Binary Search

| | Linear Search | Binary Search |
|---|---|---|
| Requirement | None | Array must be sorted |
| Time | O(n) | O(log n) |
| Best for | Unsorted/small data | Sorted/large data |

> **Why O(log n)?** Binary search halves the search space on every step. 1 billion elements → found in at most 30 comparisons (log₂(1,000,000,000) ≈ 30). That's extraordinary.

### Code Example

```javascript
// ─────────────────────────────────────────────
// Binary Search — O(log n)
// Requires: sorted array
// Strategy: compare with middle element, discard half the array
// ─────────────────────────────────────────────

function binarySearch(arr, target) {
  let left = 0;
  let right = arr.length - 1;

  while (left <= right) {
    // Calculate mid WITHOUT overflow (safer than (left + right) / 2)
    const mid = left + Math.floor((right - left) / 2);

    if (arr[mid] === target) {
      return mid; // found! return the index
    } else if (arr[mid] < target) {
      left = mid + 1;  // target is in the RIGHT half, discard left
    } else {
      right = mid - 1; // target is in the LEFT half, discard right
    }
  }

  return -1; // not found
}

// ─────────────────────────────────────────────
// Binary Search Template for "find boundary" problems
// e.g., "find the first position where condition is true"
// ─────────────────────────────────────────────

function findFirstTrue(arr, condition) {
  let left = 0, right = arr.length - 1, result = -1;

  while (left <= right) {
    const mid = left + Math.floor((right - left) / 2);
    if (condition(arr[mid])) {
      result = mid;     // record this as a candidate answer
      right = mid - 1; // but keep looking left for an earlier match
    } else {
      left = mid + 1;  // condition not met, look right
    }
  }

  return result;
}

// Example: find first element >= 5 in sorted array
const sorted = [1, 2, 3, 5, 7, 8, 10];
console.log(binarySearch(sorted, 7));                          // 4 (index)
console.log(binarySearch(sorted, 6));                          // -1 (not found)
console.log(findFirstTrue(sorted, x => x >= 5));               // 3 (index of 5)
```

---

## 3. Recursion

### What is it?
Recursion is a technique where a function **calls itself** to solve a smaller version of the same problem, until it hits a **base case** (the stopping condition).

Think of Russian nesting dolls — each doll contains a smaller version, until you reach the smallest one that can't be opened further.

### Why do we use Recursion?
- **Elegant solutions** for naturally recursive problems: trees, graphs, divide & conquer
- Code is often much shorter and more readable than iterative equivalents
- Essential for DFS traversal, backtracking, dynamic programming

### The 3 Laws of Recursion
1. Must have a **base case** (stops the recursion)
2. Must **change its state** and move toward the base case
3. Must **call itself**

### Pitfall: Stack Overflow
Every recursive call uses stack space. Without a base case (or with too deep recursion), you'll exhaust the call stack. Most languages have a limit ~10,000–50,000 calls.

### Code Example

```javascript
// ─────────────────────────────────────────────
// Recursion — From simple to powerful examples
// ─────────────────────────────────────────────

// Example 1: Factorial
// n! = n * (n-1) * (n-2) * ... * 1
function factorial(n) {
  if (n <= 1) return 1;       // BASE CASE: stop here
  return n * factorial(n - 1); // RECURSIVE CASE: smaller problem
}
// How it resolves:
// factorial(4)
//   → 4 * factorial(3)
//     → 4 * 3 * factorial(2)
//       → 4 * 3 * 2 * factorial(1)
//         → 4 * 3 * 2 * 1 = 24
console.log(factorial(4)); // 24

// ─────────────────────────────────────────────
// Example 2: Fibonacci (naive vs memoized)
// fib(n) = fib(n-1) + fib(n-2)
// ─────────────────────────────────────────────

// NAIVE — O(2^n): extremely slow, recalculates the same values repeatedly
function fibNaive(n) {
  if (n <= 1) return n;
  return fibNaive(n - 1) + fibNaive(n - 2);
}

// MEMOIZED — O(n): cache results to avoid redundant calculations
function fibMemo(n, memo = {}) {
  if (n in memo) return memo[n]; // already computed? return cached result
  if (n <= 1) return n;          // base case

  memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo); // store result
  return memo[n];
}

console.log(fibNaive(10)); // 55 — fine for small n
console.log(fibMemo(50));  // 12586269025 — fast for large n

// ─────────────────────────────────────────────
// Example 3: Flatten a nested array (classic recursion problem)
// Input:  [1, [2, [3, [4]]]]
// Output: [1, 2, 3, 4]
// ─────────────────────────────────────────────

function flatten(arr) {
  const result = [];
  for (const item of arr) {
    if (Array.isArray(item)) {
      result.push(...flatten(item)); // recurse into nested arrays
    } else {
      result.push(item); // base case: it's a plain value, just add it
    }
  }
  return result;
}

console.log(flatten([1, [2, [3, [4]]]])); // [1, 2, 3, 4]
```

---

## 4. Greedy Algorithms

### What is it?
A greedy algorithm makes the **locally optimal choice at each step**, hoping it leads to the globally optimal solution.

Think of it like always picking the biggest coin when making change — greedy, but it works for standard coin denominations.

### Why do we use Greedy Algorithms?
- **Simple and fast** — usually O(n log n) due to a sort step
- When a greedy choice is provably globally optimal (has the "greedy choice property")
- Efficient for problems like activity selection, Huffman coding, Dijkstra's algorithm

### When does greedy FAIL?
Greedy doesn't always work. The classic example: making change with coins [1, 3, 4] to make 6.
- Greedy picks: 4 + 1 + 1 = **3 coins**
- Optimal: 3 + 3 = **2 coins**

For such cases, you need **Dynamic Programming**.

### Code Example

```javascript
// ─────────────────────────────────────────────
// Greedy Example 1: Activity Selection Problem
// Given a list of activities with start/end times,
// select the maximum number of non-overlapping activities.
// ─────────────────────────────────────────────

function activitySelection(activities) {
  // Step 1: Sort by END time (greedy choice — finish early, start more)
  activities.sort((a, b) => a.end - b.end);

  const selected = [];
  let lastEndTime = -Infinity; // track when the last selected activity ended

  for (const activity of activities) {
    // Greedy choice: if this activity starts after the last one ended, take it
    if (activity.start >= lastEndTime) {
      selected.push(activity);
      lastEndTime = activity.end; // update our "last finish time"
    }
    // Otherwise, skip it — it overlaps with our last selection
  }

  return selected;
}

const activities = [
  { name: "A", start: 0, end: 6 },
  { name: "B", start: 1, end: 4 },
  { name: "C", start: 3, end: 5 },
  { name: "D", start: 5, end: 7 },
  { name: "E", start: 5, end: 9 },
  { name: "F", start: 8, end: 9 },
];

const result = activitySelection(activities);
console.log(result.map(a => a.name)); // ["B", "D", "F"] — maximum 3 non-overlapping

// ─────────────────────────────────────────────
// Greedy Example 2: Minimum Coin Change
// (works with standard denominations: [1, 5, 10, 25])
// ─────────────────────────────────────────────

function minCoins(amount, coins) {
  // Sort coins in descending order (grab the biggest first)
  coins.sort((a, b) => b - a);
  const used = [];

  for (const coin of coins) {
    while (amount >= coin) {
      used.push(coin);  // use this coin
      amount -= coin;   // reduce remaining amount
    }
  }

  return used;
}

console.log(minCoins(41, [1, 5, 10, 25])); // [25, 10, 5, 1] — 4 coins
```

---

## 5. Dynamic Programming

### What is it?
Dynamic Programming (DP) solves problems by **breaking them into overlapping subproblems** and **storing the results** to avoid recomputation.

Think of it as "smart recursion with a memory".

### DP vs Greedy
- **Greedy**: make one local choice, never look back
- **DP**: explore all possibilities, store results, guarantee the optimal

### Two Approaches
1. **Top-Down (Memoization)**: Start with the big problem, recurse, cache results
2. **Bottom-Up (Tabulation)**: Start with the smallest subproblems, build up to the answer

### When to use DP?
Two key signals:
1. **Overlapping subproblems** — same subproblems solved multiple times
2. **Optimal substructure** — optimal solution built from optimal sub-solutions

### Classic DP Problems
| Problem | Description |
|---|---|
| Fibonacci | Overlapping subproblems in tree recursion |
| 0/1 Knapsack | Maximize value with weight constraint |
| Longest Common Subsequence | Similarity between two strings |
| Coin Change | Minimum coins for a target amount |
| Longest Increasing Subsequence | Longest ascending subsequence |

### Code Example

```javascript
// ─────────────────────────────────────────────
// Classic DP: 0/1 Knapsack Problem
//
// Given: items with weights and values, and a bag capacity
// Goal: maximize total value without exceeding capacity
// Constraint: each item can only be taken once (0/1)
// ─────────────────────────────────────────────

function knapsack(capacity, weights, values, n) {
  // dp[i][w] = max value using first i items with capacity w
  const dp = Array.from({ length: n + 1 }, () => new Array(capacity + 1).fill(0));

  for (let i = 1; i <= n; i++) {
    for (let w = 0; w <= capacity; w++) {
      // Option 1: Don't take item i
      dp[i][w] = dp[i - 1][w];

      // Option 2: Take item i (only if it fits)
      if (weights[i - 1] <= w) {
        const valueIfTaken = values[i - 1] + dp[i - 1][w - weights[i - 1]];
        dp[i][w] = Math.max(dp[i][w], valueIfTaken); // take the better option
      }
    }
  }

  return dp[n][capacity]; // answer: max value with all items and full capacity
}

// Items: [ gold(2kg,$3), silver(3kg,$4), diamond(4kg,$5), ruby(5kg,$6) ]
const weights = [2, 3, 4, 5];
const values  = [3, 4, 5, 6];
const capacity = 8;
console.log(knapsack(capacity, weights, values, weights.length)); // 10

// ─────────────────────────────────────────────
// DP Example 2: Coin Change (min coins for amount)
// This is where greedy FAILS for some coin sets
// ─────────────────────────────────────────────

function coinChange(coins, amount) {
  // dp[i] = minimum coins needed to make amount i
  // Fill with Infinity initially (means "impossible")
  const dp = new Array(amount + 1).fill(Infinity);
  dp[0] = 0; // base case: 0 coins needed to make amount 0

  for (let i = 1; i <= amount; i++) {
    for (const coin of coins) {
      if (coin <= i) {
        // Using this coin: 1 + however many we needed for (i - coin)
        dp[i] = Math.min(dp[i], 1 + dp[i - coin]);
      }
    }
  }

  return dp[amount] === Infinity ? -1 : dp[amount];
}

// With coins [1, 3, 4], greedy gives 3 coins for amount 6 (4+1+1)
// DP correctly finds 2 coins (3+3)
console.log(coinChange([1, 3, 4], 6)); // 2 — optimal!
console.log(coinChange([2], 3));        // -1 — impossible
```

---

## 6. Graph Traversal

### What is it?
Graph traversal means **visiting every node** in a graph systematically. There are two fundamentally different strategies:

| | BFS (Breadth-First Search) | DFS (Depth-First Search) |
|---|---|---|
| Strategy | Explore layer by layer (level by level) | Go as deep as possible first |
| Data Structure | Queue | Stack (or recursion) |
| Finds | Shortest path in unweighted graphs | Any path, cycles, connected components |
| Space | O(V) — can be large for wide graphs | O(V) — can be large for deep graphs |
| Use cases | Shortest path, social network distance | Topological sort, cycle detection, maze solving |

### BFS — Visualized
```
Graph:
    A
   / \
  B   C
 / \   \
D   E   F

BFS order: A → B → C → D → E → F   (layer by layer)
DFS order: A → B → D → E → C → F   (go deep first)
```

### Code Example

```javascript
// ─────────────────────────────────────────────
// BFS — Breadth-First Search
// Use case: find shortest path (by number of edges) between two nodes
// ─────────────────────────────────────────────

function bfs(graph, start) {
  const visited = new Set();  // track visited nodes to avoid cycles
  const queue = [start];      // start with the source node
  const order = [];

  visited.add(start);

  while (queue.length > 0) {
    const node = queue.shift(); // dequeue the front node (FIFO)
    order.push(node);

    for (const neighbor of graph[node] || []) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);    // mark as visited BEFORE enqueuing (important!)
        queue.push(neighbor);     // explore this neighbor next
      }
    }
  }

  return order;
}

// ─────────────────────────────────────────────
// BFS Shortest Path
// Returns the minimum number of hops from source to target
// ─────────────────────────────────────────────

function shortestPath(graph, start, end) {
  if (start === end) return 0;

  const visited = new Set([start]);
  const queue = [[start, 0]]; // [node, distance from start]

  while (queue.length > 0) {
    const [node, distance] = queue.shift();

    for (const neighbor of graph[node] || []) {
      if (neighbor === end) return distance + 1; // found it!
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push([neighbor, distance + 1]);
      }
    }
  }

  return -1; // no path exists
}

// ─────────────────────────────────────────────
// DFS — Depth-First Search (recursive)
// Use case: detect cycles, topological sort, connected components
// ─────────────────────────────────────────────

function dfs(graph, start, visited = new Set(), order = []) {
  visited.add(start);
  order.push(start);

  for (const neighbor of graph[start] || []) {
    if (!visited.has(neighbor)) {
      dfs(graph, neighbor, visited, order); // go deeper before coming back
    }
  }

  return order;
}

// ─────────────────────────────────────────────
// DFS Iterative (using explicit stack instead of call stack)
// Same result, avoids stack overflow for very deep graphs
// ─────────────────────────────────────────────

function dfsIterative(graph, start) {
  const visited = new Set();
  const stack = [start];
  const order = [];

  while (stack.length > 0) {
    const node = stack.pop(); // pop from top (LIFO)

    if (!visited.has(node)) {
      visited.add(node);
      order.push(node);

      for (const neighbor of graph[node] || []) {
        if (!visited.has(neighbor)) {
          stack.push(neighbor); // push neighbors to explore later
        }
      }
    }
  }

  return order;
}

// Test with a sample graph (adjacency list)
const graph = {
  A: ["B", "C"],
  B: ["A", "D", "E"],
  C: ["A", "F"],
  D: ["B"],
  E: ["B"],
  F: ["C"]
};

console.log("BFS:", bfs(graph, "A"));          // A B C D E F
console.log("DFS:", dfs(graph, "A"));           // A B D E C F
console.log("Shortest A→F:", shortestPath(graph, "A", "F")); // 2

// ─────────────────────────────────────────────
// Topological Sort (DFS-based)
// Used for: task scheduling, build systems, course prerequisites
// Only valid for DAGs (Directed Acyclic Graphs)
// ─────────────────────────────────────────────

function topologicalSort(graph) {
  const visited = new Set();
  const result = []; // will be built in reverse order

  function dfsTopoHelper(node) {
    visited.add(node);
    for (const neighbor of graph[node] || []) {
      if (!visited.has(neighbor)) {
        dfsTopoHelper(neighbor);
      }
    }
    result.push(node); // push AFTER all descendants are processed
  }

  for (const node of Object.keys(graph)) {
    if (!visited.has(node)) {
      dfsTopoHelper(node);
    }
  }

  return result.reverse(); // reverse to get the correct topological order
}

// Course prerequisites: must take A before B, B before C, etc.
const courses = {
  "Intro":      ["Data Structures"],
  "Data Structures": ["Algorithms"],
  "Algorithms": ["Advanced Algorithms"],
  "Advanced Algorithms": []
};

console.log("Course order:", topologicalSort(courses));
// ["Intro", "Data Structures", "Algorithms", "Advanced Algorithms"]
```

---

# Quick Reference Cheat Sheet

## Data Structure — When to Use

| Data Structure | Best For | Avoid When |
|---|---|---|
| **Array** | Index-based access, iteration, sorting | Frequent mid-insertions/deletions |
| **Linked List** | Frequent head insertions/deletions, unknown size | Need random access by index |
| **Stack** | Undo/redo, call stack, bracket matching, DFS | Need access to arbitrary elements |
| **Queue** | BFS, task scheduling, print spooler | Need access to arbitrary elements |
| **BST** | Sorted data, range queries, O(log n) operations | Unsorted insertions causing imbalance |
| **Heap** | Priority queue, top-K elements, Dijkstra | Need arbitrary access or sorted traversal |
| **Graph** | Relationships, networks, paths | Simple hierarchical data (tree suffices) |
| **Hash Table** | Key-value lookup, frequency counting, caching | Need sorted keys, range queries |

## Algorithm — Complexity at a Glance

| Algorithm | Time | Space | Notes |
|---|---|---|---|
| Merge Sort | O(n log n) | O(n) | Stable, guaranteed |
| Quick Sort | O(n log n) avg | O(log n) | Fast in practice, O(n²) worst |
| Binary Search | O(log n) | O(1) | Requires sorted input |
| BFS | O(V + E) | O(V) | Shortest path (unweighted) |
| DFS | O(V + E) | O(V) | Cycles, components, topo sort |
| Dynamic Programming | Varies | Varies | Optimal subproblems + overlap |
| Greedy | O(n log n) usually | O(1) | Fast, not always optimal |

## The Problem-Solving Framework

```
1. UNDERSTAND the problem
   - What is the input? What is the output?
   - What are the constraints? (size of n, edge cases)

2. EXPLORE examples
   - Small examples, edge cases (empty, single element, duplicates)

3. BREAK IT DOWN
   - Write pseudocode or outline steps before coding

4. SOLVE it — start simple
   - Brute force first (correctness > efficiency initially)

5. OPTIMIZE
   - Identify bottlenecks: nested loops? repeated work?
   - Consider: sorting first? hash table for O(1) lookup? DP to cache?

6. VERIFY
   - Test with your examples, edge cases
   - Check time/space complexity
```

---

> **Final Note:** The difference between a good and great engineer is not memorizing every algorithm — it's recognizing *which pattern applies* to a problem. With enough practice, you'll spot "this needs a sliding window", "this is a graph BFS", "this has overlapping subproblems → DP" instinctively. That pattern recognition is the real goal.
