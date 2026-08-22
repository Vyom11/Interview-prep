# Phase 1 — Python Fundamentals (Master Document)

**Goal:** Learn Python syntax and core programming logic, progressing from basic usage to a deep, under-the-hood understanding of how CPython executes this code.

---

## 1 — Input / Output basics (`input()`, `print()`)

**1. What it means & Senior Insights**
*   `input()` reads a line of text from the user (`stdin`) and returns it as a string.
*   `print()` writes text to the standard output (`stdout`).
*   **Senior Insight:** `print()` is essentially a high-level wrapper around `sys.stdout.write()`. By default, I/O in Python is blocking. In high-throughput async applications, standard printing can bottleneck the event loop.

**2. Why this exists / alternatives**
Programs must communicate. `input()` and `print()` are the built-in ways to handle standard console interactions.
*   *Alternatives:* GUI toolkits, Web APIs, `logging` modules, and `sys.stdin`/`sys.stdout` for raw stream control. In production systems, the `logging` module is mandatory over `print()` for non-interactive output.

**3. Focused code snippet**
```python
import sys

# input() always returns a string; convert when needed
age_str = input("Enter your age: ") 
try:
    age = int(age_str)
except ValueError:
    age = None

# f-string is the modern, readable way to combine output
print(f"You are {age} years old.")

# print advanced parameters
print("A", "B", "C", sep=" | ", end=" <<< done\n")

# Senior pattern: force flush in containerized environments
print("Processing data...", flush=True) 

# Under the hood: print is doing this
sys.stdout.write("Hello standard output\n")
```

**4. All possible operations / use-cases**
*   Type conversion after input: `int()`, `float()`.
*   Interactive prompting loops to validate input.
*   Redirecting stdout: `print(..., file=open('out.txt','w'))`.

**5. Edge cases & errors**
*   `int(input())` with a non-numeric string raises `ValueError`.
*   `input()` raises `EOFError` if stdin is closed (e.g., piped input ends) or `KeyboardInterrupt` (Ctrl+C).
*   **Senior Edge Case:** Containerized apps (Docker/systemd) buffer stdout. If a script crashes, buffered `print()` statements are lost. Using `flush=True` or running Python with `python -u` (unbuffered) prevents swallowed logs.

**6. Best practices**
*   Never trust user input; always validate and explicitly convert explicitly.
*   Use `logging` for production diagnostics; reserve `print()` for debugging and CLI tool feedback.

---

## 2 — Variables and basic types

**1. What it means & Senior Insights**
Variables are names bound to objects. Python variables are dynamically typed. Basic types: `int`, `float`, `bool`, `str`, `NoneType`.
*   **Senior Insight (Object References):** Variables are not "buckets" holding values; they are **pointers** to objects in memory. `a = 10` means `a` points to an integer object `10`.
*   **Senior Insight (Interning):** CPython pre-allocates small integers (`-5` to `256`) and small strings. If `a = 100` and `b = 100`, `a is b` evaluates to `True` because they point to the exact same memory address.

**2. Why this exists / alternatives**
Variables store state. Dynamic typing simplifies rapid development. Statically typed languages (C, Java) require explicit declarations, trading development speed for compile-time safety.

**3. Focused code snippet**
```python
a = 10                # int
b = 3.14              # float
c = True              # bool (subclass of int: True == 1)

# Multiple assignments and unpacking
x = y = 0             
p, q = 1, 2           
p, q = q, p           # pythonic swap

# Senior concepts: Identity vs Equality
val1 = 256
val2 = 256
print(val1 == val2)   # True (Equality: values are the same)
print(val1 is val2)   # True (Identity: same memory address due to interning)

# Memory addresses (CPython)
print(id(val1))
```

**4. All possible operations / use-cases**
*   Rebinding: `name = new_value` (types can change at runtime).
*   Arithmetic: `+ - * / // % **`.
*   Casting: `int()`, `float()`, `str()`, `bool()`.

