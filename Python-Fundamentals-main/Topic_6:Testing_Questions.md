# Master Python Testing & Code Quality Interview Guide: Intermediate to Senior Engineer

This document evaluates a candidate's ability to write reliable, maintainable software. It tests their understanding of testing theory, their mastery of Python's testing ecosystem (`pytest`, `unittest`, `mock`), and their pragmatic approach to code quality at scale.

---

## SECTION 1: Testing Fundamentals & Architecture

#### 1. What is the "Test Pyramid," and how does it influence your testing strategy?
**Answer:**
The Test Pyramid is a framework that dictates the proportion of different types of tests in a codebase. 
*   **Bottom Layer (Unit Tests):** Should form the vast majority of tests. They are isolated, highly specific, and extremely fast.
*   **Middle Layer (Integration Tests):** Fewer in number. They verify that different parts of the system (or external dependencies like a database) work together correctly.
*   **Top Layer (End-to-End / UI Tests):** The smallest portion. They test the entire system top-to-bottom mimicking a real user, but are slow, brittle, and expensive to maintain.
*   **Senior Takeaway:** An inverted pyramid (an "Ice Cream Cone" anti-pattern) with too many E2E tests and few unit tests results in slow CI/CD pipelines and flaky test suites.

#### 2. Explain the F.I.R.S.T. principles of good Unit Testing.
**Answer:**
*   **Fast:** Tests should run in milliseconds so developers run them constantly.
*   **Isolated / Independent:** Tests should not depend on each other or guarantee a specific execution order. State shouldn't bleed between tests.
*   **Repeatable:** Tests should yield the exact same result every time, regardless of environment, network status, or time of day.
*   **Self-validating:** Tests should objectively pass or fail via assertions without requiring human inspection of logs or outputs.
*   **Timely:** Tests should ideally be written right before or alongside the production code (TDD approach).

#### 3. What is the difference between Unit Testing and Integration Testing? Where do you draw the line?
**Answer:**
*   **Unit Tests** examine a single logical component (a function or class) in absolute isolation. If the code interacts with the filesystem, a database, a network, or the system clock, it is *not* a unit test. Those elements must be mocked.
*   **Integration Tests** explicitly verify the wiring between components or external systems. They ensure that your Python code interacts correctly with a real database schema or a third-party API.

---

## SECTION 2: Python Testing Frameworks (`pytest` vs `unittest`)

#### 4. Compare `unittest` and `pytest`. Why has the Python community largely adopted `pytest`?
**Answer:**
*   **`unittest`:** Part of the standard library, built heavily on Java's JUnit OOP pattern. It requires substantial boilerplate (inheriting from `unittest.TestCase`), uses verbose assertion methods (`self.assertEqual()`, `self.assertTrue()`), and uses `setUp`/`tearDown` for state management.
*   **`pytest`:** A third-party framework that uses plain Python functions (no class inheritance needed). 
*   **Why `pytest` wins:** 
    1. Less boilerplate.
    2. Uses native Python `assert` statements (`assert x == y`) but provides deep introspection on failure to show exact variable diffs.
    3. Powerful modular Fixture system (replacing rigid `setUp`).
    4. Extensive plugin ecosystem (`pytest-django`, `pytest-asyncio`, `pytest-cov`).

#### 5. How does `pytest` perform assert introspection? (Senior Level)
**Answer:**
Because `assert` is a Python keyword, not a function, it normally just raises an `AssertionError` with no details. `pytest` uses **AST (Abstract Syntax Tree) rewriting**. Before the test module is executed, `pytest` hooks into Python's import system, rewrites the bytecode of the `assert` statements to intercept the intermediate variables, and injects code to store those values. This is why it can show exact diffs between complex dictionaries or lists on failure.

---

## SECTION 3: Fixtures & State Management

#### 6. What are `pytest` Fixtures? How are they superior to `setUp` and `tearDown`?
**Answer:**
Fixtures are functions decorated with `@pytest.fixture` that provide baseline state, data, or dependencies to tests via dependency injection (passing the fixture name as an argument to the test function).
*   **Why they are better:**
    1. **Modularity:** They are reusable across multiple test files.
    2. **Composability:** Fixtures can depend on other fixtures.
    3. **Explicitness:** You can clearly see which test uses which fixture by looking at the test's arguments, unlike `setUp` which runs blindly for every test in a class.

#### 7. Explain Fixture Scopes in `pytest`. When would you use a `session` scoped fixture?
**Answer:**
Scopes dictate how often a fixture is invoked and destroyed:
*   **`function` (default):** Invoked once per test function.
*   **`class` / `module` / `package`:** Invoked once per class, module, or package.
*   **`session`:** Invoked once per test run.
*   **Use Case for Session:** Expensive operations that only need to happen once and are safe to share, such as spinning up a Docker container, establishing a single database connection pool, or loading a massive machine learning model into memory.

#### 8. How do you handle teardown/cleanup logic within a `pytest` fixture?
**Answer:**
Instead of returning a value, you use the `yield` keyword.
```python
@pytest.fixture
def db_connection():
    conn = create_db_connection() # Setup
    yield conn                    # Inject into test
    conn.close()                  # Teardown (runs after test completes)
```

#### 9. What is `conftest.py`?
**Answer:**
It is a local per-directory plugin for `pytest`. Any fixtures, hooks, or configurations defined in `conftest.py` are automatically discovered and made globally available to all tests in that directory and its subdirectories, without needing to explicitly import them.

