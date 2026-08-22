# 🎬 Python Mocking & Patching: The Master Encyclopedia

### A Professional-Grade Guide to Test Isolation — Built for Engineers Who Want Tests That Actually Prove Something

> **"A test is only as good as its isolation. Master the mock, master the test."**

---

## 📋 Table of Contents

- [The Movie Set Philosophy](#the-movie-set-philosophy)
- [The Test Doubles Taxonomy](#the-test-doubles-taxonomy)
- [Module 1: Mock vs. MagicMock — The Basics](#module-1-mock-vs-magicmock--the-basics)
- [Module 2: Strictness Control — spec & autospec](#module-2-strictness-control--spec--autospec)
- [Module 3: AsyncMock — Testing the Async World](#module-3-asyncmock--testing-the-async-world)
- [Module 4: The Patching Namespace — Where to Patch](#module-4-the-patching-namespace--where-to-patch)
- [Module 5: Scripting Behavior — return_value vs side_effect](#module-5-scripting-behavior--return_value-vs-side_effect)
- [Module 6: Spying with wraps](#module-6-spying-with-wraps)
- [Module 7: Monkeypatching — The pytest Surgical Tool](#module-7-monkeypatching--the-pytest-surgical-tool)
- [Module 8: PropertyMock — Taming @property](#module-8-propertymock--taming-property)
- [Module 9: Patching Built-ins — open, print, input](#module-9-patching-built-ins--open-print-input)
- [Module 10: Call Order & Tracking](#module-10-call-order--tracking)
- [Module 11: Professional Stage — Fixtures + Mocker](#module-11-professional-stage--fixtures--mocker)
- [Module 12: Mocking Celery / Background Tasks](#module-12-mocking-celery--background-tasks)
- [Module 13: Handling Multiple Return Values](#module-13-handling-multiple-return-values)
- [Module 14: Verification Mastery — Advanced Assertions](#module-14-verification-mastery--advanced-assertions)
- [Module 15: Common Mocking Pitfalls & the MockerNotFound Error](#module-15-common-mocking-pitfalls--the-mockernotfound-error)
- [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)

---

## The Movie Set Philosophy

Every mocking concept maps to a role on a movie set. Keep this table on your desk.

| Role | Testing Equivalent | What It Does |
|---|---|---|
| 🎬 **Director** | `patch()` / `mocker.patch()` | Controls *what* gets replaced and *when* |
| 🦸 **Lead Actor** | Real production code | The thing you're actually testing |
| 🥋 **Stunt Double** | `Mock` / `MagicMock` / `AsyncMock` | A safe stand-in that won't break the scene |
| 📝 **Script Revision** | `return_value` / `side_effect` | Tells the stunt double how to perform |
| 🔍 **On-Set Documentary Crew** | `wraps=` parameter | Watches without replacing real performance |
| ✂️ **Quick Script Change** | `monkeypatch` fixture | A last-minute line change while filming is live |
| 🕵️ **Continuity Supervisor** | Assert methods | Checks every call was made exactly as scripted |

---

## The Test Doubles Taxonomy

> **This is the section most guides skip — and it causes the most confusion.**

"Mock" is actually an umbrella term. There are five distinct types of test doubles. Using the wrong one leads directly to fragile, over-coupled tests.

| Double | What It Is | When to Use |
|---|---|---|
| **Dummy** | An object passed around but never used | Filling required parameters that don't affect the test |
| **Stub** | Returns pre-programmed responses; does nothing else | Replacing a dependency to control what it returns (`return_value`) |
| **Spy** | Records calls while delegating to the real implementation | Observing interactions without replacing behavior (`wraps=`) |
| **Mock** | A stub that *also* verifies it was called correctly | When the interaction itself (not just the result) is what you're testing |
| **Fake** | A simplified working implementation (e.g., in-memory DB) | When you want realistic behavior without real infrastructure |

> **💡 Expert Tip:** When you use `patch()` with `return_value`, you're technically creating a **Stub**. When you add `assert_called_with()`, you've made it a **Mock**. Python's `Mock` class can play any role — but being intentional about *which* role you're casting keeps your tests clean and honest.

> **⚠️ Danger Zone:** Mocks are NOT Stubs. A stub makes tests *pass* by controlling inputs. A mock makes tests *meaningful* by verifying behavior. Conflating them is the root cause of most "Mock Hell" scenarios.

---

## Module 1: Mock vs. MagicMock — The Basics

### 📖 Plain English Definition

A `Mock` is a blank, programmable impersonator. You hand it to your code in place of a real object, and it silently accepts any attribute access or method call — recording everything for later inspection. A `MagicMock` is the same thing, but pre-wired with support for Python's special "dunder" methods (`__len__`, `__iter__`, `__enter__`, `__exit__`), making it compatible with containers, context managers, and other protocol-heavy objects right out of the box.

### 🛠️ Ways to Use This

- **Mocking a simple service call:** Replace a `PaymentService` with a `Mock` to verify `.charge()` is called without actually billing anyone.
- **Mocking a database result set:** Use `MagicMock` when your code does `for row in db_cursor:` — the `__iter__` dunder protocol works automatically.
- **Mocking a context manager:** `MagicMock` supports `with open(...) as f:` via pre-configured `__enter__` and `__exit__` dunders.

### 🎬 Movie Set Analogy

A `Mock` is a **generic stunt double** — they can stand on set and take direction, but if the scene requires juggling or speaking fluent French, you need a specialist. A `MagicMock` is the **full-package performer**, pre-trained in every "special skill" that Python's data model requires.

### 💬 The "Why" in Plain Sentences

We need `Mock` when testing code that simply calls methods on an object. We need `MagicMock` when our code uses Python's built-in protocols — loops, `with` blocks, `len()`. The difference is almost always about whether your code interacts with the object using *operators and syntax* rather than just direct method calls.

```python
# FILE: test_module1_mock_vs_magicmock.py
# PURPOSE: Learn when to reach for Mock vs. MagicMock

from unittest.mock import Mock, MagicMock

def greet_user(email_service, user_email):
    email_service.send(to=user_email)  # Plain method call, no magic

def test_mock_is_enough():
    mock_svc = Mock()              # Blank impersonator — no special skills needed
    greet_user(mock_svc, "a@b.com")
    # Verify the right method was called with the right args
    mock_svc.send.assert_called_once_with(to="a@b.com")
```

```python
from unittest.mock import MagicMock

def count_items(repo):
    return len(repo)   # len() calls __len__ — Mock raises TypeError here

def test_magicmock_handles_dunder():
    mock_repo = MagicMock()        # MagicMock has __len__ pre-configured
    mock_repo.__len__.return_value = 5   # Tell it what len() should return
    assert count_items(mock_repo) == 5   # This now works without error
```

> **Key Takeaway:** Reach for `MagicMock` by default; switch to plain `Mock` only when you want to *signal* to future readers that no protocol magic is expected.

---

## Module 2: Strictness Control — spec & autospec

### 📖 Plain English Definition

By default, a `Mock` will happily accept *any* method call — even ones that don't exist on the real object. `spec` and `autospec` are safety nets that constrain the mock to only allow attributes and method signatures that exist on the real class. This prevents your tests from going green even after you've renamed or deleted a method in production.

### 🛠️ Ways to Use This

- **Catching renamed methods:** If `user_service.get_by_id()` is renamed to `get_user()`, an `autospec` mock will fail immediately — a plain `Mock` would silently pass.
- **Validating argument signatures:** `autospec` raises `TypeError` if you call the mock with the wrong number of arguments, matching real Python behavior.
- **Documenting intent in tests:** Using `spec=MyClass` is a self-documenting signal: "this mock must behave like `MyClass`."

### 🎬 Movie Set Analogy

A plain `Mock` is a **yes-man extra** — they'll agree to do any scene, even ones not in the script. `autospec` is the **union-approved stunt coordinator** who insists the double can only perform stunts that are in the *actual script* and *within their certified skill set*.

### 💬 The "Why" in Plain Sentences

Silent failures are the worst kind of bug. Without `spec`, you can delete a method in production, forget to update your mock, and your tests keep passing — giving you false confidence. `autospec=True` makes your mock a strict contract enforcer. Use it on any dependency that might drift over time.

```python
# FILE: test_module2_autospec.py
# PURPOSE: Show how autospec catches interface drift

from unittest.mock import create_autospec

class Calculator:
    def add(self, a, b):   # Real method takes exactly 2 args
        return a + b

def test_autospec_enforces_signature():
    # create_autospec mirrors the real class's interface
    mock_calc = create_autospec(Calculator, instance=True)
    mock_calc.add.return_value = 10    # Program the return value
    result = mock_calc.add(1, 2)       # Valid call — passes fine
    assert result == 10                # Assertion confirms behavior
```

```python
import pytest
from unittest.mock import create_autospec

class Calculator:
    def add(self, a, b):
        return a + b

def test_autospec_rejects_wrong_args():
    mock_calc = create_autospec(Calculator, instance=True)
    # Calling with wrong number of args raises TypeError — just like the real class
    with pytest.raises(TypeError):
        mock_calc.add(1, 2, 3)   # Too many args — autospec catches this!
```

> **💡 Expert Tip:** Prefer `create_autospec(MyClass, instance=True)` over `Mock(spec=MyClass)`. The `instance=True` flag ensures `self` is handled correctly, preventing a subtle class-vs-instance signature mismatch.

> **Key Takeaway:** Use `autospec=True` on every external dependency mock — it's your early-warning system for interface drift.

---

## Module 3: AsyncMock — Testing the Async World

### 📖 Plain English Definition

`AsyncMock` is a mock designed specifically for Python's `async`/`await` syntax. When your code `await`s a function, Python expects a coroutine object back — a plain `Mock` or `MagicMock` can't provide that, causing your tests to crash or behave unexpectedly. `AsyncMock` returns the right type and even provides async-specific assertion methods.

### 🛠️ Ways to Use This

- **Mocking an async API client:** Replace `await http_client.get(url)` with a controlled `AsyncMock` that returns a fake response without hitting the network.
- **Simulating async database queries:** Mock `await db.fetch_one(query)` to return test data without needing a running database.
- **Testing async error handling:** Use `side_effect` on an `AsyncMock` to simulate a network timeout inside an `async` function.

### 🎬 Movie Set Analogy

Regular stunt doubles are great for synchronous action scenes — one person, one moment. But a wire-work scene requires a **specially trained aerial stunt performer**. `AsyncMock` is that specialist: the only double who knows how to "fly" through an `await` call without crashing the production.

### 💬 The "Why" in Plain Sentences

When Python sees `await some_function()`, it expects a coroutine. A regular `Mock` returns a `Mock` object — not a coroutine — which causes a `RuntimeWarning` or `TypeError`. `AsyncMock` solves this by making itself `await`-able. Since Python 3.8, `unittest.mock.patch` auto-detects `async def` functions and uses `AsyncMock` automatically.

```python
# FILE: test_module3_asyncmock.py
# PURPOSE: Test async functions without running a real event loop

import pytest
from unittest.mock import AsyncMock

async def fetch_user_name(api_client, user_id):
    result = await api_client.get_user(user_id)  # This is an async call
    return result["name"]

@pytest.mark.asyncio   # Tells pytest this is an async test
async def test_fetch_user_name():
    mock_client = AsyncMock()   # AsyncMock is await-able
    # Set what the awaited call returns
    mock_client.get_user.return_value = {"name": "Alice"}
    name = await fetch_user_name(mock_client, 42)
    assert name == "Alice"   # Our function correctly extracts the name
```

```python
import pytest
from unittest.mock import AsyncMock

async def fetch_data(client):
    return await client.fetch()   # Awaits an external async call

@pytest.mark.asyncio
async def test_async_exception():
    mock_client = AsyncMock()
    # side_effect makes the awaited call raise an exception
    mock_client.fetch.side_effect = TimeoutError("Network timeout")
    with pytest.raises(TimeoutError):
        await fetch_data(mock_client)   # Our code must handle this
```

> **💡 Expert Tip:** For `pytest.mark.asyncio` to work, you need `pytest-asyncio` installed (`pip install pytest-asyncio`). Add `asyncio_mode = "auto"` to your `pytest.ini` to avoid decorating every single async test.

> **Key Takeaway:** Use `AsyncMock` for anything behind an `await` — it's the only mock that speaks the coroutine protocol.

---

## Module 4: The Patching Namespace — Where to Patch

### 📖 Plain English Definition

Patching means temporarily replacing a name in Python's namespace with a mock. The golden rule — the one that causes the most confusion — is: **patch the name where it is *used*, not where it is *defined*.** When your module imports a function, Python creates a local reference to it. You must patch *that local reference*, not the original source.

### 🛠️ Ways to Use This

- **Patching an imported library:** If `mymodule.py` does `import requests`, patch `mymodule.requests`, not `requests.get`.
- **Patching a class method:** Use `patch.object(MyClass, "method_name")` to surgically replace one method without touching the whole class.
- **Patching a module-level function:** If `payment.py` imports `send_email` from `utils`, patch `payment.send_email`, not `utils.send_email`.

### 🎬 Movie Set Analogy

Think of your module as a **film set**. The `requests` library is an actor who was *hired* (imported) for the production. Once they're on set, they have a **local badge** (the name in your module's namespace). If the Director (`patch`) wants to replace them with a stunt double, they must go through the **set's casting office** (`mymodule.requests`), not the actor's home agency (`requests.get`). The stunt double needs to show up on *your* set, not somewhere else.

### 💬 The "Why" in Plain Sentences

When Python runs `from utils import send_email` in `payment.py`, it creates a new binding: `payment.send_email`. Patching `utils.send_email` after the import has already happened does nothing — the reference in `payment.py` still points to the original. You must patch the name as it exists in the module *under test*.

```python
# FILE: my_service.py  (the module under test)
import requests   # Python creates: my_service.requests = <requests module>

def get_data(url):
    return requests.get(url).json()   # Uses my_service.requests
```

```python
# FILE: test_module4_namespace.py
from unittest.mock import patch

def test_get_data_correct():
    # ✅ CORRECT: patch the name as it exists inside my_service
    with patch("my_service.requests") as mock_req:
        mock_req.get.return_value.json.return_value = {"ok": True}
        from my_service import get_data
        result = get_data("http://example.com")
    assert result == {"ok": True}    # The mock intercepted the call
```

```python
# FILE: test_module4_namespace_wrong.py
from unittest.mock import patch

def test_get_data_wrong():
    # ❌ WRONG: patching the source, not the destination
    # my_service.requests is UNAFFECTED — it still points to the real library
    with patch("requests.get") as mock_get:
        from my_service import get_data
        get_data("http://example.com")   # This hits the REAL internet!
```

> **⚠️ Danger Zone:** The most common mocking bug is patching the wrong namespace. If your mock isn't being called, this is almost certainly why. Always ask: "Where does the module I'm testing *see* this name?"

> **Key Takeaway:** Patch WHERE the name is USED, not WHERE it's defined — always `mymodule.dependency`, never `dependency.method`.

---

## Module 5: Scripting Behavior — return_value vs side_effect

### 📖 Plain English Definition

`return_value` is a fixed script line — every time the mock is called, it says the same thing. `side_effect` is a dynamic director — it can return different things on each call, raise exceptions, or run real logic. Think of `return_value` as a pre-recorded answer and `side_effect` as a live improv performer.

### 🛠️ Ways to Use This

- **Fixed return value:** Use `mock.get_price.return_value = 9.99` to always return a stable value.
- **Raising exceptions:** Use `side_effect = ConnectionError("timeout")` to simulate a network failure.
- **Calling real logic:** Assign a function to `side_effect` to run real computation while still tracking calls.

### 🎬 Movie Set Analogy

`return_value` is a **pre-recorded voiceover** — the same words play every time, no matter what question is asked. `side_effect` is a **live actor with stage directions** — they can react differently based on what's happening in the scene, walk off stage (raise an exception), or call in a co-star (delegate to another function).

### 💬 The "Why" in Plain Sentences

Most tests need simple, fixed outputs — that's `return_value`. But real-world code has to handle failures, state changes, and sequential data. `side_effect` covers all of these. When both are set, `side_effect` always wins and overrides `return_value`.

```python
# FILE: test_module5_return_value.py
# PURPOSE: Control a mock's output with return_value

from unittest.mock import Mock

def get_discount(pricing_service, item_id):
    return pricing_service.lookup(item_id)   # Calls external service

def test_fixed_return():
    mock_svc = Mock()
    mock_svc.lookup.return_value = 0.20   # Always return 20% discount
    result = get_discount(mock_svc, "ITEM-1")
    assert result == 0.20   # Predictable, isolated, fast
```

```python
# FILE: test_module5_side_effect.py
# PURPOSE: Raise exceptions and dynamic responses with side_effect

import pytest
from unittest.mock import Mock

def call_api(client):
    return client.fetch()   # May raise in production

def test_exception_via_side_effect():
    mock_client = Mock()
    # side_effect with an exception instance makes the mock RAISE it
    mock_client.fetch.side_effect = ConnectionError("Server down")
    with pytest.raises(ConnectionError):
        call_api(mock_client)   # Our code must handle this
```

> **💡 Expert Tip:** `side_effect` also accepts an **iterable** — `[1, 2, 3]` — making the mock return `1` on the first call, `2` on the second, etc. When the list is exhausted, it raises `StopIteration`. See Module 13 for the deep dive on this pattern.

> **Key Takeaway:** Use `return_value` for stable, fixed outputs; use `side_effect` when behavior must change, fail, or depend on input.

---

## Module 6: Spying with wraps

### 📖 Plain English Definition

The `wraps` parameter lets you create a mock that *delegates* to a real function while still recording every call. You get the best of both worlds: real behavior executes, and you can still inspect how many times it was called and with what arguments. This is the true definition of a **Spy** in test double terminology.

### 🛠️ Ways to Use This

- **Auditing a utility function:** Verify that `calculate_tax()` is called exactly once during checkout without replacing its logic.
- **Observing a real algorithm:** Wrap a sorting function to check it's invoked with the right data while letting it actually sort.
- **Monitoring cache hits:** Spy on a cache lookup to count how many times it's called without disabling the cache.

### 🎬 Movie Set Analogy

`wraps` is the **on-set documentary crew**. They follow the lead actor around with a camera, capturing every take, every stumble, every line reading. But they don't *interfere* — the actor still performs the real scene. You get a full record of everything that happened without changing what happened.

### 💬 The "Why" in Plain Sentences

Sometimes you don't want to replace behavior — you just want to *observe* it. `wraps` lets you do exactly that. The real function runs, but the mock wraps around it to record calls. This is invaluable when you need to verify *that* a function was called without changing *what* it does.

```python
# FILE: test_module6_wraps.py
# PURPOSE: Spy on a real function without replacing its logic

from unittest.mock import Mock

def add(a, b):
    return a + b   # Real production logic we want to preserve

def test_spy_with_wraps():
    spy = Mock(wraps=add)   # Wraps the real function — passes calls through
    result = spy(2, 3)      # Calls the REAL add() function underneath
    assert result == 5      # Real logic ran — result is correct
    spy.assert_called_once_with(2, 3)  # But we can still inspect the call
```

> **⚠️ Danger Zone:** If you set `return_value` on a mock that uses `wraps`, the `return_value` takes precedence and the real function will **not** be called. `wraps` is silenced by `return_value`.

> **Key Takeaway:** Use `wraps=real_fn` when you want to *observe* without *replacing* — it's the cleanest way to create a Spy.

---

## Module 7: Monkeypatching — The pytest Surgical Tool

### 📖 Plain English Definition

`monkeypatch` is a built-in pytest fixture that lets you replace attributes, environment variables, dictionary values, and more — for the duration of a single test. Unlike `patch()`, it requires no context managers or decorators. It's the go-to tool for swapping out configuration, feature flags, and environment-level settings with surgical precision.

### 🛠️ Ways to Use This

- **Overriding environment variables:** Use `monkeypatch.setenv("API_KEY", "fake-key")` to test code that reads from `os.environ`.
- **Replacing a module-level function:** Use `monkeypatch.setattr("mymodule.send_email", fake_send)` to swap in a fake.
- **Removing a config value:** Use `monkeypatch.delattr(config, "timeout")` to test how code behaves when a setting is absent.

### 🎬 Movie Set Analogy

`monkeypatch` is the **script supervisor making a last-minute line change** just before the camera rolls. They walk onto the set, swap one prop (an env var, a config value, a function reference), shout "action!", and then quietly put everything back exactly as it was the moment the scene wraps. No permanent changes. No side effects on other scenes.

### 💬 The "Why" in Plain Sentences

`monkeypatch` automatically reverts all changes after each test — you never need to worry about test pollution. It's best suited for replacing simple values, environment config, and module-level globals. For complex dependencies like database clients or HTTP clients, `patch()` with a `MagicMock` is usually more appropriate.

```python
# FILE: test_module7_monkeypatch.py
# PURPOSE: Replace env vars and attributes cleanly per-test

import os

def get_env_greeting():
    name = os.environ.get("USER_NAME", "Stranger")
    return f"Hello, {name}!"

def test_env_greeting(monkeypatch):
    # setenv replaces the env var just for THIS test
    monkeypatch.setenv("USER_NAME", "Alice")
    result = get_env_greeting()
    assert result == "Hello, Alice!"   # Env var was correctly intercepted
```

```python
# FILE: test_module7_setattr.py
# PURPOSE: Replace a module-level function using monkeypatch.setattr

import mymodule   # Contains a function we want to swap

def test_swap_function(monkeypatch):
    # Replace mymodule.compute with a lambda for this test only
    monkeypatch.setattr(mymodule, "compute", lambda x: 99)
    result = mymodule.compute(5)   # Calls our fake, not the real one
    assert result == 99             # Fake logic ran as expected
```

> **💡 Expert Tip:** `monkeypatch.setattr` accepts a dotted string path too: `monkeypatch.setattr("os.path.exists", lambda p: True)`. This is useful when you don't have a direct import of the module.

> **Key Takeaway:** Use `monkeypatch` for environment variables, config values, and simple function swaps — it cleans up automatically and keeps tests independent.

---

## Module 8: PropertyMock — Taming @property

### 📖 Plain English Definition

Python's `@property` decorator turns a method into an attribute-style access. A regular `Mock` doesn't know how to intercept this — setting `mock.my_property = 42` just sets an attribute on the mock, bypassing the property mechanism entirely. `PropertyMock` is the specialized tool that correctly intercepts property *getters* and *setters* so your tests work the way the real class does.

### 🛠️ Ways to Use This

- **Mocking a read-only computed property:** Mock `user.full_name` which is a `@property` combining first and last name.
- **Testing a setter:** Verify that setting `config.timeout = 30` actually triggers the expected setter logic.
- **Controlling a cached property:** Mock `service.is_connected` to return `True` or `False` without a real connection.

### 🎬 Movie Set Analogy

A `@property` is a **one-way trapdoor in the stage floor** — it looks like a flat surface to anyone watching, but it has special mechanics underneath. A regular stunt double (`Mock`) doesn't know the trapdoor exists and just walks over it like normal ground. `PropertyMock` is the double who has been **briefed on all the stage mechanics** and reacts correctly when they step on it.

### 💬 The "Why" in Plain Sentences

The key to `PropertyMock` is *where* you attach it. You must use `patch.object` on the **class**, not an instance, and assign the `PropertyMock` to the property name using `new_callable=PropertyMock`. If you try to set it on an instance, Python's descriptor protocol bypasses your mock entirely.

```python
# FILE: test_module8_propertymock.py
# PURPOSE: Mock a @property on a class correctly

from unittest.mock import patch, PropertyMock

class Server:
    @property
    def status(self):           # Real property — might ping a server
        return "online"

def test_mock_property():
    # Must patch on the CLASS, using new_callable=PropertyMock
    with patch.object(Server, "status", new_callable=PropertyMock) as mock_status:
        mock_status.return_value = "offline"   # Control what the property returns
        server = Server()
        result = server.status    # Accesses the mocked property
    assert result == "offline"    # Our controlled value was returned
```

> **⚠️ Danger Zone:** Never do `mock_instance.my_property = value` when mocking a `@property`. That just sets a plain attribute, completely bypassing the property descriptor. Always patch on the class using `new_callable=PropertyMock`.

> **Key Takeaway:** `PropertyMock` must be attached to the *class*, not the instance — that's where Python's property descriptor lives.

---

## Module 9: Patching Built-ins — open, print, input

### 📖 Plain English Definition

Python's built-in functions (`open`, `print`, `input`) live in the `builtins` module. Patching them requires targeting the right namespace — either `builtins.open` globally, or `mymodule.open` if your module imports it implicitly. Python's `mock_open` is a pre-configured helper that makes mocking file I/O clean, readable, and reliable.

### 🛠️ Ways to Use This

- **Mocking file reads:** Use `mock_open(read_data="file content")` to simulate reading a config file without touching the filesystem.
- **Mocking `print`:** Patch `builtins.print` to verify your function outputs the right messages.
- **Mocking `input`:** Patch `builtins.input` to simulate user keyboard entry in a controlled way.

### 🎬 Movie Set Analogy

The `builtins` module is the **studio's central prop warehouse** — the place every production pulls from when they need a generic item like a phone, a door, or a file cabinet. Patching `builtins.open` is like telling the warehouse to give everyone who asks for a file cabinet a **fake one with paper already inside it**. Patching `mymodule.open` is like only swapping the cabinet on *your* specific set, leaving every other production untouched.

### 💬 The "Why" in Plain Sentences

Always prefer patching `mymodule.open` over `builtins.open` — narrower scope means less risk of affecting other code. `mock_open` does the heavy lifting of simulating the `open()` context manager and its file handle behavior. You just tell it what content to return via `read_data`.

```python
# FILE: test_module9_mock_open.py
# PURPOSE: Test file-reading logic without touching the real filesystem

from unittest.mock import patch, mock_open

def read_config(path):
    with open(path) as f:   # We want to mock this open() call
        return f.read()

def test_read_config():
    # mock_open pre-configures a full file-handle mock
    fake_file = mock_open(read_data="debug=True")
    # Patch open as it's seen inside THIS module
    with patch("builtins.open", fake_file):
        result = read_config("config.txt")
    assert result == "debug=True"   # Fake file content was returned
```

```python
from unittest.mock import patch

def announce(message):
    print(f">> {message}")   # We want to verify this print call

def test_print_is_called():
    with patch("builtins.print") as mock_print:
        announce("Ready")
        # Verify print was called with the formatted string
        mock_print.assert_called_once_with(">> Ready")
```

> **Key Takeaway:** Use `mock_open(read_data=...)` for file mocking and patch `builtins.open` — it simulates the entire file context manager so you never need to touch the real filesystem.

---

## Module 10: Call Order & Tracking

### 📖 Plain English Definition

When a mock is called multiple times, Python records the full history: every call, every argument, in exact order. `call_args_list` is the raw call log. `attach_mock` links child mocks to a parent so you can verify the *sequence* of calls across multiple mocks in one place, using a single manager mock as the "timeline."

### 🛠️ Ways to Use This

- **Verifying call order:** Confirm that `authenticate()` is always called before `fetch_data()` in your pipeline.
- **Inspecting all arguments:** Use `call_args_list` to assert each individual call in a loop was made with the right data.
- **Multi-mock sequencing:** Use `attach_mock` to verify that mock A, then mock B, then mock C were called in the right order.

### 🎬 Movie Set Analogy

`call_args_list` is the **director's shot log** — every take, every angle, every line, written down in order. `attach_mock` is the **continuity supervisor** who watches *all the actors at once* and records a unified timeline of who did what and when, so you can catch the "coffee cup in the wrong hand" continuity error immediately.

### 💬 The "Why" in Plain Sentences

Assertions like `assert_called_with` only check the *most recent* call. When you need to verify a sequence of calls, `call_args_list` gives you the full picture. For multi-step workflows where order matters (auth before fetch, validate before save), `attach_mock` is the tool that lets you express and verify that ordering constraint cleanly.

```python
# FILE: test_module10_call_tracking.py
# PURPOSE: Inspect the full call history of a mock

from unittest.mock import Mock, call

def run_pipeline(processor, items):
    for item in items:
        processor.handle(item)   # Called once per item

def test_all_calls_recorded():
    mock_proc = Mock()
    run_pipeline(mock_proc, ["a", "b", "c"])
    # call_args_list holds the complete ordered history
    assert mock_proc.handle.call_args_list == [
        call("a"), call("b"), call("c")   # Exact order verified
    ]
```

```python
from unittest.mock import Mock, call

def test_attach_mock_ordering():
    manager = Mock()             # The "timeline" manager
    step1 = Mock()               # First mock in sequence
    step2 = Mock()               # Second mock in sequence
    manager.attach_mock(step1, "first")   # Register step1 as "first"
    manager.attach_mock(step2, "second")  # Register step2 as "second"
    step1()                       # Call them in order
    step2()
    # Verify the unified call order on the manager
    assert manager.mock_calls == [call.first(), call.second()]
```

> **Key Takeaway:** Use `call_args_list` for per-mock history and `attach_mock` to verify ordering *across* multiple mocks in a single assertion.

---

## Module 11: Professional Stage — Fixtures + Mocker

### 📖 Plain English Definition

The `mocker` fixture, provided by the `pytest-mock` plugin, is a pytest-native wrapper around `unittest.mock`. It automatically cleans up all patches after each test (no context managers needed), integrates with pytest's fixture system, and provides a cleaner API. It's the professional's default choice in any pytest codebase.

### 🛠️ Ways to Use This

- **Shared mock setup:** Define mocks in a `@pytest.fixture` and inject them into multiple tests, keeping setup DRY.
- **Combining with conftest:** Place shared `mocker`-based fixtures in `conftest.py` for project-wide reuse.
- **Cleaner test signatures:** Replace `with patch(...)` blocks with `mocker.patch(...)` calls directly in test bodies.

### 🎬 Movie Set Analogy

`patch()` is like a **camera operator who sets up, films, and then has to manually tear down all the equipment** after every scene. The `mocker` fixture is like a **production crew with a union agreement** — they set up before the scene, everyone performs, and the crew automatically strikes the set the moment "cut" is called. No manual cleanup, no forgotten equipment.

### 💬 The "Why" in Plain Sentences

`unittest.mock.patch` as a context manager requires wrapping test code in `with` blocks, which can get deeply nested. As a decorator, it reverses argument order, which trips up beginners. The `mocker` fixture solves both problems: `mocker.patch()` is a single function call, cleanup is automatic, and the mock object is returned directly for immediate use.

```python
# FILE: test_module11_mocker.py
# PURPOSE: Use the mocker fixture for clean, automatic patch management

def add_numbers(a, b):
    return a + b   # Simple function to be replaced by a mock

def test_with_mocker(mocker):
    # mocker.patch replaces the target and AUTOMATICALLY cleans up after test
    mock_add = mocker.patch("__main__.add_numbers", return_value=99)
    result = add_numbers(1, 2)   # Calls the mock, not the real function
    assert result == 99          # Controlled value returned
    mock_add.assert_called_once_with(1, 2)   # Call was recorded
```

```python
# FILE: conftest.py
# PURPOSE: Share a pre-configured mock across multiple tests via fixture

import pytest

@pytest.fixture
def mock_db(mocker):
    # This fixture is available to any test in the project
    mock = mocker.patch("myapp.database.connect")
    mock.return_value.query.return_value = []   # Default: empty result
    return mock   # Tests can override return value as needed
```

> **💡 Expert Tip:** `mocker.patch` returns the mock object directly, unlike `patch()` as a decorator which requires an additional parameter. This makes `mocker` feel more Pythonic and reduces the "parameter explosion" problem when patching many things at once.

> **Key Takeaway:** Use `mocker.patch()` in pytest projects — it's cleaner, auto-cleaning, and integrates naturally with fixtures and conftest.

---

## Module 12: Mocking Celery / Background Tasks

### 📖 Plain English Definition

Celery is a distributed task queue that runs background jobs asynchronously via a message broker (RabbitMQ, Redis). In tests, you never want to spin up a real broker — you want to verify that a task was *dispatched* with the right arguments. Mocking Celery means intercepting the `.delay()` or `.apply_async()` call and verifying its arguments, without touching any infrastructure.

### 🛠️ Ways to Use This

- **Verifying task dispatch:** Confirm that `send_welcome_email.delay(user_id=5)` is called when a new user registers.
- **Testing the task logic itself:** Call the task function directly (without `.delay()`) to unit test its internal logic in isolation.
- **Simulating task failure:** Use `side_effect` to raise a `Retry` exception to test your retry-handling logic.

### 🎬 Movie Set Analogy

A Celery task is like **a stunt scene that has to be filmed in a separate location** — a different city, with a full crew. You don't want to fly everyone there just to rehearse a line reading. Instead, you use a **location stand-in** (the mock): someone who holds a card with "STUNT SCENE HAPPENS HERE" written on it. You verify the card was handed over at the right moment with the right instructions, without actually flying anywhere.

### 💬 The "Why" in Plain Sentences

Testing Celery tasks has two distinct layers. First, test whether the task is *dispatched* correctly (mock `.delay()`). Second, test whether the task's *internal logic* works correctly (call the function directly, bypassing `.delay()`). Never mix these two concerns. Mocking lets you test the dispatch layer in milliseconds, with no broker, no workers, and no infrastructure.

```python
# FILE: tasks.py
from celery import Celery
app = Celery("myapp")

@app.task
def process_order(order_id):
    # Task logic: process the order
    return f"Order {order_id} processed"
```

```python
# FILE: test_module12_celery.py
# PURPOSE: Verify task dispatch without a real message broker

from unittest.mock import patch

def dispatch_order(order_id):
    from tasks import process_order
    process_order.delay(order_id)   # This sends the task to the queue

def test_task_dispatched(mocker):
    # Patch the .delay method on the task — not the broker!
    mock_delay = mocker.patch("tasks.process_order.delay")
    dispatch_order(42)
    # Verify .delay() was called with the right order ID
    mock_delay.assert_called_once_with(42)
```

```python
# FILE: test_module12_task_logic.py
# PURPOSE: Test the task's INTERNAL logic directly, bypassing Celery entirely

def test_process_order_logic():
    from tasks import process_order
    # Call the underlying function directly — no broker, no .delay()
    result = process_order(99)    # Just a regular function call
    assert result == "Order 99 processed"   # Test the logic, not the queue
```

> **💡 Expert Tip:** Use Celery's built-in `CELERY_TASK_ALWAYS_EAGER = True` setting in test configurations to make all Celery tasks execute synchronously and locally. This is useful for integration tests where you want real task logic to run, but still in-process.

> **Key Takeaway:** Mock `.delay()` to verify dispatch; call the task function directly to verify logic — never test both in the same unit test.

---

## Module 13: Handling Multiple Return Values

### 📖 Plain English Definition

When you assign a *list* to `side_effect`, the mock becomes a **dispenser** — returning the first item on the first call, the second on the second call, and so on. When the list is exhausted, it raises `StopIteration`. This pattern is essential for testing retry logic, pagination, or any code that calls the same function multiple times and expects different results.

### 🛠️ Ways to Use This

- **Simulating retry logic:** Return a failure on the first two calls, then a success on the third — without any real network calls.
- **Mocking pagination:** Return page 1, then page 2, then an empty result to simulate a paginated API traversal.
- **Testing state transitions:** Return `"pending"`, then `"processing"`, then `"complete"` to simulate a job status progression.

### 🎬 Movie Set Analogy

A `side_effect` list is a **stack of index cards** handed to the stunt double before filming. On take 1, they read card 1. On take 2, card 2. The director calls the exact sequence and the double delivers each line in order. When the cards run out, filming stops (`StopIteration`). Use `itertools.cycle` if you need the deck to loop back to the top.

### 💬 The "Why" in Plain Sentences

Fixed `return_value` can't simulate sequential state. A `side_effect` list solves this by consuming one item per call. An exception in the list is *raised*, not returned — this lets you mix successes and failures in a single sequence. Use `itertools.cycle([...])` when you need an infinite, repeating pattern.

```python
# FILE: test_module13_multiple_returns.py
# PURPOSE: Simulate sequential responses with a side_effect list

from unittest.mock import Mock

def fetch_with_retry(client, max_retries=3):
    for attempt in range(max_retries):
        result = client.get()    # Called multiple times
        if result != "error":
            return result        # Return on first success
    return None

def test_retry_succeeds_on_third_attempt():
    mock_client = Mock()
    # First call → "error", second → "error", third → "data"
    mock_client.get.side_effect = ["error", "error", "data"]
    result = fetch_with_retry(mock_client)
    assert result == "data"          # Eventually succeeded
    assert mock_client.get.call_count == 3   # Took exactly 3 tries
```

```python
from unittest.mock import Mock
import pytest

def test_raises_mixed_with_returns():
    mock_svc = Mock()
    # Mix: first call raises, second call returns a value
    mock_svc.call.side_effect = [ConnectionError("down"), "ok"]
    with pytest.raises(ConnectionError):
        mock_svc.call()     # First call raises
    result = mock_svc.call()  # Second call returns normally
    assert result == "ok"
```

> **💡 Expert Tip:** Once a `side_effect` list is exhausted, the mock raises `StopIteration`. If your code might call the mock more times than you have items in the list, wrap the list in `itertools.cycle()` to create an infinite repeating sequence.

> **Key Takeaway:** Assign a list to `side_effect` for sequential, call-by-call control — mix return values and exception types freely in the same list.

---

## Module 14: Verification Mastery — Advanced Assertions

### 📖 Plain English Definition

Beyond "was this called?", Python's mock library offers a suite of precision assertion tools. `assert_called_with` checks only the *last* call. `assert_has_calls` verifies a *sequence* of calls. `assert_any_call` confirms a specific call appeared *somewhere* in the history. These tools let you write assertions that are as precise — or as flexible — as your test requires.

### 🛠️ Ways to Use This

- **Ordered sequence verification:** Use `assert_has_calls([call("a"), call("b")])` to confirm calls happened in the right order.
- **Flexible membership check:** Use `assert_any_call("critical_event")` to confirm a call was made at some point, regardless of order.
- **Exact call count:** Use `mock.call_count == 3` when you need to verify a precise number of invocations.

### 🎬 Movie Set Analogy

`assert_called_with` is the **continuity supervisor checking only the final scene**. `assert_has_calls` is the supervisor reviewing the **entire shooting schedule** to ensure every scene happened in the right order. `assert_any_call` is a **spot-checker** who just needs to confirm a specific scene was shot at least once, somewhere in the production.

### 💬 The "Why" in Plain Sentences

The most common mistake is using `assert_called_with` when you meant `assert_called_once_with`. The former only checks the *last* call — if your mock was called 5 times and you check the last call's args, the first 4 calls go completely unverified. When the number of calls matters, always also assert `call_count` or use `assert_called_once_with`.

```python
# FILE: test_module14_assert_has_calls.py
# PURPOSE: Verify an ordered sequence of calls

from unittest.mock import Mock, call

def run_workflow(notifier):
    notifier.send("start")    # First notification
    notifier.send("middle")   # Second notification
    notifier.send("end")      # Third notification

def test_call_sequence():
    mock_notifier = Mock()
    run_workflow(mock_notifier)
    # assert_has_calls checks that these calls appear IN ORDER
    mock_notifier.send.assert_has_calls([
        call("start"), call("middle"), call("end")
    ])
```

```python
from unittest.mock import Mock, call

def test_any_order_calls():
    mock_svc = Mock()
    mock_svc.process("b")    # Called in any order
    mock_svc.process("a")
    # any_order=True: all specified calls must appear, but order doesn't matter
    mock_svc.process.assert_has_calls(
        [call("a"), call("b")], any_order=True
    )
```

> **⚠️ Danger Zone:** `assert_called_with(args)` only checks the **most recent call**. If called 10 times and you only assert the last call's args, you've verified nothing about the first 9 calls. Use `assert_called_once_with` when you need to guarantee *exactly one* call occurred.

> **Key Takeaway:** `assert_has_calls` is your tool for sequence verification; `assert_any_call` for membership; always pair `assert_called_with` with a `call_count` check when frequency matters.

---

## Module 15: Common Mocking Pitfalls & the MockerNotFound Error

### 📖 Plain English Definition

Mocking pitfalls are the recurring patterns that cause tests to pass when they shouldn't (false positives) or fail for the wrong reasons (brittle tests). The `fixture 'mocker' not found` error is the single most common first-encounter error with pytest-mock, and it has exactly one root cause: `pytest-mock` is not installed in the active environment.

### 🛠️ Ways to Use This

- **Debugging a mock that's not being called:** Check the patch target namespace first — almost always a wrong import path.
- **Fixing brittle tests:** If a test breaks on every refactor, you're mocking implementation details instead of interfaces.
- **Resolving `mocker` not found:** Install `pytest-mock`, check your virtual environment, and ensure you haven't misspelled `mocker`.

### 🎬 Movie Set Analogy

Mocking pitfalls are like **film continuity errors** — the coffee cup that changes hands between cuts, the beard that disappears mid-scene. Most of them go unnoticed until a sharp-eyed audience member (a failing integration test) spots them. The `mocker` not found error is simpler: it's like showing up to a shoot and discovering **the camera crew isn't contracted for this production**. You just need to hire them (`pip install pytest-mock`).

### 💬 The "Why" in Plain Sentences

The most dangerous mocking mistake isn't a crash — it's a silent false positive. Tests that over-mock internal details break on every refactor and give zero signal about real behavior. The second most dangerous is wrong patch targets: your mock never intercepts the real call, the real code runs, and your test passes for entirely the wrong reason. Build the habit of always questioning: "Is my mock *actually* intercepting anything?"

---

### 🔴 Pitfall 1: Mocking Implementation Details

**The Problem:** Mocking internal helper methods creates tests that break when you refactor — even if external behavior is unchanged.

```python
# ❌ BRITTLE: Tests internal implementation, not the public contract
def test_full_name_brittle(mocker):
    user = User()
    mocker.patch.object(user, "get_first_name", return_value="Jane")
    mocker.patch.object(user, "get_last_name", return_value="Smith")
    assert user.get_full_name() == "Jane Smith"   # Breaks if refactored!
```

```python
# ✅ ROBUST: Tests the public contract — doesn't care how it's implemented
def test_full_name_robust():
    user = User()                          # No mocking of internals
    assert user.get_full_name() == "John Doe"  # Tests the observable output
```

---

### 🔴 Pitfall 2: Wrong Patch Target (The #1 Cause of Silent Failures)

```python
# ❌ WRONG: Patches the source module — doesn't affect payment.py's local reference
with patch("requests.post") as mock:
    process_payment(100)   # Real requests.post still called!
```

```python
# ✅ CORRECT: Patches the name as it exists inside the module under test
with patch("payment.requests.post") as mock:
    process_payment(100)   # Mock intercepts the call correctly
```

---

### 🔴 Pitfall 3: Deep / Chained Mocks (Mock Hell)

```python
# ❌ FRAGILE: Chains of mock attributes break on any implementation change
mock_obj.layer1.layer2.layer3.method.return_value = "x"
```

**Fix:** If you need three levels of chained mocks, your code has a dependency injection problem. Refactor to accept the final dependency directly, then mock it at that level.

---

### 🔴 Pitfall 4: The `fixture 'mocker' not found` Error

This error has one root cause and a handful of secondary causes:

**Diagnostic Checklist (in order):**

1. **Install `pytest-mock`:** `pip install pytest-mock` — this is the cause 90% of the time.
2. **Check your environment:** Run `pip list | grep pytest-mock`. If absent, you're in the wrong virtual environment.
3. **Check spelling:** The fixture is `mocker` (not `mock`, not `Mocker`).
4. **Do not import `mocker` explicitly:** It's injected by pytest automatically — no import needed.
5. **Check `pytest.ini` / `pyproject.toml`:** No configuration should be disabling `pytest-mock`.
6. **Check `conftest.py`:** A local fixture named `mocker` in conftest will shadow the plugin's fixture.

```python
# ✅ CORRECT: pytest-mock installed, fixture injected automatically
def test_example(mocker):   # 'mocker' must be the exact parameter name
    mock_fn = mocker.patch("mymodule.my_function")
    # ...
```

---

### 🔴 Pitfall 5: Not Using autospec (Silent Method Drift)

```python
# ❌ DANGEROUS: Plain Mock accepts ANY method name — even deleted ones
mock_svc = Mock()
mock_svc.get_by_email("a@b.com")   # Passes even if method was renamed!
```

```python
# ✅ SAFE: autospec enforces the real class interface
mock_svc = create_autospec(UserService, instance=True)
mock_svc.get_by_email("a@b.com")   # Fails immediately if method doesn't exist
```

> **Key Takeaway:** If a mock isn't being called, check the patch namespace first. If tests break on every refactor, you're mocking implementation details. If you see `fixture 'mocker' not found`, run `pip install pytest-mock`.

---

## Quick Reference Cheat Sheet

```python
# ── INSTALLATION ─────────────────────────────────────────────────
# pip install pytest pytest-mock pytest-asyncio

# ── CREATING MOCKS ───────────────────────────────────────────────
from unittest.mock import Mock, MagicMock, AsyncMock, create_autospec, mock_open

m = Mock()                                  # Blank mock, no dunder methods
m = MagicMock()                             # Mock + all dunder methods (DEFAULT)
m = AsyncMock()                             # Mock for async/await code
m = create_autospec(MyClass, instance=True) # Spec-validated — enforces signatures
m = mock_open(read_data="file content")     # Pre-configured for file I/O

# ── THE MOCKER FIXTURE (pytest-mock) ─────────────────────────────
def test_example(mocker):
    mocker.patch("module.name")                          # Returns MagicMock
    mocker.patch("module.name", return_value=42)         # With return value
    mocker.patch("module.name", new_callable=AsyncMock)  # Specific type
    mocker.patch.object(obj, "method")                   # Patch one method
    mocker.patch.dict(os.environ, {"KEY": "value"})      # Patch dict

# ── CONFIGURING BEHAVIOR ─────────────────────────────────────────
m.method.return_value = 42                  # Always return 42
m.method.side_effect = ValueError("bad")    # Raise this exception instance
m.method.side_effect = ValueError           # Raise exception class
m.method.side_effect = [1, 2, 3]           # Return 1, then 2, then 3
m.method.side_effect = my_function          # Call fn with same args

# ── ASSERTIONS ───────────────────────────────────────────────────
m.method.assert_called()                          # Called ≥ once
m.method.assert_called_once()                     # Called exactly once
m.method.assert_called_with(a, b=c)               # Last call had these args
m.method.assert_called_once_with(a, b=c)          # Only call, these exact args
m.method.assert_any_call(a)                       # Any call had this arg
m.method.assert_not_called()                      # Never called
m.method.assert_has_calls([call(a), call(b)])     # Ordered sequence
m.method.assert_has_calls([...], any_order=True)  # Unordered sequence
m.method.call_count                               # Number of calls (int)
m.method.call_args_list                           # Full call history

# ASYNC-SPECIFIC (AsyncMock)
await_mock.assert_awaited()
await_mock.assert_awaited_once_with(arg)
await_mock.assert_not_awaited()

# RESET
m.reset_mock()  # Clears call history, return_value, side_effect

# ── PATCHING ─────────────────────────────────────────────────────
from unittest.mock import patch

with patch("mymodule.ClassName") as mock:              # Context manager
    ...

@patch("mymodule.ClassName")                           # Decorator
def test(mock): ...

with patch.object(MyClass, "method") as mock: ...      # Specific method
with patch.dict(os.environ, {"KEY": "val"}): ...       # Dict patching
with patch("builtins.open", mock_open(read_data="x")): # File I/O

# DECORATOR STACKING — BOTTOM decorator = FIRST parameter
@patch("mymodule.B")   # → second parameter (mock_b)
@patch("mymodule.A")   # → first parameter (mock_a)
def test(mock_a, mock_b): ...

# ── MONKEYPATCH (pytest fixture) ──────────────────────────────────
def test_example(monkeypatch):
    monkeypatch.setattr(obj, "attr", new_value)     # Replace attribute
    monkeypatch.setattr("module.func", fake_func)   # Replace by path
    monkeypatch.delattr(obj, "attr")                # Remove attribute
    monkeypatch.setenv("VAR", "value")              # Set env var
    monkeypatch.delenv("VAR", raising=False)        # Remove env var
    monkeypatch.setitem(my_dict, "key", "val")      # Set dict item

# ── THE GOLDEN RULES ─────────────────────────────────────────────
# 1. Patch WHERE the name is USED, not where it's defined.
#    ✅ patch("mymodule.requests")   ❌ patch("requests.get")
#
# 2. Use MagicMock by default. Use Mock only when signaling "no magic needed."
#
# 3. Use AsyncMock for anything behind async def or await.
#
# 4. Use autospec=True / create_autospec to catch interface drift.
#
# 5. Use wraps= to spy without replacing real behavior.
#
# 6. Use monkeypatch for env vars and config.
#    Use patch() for service dependencies and external I/O.
#
# 7. Don't mock internals. Test interfaces, not implementation.
#
# 8. When mocks get complex, use a Fake instead.
#
# 9. Use Dependency Injection to make mocking clean and optional.
#
# 10. Always back up unit tests with integration tests.
```

---

*Built for mastery. Every module grounded in real-world sources and battle-tested patterns. Mock confidently. Test fearlessly.*