**5. Edge cases & errors**
*   Division by zero: `ZeroDivisionError`.
*   Floating point precision: `0.1 + 0.2 != 0.3` due to IEEE 754 binary representation.
*   **Senior Edge Case:** `bool` is a subclass of `int`. `True + True == 2` is valid Python, which can cause subtle logic bugs if mixing types. Python handles arbitrarily large ints seamlessly, but operations on massive ints consume heavy memory/CPU.

**6. Best practices**
*   Use descriptive variable names (`snake_case` in Python).
*   Prefer `isinstance(obj, type)` over `type(obj) == type` for type checking, as it supports inheritance.
*   Use `is` for comparing to `None` (`if x is None:`), and `==` for comparing values.

---

## 3 — String basics

**1. What it means & Senior Insights**
Strings (`str`) are immutable sequences of Unicode characters.
*   **Senior Insight (PEP 393):** CPython dynamically sizes strings in memory. An all-ASCII string uses 1 byte per character, but adding a single emoji converts the *entire* string array to use 4 bytes per character in memory.
*   **Senior Insight (f-strings):** f-strings are not just syntax sugar; they are evaluated at runtime directly into C code, making them faster than `.format()` or `%`.

**2. Why this exists / alternatives**
Strings handle textual data. Python’s default Unicode support is crucial for global apps. 
*   *Alternative:* `bytes` for raw binary data; `bytearray` for mutable binary.

**3. Focused code snippet**
```python
s = "Hello, world!"
raw = r"C:\new\text"       # raw string (ignores backslash escapes)

# Indexing and slicing: string[start:stop:step]
first = s[0]               # 'H'
slice_mid = s[7:12]        # 'world'

# Formatting
name, age = "Bob", 25
msg = f"{name} is {age} years old."

# Senior Pattern: Efficient string building
words = ["A", "B", "C"]
efficient_concat = "".join(words)  # O(N) time
```

**4. All possible operations / use-cases**
*   Indexing, slicing, concatenation (`+`), repetition (`*`).
*   Methods: `.upper()`, `.lower()`, `.strip()`, `.split()`, `.replace()`.
*   Membership: `"sub" in s`.

**5. Edge cases & errors**
*   Out of range indexing raises `IndexError` (though slicing gracefully handles out-of-bounds).
*   **Senior Edge Case (Immutability Trap):** Concatenating strings in a massive loop (`s += new_chunk`) is an anti-pattern. Because strings are immutable, it copies the entire string in memory on every loop, resulting in `O(N^2)` time complexity. Always append to a list and use `''.join(list)`.

**6. Best practices**
*   Always use f-strings for formatting.
*   Be mindful of encoding (`.encode('utf-8')` / `.decode('utf-8')`) when moving between `str` and `bytes`.

---

## 4 — Control Flow (`if` / `elif` / `else`)

**1. What it means & Senior Insights**
Conditionals guide program flow based on boolean expressions.
*   **Senior Insight (Truthiness):** Python evaluates objects implicitly. Empty collections (`[]`, `{}`, `""`), `0`, and `None` are considered `False`. This works because CPython checks the object's `__bool__()` or `__len__()` dunder methods.
*   **Senior Insight (Short-Circuiting):** In `if A and B:`, Python stops evaluating if `A` is `False`. In `if A or B:`, it stops if `A` is `True`.

**2. Why this exists / alternatives**
Programs must react to data dynamically. 
*   *Alternatives:* Ternary operator `x if cond else y`; Structural Pattern Matching (`match-case`).

**3. Focused code snippet**
```python
x = 10
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# Ternary expression
result = "even" if x % 2 == 0 else "odd"

# Senior pattern: Short-circuit evaluation for safety
data = None
if data is not None and data.get("key") == "value":
    pass  # Prevents AttributeError if data is None

# Truthiness
items = []
if not items:
    print("List is empty")  # Pythonic way to check emptiness
```

**5. Edge cases & errors**
*   Using `=` (assignment) instead of `==` (comparison) raises `SyntaxError`. Python 3.8+ introduced the Walrus operator (`:=`) for deliberate inline assignment.
*   **Senior Edge Case:** Relying too heavily on truthiness can hide bugs. `if value:` triggers on `0`, `False`, `None`, and `""`. If you specifically mean "not null", explicitly write `if value is not None:`.

