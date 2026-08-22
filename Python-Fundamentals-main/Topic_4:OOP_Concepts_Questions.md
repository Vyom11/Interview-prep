# Master Python OOP Interview Guide: Intermediate to Senior Engineer

This document evaluates candidates progressively. It begins with architectural fundamentals, moves into everyday intermediate Python mechanics, and scales up to advanced topics like memory management, the descriptor protocol, and metaprogramming.

---

## SECTION 1: Fundamental OOP Concepts & Architecture

#### 1. Explain the four pillars of OOP and how they manifest specifically in Python.
**Answer:**
*   **Encapsulation:** Bundling data and methods into a single unit and restricting access to internal states. *Pythonic implementation:* Python lacks strict `private` or `protected` keywords. It relies on convention (single underscore `_attr` for internal use) and name mangling (double underscore `__attr` to prevent naming collisions). 
*   **Abstraction:** Hiding complex implementation details and exposing only what is necessary. *Pythonic implementation:* Implemented using the `abc` module (Abstract Base Classes) to define interfaces via `@abstractmethod`, preventing instantiation of incomplete classes.
*   **Inheritance:** Establishing an "is-a" relationship to reuse code from parent classes. *Pythonic implementation:* Python supports both single and multiple inheritance, relying on the C3 Linearization algorithm (MRO) to resolve method calls.
*   **Polymorphism:** The ability of different objects to respond to the same method call in their own way. *Pythonic implementation:* Achieved largely through **Duck Typing** ("If it walks like a duck..."). Python checks for method presence at runtime rather than requiring strict inheritance hierarchies.

#### 2. "Favor Composition over Inheritance." Why is this a core architectural principle, and how does it look in Python?
**Answer:**
*   **The Problem with Inheritance:** Deep inheritance trees create tight coupling. Changes in a base class can break downstream subclasses (the "Fragile Base Class" problem).
*   **The Composition Solution:** Composition builds objects using "has-a" relationships instead of "is-a". Rather than a `FlyingCar` inheriting from both `Car` and `Plane`, a `Vehicle` class contains an `Engine` object and a `Wings` object. 
*   **In Python:** Composition is heavily utilized via Dependency Injection. Dataclasses (`@dataclass`) make composition exceptionally clean by easily bundling components together as fields.

#### 3. How do the SOLID principles apply to Python? Give examples.
**Answer:**
*   **S - Single Responsibility:** A `ReportGenerator` class shouldn't also manage database connections.
*   **O - Open/Closed:** Using Python's `functools.singledispatch` or plugins to add new behaviors without editing existing core classes.
*   **L - Liskov Substitution:** Subclasses should be replaceable for their parent classes. Static type checkers like `mypy` enforce this (e.g., ensuring overridden methods return matching types).
*   **I - Interface Segregation:** Instead of one massive interface, use smaller `typing.Protocol` classes to define narrow capabilities (e.g., `Loggable`, `Serializable`).
*   **D - Dependency Inversion:** High-level modules should depend on abstractions. Pass an abstract `StorageBackend` instance into an app layer rather than hardcoding an `S3Bucket` initialization inside it.

---

## SECTION 2: Intermediate Python OOP Mechanics

#### 4. What is the `@property` decorator and when should you use it?
**Answer:**
The `@property` decorator transforms a method into an attribute. It allows developers to define getters, setters (`@attr.setter`), and deleters (`@attr.deleter`).
*   **Usage:** It provides encapsulation. You can start with a simple public attribute (`obj.price`). If requirements change and you later need to validate the price before setting it, you can convert it to a `@property` without breaking the API for any clients currently using `obj.price = 10`.

#### 5. What is the difference between Class Variables and Instance Variables? What is the common "mutable default" gotcha?
**Answer:**
*   **Class Variables:** Declared inside the class but outside any methods. They are shared across *all* instances of the class. 
*   **Instance Variables:** Declared inside `__init__` using `self.variable_name`. They are unique to each instantiated object.
*   **The Gotcha:** If a class variable is mutable (like a `list` or `dict`), appending to it from one instance will alter it for *all* instances. Subclasses or instances should initialize mutable types in `__init__`.