---

## SECTION 4: Mocking, Patching, and Dependency Isolation

#### 10. Explain the difference between a Dummy, Stub, Spy, Mock, and Fake. (Senior Level)
**Answer:**
These are all "Test Doubles," but they serve different purposes:
*   **Dummy:** Objects passed around just to satisfy parameters, but never actually used/called.
*   **Stub:** Returns hardcoded, predefined data to calls (e.g., a function that always returns `{"status": 200}`).
*   **Spy:** Wraps a real object to record how it was used (e.g., recording how many times a method was called and with what arguments), while still executing the real code.
*   **Mock:** Objects pre-programmed with expectations. You verify that the mock was called exactly as expected (behavioral verification).
*   **Fake:** An object with a working, but simplified, implementation (e.g., an in-memory SQLite database replacing PostgreSQL, or an in-memory list replacing a Redis queue).

#### 11. What is the fundamental rule of "where to patch" when using `unittest.mock.patch`? Give an example.
**Answer:**
**Rule:** *"Patch where the object is used (looked up), not where it is defined."*
*   **Example:** You have `module_a.py` which contains `from my_app.services import fetch_data`.
*   If you are testing `module_a`, you must patch `module_a.fetch_data`.
*   **Gotcha:** If you try to patch `my_app.services.fetch_data`, it will fail because `module_a` has already imported the original reference into its own namespace before the patch was applied.

#### 12. What is the difference between `Mock` and `MagicMock` in Python?
**Answer:**
`MagicMock` is a subclass of `Mock` that comes pre-configured with mostly default implementations of Python's "magic" (dunder) methods. 
*   If you mock an object and need to use it in a `for` loop (requires `__iter__`), get its length (requires `__len__`), or use it as a context manager (requires `__enter__` and `__exit__`), `Mock` will throw an error, whereas `MagicMock` will succeed.

#### 13. What are the dangers of over-mocking?
**Answer:**
"Mocking out the world" leads to tests that are tightly coupled to the implementation details rather than the desired output. 
*   **False Positives:** Tests pass because the mocks return what you expect, but the real system fails in production because an underlying API changed.
*   **Refactoring friction:** If you change an internal variable name or function signature, you have to rewrite dozens of mock assertions, even if the overall behavior hasn't changed.

---

## SECTION 5: Coverage & Code Quality

#### 14. What is Code Coverage vs. Branch Coverage?
**Answer:**
*   **Line Coverage:** The percentage of executed lines of code during a test run.
*   **Branch Coverage:** A deeper metric. It ensures that both the `True` and `False` paths of control structures (`if`/`else` statements, `try`/`except` blocks) are executed. You can have 100% line coverage but miss branch coverage if an `if` statement evaluates to true and executes a line, but the false condition is never tested.

#### 15. Is 100% test coverage a good engineering goal? (Architectural Level)
**Answer:**
*   Generally, **no**. It is a metric, not a target. Striving for 100% often leads to diminishing returns, resulting in developers writing trivial tests just to satisfy the coverage tool (e.g., testing simple getters/setters or mocking 99% of a complex dependency just to hit a single line).
*   **Pragmatic Approach:** Target high coverage (80-90%) on core business logic, complex algorithms, and state machines. Lower coverage is acceptable on simple glue code, UI layers, or third-party wrappers where E2E tests are more effective.

---

## SECTION 6: Advanced Scenarios & Whiteboard

#### 16. Whiteboard Scenario: Parametrized Testing
**Question:** *"You have a function `is_valid_email(email)`. Instead of writing 10 different test functions for 10 different email strings, how would you test this cleanly?"*
**Answer:**
The candidate should demonstrate `@pytest.mark.parametrize`.
```python
import pytest

@pytest.mark.parametrize("email, expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("user@sub.domain.org", True),
    ("", False)
])
def test_is_valid_email(email, expected):
    assert is_valid_email(email) == expected
```
*Bonus points:* Mentioning that `pytest` registers each parameter set as a completely distinct, independent test in the console output.

#### 17. How do you test asynchronous Python code (`asyncio`)?
**Answer:**
Native `pytest` does not inherently understand `async` functions (they return coroutine objects instead of executing). 
*   **Solution:** Use the `pytest-asyncio` plugin and decorate the test with `@pytest.mark.asyncio`. 
*   **Mocking Async:** When mocking an async function, standard `Mock` won't work because it returns a regular object, not an awaitable. You must use `AsyncMock` (introduced in Python 3.8).

#### 18. Whiteboard Scenario: The Flaky Test
**Question:** *"A test occasionally fails on CI/CD but passes locally. It involves fetching data from an external API, calculating a timestamp, and updating a database. How do you debug and fix this?"*
**Answer:**
A senior candidate should instantly recognize the major causes of flakiness:
1.  **External Dependencies:** The test shouldn't be making real API calls. *Fix:* Use `responses` or `vcrpy` to mock the HTTP responses.
2.  **Time/Concurrency Dependencies:** If the test asserts `created_at == datetime.now()`, it will fail sporadically due to execution micro-delays. *Fix:* Use a library like `freezegun` (`@freeze_time`) or mock `datetime` to lock the system clock during the test.
3.  **Database State Bleed:** The test might be failing because a previous test left records in the database. *Fix:* Ensure tests run within a database transaction that is rolled back after the test completes (e.g., using `pytest-django`'s `db` fixture).