**6. Best practices**
*   Extract complex compound conditions into well-named variables: `is_valid_user = (age > 18 and has_license)`.
*   Return early from functions to avoid deeply nested `if/else` statements (Guard clauses).

---

## 5 — Loops (`for` / `while`)

**1. What it means & Senior Insights**
*   **`for`**: Iterates over an iterable. **Senior Insight:** Under the hood, the `for` loop calls `iter(obj)` to get an Iterator, then calls `next(obj)` repeatedly until a `StopIteration` exception is raised.
*   **`while`**: Repeats while a condition is true.
*   **Senior Insight (`for...else`):** Python has a unique `else` block for loops. It executes *only* if the loop finishes naturally (without hitting a `break`).

**2. Why this exists / alternatives**
Iteration. Alternatives include `map()` / `filter()`, list comprehensions, or recursion.

**3. Focused code snippet**
```python
fruits = ["apple", "banana", "cherry"]

# Basic for loop with enumerate
for i, fruit in enumerate(fruits):
    print(i, fruit)

# while loop
n = 3
while n > 0:
    n -= 1

# Senior pattern: The for...else construct for searching
target = "cherry"
for fruit in fruits:
    if fruit == target:
        print("Found it!")
        break
else:
    # Runs ONLY if the loop did NOT break
    print("Target not found.")
```

**5. Edge cases & errors**
*   Infinite loops: `while True:` without a reachable `break`.
*   **Senior Edge Case:** Modifying a list while iterating over it yields skipped items or infinite loops. *Fix:* Iterate over a copy (`for item in my_list[:]:`) or build a new list.
*   **Senior Edge Case:** Iterating over massive lists consumes high memory. Seniors use **Generators** (`(x for x in data)`) to yield items one at a time efficiently.

**6. Best practices**
*   Use `for` when iterating over collections; `while` for event/condition-driven loops.
*   Never manage indices manually if `enumerate()` or `zip()` can do it for you.

---

## 6 — `range()`

**1. What it means & Senior Insights**
`range()` produces an immutable sequence of numbers. 
*   **Senior Insight:** `range` is a lazy **Sequence object**, NOT a generator or an iterator. You can iterate over it, but you can also get its length (`len(range(10))`) and index it (`range(10)[5]`) without materializing it. 
*   **Senior Insight (O(1) Membership):** `999_999_999 in range(1_000_000_000)` executes instantly. Python doesn't iterate to check; it uses math under the hood: `(val - start) % step == 0`.

**3. Focused code snippet**
```python
# range(start, stop, step)
for i in range(10, 0, -2):
    print(i)  # 10, 8, 6, 4, 2

# Efficient Senior operations
r = range(0, 1000000, 5)
print(len(r))       # Instant
print(999995 in r)  # Instant O(1) math check
```

**5. Edge cases & errors**
*   `step=0` raises `ValueError`.
*   Converting massive ranges to lists (`list(range(10**9))`) will cause a `MemoryError`.
*   Floats are invalid; `range()` only accepts `int`.

---

## 7 — Loop controls (`break`, `continue`, `pass`)

**1. What it means & Senior Insights**
*   `break`: Exits the nearest enclosing loop.
*   `continue`: Skips the rest of the current iteration, moves to the next.
*   `pass`: Syntactic no-op.
*   **Senior Insight:** If a loop is wrapped in a `try...finally` block, `break` or `continue` will still guarantee that the `finally` block executes before the jump occurs.

**3. Focused code snippet**
```python
for i in range(5):
    if i == 1:
        continue  # skip 1
    if i == 3:
        break     # stop at 3
    print(i)      # prints 0, 2

def incomplete_function():
    pass  # Placeholder, prevents SyntaxError
```

**6. Best practices**
*   Use `break` early to flatten loop logic.
*   Avoid overusing `continue` in highly nested loops as it makes control flow hard to track (spaghetti code).

---

## 8 — `match-case` (Structural Pattern Matching)

**1. What it means & Senior Insights**
Introduced in Python 3.10, `match-case` is far more than a switch statement. It allows you to match variables against values, types, and complex data structures while simultaneously **destructuring** (extracting) the data.