#### 6. Explain the difference between `@classmethod` and `@staticmethod`.
**Answer:**
*   **`@classmethod`:** Takes `cls` as its first implicit argument. It can access and modify class state (which affects all instances). **Primary use case:** Creating "Factory Methods" (alternative constructors), e.g., `Date.from_string("2023-01-01")`.
*   **`@staticmethod`:** Takes neither `self` nor `cls`. It behaves exactly like a regular function but belongs to the class's namespace. **Primary use case:** Utility or helper functions logically related to the class but that don't need to read or modify class/instance state.

#### 7. What are "dunder" methods? Explain the difference between `__str__` and `__repr__`.
**Answer:**
Dunder (Double UNDERscore) methods, or magic methods, let classes interact with built-in Python functions and operators.
*   **`__str__`:** Meant to be **readable** and human-friendly. Used by `print()` and `str()`. If not defined, Python falls back to `__repr__`.
*   **`__repr__`:** Meant to be **unambiguous** and developer-friendly. Used by REPLs, logging, and `repr()`. Ideally, it should return a string containing valid Python code that could recreate the object (e.g., `Point(x=1, y=2)`).

#### 8. How do you make an object callable like a standard function?
**Answer:**
By implementing the `__call__(self, *args, **kwargs)` dunder method. This allows an instance of a class to be invoked as `obj()`. It is frequently used to create stateful functions, closures, or class-based decorators where you need to maintain state between calls.

---

## SECTION 3: Advanced Object Model & Execution (Senior Level)

#### 9. How does Python's Method Resolution Order (MRO) work, and how does it relate to `super()`?
**Answer:**
Python uses the **C3 Linearization algorithm** to determine MRO. It ensures a class always precedes its parents, and in multiple inheritance, base classes are searched in the order they are listed.
*   **`super()`:** `super()` does *not* simply call the parent. It delegates to the *next class in the MRO*. In cooperative multiple inheritance, `super()` inside a parent class might actually trigger a sibling class's method, not its own ancestor.

#### 10. What is the difference between `__new__` and `__init__`?
**Answer:**
*   `__new__` is an implicit class method responsible for **allocating memory** and returning a new instance.
*   `__init__` is an instance method responsible for **initializing** the object's state *after* creation. It returns `None`.
*   **Override `__new__` when:** Implementing the Singleton pattern, subclassing immutable built-ins (`tuple`, `str`), or in metaclass programming where the requested class might return a completely different type of object.

#### 11. Explain `__getattr__` vs. `__getattribute__`. What are the dangers?
**Answer:**
*   `__getattribute__` is called **unconditionally** every time an attribute is accessed.
*   `__getattr__` is called only as a **fallback** when an attribute is *not* found via normal lookup and `__getattribute__` raises an `AttributeError`.
*   **Dangers:** Overriding `__getattribute__` easily causes infinite recursion. Accessing `self.attr` inside it re-triggers the method. You must use `super().__getattribute__(item)` to fetch internal state safely.

---

## SECTION 4: State, Memory & Performance (Senior Level)

#### 12. What are `__slots__`? How do they work and what are their limitations?
**Answer:**
By default, objects store attributes in a dynamic dictionary (`__dict__`), carrying memory overhead. Defining `__slots__ = ('x', 'y')` suppresses `__dict__` creation, allocating space for fixed attributes via an array of pointers.
*   **Pros:** Slashes memory usage for millions of objects and speeds up attribute access.
*   **Limitations:** You cannot dynamically add new attributes at runtime. They complicate multiple inheritance, and they break weak references unless `'__weakref__'` is explicitly included in the slots.

