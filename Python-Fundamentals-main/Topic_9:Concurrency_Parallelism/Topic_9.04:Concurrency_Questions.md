# Phase 09 — Concurrency and Parallelism (Interview Q&A)

### Q1: You are designing a data ingestion pipeline. One part of the application makes thousands of API calls over the network, while another part performs heavy image processing. How do you choose between Threading, Multiprocessing, and Asyncio for these tasks?
**Expected Answer:**
The choice depends entirely on whether the bottleneck is **I/O-bound** or **CPU-bound**, and the overhead of context switching.
*   **For the API calls (I/O-bound):** I would choose **Asyncio** (if the libraries I am using are asynchronous, like `aiohttp` or `httpx`). Asyncio uses cooperative multitasking running on a single thread. It scales effortlessly to tens of thousands of concurrent connections because it doesn't incur the memory overhead of OS thread context switching. If I must use synchronous libraries (like `requests`), I would use **Threading** (via `ThreadPoolExecutor`), since the OS will swap threads while waiting for network sockets to respond.
*   **For the image processing (CPU-bound):** I must use **Multiprocessing** (via `ProcessPoolExecutor`). Because of Python's Global Interpreter Lock (GIL), multiple threads cannot execute Python bytecodes simultaneously. Multiprocessing spawns entirely separate OS processes, each with its own memory space and its own GIL, allowing true parallel execution across multiple CPU cores.

### Q2: What exactly is the Global Interpreter Lock (GIL), why did Python's creators include it, and how does it impact Threading?
**Expected Answer:**
The GIL is a C-level mutex (lock) in CPython that allows only one OS thread to execute Python bytecode at a time. 
*   **Why it exists:** CPython's memory management relies heavily on **Reference Counting**. If multiple threads incremented and decremented object reference counts concurrently, it would cause race conditions leading to memory leaks or Segfaults. The GIL protects the internal state of CPython by making reference counting thread-safe without needing to wrap every single variable in its own lock (which would make single-threaded Python excruciatingly slow).
*   **Impact on Threading:** Because of the GIL, multithreading in Python does *not* result in parallel CPU execution. Threads run concurrently, not in parallel. However, the GIL is automatically released during I/O operations (like `time.sleep()`, socket reads, or file writes) and inside many C extensions (like `NumPy` matrix multiplications), which is why Threading is still highly effective for I/O-bound tasks.

### Q3: A junior developer writes an `async def` function, but puts `import time; time.sleep(5)` or `requests.get('url')` inside it. What happens to the application, and how do you fix it?
**Expected Answer:**
This is a fatal error in asynchronous programming known as **"blocking the event loop."** 
Because Asyncio runs on a single thread, calling a blocking synchronous function (like `time.sleep()` or `requests.get()`) halts the entire thread. The event loop cannot process any other tasks, meaning all other concurrent users or websocket connections will freeze for those 5 seconds.
*   **How to fix it:** If I cannot rewrite the code to use an async-native library (like `asyncio.sleep()` or `aiohttp`), I must offload the blocking call to a separate thread so the event loop can keep spinning. I would use `loop.run_in_executor(None, requests.get, 'url')` or in modern Python (3.9+), `asyncio.to_thread(requests.get, 'url')`. This wraps the blocking call in a Future and executes it in a background thread pool.

### Q4: Explain what a Race Condition is in the context of Python threading. How do you prevent it? Give a specific example involving a shared counter.
**Expected Answer:**
A race condition occurs when two or more threads access shared data concurrently, and the final state depends on the unpredictable order in which the OS scheduler executed the threads.
*   **Example:** Imagine a global variable `counter = 0`. Thread A and Thread B both execute `counter += 1`. In bytecode, `+= 1` is three steps: 1) Load `counter`, 2) Add `1`, 3) Store `counter`. If the OS context switches from Thread A to Thread B right after Thread A loads `0`, Thread B also loads `0`, increments to `1`, and stores `1`. Thread A wakes up, finishes its addition (0+1=1), and stores `1`. We expected `2`, but got `1`.
*   **Prevention:** I would use **Synchronization Primitives**, specifically a `threading.Lock()` (Mutex). Before incrementing, the thread must acquire the lock (`with lock: counter += 1`). This makes the read-modify-write operation **atomic**, forcing other threads to wait until the lock is released.