**2. Why this exists / alternatives**
It replaces long, unreadable chains of `if isinstance(...) and len(...) == ...` with declarative, clean matching logic (inspired by functional languages like Rust and Scala).

**3. Focused code snippet**
```python
def process_response(data):
    match data:
        # Match literal
        case 200:
            return "OK"
        # Destructure a sequence (list/tuple)
        case ["error", code, msg]:
            return f"Error {code}: {msg}"
        # Match dictionary, extract specific keys, add a guard (if)
        case {"user": name, "age": int(age)} if age >= 18:
            return f"Adult user: {name}"
        # Match object by type
        case ValueError(args=(msg,)):
            return f"ValueError caught: {msg}"
        # Wildcard fallback
        case _:
            return "Unknown format"

print(process_response({"user": "Alice", "age": 25, "extra": "ignored"}))
```

**5. Edge cases & errors**
*   **The Name Binding Trap:** `case x:` binds the matched value to a new variable `x`. It does *not* compare against an existing variable `x`. To compare against an existing variable or constant, use dotted names (e.g., `case constants.SUCCESS:`).
*   Dictionaries structurally match explicitly mentioned keys; extra keys in the dictionary are ignored automatically.

---

## 9 — Functions (The Core of Logic)

**1. What it means & Senior Insights**
Functions are reusable blocks of code. 
*   **Senior Insight:** Functions in Python are "First-Class Citizens" (objects of type `function`). They can be passed as arguments, returned from other functions, and have attributes attached to them.
*   **Scope:** Python resolves variables using the **LEGB rule**: Local, Enclosing, Global, Built-in.