#### 13. How does Garbage Collection work for Python objects? 
**Answer:**
Python utilizes **Reference Counting**; when an object's reference count hits zero, it is immediately deallocated.
*   **Cyclic References:** If Object A and Object B reference each other, their counts never hit zero.
*   **Generational GC:** To fix cycles, Python runs a tracing Garbage Collector with three "generations" (0, 1, 2). New objects start in Gen 0. If they survive a GC sweep, they are promoted. The GC specifically hunts down unreachable cyclic clusters and purges them.

---

## SECTION 5: Metaprogramming & Modern Python (Senior Level)

#### 14. Explain the Descriptor Protocol. Data vs. Non-Data Descriptors?
**Answer:**
A descriptor is any object defining `__get__`, `__set__`, or `__delete__`. Features like `@property`, `@classmethod`, and regular methods are all descriptors under the hood.
*   **Data Descriptor:** Defines both `__get__` and `__set__` (or `__delete__`). Data descriptors take precedence over the instance dictionary (`__dict__`). 
*   **Non-Data Descriptor:** Defines only `__get__`. The instance dictionary takes precedence over non-data descriptors (this is how instance variables can override methods).

#### 15. What is a Metaclass? Give a practical use case.
**Answer:**
Classes are instances of **metaclasses** (default is `type`). A metaclass intercepts and alters class creation at definition time.
*   **Use Cases:** 
    *   **ORMs (Django/SQLAlchemy):** Translating class attributes into database columns automatically during definition.
    *   **Registry Pattern:** Automatically registering subclasses to a central registry upon import without needing explicit decorators.

#### 16. What is the difference between Abstract Base Classes (ABCs) and Protocols (`typing.Protocol`)?
**Answer:**
*   **ABCs (`abc` module):** Enforce **Nominal Subtyping**. A class must explicitly inherit from the ABC. Enforced at runtime (prevents instantiation if abstract methods are missing).
*   **Protocols (PEP 544):** Enforce **Structural Subtyping** (Static Duck Typing). A class satisfies a Protocol simply by implementing the expected methods, *without* needing to inherit from the Protocol. Used primarily by static type checkers (`mypy`) for loose-coupling.

#### 17. How do `dataclasses` work? Why use `default_factory`?
**Answer:**
`@dataclass` reads class variable type hints and auto-generates boilerplate dunder methods (`__init__`, `__repr__`, `__eq__`).
*   **Mutable Defaults Problem:** Using `items: list = []` shares that single list across *all* instances. 
*   **`default_factory`:** Passing `field(default_factory=list)` calls `list()` to generate a fresh, isolated list for each new object.

---

## SECTION 6: Architecture Patterns & Whiteboard Scenarios

#### 18. Explain the concept of Mixins. How do you safely use them?
**Answer:**
A Mixin provides specific functionality via multiple inheritance but is not meant to be instantiated on its own.
*   **Safe usage:** Mixins should be **stateless** (no `__init__`). They must be listed **first** in the inheritance list (e.g., `class View(AuthMixin, BaseView):`) so their methods are prioritized in the MRO over the base class.

#### 19. Whiteboard Scenario: Operator Overloading (Dunder Math)
**Question:** *"Implement a `Vector` object that allows adding an integer to it, e.g., `Vector([1, 2]) + 5` AND `5 + Vector([1, 2])`."*
**Answer:** 
The candidate must demonstrate `__add__` and `__radd__`.
*   `__add__(self, other)` handles `Vector + 5`.
*   `__radd__(self, other)` handles `5 + Vector`. The built-in `int` does not know how to add a `Vector`, returning `NotImplemented`. Python then falls back to invoking `__radd__` on the right-hand operand (the Vector).

#### 20. Whiteboard Scenario: Resource Management
**Question:** *"Design a thread-safe database connection class that automatically acquires locks and closes connections, even if an exception occurs."*
**Answer:**
The candidate should implement the **Context Manager Protocol** (`__enter__` and `__exit__`).
*   `__enter__` acquires the lock and connection.
*   `__exit__(self, exc_type, exc_val, traceback)` handles teardown. It guarantees execution (like `finally`). The candidate should demonstrate checking `exc_type` to rollback a transaction on error, or commit if `exc_type is None`, before releasing the lock.