### Q5: What is a Deadlock? How can it happen, and what architectural strategies do you use to prevent them in heavily multithreaded code?
**Expected Answer:**
A deadlock occurs when two or more threads are blocked indefinitely, each waiting for a lock that the other thread is currently holding. (E.g., Thread A holds Lock 1 and waits for Lock 2. Thread B holds Lock 2 and waits for Lock 1).
**Strategies to prevent deadlocks:**
1.  **Strict Lock Ordering:** Architect the system so that whenever a thread needs multiple locks, it must acquire them in a globally agreed-upon order (e.g., always acquire Lock A before Lock B).
2.  **Timeouts:** Use `lock.acquire(timeout=5)`. If the thread cannot get the lock in 5 seconds, it catches the failure, releases all its currently held locks, backs off, and retries. This breaks the deadlock cycle.
3.  **Avoid Nested Locks:** Minimize the surface area of locked code. Keep critical sections as tiny as possible and avoid calling external or unknown functions while holding a lock.

### Q6: Under the hood, how does the Asyncio Event Loop actually work? How does it know when a network response is ready?
**Expected Answer:**
The Asyncio event loop is essentially an infinite `while` loop that relies on the OS-level I/O multiplexing API—specifically `epoll()` on Linux or `kqueue()` on macOS (exposed via Python's `selectors` module).
When an async task makes a network request (e.g., reading a socket), it registers the file descriptor (socket) with the event loop and yields control back to the loop via `await` (using Python generators/coroutines). 
The event loop then calls `epoll_wait()`, asking the Operating System: *"Which of these thousands of sockets has data ready to be read?"* The OS wakes up the event loop and hands it a list of ready sockets. The event loop then resumes the specific coroutines (Tasks) associated with those sockets.

### Q7: You are trying to pass large Python objects (like huge Pandas DataFrames) between processes using `multiprocessing.Queue`. It is incredibly slow and sometimes crashes with a `PicklingError`. Why? How do you fix it?
**Expected Answer:**
Unlike threads, separate processes do not share memory. When you put an object into a `multiprocessing.Queue`, Python must serialize the object into bytes using the `pickle` module, send those bytes across an Inter-Process Communication (IPC) pipe, and deserialize (unpickle) it in the other process. This serialization/deserialization CPU overhead is massive and negates the benefits of parallel processing. Furthermore, not all objects (like open file handles or DB connections) can be pickled.
*   **How to fix it:**
    1.  **Shared Memory:** Use `multiprocessing.shared_memory` (introduced in Python 3.8). This allocates a block of RAM that all processes can read/write to directly, bypassing IPC pickling completely.
    2.  **Granular Passing:** Instead of passing a 10GB DataFrame through a queue, save it to disk (e.g., a Parquet file) or a Redis instance, and just pass the file path or Redis key through the Queue.

### Q8: What is the difference between `concurrent.futures.Future` and `asyncio.Future` (or `Task`)?
**Expected Answer:**
Both represent the eventual result of an asynchronous operation, but they belong to different execution models.
*   **`concurrent.futures.Future`:** Used in multithreading/multiprocessing (e.g., `ThreadPoolExecutor`). It is tied to OS-level threads. Calling `future.result()` is a **blocking** operation; it will freeze the current thread until the background thread completes.
*   **`asyncio.Future` (and `asyncio.Task`):** Used in the cooperative asyncio event loop. Calling `await future` is **non-blocking**; it yields control back to the event loop, allowing other tasks to run until this future is resolved. (Note: A `Task` is simply a subclass of `Future` that wraps a coroutine).

### Q9: What is the difference between a `Lock`, an `RLock`, an `Event`, and a `Condition` in the `threading` module?
**Expected Answer:**
These are all synchronization primitives:
*   **`Lock`:** A standard mutual exclusion lock. If a thread acquires it, and tries to acquire it *again* before releasing it, it will deadlock itself.
*   **`RLock` (Reentrant Lock):** A lock that can be acquired multiple times by the *same* thread without blocking. The thread must release it the exact same number of times before another thread can acquire it. Highly useful for recursive functions.
*   **`Event`:** A boolean flag used for communication. Thread A calls `event.wait()` and blocks. Thread B does some work and calls `event.set()`, instantly waking up Thread A (and any other threads waiting on that event).
*   **`Condition`:** Combines a Lock and an Event. It allows threads to wait until a specific state is achieved. A thread acquires the condition lock, checks a shared state, and if it's not ready, calls `condition.wait()` (which releases the lock and goes to sleep). Another thread changes the state and calls `condition.notify()`, waking up the waiting thread.

### Q10: You have an `asyncio` application with a background task running an infinite loop (e.g., pinging a health-check endpoint). The application needs to shut down gracefully. How do you properly cancel this task without leaving corrupted state?
**Expected Answer:**
You cancel the task using `task.cancel()`. However, this does not aggressively kill the task like a Unix `SIGKILL`. 
Instead, it throws an `asyncio.CancelledError` *inside* the coroutine at the exact line where it is currently `await`ing. 
To shut down gracefully, the coroutine must be designed to handle this. I would wrap the background logic in a `try/except asyncio.CancelledError:` block, or more commonly, a `try/finally:` block. Inside the `finally` block, I put the cleanup code (e.g., closing database connections or open network sessions). This ensures that even when the event loop forcefully cancels the task, resources are properly released.

---

### Q11: You need to scrape 10,000 URLs asynchronously, but the target server will block your IP if you exceed 50 concurrent requests. How do you implement rate limiting in Asyncio?
**Expected Answer:**
I would use `asyncio.Semaphore(50)`. 
A Semaphore is an internal counter. When a task calls `async with semaphore:`, the counter decrements. If the counter hits 0, any subsequent tasks will automatically pause (suspend execution) until one of the running tasks finishes and releases the semaphore. This guarantees that exactly 50 connections are actively making requests at any given time, preventing IP bans without needing complex manual queues.

### Q12: Explain how you would implement a robust Producer-Consumer architecture using Asyncio. How do you safely signal to the consumer that there is no more work to do?
**Expected Answer:**
I would use an `asyncio.Queue`. 
The Producer generates items and puts them into the queue (`await queue.put(item)`). The Consumer runs in an infinite loop, pulling items off the queue (`item = await queue.get()`), processing them, and then explicitly calling `queue.task_done()` to indicate completion.
To signal the end of work, I would use a **Sentinel Value** (e.g., `None`). The Producer puts `None` into the queue when it finishes. When the Consumer retrieves `None`, it breaks out of its infinite loop and terminates cleanly. Finally, the main function uses `await queue.join()` to block until every item in the queue has been fully processed.

### Q13: You have 5 independent API calls to make asynchronously. What is the difference between `asyncio.gather()` and `asyncio.wait()`, and when would you use which?
**Expected Answer:**
*   **`asyncio.gather(*tasks)`:** I use this when I care about the *results in order*. It runs everything concurrently and returns a list of results exactly matching the order of the tasks I passed in. By default, if one task raises an exception, `gather` throws the exception immediately (unless `return_exceptions=True` is set).
*   **`asyncio.wait(tasks)`:** I use this when I care about the *state of execution* rather than strict ordering. It returns two sets: `done` and `pending`. It is highly powerful because it accepts a `return_when` parameter (e.g., `FIRST_COMPLETED`, `FIRST_EXCEPTION`, or `ALL_COMPLETED`), making it perfect for scenarios where I need to implement a timeout or just want the fastest API response out of multiple redundant calls.

### Q14: You are using `multiprocessing.Pool.map()` to process a list of 1,000,000 items. It executes, but the execution time is slow and system RAM usage skyrockets. What parameter can you tweak to optimize this?
**Expected Answer:**
I would tweak the `chunksize` parameter.
By default (or if configured poorly), the multiprocessing pool might send one item at a time to the worker processes. For 1,000,000 items, this results in 1,000,000 Inter-Process Communication (IPC) calls, pickling and unpickling data back and forth, which dominates the CPU time. By setting a higher `chunksize` (e.g., 10,000), the parent process batches 10,000 items together, sends them in a single IPC transaction to a worker, and the worker processes them all before communicating back. This drastically reduces IPC overhead and memory fragmentation.

### Q15: You are building an Asyncio web framework and need to track a unique `request_id` for logging across dozens of nested coroutines. Why can't you use `threading.local()`, and what is the correct alternative?
**Expected Answer:**
`threading.local()` attaches data to the current OS thread. Because `asyncio` runs hundreds or thousands of concurrent tasks cooperatively on a *single* thread, if Task A sets a `request_id` in `threading.local()`, Task B will read Task A's ID when the event loop switches context.
The correct alternative is the **`contextvars`** module (specifically `ContextVar`). It natively supports asyncio. When a context variable is set, it is scoped to the *current logical async task*. Even if the event loop switches back and forth between Task A and Task B on the same thread, `contextvars` ensures each task only sees its own isolated state.

### Q16: What is a Daemon Thread in Python? What happens if your main program finishes, but a Daemon Thread is still halfway through writing to a database?
**Expected Answer:**
A Daemon thread (created via `threading.Thread(daemon=True)`) is a background thread that runs continuously. Its defining characteristic is that **it does not prevent the Python program from exiting.** When the main thread completes, the OS forcefully terminates all active daemon threads immediately.
If a daemon thread is halfway through writing to a database or file, it will be brutally killed mid-write, leading to corrupted data or locked database rows. Because of this, daemon threads should only be used for stateless, non-critical background tasks (like pinging a telemetry endpoint or a heartbeat). For critical operations, use non-daemon threads and implement an `Event` to signal graceful shutdown.

### Q17: When using `ThreadPoolExecutor`, what is the architectural difference between using `.map()` vs `.submit()` combined with `as_completed()`?
**Expected Answer:**
*   **`executor.map(func, iter)`:** This applies the function to the iterable concurrently, but it yields the results **in the exact order of the original iterable**. Even if the 10th item finishes in 1 second, but the 1st item takes 10 seconds, your code will block for 10 seconds waiting to return the 1st item before it lets you see the 10th.
*   **`executor.submit()` + `as_completed()`:** `submit()` returns a `Future` immediately. If you pass a list of these Futures into `concurrent.futures.as_completed()`, it yields results **as soon as they finish**, regardless of the order they were submitted. This is superior for streaming data to a user or moving fast tasks down the pipeline while slow tasks are still computing.

### Q18: What are "Subinterpreters" (Per-Interpreter GILs) introduced in Python 3.12 (PEP 684), and how will they change the Python concurrency landscape?
**Expected Answer:**
Historically, to bypass the GIL and use multiple CPU cores, you had to use Multiprocessing, which incurs heavy IPC overhead because separate OS processes do not share memory easily. 
PEP 684 introduces the ability to spawn multiple Python interpreters within a **single OS process**. Crucially, each subinterpreter now gets its **own GIL**. 
This is a game-changer because it allows true parallel execution on multiple CPU cores inside a single process. It bridges the gap between threading (low overhead but no CPU parallelism) and multiprocessing (CPU parallelism but massive IPC overhead), allowing for extremely fast, parallel Python code that can share memory more efficiently at the C-level.