**2. Why this exists / alternatives**
Encapsulation, reusability (DRY - Don't Repeat Yourself), and defining specific scopes.

**3. Focused code snippet**
```python
# Type hinting for Senior-level readability
def fetch_data(url: str, retries: int = 3, *, timeout: float = 5.0) -> dict:
    """
    Fetch data. The '*' forces 'timeout' to be a Keyword-Only argument.
    """
    return {"status": "success"}

# *args (tuple of pos args) and **kwargs (dict of keyword args)
def wrapper(*args, **kwargs):
    print(f"Positional: {args}, Keyword: {kwargs}")

# Scope & Closures
def outer():
    x = "enclosing"
    def inner():
        nonlocal x      # Modifies the enclosing scope, NOT global
        x = "modified"
    inner()
    return x
```

**5. Edge cases & errors**
*   **The Mutable Default Argument Trap (Classic Interview Question):** 
    `def append_item(item, my_list=[]):` -> Default arguments are evaluated **once at definition time**, not at execution time. The same list persists across calls! 
    *Senior fix:* `def append_item(item, my_list=None): my_list = my_list or []`.
*   **Late Binding Closures:** `functions = [lambda: i for i in range(3)]`. All lambdas return `2` because they look up `i` at execution time, not definition time.
*   **Recursion Limits:** Python does *not* have Tail Call Optimization (TCO). Deep recursion will hit `sys.getrecursionlimit()` (default 1000) and crash with a `RecursionError`. Use iteration for deep tree traversals.

---

## 10 — Comments, Docstrings & Type Hints

**1. What it means & Senior Insights**
*   **Comments (`#`)**: Explain *why* code exists, not *what* it does.
*   **Docstrings (`"""..."""`)**: Attached to the `__doc__` attribute of modules, classes, and functions. Accessible via `help()`.
*   **Type Hints (`: type`)**: Introduced in PEP 484. They do not affect runtime (Python remains dynamically typed), but allow IDEs and static analyzers (`mypy`) to catch bugs before execution.

**3. Focused code snippet**
```python
def calculate_discount(price: float, discount: float) -> float:
    """
    Calculate the final price after a discount.
    
    Args:
        price (float): Original price.
        discount (float): Discount percentage (0.0 to 1.0).
        
    Returns:
        float: The final calculated price.
    """
    # Using max() ensures the price never drops below 0
    return max(0.0, price - (price * discount))
```

**6. Best practices**
*   Follow **PEP 8** (Style Guide) and **PEP 257** (Docstring Conventions).
*   Avoid redundant comments (e.g., `x = x + 1 # adds 1 to x`). Let the code explain *what*; let the comment explain *why* (e.g., `# offset by 1 to handle zero-indexed arrays`).
*   In a senior environment, explicitly type-hint all function signatures.

### Interview Questions:
---

### Category 1: Memory, Variables, and Built-in Types
1. **The Equality vs Identity Question:** "Explain the difference between the `is` operator and the `==` operator. When is it strictly required to use `is`?"
    * *What they look for:* `is` checks memory address (identity), `==` checks value (equality). `is` should be used for singletons like `None`, `True`, or `False`.
2. **The Interning Question:** "If I type `a = 256; b = 256`, `a is b` returns `True`. But if I type `a = 257; b = 257` in the REPL, `a is b` returns `False`. Why?"
    * *What they look for:* Knowledge of CPython's small integer caching/interning (pre-allocating integers from -5 to 256).
3. **The Garbage Collection Question:** "How does Python manage memory under the hood when variables are reassigned or go out of scope?"
    * *What they look for:* Reference counting (`sys.getrefcount`) as the primary mechanism, backed by a cyclic Garbage Collector to detect circular references.
4. **The Boolean Trap:** "What is the result of `True + True` in Python, and why?"
    * *What they look for:* `bool` is a subclass of `int`. The result is `2`. This tests knowledge of Python's type hierarchy.

### Category 2: Strings and Performance
5. **The String Concatenation Trap:** "You need to concatenate 100,000 strings in a `for` loop. If you use `s += new_string`, what is the time complexity, and why? What is the pythonic alternative?"
    * *What they look for:* Strings are immutable. `+=` creates a new string in memory every iteration, resulting in $O(N^2)$ time. The senior alternative is appending to a list and using `''.join(list)` for $O(N)$ time.
6. **The f-string internals:** "We have `.format()`, `%s`, and f-strings. Why are f-strings functionally faster than the other two?"
    * *What they look for:* f-strings are evaluated directly at runtime into efficient C code, whereas `.format()` requires parsing a string method and looking up arguments.
7. **The PEP 393 Question:** "How does CPython determine the memory size of a string? What happens to memory if I append a single Unicode emoji to a massive ASCII string?"
    * *What they look for:* Flexible String Representation. CPython dynamically resizes the *entire* string array to 4 bytes per character (UCS-4) if even one character requires it.

### Category 3: Functions, Scope, & Closures (High Hit Rate)
8. **The Mutable Default Argument (Classic Trap):** "Explain what happens here: `def add_item(item, result=[]): result.append(item); return result`. How do you fix it?"
    * *What they look for:* Default arguments are evaluated *once* at definition (compile) time, not runtime. The list persists across calls. Fix: `result=None`, then `if result is None: result = []`.
9. **The Late Binding Closure:** "What does this output: `funcs = [lambda: i for i in range(3)]; print([f() for f in funcs])`. Why?"
    * *What they look for:* It outputs `[2, 2, 2]`. Lambdas look up the variable `i` at execution time, at which point the loop has finished and `i` is 2. Fix: `lambda i=i: i`.
10. **The LEGB Rule:** "How does Python resolve variable scopes? What is the LEGB rule?"
    * *What they look for:* Local, Enclosing, Global, Built-in.
11. **Keyword-Only Arguments:** "If I write a function signature like `def fetch(url, *, timeout=5):`, what does the `*` do?"
    * *What they look for:* It forces `timeout` to be a keyword-only argument. You cannot call `fetch("url", 5)`.
12. **Recursion Limit:** "Does Python support Tail Call Optimization (TCO)? What happens if I write a highly recursive function?"
    * *What they look for:* No TCO. It will hit `sys.getrecursionlimit()` (usually 1000) and raise a `RecursionError`.
13. **Global vs Nonlocal:** "When would you use the `nonlocal` keyword instead of `global`?"
    * *What they look for:* `nonlocal` modifies variables in the *enclosing* function's scope (useful in closures and decorators), while `global` modifies module-level variables.

### Category 4: Control Flow, Truthiness & `match-case`
14. **Truthiness Mechanics:** "How does Python determine if a custom object is 'truthy' or 'falsy' in an `if` statement?"
    * *What they look for:* Python looks for the `__bool__()` dunder method. If missing, it falls back to `__len__()` (where 0 is False).
15. **Short-Circuit Evaluation:** "Why is `if user is not None and user.is_active:` safe from an AttributeError if `user` is None?"
    * *What they look for:* `and` stops evaluating immediately if the left side is False.
16. **The Match-Case Name Trap:** "In Python 3.10+, I have a constant `SUCCESS = 200`. I write `case SUCCESS:` inside a match block. But it matches everything. Why?"
    * *What they look for:* `case x:` binds the matched value to the local variable name. It overrides the constant. You must use dotted names like `case constants.SUCCESS:` to check against a value.
17. **Match-case vs Dict `get`:** "Can `match-case` match dictionaries without explicitly matching every single key?"
    * *What they look for:* Yes, structural pattern matching in dicts only checks the explicitly requested keys and automatically ignores extra keys.

### Category 5: Loops, Iterators, and `range`
18. **The `for...else` Construct:** "What does the `else` block do in a `for` loop? Give a real-world use case."
    * *What they look for:* It executes only if the loop completes without hitting a `break`. Used for search algorithms ("search for item, break if found; else handle not found").
19. **Looping Mutability:** "What is the danger of removing items from a list while iterating over it in a `for` loop? How do you safely accomplish this?"
    * *What they look for:* It shifts indices, causing elements to be skipped or resulting in an `IndexError`. Safest way: iterate over a copy (`for item in my_list[:]:`) or use a list comprehension to build a new list.
20. **Is Range an Iterator?:** "If I type `type(range(10))`, what does it return? Is it a generator?"
    * *What they look for:* It returns `<class 'range'>`. It is a lazy *Sequence*, not an Iterator or Generator. 
21. **Range O(1) Membership:** "Why does `999999999 in range(1000000000)` execute instantly, while `999999999 in [0, 1, ..., 1000000000]` takes time and crashes memory?"
    * *What they look for:* `range` implements `__contains__` via O(1) mathematical computation (`(val - start) % step == 0`), rather than O(N) iteration.
22. **The `finally` loop jump:** "If you have a `continue` inside a `try` block that is inside a `for` loop, and you also have a `finally` block... does the `finally` block run before the loop skips to the next iteration?"
    * *What they look for:* Yes. The `finally` block is guaranteed to execute before the jump (`break`, `continue`, or `return`) occurs.

### Category 6: Standard I/O & Execution Environment
23. **The Docker/Stdout Trap:** "Your Python script is running in a Docker container or managed by Systemd. The script crashes, but your `print()` statements from right before the crash aren't in the logs. Why?"
    * *What they look for:* Python's `stdout` is buffered. Use `print(..., flush=True)` or run python with the `-u` (unbuffered) flag.
24. **Blocking I/O:** "In an asynchronous application (like FastAPI), why is it a bad idea to use the built-in `print()` function heavily?"
    * *What they look for:* `print()` is synchronous and blocking. It halts the event loop until the OS confirms the I/O write, drastically reducing the throughput of async servers.

### Category 7: Type Hints & Best Practices
25. **Typing at Runtime:** "Do Python type hints enforce type checking at runtime? What happens if I pass a string to `def add(a: int, b: int) -> int:`?"
    * *What they look for:* No, Python ignores them at runtime (it remains dynamically typed). The function will execute normally (and might concatenate strings). They are for static analysis tools like `mypy` and IDEs.
26. **Docstrings vs Comments:** "As a senior, how do you differentiate what should go in a `# comment` versus what goes in a `\"\"\" docstring \"\"\"`?"
    * *What they look for:* Docstrings define the contract (What does this do, arguments, return types) and are programmatically accessible via `__doc__`. Comments explain the *why* of specific lines of logic inside the code (e.g., "offset by 1 due to third-party API bug").