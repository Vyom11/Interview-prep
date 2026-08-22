# Advanced Design Patterns in Python: Architectural Blueprints & Best Practices

> 💡 **Tip:** Use the Table of Contents to jump between structural blueprints and senior-level interview preparation.

---

## Table of Contents

### Foundation & Theory
- [What Are Design Patterns?](#what-are-design-patterns)
- [Design Pattern vs. Algorithm](#design-pattern-vs-algorithm)
- [History of Design Patterns (GoF)](#history-of-design-patterns-gof)
- [5 Key Benefits](#5-key-benefits)
- [Classification of Design Patterns](#classification-of-design-patterns)
- [How to Apply Design Patterns](#how-to-apply-design-patterns)
- [Common Misconceptions](#common-misconceptions)
- [Criticisms of Design Patterns](#criticisms-of-design-patterns)
- [Most Important Takeaway](#most-important-takeaway)

### Creational Patterns
- [Singleton Pattern](#singleton-pattern)
- [Factory Method Pattern](#factory-method-pattern)
- [Abstract Factory Pattern](#abstract-factory-pattern)
- [Builder Pattern](#builder-pattern)
- [Prototype Pattern](#prototype-pattern)

### Structural Patterns
- [Adapter Pattern](#adapter-pattern)
- [Bridge Pattern](#bridge-pattern)
- [Composite Pattern](#composite-pattern)
- [Decorator Pattern](#decorator-pattern)
- [Facade Pattern](#facade-pattern)
- [Flyweight Pattern](#flyweight-pattern)
- [Proxy Pattern](#proxy-pattern)

### Behavioral Patterns
- [Observer Pattern](#observer-pattern)
- [Strategy Pattern](#strategy-pattern)
- [State Pattern](#state-pattern)
- [Chain of Responsibility Pattern](#chain-of-responsibility-pattern)
- [Command Pattern](#command-pattern)
- [Iterator Pattern](#iterator-pattern)
- [Mediator Pattern](#mediator-pattern)
- [Memento Pattern](#memento-pattern)
- [Template Method Pattern](#template-method-pattern)
- [Visitor Pattern](#visitor-pattern)

### Career & Industry Insights
- [The Complexity Rule](#the-complexity-rule)
- [Pythonic Patterns vs Java](#pythonic-patterns-vs-java)
- [Factory vs. Abstract Factory: Architect's Note](#factory-vs-abstract-factory-architects-note)
- [Master Revision Table](#master-revision-table)
- [The Interview Trap Vault](#the-interview-trap-vault)

---

# Foundation & Theory

## What Are Design Patterns?

Design Patterns are **standard reusable solutions** for commonly occurring problems in software design.

### The "Blueprints vs. Buildings" Analogy

> 🏗️ **Blueprints — not ready-made buildings.**

Think of design patterns like architectural blueprints:
- You **don't copy** them directly.
- You **understand** them, then implement according to your specific problem.
- They help you **design better architecture**, not just write code.

A pattern is a template. The building (your implementation) is unique to your requirements. This distinction is critical: patterns are starting points for thinking, not copy-paste solutions.

---

## Design Pattern vs. Algorithm

> ⚠️ **VERY IMPORTANT INTERVIEW POINT**

Design Pattern ≠ Algorithm. This is one of the most commonly confused distinctions in software engineering interviews.

| **Design Pattern** | **Algorithm** |
|---|---|
| Solves a design/architecture problem | Solves a computational problem |
| High-level concept | Step-by-step logic |
| Flexible implementation | Fixed logic |
| Reusable strategy | Reusable procedure |

**Example that clarifies the distinction:**
- The **Strategy Pattern** → lets you *choose* a sorting algorithm at runtime.
- **Quick Sort logic** → the actual sorting algorithm you choose.

The Strategy Pattern is the *architectural decision* about how to plug in algorithms. Quick Sort is the *algorithm itself*. They operate at completely different levels of abstraction.

---

## History of Design Patterns (GoF)

Design Patterns were popularized by the famous book:

> 📘 **"Design Patterns: Elements of Reusable Object-Oriented Software"**
> Written by the **Gang of Four (GoF)**: Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

The GoF introduced **23 Design Patterns** divided into three categories:
1. **Creational** — How objects are created
2. **Structural** — How objects/classes are combined
3. **Behavioral** — How objects interact

This classification is still universally used today across all major programming languages and frameworks.

---

## 5 Key Benefits

### 1. Reusability
Solutions already tested → save time. You don't need to redesign object creation logic from scratch — patterns encode battle-tested approaches.

**Example:** Factory pattern → you don't redesign object creation logic every time you need polymorphic instantiation.

### 2. Maintainability
Pattern-based code becomes:
- Modular
- Organized
- Easier to debug
- Easier to modify

When a developer sees "this is a Singleton" or "this is an Observer," they immediately understand the intent without reading all the code.

### 3. Scalability
System can grow without breaking existing functionality.

**Example:** Observer pattern → you can add new listeners/subscribers without changing the core notification logic at all.

### 4. Consistency
Developers speak the same vocabulary:
- *"Use Singleton here"*
- *"Make it Strategy Pattern"*

Team communication becomes dramatically faster. Patterns form a shared language for architecture discussions.

### 5. Efficiency
Avoid reinventing solutions that thousands of engineers have already refined and battle-tested over decades.

---

## Classification of Design Patterns

### 📦 1. Creational Patterns (Object Creation)
**Focus:** How objects are created

**Patterns:** Singleton, Factory Method, Abstract Factory, Builder, Prototype

**Goal:** Flexible object creation + reduce coupling.

---

### 🧱 2. Structural Patterns (Object Composition)
**Focus:** How objects/classes are combined and structured

**Patterns:** Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy

**Goal:** Build large structures while keeping flexibility.

---

### 🤝 3. Behavioral Patterns (Object Communication)
**Focus:** How objects interact and distribute responsibility

**Patterns:** Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor

**Goal:** Clean responsibility distribution + communication.

---

## How to Apply Design Patterns

> ⚠️ **VERY IMPORTANT REAL WORLD POINT**

Pattern use is an art. It requires judgment, not just knowledge.

**Rules:**
- ✅ Use a pattern when the **problem is complex enough** to warrant it
- ❌ Do **NOT** use a pattern just because you know it

**Bad Example:**
Using Factory pattern for creating just 2 simple objects → **Over-engineering**

**Good Example:**
Multiple object types + runtime decision → **Factory makes sense**

> 🔥 **The Complexity Rule:** `Pattern complexity = Problem complexity`

If the pattern adds more complexity than the problem itself, you're doing it wrong. The code becomes harder to maintain, not easier.

---

## Common Misconceptions

### ❌ Myth 1 — Design Patterns Fix Bad Code

**Reality:**
> They improve *good* design. They cannot rescue poor architecture.

Patterns are tools for architects, not repair kits for spaghetti code.

---

### ❌ Myth 2 — Patterns Are Rigid Templates

**Reality:** Patterns are **guidelines**, not rules.

Python especially allows:
- Functional style
- Duck typing
- Decorators
- Dynamic behavior

So patterns often look **different in Python vs Java**. A Singleton in Python using a module is perfectly valid. The same pattern in Java would require `private static` fields and `getInstance()` methods.

---

## Criticisms of Design Patterns

Some critics make valid points that every senior developer should understand:

### 1. Patterns Exist Because Languages Are Weak
If a language has better abstractions → the pattern may not be needed.

**Example:** Higher-order functions in Python can replace the Strategy pattern entirely. In Python, you can just pass a function as a parameter instead of building a whole Strategy class hierarchy.

### 2. Patterns May Cause Code Duplication
Bad implementation → boilerplate-heavy code. Poorly applied patterns can produce more lines of code than the problem they solve.

### 3. Patterns Sometimes Rename Old Ideas
**Example:** MVC (Model-View-Controller) existed long before the GoF patterns were published.

---

### Why Patterns Are Still Powerful Despite Criticisms

Patterns remain essential thinking tools because they:
- Organize systems
- Scale architecture
- Communicate design decisions across teams

The criticisms are about *misuse*, not about the patterns themselves.

---

## Most Important Takeaway

Design Pattern is **not**:
- ❌ Syntax
- ❌ A library
- ❌ A framework

It **is**:
- ✅ **A thinking approach for designing scalable software**

---

# Creational Patterns

## Singleton Pattern

### Core Concept

Singleton Pattern ensures that:

> 🔥 **Only ONE instance of a class exists in the entire application**, and provides a global access point to that instance.

**The problem it solves:** Sometimes in a system we must avoid multiple objects because:
- Resource is heavy to create
- Data must remain consistent across the application
- System state must be centralized

**Example problems without Singleton:**
- Database connection pool — each module creating its own connection → server crash, memory waste, data inconsistency
- Logger system — multiple loggers writing to the same file inconsistently
- Configuration manager — different parts of app reading different configs
- Cache manager — cache invalidation becomes impossible
- Thread pool manager — duplicate threads waste system resources

If multiple objects are created: ❌ data inconsistency, ❌ memory waste, ❌ synchronization issues, ❌ unexpected behavior.

---

### The Core Analogy

> 🏛️ **Country's Prime Minister**

A country has only ONE Prime Minister. Everyone accesses the same PM — no duplicate PMs exist.

**Second analogy:** There is only one **Election Commission** in a country. Everyone uses the same authority.

Similarly: Singleton → only one object, globally accessible.

---

### Internal Working (Step-by-Step)

```
Step 1 → Check if object already exists (via class variable _instance)
Step 2 → If object EXISTS → return same object
Step 3 → If object does NOT exist → create new object and store reference
```

Key Python distinction:
- `__init__` → **initializes** an object (runs after creation)
- `__new__` → **creates** an object (runs before `__init__`)

Singleton must control **creation** → so we override `__new__`, not `__init__`.

---

### Python Implementation

#### Classic Implementation

```python
class Singleton:
    _instance = None  # Class-level storage for the single instance

    def __new__(cls) -> 'Singleton':
        if cls._instance is None:
            print("Creating instance")
            cls._instance = super().__new__(cls)
        return cls._instance

# Dry Run
s1 = Singleton()  # Output: Creating instance
s2 = Singleton()  # No output — returns existing instance
print(s1 is s2)   # Output: True — both point to SAME object
```

---

#### Singleton with Initialization Guard (Very Important)

```python
class Singleton:
    _instance = None
    _initialized: bool = False

    def __new__(cls) -> 'Singleton':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Problem: __init__ runs EVERY time object is requested
        # Solution: Guard with _initialized flag
        if not self._initialized:
            print("Initializing")
            Singleton._initialized = True
```

---

#### Thread-Safe Singleton (VERY INTERVIEW IMPORTANT)

```python
from threading import Lock

class Singleton:
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls) -> 'Singleton':
        # In multithreading: two threads may create two objects simultaneously
        # Solution: use a Lock to serialize access
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
```

> **Senior Tip:** Note that `with cls._lock` is applied on EVERY call, not just when `_instance is None`. A more optimized version (double-checked locking) checks `_instance` before acquiring the lock for performance in high-throughput scenarios.

---

#### Pythonic Singleton Using Decorator (Very Powerful)

```python
from typing import Callable, Any

def singleton(cls: type) -> Callable:
    instances: dict = {}

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper

@singleton
class Database:
    pass

db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

---

#### Singleton Using Module (Most Pythonic — Real Industry Use)

```python
# config.py — This FILE itself is a Singleton
DB_URL: str = "localhost"
MAX_CONNECTIONS: int = 10
DEBUG: bool = False

# Anywhere in your project:
import config
# config is the SAME object everywhere — Python loads modules only once
print(config.DB_URL)
```

> 🔥 **Senior Python developers prefer this approach.** Python modules are loaded once into `sys.modules` and cached. Every subsequent `import config` returns the same module object. This is the most idiomatic Python Singleton.

---

### Real-World Industry Usage

- **Database connection pool** (PostgreSQL, MongoDB connection managers)
- **Logger system** (`logging` module in Python uses this pattern)
- **Configuration manager** (reading `.env` files, YAML configs)
- **Cache manager** (Redis client, in-memory cache)
- **Thread pool manager** (thread orchestration)
- **Hardware device controller** (printer spooler, audio driver)
- **File system manager**

---

### Advantages

- ✅ Memory efficient — only one object in memory
- ✅ Controlled access — single point of creation
- ✅ Consistent data — everyone uses same state
- ✅ Lazy initialization possible — object created only when first needed
- ✅ Centralized logic

---

### Disadvantages

- ❌ Hard to unit test (global dependency makes mocking difficult)
- ❌ Hidden coupling — modules secretly depend on global state
- ❌ Breaks OOP principles sometimes
- ❌ Tight coupling between Singleton and its consumers
- ❌ Concurrency complexity in multithreaded environments
- ❌ Can become anti-pattern if overused (**"Hidden Global Variable Problem"**)

> ❌ **When NOT to Use:**
> - When object is lightweight and multiple instances are fine
> - When you need multiple states across components
> - When testing becomes hard (dependency injection is better)
> - When global state creates tight coupling
> - When dependency injection is the right tool instead

---

### Interview Trap Vault — Singleton

**Q1: Why override `__new__` and not `__init__`?**
Because `__init__` runs **AFTER** object creation. To prevent object creation from happening, you must intercept at `__new__` which is responsible for allocating and returning the new object.

**Q2: Is Singleton an anti-pattern?**
Sometimes YES — because global state harms testability, scalability, and can create hidden dependencies. The answer depends on use case. For logger, DB pool: appropriate. For business logic state: usually a bad idea.

**Q3: What is the most Pythonic Singleton?**
Module Singleton. Python's import system caches modules in `sys.modules`, so a module loaded once acts as a natural singleton.

**Q4: Is Singleton thread-safe by default?**
**NO.** Two threads may simultaneously check `_instance is None`, both find it True, and both create separate instances. You must use a Lock for thread safety.

> 🔥 **Most Important Concept:**
> Singleton is not about "creating only one object."
> It is about **"Controlling object lifecycle globally."**

---

## Factory Method Pattern

### Core Concept

Factory Method Pattern means:

> 🔥 **Object creation logic is moved to a separate method (factory), instead of directly using the constructor.**

So instead of:
```python
car = BMW()
```
We do:
```python
car = CarFactory.create_car("BMW")
```

---

### The Core Analogy

> 🍽️ **Restaurant Kitchen**

The customer doesn't cook food. The customer gives an order → the kitchen prepares it.

Similarly: The client asks the factory → the factory creates the correct object. The client never needs to know which class was instantiated internally.

---

### Internal Working (Step-by-Step)

**Without Factory (the problem):**
```python
if payment_type == "card":
    payment = CardPayment()
elif payment_type == "upi":
    payment = UPIPayment()
elif payment_type == "netbank":
    payment = NetBankingPayment()
# This logic gets duplicated: checkout page, refund system, subscription module...
```

**With Factory (the solution):**
```
Step 1 → User requests an object type from the factory
Step 2 → Factory checks condition / uses polymorphism
Step 3 → Factory creates the correct concrete object
Step 4 → Returns the object to the client
Step 5 → Client uses the interface without knowing which class was used
```

**Why Factory improves design:**
- Without Factory → client depends on concrete classes, creation logic, condition logic
- With Factory → client depends ONLY on the **interface** (follows Dependency Inversion Principle — SOLID)

---

### Python Implementation

#### Basic Factory (Simple Factory with if-else)

```python
from abc import ABC, abstractmethod
from typing import Union

# Step 1 — Product Interface
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

# Step 2 — Concrete Products
class Dog(Animal):
    def speak(self) -> str:
        return "Bark"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow"

# Step 3 — Factory
class AnimalFactory:
    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

# Step 4 — Usage
animal: Animal = AnimalFactory.create_animal("dog")
print(animal.speak())  # Output: Bark
```

---

#### Factory Method Pattern (Polymorphic Version — True GoF)

```python
from abc import ABC, abstractmethod

# Product interface
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):
    def speak(self) -> str:
        return "Bark"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow"

# Creator class — defines the factory method
class Creator(ABC):
    @abstractmethod
    def factory_method(self) -> Animal:
        pass

    def operation(self) -> str:
        product = self.factory_method()
        return product.speak()

# Concrete Creators — no condition logic, fully polymorphic
class DogCreator(Creator):
    def factory_method(self) -> Dog:
        return Dog()

class CatCreator(Creator):
    def factory_method(self) -> Cat:
        return Cat()

# Usage
creator: Creator = DogCreator()
print(creator.operation())  # Output: Bark
```

> 🔥 Now: **No condition logic**, **Fully polymorphic**, **Easily extendable**.
> Adding a new animal? Create `FishCreator` — existing code never changes.

---

#### Real Backend Example — Database Factory

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self) -> str:
        pass

class MongoDB(Database):
    def connect(self) -> str:
        return "Connected to MongoDB"

class PostgreSQL(Database):
    def connect(self) -> str:
        return "Connected to PostgreSQL"

class Redis(Database):
    def connect(self) -> str:
        return "Connected to Redis"

class DBFactory:
    @staticmethod
    def get_db(db_type: str) -> Database:
        db_map = {
            "mongo": MongoDB,
            "postgres": PostgreSQL,
            "redis": Redis
        }
        db_class = db_map.get(db_type)
        if not db_class:
            raise ValueError(f"Unsupported database: {db_type}")
        return db_class()

# Flask API usage
db: Database = DBFactory.get_db("mongo")
# Tomorrow add Cassandra, DynamoDB — client code does NOT change
```

---

### Real-World Industry Usage

- **Payment gateway integration** (Stripe, Razorpay, UPI — switch at runtime)
- **Flask App Factory** (`create_app()` pattern in Flask)
- **Django DB backend selection** (MySQL, PostgreSQL, SQLite)
- **Logging module handlers** (File handler, Stream handler, Email handler)
- **File parsers** (XML, JSON, CSV parsers selected by file type)
- **DB driver selection** (SQLAlchemy dialect factories)
- **Plugin systems** (load the right plugin class at runtime)
- **Notification sender creation** (Email, SMS, Push — selected by user preference)
- **Game enemy creation** (different enemy types in game loops)

---

### Advantages

- ✅ Loose coupling — client depends on interfaces, not concrete classes
- ✅ Single responsibility — object creation separated from business logic
- ✅ Scalable architecture — add new types without modifying existing code
- ✅ Easy testing — mock the factory in unit tests
- ✅ Runtime flexibility — decide which object to create based on config/input
- ✅ Open/Closed Principle — open for extension, closed for modification

---

### Disadvantages

- ❌ More classes added to codebase
- ❌ More abstraction layers (harder to trace for beginners)
- ❌ Slight complexity increase
- ❌ Hard for beginners to grasp initially

> ❌ **When NOT to Use:**
> - When only 1 object type exists
> - When creation logic is very simple
> - When over-engineering small applications
> - When object creation is trivial (just `MyClass()`)

---

### Simple Factory vs Factory Method (Important Distinction)

| **Simple Factory** | **Factory Method** |
|---|---|
| Uses if-else | Uses polymorphism (subclasses) |
| Central logic in one place | Distributed logic across creators |
| Less scalable | Highly scalable |
| Not a true GoF pattern | Real GoF pattern |

---

### Interview Trap Vault — Factory

**Q1: Factory vs Constructor?**
Constructor creates a **specific** object.
Factory **decides WHICH** object to create. This distinction enables runtime polymorphism.

**Q2: Factory vs Abstract Factory?**
Factory → Creates **one product type**
Abstract Factory → Creates **families of related products**

**Q3: Where is Factory used in real frameworks?**
- Flask App Factory pattern (`create_app()`)
- Django database backend factory
- Python `logging` module handler creation
- Payment SDKs (Stripe, PayPal SDK factories)

> 🔥 **Most Important Takeaway:**
> Factory pattern is about **"Encapsulating object creation so the system becomes extensible."**

---

## Abstract Factory Pattern

### Core Concept

Abstract Factory means:

> 🔥 **A factory that creates multiple related objects (a family of objects) without specifying their concrete classes.**

Simple words:
- **Factory** → creates **ONE** product
- **Abstract Factory** → creates a **GROUP of related products** (a family)

---

### The Core Analogy

> 🪑 **Furniture Store / Showroom**

You choose a furniture set:
- Modern Set → Modern sofa + Modern table + Modern chair
- Victorian Set → Victorian sofa + Victorian table + Victorian chair

You would **never** mix: Modern Sofa + Victorian Table

Abstract Factory ensures the **whole set is consistent**. It prevents incompatible objects from being mixed together.

---

### Internal Working (Step-by-Step)

**The Problem:**
```python
button = DarkButton()
textbox = LightTextBox()  # ❌ Wrong mix — inconsistent UI
```

**The Solution:**
```
Step 1 → Define abstract product interfaces (Button, Checkbox, etc.)
Step 2 → Create concrete products per theme (LightButton, DarkButton)
Step 3 → Create abstract factory interface with methods for each product
Step 4 → Create concrete factories per theme (LightThemeFactory, DarkThemeFactory)
Step 5 → Client uses the factory — never touches concrete classes
```

---

### Python Implementation

#### Complete UI Theme Example

```python
from abc import ABC, abstractmethod

# Step 1 — Abstract Products
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

# Step 2 — Concrete Products: Light Theme
class LightButton(Button):
    def render(self) -> str:
        return "Light Button"

class LightCheckbox(Checkbox):
    def render(self) -> str:
        return "Light Checkbox"

# Step 3 — Concrete Products: Dark Theme
class DarkButton(Button):
    def render(self) -> str:
        return "Dark Button"

class DarkCheckbox(Checkbox):
    def render(self) -> str:
        return "Dark Checkbox"

# Step 4 — Abstract Factory
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

# Step 5 — Concrete Factories
class LightThemeFactory(UIFactory):
    def create_button(self) -> LightButton:
        return LightButton()

    def create_checkbox(self) -> LightCheckbox:
        return LightCheckbox()

class DarkThemeFactory(UIFactory):
    def create_button(self) -> DarkButton:
        return DarkButton()

    def create_checkbox(self) -> DarkCheckbox:
        return DarkCheckbox()

# Step 6 — Client Code
def render_ui(factory: UIFactory) -> None:
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    print(button.render())
    print(checkbox.render())

# Usage — switch entire theme with one line
factory: UIFactory = DarkThemeFactory()
render_ui(factory)
# Output:
# Dark Button
# Dark Checkbox
```

> 🔥 **This is Dependency Injection Friendly Design.** Swap `DarkThemeFactory()` with `LightThemeFactory()` and the entire UI theme changes. Client code never changes.

---

#### Cross-Platform UI Example

```python
class WinButton:
    def paint(self) -> None:
        print("Windows Button")

class MacButton:
    def paint(self) -> None:
        print("Mac Button")

class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> object:
        pass

class WinFactory(UIFactory):
    def create_button(self) -> WinButton:
        return WinButton()

class MacFactory(UIFactory):
    def create_button(self) -> MacButton:
        return MacButton()

# Client never writes: if platform == "windows"
factory: UIFactory = WinFactory()
btn = factory.create_button()
btn.paint()  # Windows Button
```

---

#### Real Backend Example — Database Family

```python
# Each database needs: Connection + QueryBuilder + TransactionManager
# Abstract Factory creates the entire family consistently

class DBFactory(ABC):
    @abstractmethod
    def create_connection(self) -> object:
        pass

    @abstractmethod
    def create_query_builder(self) -> object:
        pass

    @abstractmethod
    def create_transaction(self) -> object:
        pass

# Switch DB → just change factory. Entire backend adapts.
# This is used in ORMs internally (SQLAlchemy dialects).
```

---

### Real-World Industry Usage

- **UI frameworks** (cross-platform widget creation)
- **Database drivers family** (PostgreSQL family vs MongoDB family)
- **Django DB backend** (abstract factory for database adapters)
- **SQLAlchemy dialects** (each dialect is a family)
- **Theme engines** (Dark/Light/High-contrast themes)
- **OS abstraction libraries** (Windows vs Linux vs macOS families)
- **Payment gateway environments** (Sandbox vs Production factory)
- **Test environment mocking** (replace production factory with test factory)
- **Game environment objects** (game world themes)

---

### Advantages

- ✅ Strong consistency between related objects (no mismatching)
- ✅ Loose coupling — client never depends on concrete classes
- ✅ Easy scalability — add new product family by adding new factory
- ✅ High abstraction
- ✅ Easy swapping of entire environment
- ✅ Open/Closed Principle

---

### Disadvantages

- ❌ Large number of classes (each product × each factory)
- ❌ Hard to understand initially
- ❌ Complex architecture
- ❌ Difficult debugging sometimes
- ❌ Hard to add **new product types** to existing factory family (requires modifying all factories)

> ❌ **When NOT to Use:**
> - When only one product type is needed
> - When system is small and won't grow
> - When product families don't conceptually exist
> - When it would be over-engineering

---

### Interview Trap Vault — Abstract Factory

**Q1: Can Abstract Factory use Factory Method internally?**
YES — very common. Each concrete factory's `create_button()` is itself a Factory Method.

**Q2: Is Abstract Factory a replacement for Dependency Injection?**
NO — but it works beautifully WITH DI. Use DI to inject the factory; use Abstract Factory to create the product family.

**Q3: Real frameworks using Abstract Factory?**
- Django database backend
- SQLAlchemy dialect system
- GUI frameworks (Qt, wxPython)
- OS abstraction libraries

> 🔥 **Most Important Takeaway:**
> Abstract Factory is about **"Designing a system that can switch its entire behavior family at runtime safely."**

---

## Builder Pattern

### Core Concept

Builder Pattern means:

> 🔥 **Construct a complex object step-by-step instead of creating it in one huge constructor.**

Instead of:
```python
user = User("Siddhi", 22, "Ahmedabad", "Engineer", True, "Premium")
# Hard to remember order, what does 'True' mean here?
```

We do:
```python
user = (UserBuilder()
    .set_name("Siddhi")
    .set_age(22)
    .set_city("Ahmedabad")
    .build())
```

---

### The Core Analogy

> 🍕 **Ordering Pizza**

You choose:
- Base (thin crust / thick crust)
- Sauce (tomato / pesto)
- Cheese (mozzarella / cheddar)
- Toppings (one at a time)

The chef builds the pizza step by step. The Builder pattern = the pizza-making process.

---

### Internal Working (Step-by-Step)

**Problems with large constructors:**
- ❌ Too many parameters
- ❌ Hard to remember parameter order
- ❌ Optional fields become messy (None, None, None...)
- ❌ Poor readability
- ❌ Object may be partially constructed
- ❌ Difficult to maintain

**Key concept — Method Chaining:**
Each builder method returns `self`, enabling **Fluent Interface**:
```python
return self  # This is what makes chaining possible
```

---

### Python Implementation

#### Basic House Builder

```python
from typing import Optional

class House:
    def __init__(self) -> None:
        self.walls: Optional[str] = None
        self.roof: Optional[str] = None
        self.garden: Optional[str] = None

    def show(self) -> str:
        return f"Walls:{self.walls}, Roof:{self.roof}, Garden:{self.garden}"

class HouseBuilder:
    def __init__(self) -> None:
        self.house = House()

    def build_walls(self) -> 'HouseBuilder':
        self.house.walls = "Concrete"
        return self  # Return self for method chaining

    def build_roof(self) -> 'HouseBuilder':
        self.house.roof = "Tiles"
        return self

    def build_garden(self) -> 'HouseBuilder':
        self.house.garden = "Beautiful"
        return self

    def build(self) -> House:
        return self.house

# Fluent Interface — reads like natural language
house = (
    HouseBuilder()
    .build_walls()
    .build_roof()
    .build_garden()
    .build()
)
print(house.show())
# Output: Walls:Concrete, Roof:Tiles, Garden:Beautiful
```

---

#### Director Concept (Optional but Important)

```python
class Director:
    def construct_simple_house(self, builder: HouseBuilder) -> House:
        return builder.build_walls().build_roof().build()

    def construct_full_house(self, builder: HouseBuilder) -> House:
        return builder.build_walls().build_roof().build_garden().build()

# Client usage
house = Director().construct_simple_house(HouseBuilder())
```

The **Director** defines the **order** of building steps. The **Builder** defines **how** each step is executed. They can vary independently.

---

#### Real Backend Example — HTTP Request Builder

```python
from typing import Dict, Any, Optional

class HTTPRequest:
    def __init__(self) -> None:
        self.url: Optional[str] = None
        self.method: Optional[str] = None
        self.headers: Dict[str, str] = {}
        self.body: Optional[Any] = None

class RequestBuilder:
    def __init__(self) -> None:
        self.request = HTTPRequest()

    def set_url(self, url: str) -> 'RequestBuilder':
        self.request.url = url
        return self

    def set_method(self, method: str) -> 'RequestBuilder':
        self.request.method = method
        return self

    def add_header(self, key: str, value: str) -> 'RequestBuilder':
        self.request.headers[key] = value
        return self

    def set_body(self, data: Any) -> 'RequestBuilder':
        self.request.body = data
        return self

    def build(self) -> HTTPRequest:
        return self.request

# Used in SDKs, API clients, testing tools, microservices
request = (
    RequestBuilder()
    .set_url("/users")
    .set_method("POST")
    .add_header("Authorization", "Bearer token123")
    .set_body({"name": "Siddhi"})
    .build()
)
```

---

#### SQL Query Builder (Industry Reality)

```python
class QueryBuilder:
    def __init__(self) -> None:
        self._select: str = "*"
        self._table: str = ""
        self._where: str = ""
        self._order: str = ""

    def select(self, cols: str) -> 'QueryBuilder':
        self._select = cols
        return self

    def from_table(self, table: str) -> 'QueryBuilder':
        self._table = table
        return self

    def where(self, condition: str) -> 'QueryBuilder':
        self._where = condition
        return self

    def order_by(self, col: str) -> 'QueryBuilder':
        self._order = col
        return self

    def build(self) -> str:
        query = f"SELECT {self._select} FROM {self._table}"
        if self._where:
            query += f" WHERE {self._where}"
        if self._order:
            query += f" ORDER BY {self._order}"
        return query

# ORMs internally use this exact thinking
query = (
    QueryBuilder()
    .select("*")
    .from_table("users")
    .where("age > 20")
    .order_by("name")
    .build()
)
print(query)
# Output: SELECT * FROM users WHERE age > 20 ORDER BY name
```

---

### Real-World Industry Usage

- **SQL Query Builders** (SQLAlchemy `query.filter().order_by().all()`)
- **HTTP Request Builders** (Requests library, API clients)
- **SDKs** (AWS SDK, Google Cloud SDK use builder-style configuration)
- **API clients** (Microservice communication layers)
- **Testing tools** (pytest fixtures, test data builders)
- **JSON payload construction** (REST API response building)
- **UI layout builders** (Android `AlertDialog.Builder`)
- **Document generation** (PDF builders, report builders)

---

### Advantages

- ✅ Step-by-step construction — clear and readable
- ✅ Readable object creation — self-documenting code
- ✅ Optional configuration — skip optional fields cleanly
- ✅ Immutable final object possible — call `build()` once
- ✅ Avoid constructor explosion
- ✅ Same process → different representations (Director pattern)

---

### Disadvantages

- ❌ More code overall (builder class + product class)
- ❌ Extra abstraction layer
- ❌ Over-engineering for simple objects

> ❌ **When NOT to Use:**
> - When object is simple (few fields, all required)
> - When you don't need optional fields
> - When construction order is trivial

---

### Interview Trap Vault — Builder

**Q1: What is the "Fluent Interface" in Builder?**
Method chaining via `return self`. Allows `builder.set_name("X").set_age(22).build()` — reads like a sentence.

**Q2: What is the Director's role?**
The Director defines the **construction algorithm** (the sequence of builder calls). The Builder defines **how** each step is executed. They can be varied independently. Director is optional — some teams skip it and call builder methods directly.

**Q3: Builder vs Constructors with keyword args (Python-specific)?**
In Python, `dataclasses` and keyword arguments reduce the need for Builder in simple cases. But Builder shines for objects with complex construction logic, validation during build, or multiple representations.

---

## Prototype Pattern

### Core Concept

> **Create a new object by cloning an existing object instead of creating from scratch.**

Useful when:
- Object creation is expensive (heavy database load, network call, complex computation, AI model loading)
- Many similar objects are needed with minor variations

---

### The Core Analogy

> 📄 **Photocopy Machine**

Instead of rewriting a document from scratch → you just photocopy it, then make your edits.

---

### Internal Working (Step-by-Step)

```
Step 1 → Create base object (the "prototype")
Step 2 → Clone the object (shallow or deep copy)
Step 3 → Modify the clone as needed
```

---

### Python Implementation

```python
import copy
from typing import Optional

class Car:
    def __init__(self, color: str, model: str) -> None:
        self.color = color
        self.model = model

    def clone(self) -> 'Car':
        return copy.copy(self)  # Shallow copy

    def deep_clone(self) -> 'Car':
        return copy.deepcopy(self)  # Deep copy (for nested objects)

car1 = Car("Red", "BMW")
car2 = car1.clone()
car2.color = "Blue"

print(car1.color)  # Red — original unchanged
print(car2.color)  # Blue — independent copy
```

---

### Real-World Industry Usage

- **Game enemy spawning** (clone base enemy type, then vary stats)
- **Document templates** (clone base template, fill specific fields)
- **Machine learning model instances** (clone a loaded model to avoid re-loading)
- **Cache object duplication** (clone cached results for safe modification)
- **UI template replication**
- **Caching templates** (prototype stored in registry, cloned on demand)

---

### Advantages

- ✅ Fast object creation (avoids expensive re-initialization)
- ✅ Avoid heavy initialization cost
- ✅ Reduce subclass explosion
- ✅ Object registry pattern possible (store named prototypes, clone by name)

---

### Disadvantages

- ❌ Deep copy complexity (nested objects require careful handling)
- ❌ Circular reference problems (deepcopy can fail)
- ❌ Hard debugging

> ❌ **When NOT to Use:**
> - When object creation is cheap
> - When cloning logic is complex and error-prone

> **Revision Line:** Prototype = cloning instead of constructing.

---

# Structural Patterns

## Adapter Pattern

### Core Concept

> **Convert one interface into another expected interface.**

---

### The Core Analogy

> 🔌 **Power Plug Adapter**

A laptop with a US plug in a UK socket — you need an adapter that translates one interface to another. The laptop and socket haven't changed; only the adapter bridges them.

---

### Internal Working

The Adapter:
- Wraps the incompatible object (adaptee)
- Exposes the expected interface
- Internally delegates calls to the adaptee

**Use case:** You have an old payment API with `get_data_old()`. Your new system expects `fetch_data()`. The adapter bridges the gap without modifying either system.

---

### Python Implementation

```python
from typing import Any

# Existing (old) API you can't modify
class OldAPI:
    def get_data(self) -> str:
        return "Old Data"

# Target interface the new system expects
class NewAPIInterface:
    def fetch_data(self) -> str:
        raise NotImplementedError

# Adapter bridges the gap
class Adapter(NewAPIInterface):
    def __init__(self, old: OldAPI) -> None:
        self.old = old

    def fetch_data(self) -> str:
        return self.old.get_data()  # Translates the call

# Client code uses the new interface
obj = Adapter(OldAPI())
print(obj.fetch_data())  # Output: Old Data
```

---

### Real-World Industry Usage

- **Third-party library integration** (adapting external APIs to your interface)
- **Legacy system migration** (wrap old code with new interface)
- **Different API contracts** (standardize multiple payment providers)
- **Data format conversion** (XML → JSON adapter)

---

### Advantages

- ✅ Reuse legacy code without modifying it
- ✅ Smooth integration of incompatible interfaces
- ✅ Single Responsibility Principle

### Disadvantages

- ❌ Extra indirection layer
- ❌ May hide complexity from callers

> **Revision:** Adapter = Interface Translator.

---

## Bridge Pattern

### Core Concept

> **Separate abstraction from implementation so both can change independently.**

---

### The Core Analogy

> 📺 **Universal Remote Control**

The same remote (abstraction) can control many different devices (implementations): TV, Radio, AC. Adding a new device doesn't change the remote. Adding a new remote type doesn't change the devices.

---

### Internal Working

**Without Bridge — Class Explosion:**
```
BasicTVRemote, SmartTVRemote
BasicRadioRemote, SmartRadioRemote
BasicACRemote, SmartACRemote...
```

**With Bridge — Composition over inheritance:**
```
Remote + Device → compose them
Any Remote × Any Device = one new combination (no new classes)
```

---

### Python Implementation

```python
from abc import ABC, abstractmethod

# Implementation interface
class Device(ABC):
    @abstractmethod
    def turn_on(self) -> None:
        pass

class TV(Device):
    def turn_on(self) -> None:
        print("TV ON")

class Radio(Device):
    def turn_on(self) -> None:
        print("Radio ON")

# Abstraction — uses composition to hold implementation
class Remote:
    def __init__(self, device: Device) -> None:
        self.device = device  # Bridge via composition

    def power(self) -> None:
        self.device.turn_on()

# Usage — mix and match freely
remote = Remote(TV())
remote.power()   # TV ON

remote = Remote(Radio())
remote.power()   # Radio ON
```

---

### Real-World Industry Usage

- **Device drivers** (abstract driver interface, different hardware implementations)
- **Payment processing abstraction** (payment logic vs payment gateway)
- **GUI frameworks** (abstract widget vs OS-specific rendering)
- **Cloud provider abstraction** (abstract storage vs AWS/GCP/Azure)
- **Messaging services** (abstract notification vs Email/SMS/Push)

---

### Advantages

- ✅ Prevents class explosion
- ✅ Both abstraction and implementation evolve independently
- ✅ High flexibility
- ✅ Follows Open/Closed Principle

### Disadvantages

- ❌ More abstraction layers
- ❌ Hard to understand initially

> ❌ **When NOT to Use:** When only one dimension of variation exists.

> **Revision:** Bridge = Avoid class explosion.

---

## Composite Pattern

### Core Concept

> **Treat individual objects and groups of objects uniformly.**

---

### The Core Analogy

> 🏢 **Company Organization Chart**

- CEO
  - → Managers
    - → Employees

You can calculate the total salary expense of an entire department using the same `calculate_salary()` call — whether it's a single employee or a nested department. Recursion makes it seamless.

---

### Internal Working

**The problem (File System):**
- File: calculate size → simple
- Folder: calculate size → loop all children recursively
- Without Composite → write different logic for File vs Folder everywhere

**With Composite:**
```
Step 1 → Create Component interface (shared interface)
Step 2 → Create Leaf class (individual object — File)
Step 3 → Create Composite class (group object — Folder, stores children)
Step 4 → Composite delegates operation to all children
Step 5 → Client treats both Leaf and Composite identically
```

---

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import List

# Component — shared interface
class Component(ABC):
    @abstractmethod
    def show(self) -> None:
        pass

# Leaf — individual object
class File(Component):
    def __init__(self, name: str) -> None:
        self.name = name

    def show(self) -> None:
        print("File:", self.name)

# Composite — group object
class Folder(Component):
    def __init__(self, name: str) -> None:
        self.name = name
        self.children: List[Component] = []

    def add(self, comp: Component) -> None:
        self.children.append(comp)

    def show(self) -> None:
        print("Folder:", self.name)
        for c in self.children:
            c.show()  # Recursive — works for both File and Folder

# Build tree structure
root = Folder("Root")
file1 = File("A.txt")
file2 = File("B.txt")
sub = Folder("SubFolder")

sub.add(file2)
root.add(file1)
root.add(sub)

root.show()
# Output:
# Folder: Root
# File: A.txt
# Folder: SubFolder
# File: B.txt
```

---

### Real-World Industry Usage

- **File system hierarchy** (OS file explorers)
- **Organization hierarchy** (HR systems)
- **UI components** (container → panel → button → icon)
- **HTML DOM tree** (traverse entire document uniformly)
- **Menu systems** (menus containing sub-menus)

---

### Advantages

- ✅ Tree structure becomes easy to implement
- ✅ Uniform handling of single and group objects
- ✅ Recursive operations simplified
- ✅ Scalable hierarchy

### Disadvantages

- ❌ Hard to restrict which child types a Composite can hold
- ❌ Overgeneralization possible

> ❌ **When NOT to Use:** When hierarchy does not exist, or when structure is flat.

> **Revision:** Composite = Tree Structure Handling.

---

## Decorator Pattern

### Core Concept

> **Add new functionality to an object at runtime WITHOUT modifying its class.**

---

### The Core Analogy

> 🧥 **Wearing Clothes (Layering)**

You wear:
- T-shirt → Jacket → Scarf

Each layer **adds a feature** without changing the body underneath. Decorators work the same way — each wrapper adds behavior around the original.

---

### Internal Working

**The Problem (Coffee System):**
```
Simple coffee
Coffee + Milk
Coffee + Sugar
Coffee + Milk + Sugar
Coffee + Cream + Chocolate
```
Creating a subclass for each combination → **class explosion**.

**With Decorator:**
```
Step 1 → Decorator has SAME interface as the original object
Step 2 → Decorator stores reference to the original object
Step 3 → Decorator adds behavior BEFORE or AFTER delegating to original
Step 4 → Stack decorators for combined features
```

---

### Python Implementation

#### Object-Oriented Decorator Pattern

```python
from typing import Union

# Base component
class Coffee:
    def cost(self) -> int:
        return 50

# Decorators — each adds a feature
class MilkDecorator:
    def __init__(self, coffee: Union['Coffee', 'MilkDecorator', 'SugarDecorator']) -> None:
        self.coffee = coffee

    def cost(self) -> int:
        return self.coffee.cost() + 10  # Add milk cost

class SugarDecorator:
    def __init__(self, coffee: Union['Coffee', 'MilkDecorator', 'SugarDecorator']) -> None:
        self.coffee = coffee

    def cost(self) -> int:
        return self.coffee.cost() + 5  # Add sugar cost

# Stack decorators
c = Coffee()
c = MilkDecorator(c)    # Coffee + Milk = 60
c = SugarDecorator(c)   # Coffee + Milk + Sugar = 65

print(c.cost())  # Output: 65
```

#### Pythonic Decorator (Function-Based)

```python
from functools import wraps
from typing import Callable, Any

def logger(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@logger
def process_payment(amount: float) -> str:
    return f"Processed ${amount}"

process_payment(100.0)
```

---

### Real-World Industry Usage

- **Python logging decorators** (`@app.route`, `@login_required`)
- **Flask routes** (decorators for URL routing, auth checks)
- **Authentication** (`@require_auth` decorators)
- **Caching** (`@cache`, `@lru_cache`)
- **Rate limiting** (`@rate_limit`)
- **Middleware systems** (Django middleware stack)
- **UI styling layers** (CSS-in-JS style composition)
- **Stream processing** (add filters/transformations to data streams)
- **Security filters**

---

### Advantages

- ✅ Runtime flexibility — add/remove behaviors dynamically
- ✅ Avoids subclass explosion
- ✅ Follows Open/Closed Principle
- ✅ Clean feature layering — each decorator has single responsibility

### Disadvantages

- ❌ Many small wrapper objects created
- ❌ Debugging call stack becomes confusing (many layers to trace)

> ❌ **When NOT to Use:**
> - When behavior is static and won't change
> - When performance is critical (each decorator adds a call)

> **Revision:** Decorator = Dynamic feature addition.

---

## Facade Pattern

### Core Concept

> **Provide a simplified interface to a complex subsystem.**

---

### The Core Analogy

> 💻 **Computer Start Button**

When you press the power button (`computer.start()`), internally:
- CPU starts
- Memory loads
- Disk initializes
- OS boots

You only see `start()`. The Facade hides all the complexity.

---

### Python Implementation

```python
class CPU:
    def start(self) -> None:
        print("CPU starting")

class Memory:
    def load(self) -> None:
        print("Memory loading")

class Disk:
    def initialize(self) -> None:
        print("Disk initializing")

# Facade — simplified interface
class Computer:
    def __init__(self) -> None:
        self.cpu = CPU()
        self.memory = Memory()
        self.disk = Disk()

    def start(self) -> None:
        self.cpu.start()
        self.memory.load()
        self.disk.initialize()
        print("Computer ready!")

# Client only uses the facade
pc = Computer()
pc.start()
```

---

### Real-World Industry Usage

- **API Gateway** (hides microservices behind a single endpoint)
- **Library APIs** (high-level library hiding complex internals)
- **Framework initialization** (Flask `create_app()`)
- **Home automation systems** (one command triggers many devices)

> **Revision:** Facade = Simplification layer.

---

## Flyweight Pattern

### Core Concept

> **Reduce memory usage by sharing common object data.**

---

### The Core Analogy

> 📚 **Library Books**

Many students share the same type of book. They don't each own a separate physical copy of the book's content — they share the reference. Only their **bookmark** (position) is unique to each student.

---

### Internal Working

**The Problem:**
Imagine a game with 10,000 trees. Each tree object stores:
- Texture (large — same for all green trees)
- Color (same for all green trees)
- Height (varies)
- Position (varies)

**Flyweight solution:**
- **Intrinsic state** (shared): Texture, Color → stored ONCE
- **Extrinsic state** (unique): Position, Height → stored per instance

```
Step 1 → Identify intrinsic (shared) vs extrinsic (unique) data
Step 2 → Factory manages shared objects (cache them)
Step 3 → Objects reference shared data instead of storing it
```

---

### Python Implementation

```python
from typing import Dict

# Flyweight — stores intrinsic (shared) state
class TreeType:
    def __init__(self, color: str) -> None:
        self.color = color  # Shared data — stored ONCE

# Factory — manages shared objects
class TreeFactory:
    types: Dict[str, TreeType] = {}

    @classmethod
    def get_type(cls, color: str) -> TreeType:
        if color not in cls.types:
            cls.types[color] = TreeType(color)  # Create only if not exists
        return cls.types[color]

# Context — stores extrinsic (unique) state
class Tree:
    def __init__(self, x: int, y: int, type_obj: TreeType) -> None:
        self.x = x          # Unique position
        self.y = y          # Unique position
        self.type = type_obj  # Shared type reference

# Two trees share the SAME type object
t1 = Tree(10, 20, TreeFactory.get_type("Green"))
t2 = Tree(30, 40, TreeFactory.get_type("Green"))

print(t1.type is t2.type)  # True — same object in memory!
```

---

### Real-World Industry Usage

- **Game engines** (10,000+ similar objects — bullets, particles, trees)
- **Text editors** (character rendering — each character style shared)
- **Map systems** (shared tile textures)
- **Icon rendering** (same icon bitmap shared across multiple instances)
- **Browser DOM optimization** (shared style objects)

---

### Advantages

- ✅ Huge memory savings
- ✅ Performance improvement
- ✅ Object reuse

### Disadvantages

- ❌ Complex design
- ❌ Hard debugging (shared state can be surprising)
- ❌ Requires immutability discipline (shared objects must not change)

> ❌ **When NOT to Use:**
> - When objects are few and memory is not a concern
> - When objects are completely unique

> **Revision:** Flyweight = Memory optimization.

---

## Proxy Pattern

### Core Concept

> **Provide a substitute (placeholder) object that controls access to a real object.**

---

### The Core Analogy

> 🛡️ **Security Guard at Office Gate**

You don't directly meet the CEO. The security guard (proxy) **controls access** to the CEO (real object). The guard can:
- Check if you have an appointment (authorization)
- Log your visit (logging)
- Make you wait (lazy access)

---

### Internal Working

**Why Proxy exists:**
The real object may be:
- Heavy to load (large image, database result)
- A remote server object
- A sensitive/protected object

**Proxy can:**
- Delay creation (lazy loading)
- Add security (access control)
- Add logging (audit trail)
- Add caching (avoid repeated expensive calls)

```
Step 1 → Proxy has SAME interface as real object
Step 2 → Proxy stores a reference to real object (created lazily)
Step 3 → Proxy intercepts requests and controls flow
Step 4 → Proxy delegates to real object when appropriate
```

---

### Python Implementation

```python
from typing import Optional

class RealImage:
    def display(self) -> None:
        print("Loading image from disk...")  # Expensive operation

class ProxyImage:
    def __init__(self) -> None:
        self.real: Optional[RealImage] = None  # Not loaded until needed

    def display(self) -> None:
        if self.real is None:
            print("Proxy: Loading real object for first time")
            self.real = RealImage()  # Lazy initialization
        print("Proxy: Access check passed")
        self.real.display()

img = ProxyImage()
img.display()  # Creates real object — first call
img.display()  # Reuses real object — second call
```

---

### Real-World Industry Usage

- **API Gateway** (proxy between client and microservices — adds auth, rate limiting, logging)
- **Lazy database loading** (ORM lazy-loads relationships: `user.orders` loads when accessed)
- **Access control** (role-based access proxy)
- **Virtual image loading** (load low-res placeholder, load full image on demand)
- **Network proxies** (HTTP proxies, reverse proxies like Nginx)

---

### Advantages

- ✅ Lazy loading — load heavy resources only when needed
- ✅ Security layer — control who can access what
- ✅ Logging / caching — add cross-cutting concerns without modifying real object
- ✅ Performance optimization through caching

### Disadvantages

- ❌ Extra indirection layer
- ❌ Can increase response time if not implemented carefully

> ❌ **When NOT to Use:**
> - When object access is simple and direct
> - When performance must be ultra-fast and overhead is unacceptable

> **Revision:** Proxy = Controlled access wrapper.

---

# Behavioral Patterns

## Observer Pattern

### Core Concept

> **One object (Subject) notifies many dependent objects (Observers) when its state changes.**

---

### The Core Analogy

> 📧 **Newsletter Subscription**

You subscribe to a company newsletter. When the company publishes an update → the company sends it to all subscribers. You don't poll the company website; the company pushes updates to you.

---

### Internal Working

**The Problem:**
Stock price changes → many screens need update:
- User portfolio screen
- News alert system
- Analytics module
- Risk engine

Without Observer: Each module must manually poll the stock price → wasteful and tightly coupled.

**Two roles:**
- **Subject** (Publisher) → the main object that changes state
- **Observers** (Subscribers) → the listeners that react

```
Step 1 → Observer subscribes to Subject
Step 2 → Subject state changes
Step 3 → Subject notifies ALL observers automatically
Step 4 → Each observer handles the update in its own way
```

---

### Python Implementation

```python
from typing import List

class Observer:
    def update(self) -> None:
        raise NotImplementedError

class Subject:
    def __init__(self) -> None:
        self.observers: List[Observer] = []

    def subscribe(self, obs: Observer) -> None:
        self.observers.append(obs)

    def unsubscribe(self, obs: Observer) -> None:
        self.observers.remove(obs)  # Important! Prevent memory leaks

    def notify(self) -> None:
        for obs in self.observers:
            obs.update()

class UserNotification(Observer):
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self) -> None:
        print(f"{self.name}: Notification received!")

# Usage
stock = Subject()
u1 = UserNotification("Portfolio Screen")
u2 = UserNotification("Analytics Module")

stock.subscribe(u1)
stock.subscribe(u2)
stock.notify()
# Portfolio Screen: Notification received!
# Analytics Module: Notification received!
```

---

### Real-World Industry Usage

- **Django signals** (`post_save`, `pre_delete` signals)
- **Event buses** (internal application event systems)
- **Pub/Sub systems** (RabbitMQ, Kafka, Redis Pub/Sub)
- **YouTube notifications** (subscriber gets notified on new video)
- **Email subscription systems**
- **Live sports score updates**
- **Microservices event bus** (domain events between services)
- **GUI button click events** (event listeners in UI frameworks)

---

### Advantages

- ✅ Real-time updates without polling
- ✅ Decoupled communication between Subject and Observers
- ✅ Event-driven architecture foundation
- ✅ Scalable — add new observers without changing Subject

### Disadvantages

- ❌ Debugging difficult (hard to trace notification chains)
- ❌ Too many notifications possible (notification storms)
- ❌ **Memory leaks** if observers are not properly unsubscribed

> ❌ **When NOT to Use:**
> - When updates are rare and a direct method call is simpler
> - When notification chains create circular dependencies

---

## Strategy Pattern

### Core Concept

> **Define a family of algorithms, encapsulate each one, and make them interchangeable.**

---

### The Core Analogy

> 🗺️ **GPS Navigation Route Selection**

The navigation app can route you via:
- Walking route
- Car route
- Bicycle route
- Public transit route

You select the strategy (algorithm) at runtime. The Navigator doesn't change — only the routing strategy does.

---

### Internal Working

**The Problem:**
```python
if sort_type == "quick":
    quick_sort(data)
elif sort_type == "merge":
    merge_sort(data)
elif sort_type == "bubble":
    bubble_sort(data)
# This if-else grows forever and is everywhere
```

**With Strategy:** Pass the algorithm as an object. The context (caller) doesn't care which algorithm — it just calls `strategy.execute()`.

---

### Python Implementation

```python
from abc import ABC, abstractmethod

class RouteStrategy(ABC):
    @abstractmethod
    def route(self) -> None:
        pass

class WalkStrategy(RouteStrategy):
    def route(self) -> None:
        print("Walking route: via park")

class CarStrategy(RouteStrategy):
    def route(self) -> None:
        print("Car route: via highway")

class BicycleStrategy(RouteStrategy):
    def route(self) -> None:
        print("Bicycle route: via bike lane")

class Navigator:
    def __init__(self, strategy: RouteStrategy) -> None:
        self.strategy = strategy

    def set_strategy(self, strategy: RouteStrategy) -> None:
        self.strategy = strategy  # Change at runtime

    def navigate(self) -> None:
        self.strategy.route()

# Usage
nav = Navigator(CarStrategy())
nav.navigate()  # Car route: via highway

nav.set_strategy(WalkStrategy())
nav.navigate()  # Walking route: via park
```

#### Pythonic Strategy (Using Functions)

```python
from typing import Callable, List

def quick_sort(data: List) -> List:
    return sorted(data)  # Simplified for example

def bubble_sort(data: List) -> List:
    return sorted(data, reverse=False)  # Simplified

class Sorter:
    def __init__(self, strategy: Callable) -> None:
        self.strategy = strategy

    def sort(self, data: List) -> List:
        return self.strategy(data)

sorter = Sorter(quick_sort)
# In Python, functions are first-class — no class hierarchy needed!
```

---

### Real-World Industry Usage

- **Payment method selection** (Credit Card, UPI, Net Banking — each a strategy)
- **Compression algorithm** (ZIP, GZIP, BZIP2 — select at runtime)
- **Authentication method** (JWT, OAuth, Session — pluggable strategies)
- **Shipping cost calculation** (FedEx, DHL, Standard post — different pricing strategies)
- **Sorting algorithm selection**

---

### Advantages

- ✅ Open/Closed Principle — add new strategy without modifying context
- ✅ Replace logic dynamically at runtime
- ✅ Cleaner code — eliminates complex if-else chains
- ✅ Each strategy independently testable

### Disadvantages

- ❌ Many classes for complex strategy sets
- ❌ Hard to manage many strategies if poorly organized

> **Revision:** Strategy = Runtime algorithm selection.

---

## State Pattern

### Core Concept

> **Object behavior changes based on its internal state.**

---

### The Core Analogy

> 🏧 **ATM Machine**

- State: No Card → only accepts card
- State: Card Inserted → only asks for PIN
- State: Authenticated → allows withdrawal/balance
- State: Dispensing → processes transaction

The ATM behaves completely differently depending on state. Same button press → different behavior.

---

### Python Implementation

```python
from abc import ABC, abstractmethod

class OrderState(ABC):
    @abstractmethod
    def process(self) -> None:
        pass

class PaidState(OrderState):
    def process(self) -> None:
        print("Order: Payment confirmed")

class ShippedState(OrderState):
    def process(self) -> None:
        print("Order: Shipped to customer")

class DeliveredState(OrderState):
    def process(self) -> None:
        print("Order: Successfully delivered")

class Order:
    def __init__(self, state: OrderState) -> None:
        self.state = state

    def change_state(self, state: OrderState) -> None:
        self.state = state

    def process(self) -> None:
        self.state.process()

# Order lifecycle
order = Order(PaidState())
order.process()              # Order: Payment confirmed

order.change_state(ShippedState())
order.process()              # Order: Shipped to customer

order.change_state(DeliveredState())
order.process()              # Order: Successfully delivered
```

---

### Real-World Industry Usage

- **Order lifecycle** (Created → Paid → Shipped → Delivered → Refunded)
- **ATM machine states** (No Card, Card Inserted, Authenticated)
- **Traffic light systems** (Red → Green → Yellow → Red)
- **Game character states** (Idle, Running, Jumping, Attacking)

---

### Advantages

- ✅ Removes complex if-else chains
- ✅ Clean state transitions
- ✅ Maintainable logic
- ✅ Each state independently testable

### Disadvantages

- ❌ Many state classes for complex systems
- ❌ Slight complexity overhead

> **Revision:** State = Behavior switching.

---

## Chain of Responsibility Pattern

### Core Concept

> **Pass a request through a chain of handlers until one of them handles it.**

---

### The Core Analogy

> 📋 **Expense Approval Chain**

- Expense under $100 → Team Lead approves
- Expense under $1000 → Manager approves
- Expense under $10,000 → Director approves
- Larger → CEO approves

Each handler in the chain either handles it or passes it up.

---

### Real-World Industry Usage

- **Logging levels** (DEBUG → INFO → WARNING → ERROR → CRITICAL)
- **HTTP middleware pipeline** (auth → validation → processing → response)
- **Exception handling chains**
- **Event propagation in UI** (child → parent → root)

> **Revision:** Chain = Pipeline processing.

---

## Command Pattern

### Core Concept

> **Encapsulate a request as an object.**

---

### Real-World Industry Usage

- **Undo/Redo systems** (text editors, graphic tools)
- **Job queues** (enqueue command objects for later execution)
- **Task scheduling** (Celery tasks are command objects)
- **Transaction systems** (rollback = undo command)

> **Revision:** Command = Action object.

---

## Iterator Pattern

### Core Concept

> **Provide sequential access to elements of a collection without exposing its internal structure.**

---

### The Core Analogy

> 📖 **Book Page Turner**

You flip pages one at a time without knowing how the book's binding works internally.

---

### Python Implementation

```python
from typing import List, Any

class MyCollection:
    def __init__(self, data: List[Any]) -> None:
        self.data = data

    def __iter__(self) -> 'MyCollection':
        self.index = 0
        return self

    def __next__(self) -> Any:
        if self.index < len(self.data):
            val = self.data[self.index]
            self.index += 1
            return val
        else:
            raise StopIteration

# Usage — Python's for loop uses the iterator protocol
col = MyCollection([1, 2, 3])
for i in col:
    print(i)
# Output: 1, 2, 3
```

> **Python Note:** Python's `__iter__` and `__next__` are the built-in implementation of the Iterator pattern. Generators (`yield`) are an even more Pythonic approach.

---

### Real-World Industry Usage

- **Database result iteration** (cursor-based pagination)
- **File system traversal** (`os.walk()`)
- **Tree traversal** (BFS/DFS iterators)
- **Pagination systems** (page through API results)
- **Streaming APIs** (process stream element by element)

---

### Advantages

- ✅ Uniform traversal across different data structures
- ✅ Hides internal structure
- ✅ Clean client code

### Disadvantages

- ❌ Extra object creation overhead
- ❌ Slight performance overhead for simple loops

> ❌ **When NOT to Use:** When a simple `for` loop is sufficient.

> **Revision:** Iterator = Controlled traversal.

---

## Mediator Pattern

### Core Concept

> **A central object handles all communication between components, reducing direct dependencies.**

---

### The Core Analogy

> 💬 **Air Traffic Control Tower**

Planes don't communicate directly with each other. All communication goes through the control tower (mediator). This prevents mid-air collision (direct coupling chaos).

---

### Real-World Industry Usage

- **Chat room server** (central server routes messages between users)
- **Message broker** (RabbitMQ, Kafka as mediator between services)
- **Event bus** (central dispatcher for UI events)
- **MVC Controllers** (Controller mediates between View and Model)

> **Revision:** Mediator = Communication hub.

---

## Memento Pattern

### Core Concept

> **Capture and externalize an object's internal state so it can be restored to that state later.**

---

### The Core Analogy

> 💾 **Save Game Checkpoint**

You save your progress at a checkpoint. If you die, you restore to the saved checkpoint. The game state was captured (Memento) and can be restored.

---

### Real-World Industry Usage

- **Undo systems** (text editors, photo editors)
- **Transaction rollback** (database transaction management)
- **Version history** (Git commits are mementos)
- **Game save states**

> **Revision:** Memento = State snapshot.

---

## Template Method Pattern

### Core Concept

> **Define the skeleton of an algorithm in a base class, and let subclasses override specific steps without changing the algorithm's structure.**

---

### Real-World Industry Usage

- **Data processing pipeline** (read → process → save — steps vary, structure fixed)
- **Web framework request handling** (receive → authenticate → process → respond)
- **Report generation** (gather data → format → export — format step varies)
- **Game AI** (turn structure fixed, specific actions vary)

> **Revision:** Template Method = Algorithm blueprint.

---

## Visitor Pattern

### Core Concept

> **Add new operations to existing object structures without modifying those objects.**

---

### Real-World Industry Usage

- **Compilers** (AST traversal — add new analysis passes without modifying AST nodes)
- **Abstract Syntax Tree processing** (code analysis, code generation)
- **Document export** (export to PDF, HTML, Word — visitor per format)
- **Tax calculation systems** (different tax rules applied to different product types)

> **Revision:** Visitor = External behavior injection.

---

# Career & Industry Insights

## The Complexity Rule

> 🔥 **Pattern complexity must equal problem complexity.**

This is the most important practical rule for senior engineers:

| Situation | Right Choice |
|---|---|
| Simple object creation (1-2 classes) | Just use constructor directly |
| Multiple object types, runtime decision | Factory Pattern |
| Families of related objects, must be consistent | Abstract Factory |
| Complex object with many optional fields | Builder Pattern |
| One global resource with heavy initialization | Singleton |
| Adding behaviors dynamically | Decorator |
| Controlling access to resource | Proxy |

**The test:** Does the pattern reduce complexity for the reader? If not — remove it.

> Over-engineering is just as harmful as under-engineering. A `UserFactory` that only ever creates `User` objects is pure noise.

---

## Pythonic Patterns vs Java

Python's dynamic features fundamentally change how patterns are implemented:

### Duck Typing Replaces Formal Interfaces
```python
# Python — no need to explicitly declare interface implementation
class Dog:
    def speak(self): return "Bark"

class Cat:
    def speak(self): return "Meow"

# Both work with any factory — duck typing handles it
```

### Decorators Replace Decorator Pattern Classes
```python
# Python built-in decorator syntax IS the Decorator pattern
@require_auth
@rate_limit
@cache
def my_api_endpoint():
    pass
```

### Modules Replace Singleton
```python
# config.py is ALREADY a Singleton — no class needed
```

### First-Class Functions Replace Strategy
```python
# Pass a function directly — no Strategy class hierarchy needed
sorter = Sorter(strategy=quick_sort)
```

### Key Differences from Java

| Java Pattern | Python Equivalent |
|---|---|
| Singleton class with `getInstance()` | Module-level variables |
| Strategy interface + concrete classes | First-class functions |
| Decorator class hierarchy | `@decorator` syntax |
| Iterator with `hasNext()`/`next()` | `__iter__`/`__next__` / generators |
| Abstract Factory | ABCs with `abstractmethod` |

> **Senior Python developers prefer idiomatic Python over Java-style patterns.** Use classes and inheritance when there's genuine abstraction to express, not to mimic Java patterns.

---

## Factory vs. Abstract Factory: Architect's Note

This is one of the most frequently confused distinctions in interviews:

| Dimension | Factory | Abstract Factory |
|---|---|---|
| Creates | **One** object type | **Family** of related objects |
| Complexity | Simpler | More complex |
| Mechanism | if-else or polymorphism | Multiple factories |
| Scalability | Less scalable | Highly scalable |
| Best for | Small-to-mid systems | Large architecture |
| Product consistency | Not enforced | Enforced — no mixing |

**The deciding question:** "Do I need to ensure that my objects are *compatible with each other*?"

- If YES → Abstract Factory (ensures entire family is consistent)
- If NO → Factory (just need the right type at runtime)

---

## Master Revision Table

| Category | Patterns |
|---|---|
| **Creational** | Singleton, Factory Method, Abstract Factory, Builder, Prototype |
| **Structural** | Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy |
| **Behavioral** | Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor |

### Quick Mental Models

| Pattern | One-line Mental Model |
|---|---|
| Singleton | Only one object — globally controlled lifecycle |
| Factory | "Give me the right object" — creation delegated |
| Abstract Factory | "Give me the right family" — consistent groups |
| Builder | Step-by-step construction with fluent interface |
| Prototype | Clone instead of construct |
| Adapter | Interface translator |
| Bridge | Avoid class explosion via composition |
| Composite | Tree structure — treat leaf and group uniformly |
| Decorator | Dynamic feature layering |
| Facade | Simplification layer over complexity |
| Flyweight | Share intrinsic state to save memory |
| Proxy | Controlled access wrapper |
| Observer | Event subscription — push notifications |
| Strategy | Runtime algorithm selection |
| State | Behavior switches when state changes |
| Chain | Pipeline — pass until handled |
| Command | Encapsulate action as object |
| Iterator | Controlled traversal without exposing structure |
| Mediator | Central communication hub |
| Memento | State snapshot for undo/restore |
| Template Method | Algorithm blueprint with variable steps |
| Visitor | External behavior injection |

### Pattern Confusion Resolver

| vs. | Distinction |
|---|---|
| Strategy vs State | Strategy = algorithm selection; State = behavior tied to lifecycle stage |
| Strategy vs Factory | Strategy = runtime behavior selection; Factory = runtime object creation |
| Proxy vs Decorator | Proxy = access control; Decorator = behavior addition |
| Facade vs Adapter | Facade = simplify complex system; Adapter = translate incompatible interfaces |
| Observer vs Mediator | Observer = broadcast to all; Mediator = route to specific recipients |
| Composite vs Decorator | Composite = tree structure; Decorator = stacked features on single object |

---

## The Interview Trap Vault

> ⚠️ These are the **high-value tricky scenario questions** from real architecture interviews. Study these carefully.

---

### Singleton Traps

**Trap 1: "Show me a Singleton" — then ask "Is it thread-safe?"**

Most candidates write the basic version. The trap is thread safety. Two threads can simultaneously find `_instance is None` and both create separate instances.

```python
# WRONG — not thread-safe
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Race condition here!
        return cls._instance

# CORRECT — thread-safe
from threading import Lock
class Singleton:
    _instance = None
    _lock = Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
```

**Trap 2: "Is Singleton always the right choice for a logger?"**

Answer: Not always. In microservices, you might want per-request loggers with request IDs. Singleton logger would mix up log entries from concurrent requests without proper scoping. Use thread-local or context-local loggers in high-concurrency scenarios.

**Trap 3: "Why override `__new__` not `__init__`?"**

`__init__` runs **after** the object is already created. By the time `__init__` runs, the new object already exists in memory. To prevent creation, you must intercept at `__new__`.

**Trap 4: "Can you unit test Singleton easily?"**

NO — global state makes test isolation impossible. Tests may affect each other if they share the same Singleton instance. Solution: dependency injection + reset mechanism for testing:
```python
@classmethod
def reset(cls):  # Test helper only!
    cls._instance = None
```

---

### Factory Traps

**Trap 1: "Factory vs Abstract Factory — explain with a real system"**

Wrong answer: "Factory creates one object, Abstract Factory creates many."
Better answer: "Factory is for single product types. Abstract Factory is when you need to guarantee that a whole group of objects are compatible with each other — like ensuring your database connection, query builder, and transaction manager all work together for the same database engine."

**Trap 2: "Can you replace a Factory with a dictionary?"**

Yes, in Python — and this is often more Pythonic:
```python
REGISTRY = {
    "dog": Dog,
    "cat": Cat,
}

def create_animal(animal_type: str) -> Animal:
    cls = REGISTRY.get(animal_type)
    if not cls:
        raise ValueError(f"Unknown: {animal_type}")
    return cls()
```
This avoids class hierarchy for simple cases. Know WHEN the full pattern is warranted.

**Trap 3: "Where does Factory violate Open/Closed Principle?"**

The Simple Factory (with if-else) violates Open/Closed because adding a new type requires modifying the factory's `if-else` block. The proper Factory Method pattern (polymorphic creators) solves this — you add a new `ConcreteCreator` subclass without touching existing code.

---

### Abstract Factory Traps

**Trap 1: "What's the downside of Abstract Factory?"**

Adding a NEW **product type** (not a new factory/theme) is hard. If you have `LightThemeFactory` and `DarkThemeFactory` and want to add `Slider` widgets, you must modify the `UIFactory` interface AND both concrete factories. This violates Open/Closed for product expansion.

**Trap 2: "Can Abstract Factory use Factory Method internally?"**

YES — very common. Each `create_button()` in a concrete factory is itself a Factory Method.

**Trap 3: "Is Abstract Factory the same as Dependency Injection?"**

NO — DI is a technique for providing dependencies to objects; Abstract Factory is a pattern for creating families of related objects. But they work beautifully together: inject the factory, let it create the family.

---

### Builder Traps

**Trap 1: "Builder vs keyword arguments in Python"**

In Python, `dataclasses` and keyword arguments reduce the need for Builder for simple cases. But Builder wins when: validation logic is needed during `.build()`, the object has multiple valid configurations with complex rules, or you need different "representations" from the same building steps (Director pattern).

**Trap 2: "What if I call .build() before setting required fields?"**

The `.build()` method should validate that all required fields are set and raise `ValueError` if not. This is the "immutable object" guarantee — build fails fast rather than creating an invalid object.

**Trap 3: "Is method chaining always good?"**

No. Method chaining breaks debuggability (can't set breakpoints between chained calls easily). Use it for fluent interfaces where the readability benefit is clear, not everywhere.

---

### Observer Traps

**Trap 1: "What happens if an observer throws an exception during notify()?"**

Without protection, one bad observer can break ALL subsequent notifications. Use try-catch inside the notification loop:
```python
def notify(self):
    for obs in self.observers:
        try:
            obs.update()
        except Exception as e:
            print(f"Observer {obs} failed: {e}")
```

**Trap 2: "How do you prevent memory leaks with Observer?"**

If observers are not removed when they're destroyed, the Subject holds a strong reference → memory leak. Solutions:
- Explicit `unsubscribe()` calls (manual)
- Weak references (`weakref.ref`) to observers
- Context managers for subscription lifecycle

**Trap 3: "Observer vs Pub/Sub — what's the difference?"**

Observer: Subject has direct reference to Observers (tight coupling on both sides).
Pub/Sub: Publisher and Subscriber don't know each other — a message broker/bus sits between them (looser coupling). Kafka, RabbitMQ implement Pub/Sub. Django signals implement a hybrid.

---

### Strategy Traps

**Trap 1: "Strategy vs State — give me a real example of when they look similar"**

Payment processing can look like either:
- **Strategy**: User CHOOSES their payment method (Credit Card, UPI) — same context, different algorithm, user decides.
- **State**: Payment goes through lifecycle (Pending → Processing → Completed → Failed) — context changes behavior based on its stage.

The key: **Strategy** is about the client's **choice**. **State** is about the object's **lifecycle**.

**Trap 2: "In Python, do you even need the Strategy pattern?"**

Often no — just pass a function. The pattern shines when strategies are complex objects with their own state (e.g., a compression strategy that maintains a dictionary), or when you need a formal interface contract.

---

### Proxy Traps

**Trap 1: "Proxy vs Decorator — when do you use which?"**

Use **Proxy** when: controlling access to a resource, adding security checks, lazy loading heavy objects, caching results of expensive calls.

Use **Decorator** when: adding features/behaviors, wrapping functionality without access control, stacking multiple features dynamically.

The philosophical difference: Proxy is about **access control**. Decorator is about **feature enrichment**.

**Trap 2: "How is Django ORM's lazy loading a Proxy?"**

```python
user = User.objects.get(id=1)
# user.orders is NOT loaded yet — it's a proxy/promise
orders = user.orders.all()  # NOW it loads — lazy evaluation
```

The `orders` relationship is a Proxy that only triggers the database query when you actually access it.

---

### General Architecture Traps

**Trap 1: "Design a notification system for an e-commerce app"**

Expected use of Observer/Pub-Sub:
- Order placed → notify: Email service, SMS service, Analytics, Inventory
- Don't couple OrderService directly to EmailService
- Use event bus: `order_placed.emit(order)` → all subscribers react

**Trap 2: "I need to support PostgreSQL and MongoDB in my app — which pattern?"**

Use **Abstract Factory**: Create `PostgreSQLFactory` and `MongoDBFactory`. Each produces compatible Connection, QueryBuilder, and TransactionManager. Switch the factory → entire database layer adapts.

**Trap 3: "What's wrong with using Singleton for user session data?"**

Singleton is global and shared across all requests in a server process. In a multi-user web app, all users would share the SAME session object → catastrophic security vulnerability. Per-request state must never be a Singleton.

**Trap 4: "Over-engineering question: should a simple TODO app use design patterns?"**

NO — for a simple TODO app, a single `TodoRepository` class with CRUD operations is fine. Applying Factory, Abstract Factory, Builder etc. to a TODO app is over-engineering. Pattern complexity must match problem complexity.

---

### FAANG-Level Senior Tips

> 🔥 **How engineers at top tech companies actually use patterns:**

1. **Patterns are rarely named** — Engineers don't say "let's use Abstract Factory here." They say "let's make this pluggable" and the pattern emerges naturally.

2. **Pythonic > Pattern-correct** — A Python module import beats a Singleton class. A lambda beats a Strategy class for simple cases.

3. **SOLID over patterns** — If you apply SOLID principles correctly, patterns emerge naturally. Don't force patterns; apply principles.

4. **Most important patterns in production:**
   - **Factory/Abstract Factory**: Every major framework uses these internally
   - **Observer/Pub-Sub**: Every event-driven system (Django signals, Kafka consumers)
   - **Builder**: Every SDK, every ORM query interface
   - **Proxy**: Every ORM lazy loading, every API gateway
   - **Singleton**: Every logger, every connection pool

5. **Don't memorize — understand:** When you face a problem of "too many if-else for object creation" → Factory appears naturally. When you face "all UI components must match" → Abstract Factory appears naturally. Understand problems deeply; patterns are the solutions.

> 🧠 **Final Senior Advice:**
> **Design Patterns are Mental Models — not a syllabus.**
> Understand the problem deeply → the right pattern will appear naturally.
> The goal is: Scalability, Maintainability, Low coupling, High cohesion, Future extension.

---

## Alternative Resources

For decision-tree based pattern selection: [Stop Memorizing Design Patterns — Use This Decision Tree Instead](https://medium.com/womenintechnology/stop-memorizing-design-patterns-use-this-decision-tree-instead-e84f22fca9fa)

---

*These notes represent complete, production-grade coverage of all 23 GoF Design Patterns with Python implementations, real-world examples, and senior-level interview preparation. Every analogy, interview trap, and industry example is preserved from source.*
