# Walkthrough Defense: Comprehensive Q&A System
**Goal:** Prepare you to defend every single line of code, framework choice, and schema design decision during your live walkthrough.

---

## Category 1: Architectural Decisions

### Q1.1: Why did you partition the backend into API, Service, Domain, Clients, and Repositories layers?
*   **Answer:** We used **Layered Clean Architecture**. This pattern isolates our core business logic (the domain rules) from database drivers (`motor`), web frameworks (`FastAPI`), and network packages (`httpx`).
    *   **What it does:** It creates strict boundaries. The API routes only speak HTTP, the Clients handle third-party network calls, the Repository manages database queries, the Service orchestrates the flow, and the Domain only handles calculations.
    *   **Why it was chosen:** It makes testing and future updates simple. For example, if we want to swap MongoDB for PostgreSQL, we only change the `MongoProfileRepository` class. The business logic in `ProfileService` and `aggregation.py` remains completely untouched.
    *   **Alternatives:** A single script or flat file layout. While simpler, mixing HTTP endpoints, database queries, and raw calculations in one place makes it difficult to write mock tests and results in fragile code.

---

### Q1.2: Why did you use Python Protocols instead of abstract base classes (ABCs) for your repository interfaces?
*   **Answer:** Python `Protocol` provides **structural subtyping** (or static duck typing) rather than nominal subtyping.
    *   **What it does:** With a `Protocol` (like `ProfileRepository` in [base.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/repositories/base.py)), any class that implements the methods `find_by_username`, `upsert`, and `ensure_indexes` is automatically considered a profile repository by the type checker.
    *   **Why it was chosen:** It decouples the implementation from the interface. The concrete database repository doesn't need to inherit from the Protocol explicitly; it just implements the signature. This is clean, flexible, and makes mocking in tests straightforward.
    *   **Alternatives:** `abc.ABC` (nominal subtyping). This requires the database class to inherit from the base class (`class MongoProfileRepository(ProfileRepositoryABC)`). This couples the implementation file directly to the base class module.

---

### Q1.3: How does dependency injection work in your backend, and why is it beneficial here?
*   **Answer:** In [profile.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/routes/profile.py#L25-L48), the router function `_build_service` instantiates the `MongoProfileRepository`, `GithubClient`, and `OllamaClient` and injects them into the constructor of `ProfileService`.
    *   **What it does:** Instead of the service instantiating its own database connectors or API clients internally, they are passed as parameters during service creation.
    *   **Why it was chosen:** It makes mock testing easy. In our unit tests, we can instantiate the service and pass a mock database client (`mongomock`) and a mock HTTP transport (`respx`), allowing us to verify service logic without making network calls.
    *   **Alternatives:** Hardcoding client creation inside the service. This would tightly couple the service to active network ports and database connections, making tests slow and flaky.

---

### Q1.4: Why did you build the frontend in Streamlit instead of React or Next.js?
*   **Answer:** Speed of development and visual dashboard integration.
    *   **What it does:** Streamlit executes Python scripts from top to bottom, turning widgets (like text inputs) into variables and automatically rendering layout columns, Plotly charts, and tables.
    *   **Why it was chosen:** The project requires a data dashboard with graphs and statistics. Streamlit includes built-in components for tables, charts, and metrics, allowing us to build a rich frontend in Python without writing HTML, JavaScript, CSS, or build tools.
    *   **Alternatives:** React or Next.js. While React allows for more custom UI logic, it requires building a separate web application, setting up a packaging environment, and writing custom CSS, which is too complex for this project.

---

### Q1.5: Why did you separate backend and frontend into two containers instead of running Streamlit as the entire application?
*   **Answer:** Decoupling of concerns and future-proofing.
    *   **What it does:** The backend container focuses purely on fetching, persisting, caching, and serving profile data via a REST API. The frontend container is a consumer of this API.
    *   **Why it was chosen:** If we decide to build a React web frontend or a mobile app in the future, we don't have to rewrite our database queries or aggregation logic. The backend remains unchanged.
    *   **Alternatives:** Running Streamlit directly against MongoDB and the GitHub API. This would combine presentation logic with data access, making the code harder to scale or reuse.

---

## Category 2: Database Schema & Data Modeling

### Q2.1: Explain your MongoDB document schema. Why is it a single document per developer?
*   **Answer:** A developer profile contains a hierarchical data structure: user profile details, a list of repositories, and aggregated metrics.
    *   **What it does:** All profile data for a developer is saved inside one nested document.
    *   **Why it was chosen:** In MongoDB, this document represents an aggregate root. Because our application always queries and writes the entire profile at the same time, nesting repos inside the profile matches this read/write access pattern. This avoids joins and guarantees atomic updates.
    *   **Alternatives:** Splitting the data into a `users` collection, a `repositories` collection, and an `aggregates` collection. This would require database transactions and multiple round-trips to perform updates.

---

### Q2.2: Why did you use the lowercased username as the `_id` field instead of an auto-generated `ObjectId`?
*   **Answer:** To enforce uniqueness and optimize lookups.
    *   **What it does:** We override MongoDB's default `ObjectId` with the lowercase username (e.g. `_id: "octocat"`).
    *   **Why it was chosen:** Username is a natural key on GitHub—it is unique and case-insensitive. By using it as the primary key (`_id`), we automatically get a unique index on the username and can run lookups directly on the primary index without needing a secondary index query.
    *   **Alternatives:** Using `ObjectId` as `_id` and setting a secondary unique index on `username`. This would require maintaining two indexes and double index lookups on queries.

---

### Q2.3: How does the schema handle the 16MB BSON document limit in MongoDB?
*   **Answer:** With protective limits.
    *   **What it does:** In [profile_service.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/services/profile_service.py#L25), we define a `MAX_REPOS_STORED = 2000` limit. If a user has more than 2,000 repositories, we sort by stars and keep only the top 2,000.
    *   **Why it was chosen:** A single repository record in our schema takes about 500 bytes. At 2,000 repositories, the list takes about 1MB, which is well below the 16MB document limit. This prevents the database from failing on users with extremely large profiles.
    *   **Alternatives:** Storing repositories in a separate collection. This would allow an infinite number of repositories but would complicate our caching and refresh operations.

---

### Q2.4: Why do you store the `aggregated_profile` in the database instead of computing it dynamically on reads?
*   **Answer:** To optimize query speeds and reduce CPU usage.
    *   **What it does:** Aggregation math is performed during the fetch/write phase, and the result is saved under the `aggregated_profile` field.
    *   **Why it was chosen:** Profiles are read frequently but only updated when refreshed. By calculating metrics once on write, we reduce CPU usage during reads.
    *   **Alternatives:** Computing statistics dynamically on the backend during the `GET` request. While this guarantees up-to-date calculations, it would run the aggregation loop on every request, wasting CPU cycles.

---

### Q2.5: Why did you include a `schema_version` field in the database model?
*   **Answer:** To support future database migrations.
    *   **What it does:** It stores an integer (currently `1`) identifying the document structure version.
    *   **Why it was chosen:** As the application grows, we might rename fields or change calculations. Having a version number allows us to write migration scripts that only target older document formats.
    *   **Alternatives:** Omitting the version field. This would make it difficult to run migrations without scanning and guessing document structures.

---

## Category 3: Core Algorithms & AI Prompt Engineering

### Q3.1: Explain your aggregation math. How do you calculate language breakdown percentages?
*   **Answer:** In [aggregation.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/aggregation.py#L26-L40), we use a `Counter` to sum language byte counts across all repositories.
    *   **What it does:** We sum the bytes for each language and divide it by the total byte size across all languages:
        $$\text{Percentage} = \text{round}\left( \frac{\text{Bytes for Language } X}{\text{Total Bytes}} \times 100, 1 \right)$$
    *   **Why it was chosen:** It provides an accurate representation of a developer's codebase compared to simply counting primary repository languages.
    *   **Alternatives:** Counting the primary language of each repository. This is less accurate because a large Python repository with a tiny shell script would count python and shell equally.

---

### Q3.2: How do you identify a developer's "most active month"?
*   **Answer:** We count the number of repository push events per month.
    *   **What it does:** In [aggregation.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/aggregation.py#L59-L78), we parse the `pushed_at` timestamp from each repository, format it as `YYYY-MM`, count the occurrences, and find the month with the highest count.
    *   **Why it was chosen:** It is a reliable proxy for activity that only requires repository-level metadata.
    *   **Alternatives:** Fetching commit histories for every repository. While more accurate, this would require querying thousands of commits, which would exceed the GitHub API rate limit.

---

### Q3.3: Why do you format the Ollama LLM prompt input as a CSV instead of JSON?
*   **Answer:** To reduce token counts and improve local model execution speeds.
    *   **What it does:** In [profile_csv.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/profile_csv.py), we compile statistics and repository tables into structured CSV text.
    *   **Why it was chosen:** CSV uses fewer characters than JSON. It omits repeated keys, curly braces, and brackets, reducing token footprint and saving GPU/CPU memory on local models.
    *   **Alternatives:** Feeding raw JSON arrays directly to the LLM. This increases prompt sizes, leading to slower inference times on local systems.

---

### Q3.4: What are "Persona Hints" and why are they compiled into the LLM prompt?
*   **Answer:** They are rule-based tags calculated on the backend to guide the LLM.
    *   **What it does:** In [persona_rules.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/persona_rules.py), we analyze user statistics and append tags (like `polyglot` or `superstar`) to the prompt context.
    *   **Why it's useful:** Local 7B models can struggle to follow complex reasoning rules. Providing these pre-calculated tags guides the model, ensuring it generates high-quality developer summaries.
    *   **Alternatives:** Asking the model to figure out these metrics from raw data, which often results in inconsistent outputs from smaller models.

---

## Category 4: Edge Cases & Error Resilience

### Q4.1: How does the application handle GitHub API rate limits?
*   **Answer:** Proactively, by inspecting response headers.
    *   **What it does:** During HTTP calls, we inspect `X-RateLimit-Remaining`. If it is `0`, we raise `RateLimitExceededError` before making more calls.
    *   **Why it was chosen:** It prevents the app from making requests that are guaranteed to fail and provides a clear recovery message showing when the rate limit resets.
    *   **Alternatives:** Catching `403` status codes after a request has failed. This is less proactive and can result in partial data writes.

---

### Q4.2: How does the system handle a user with zero public repositories?
*   **Answer:** By verifying lists before performing calculations.
    *   **What it does:** In `aggregation.py`, the code checks if the repository list is empty and returns default values (e.g. `total_repos = 0`, `most_used_language = None`, `top_topics = []`).
    *   **Why it was chosen:** It prevents division by zero errors during calculations, allowing the backend to save a clean profile document in MongoDB.
    *   **Alternatives:** Crashing the request or returning an error message. A user with no public repositories is a valid GitHub account, so the app should display their profile correctly.

---

### Q4.3: What happens if Ollama is offline or slow during a refresh request?
*   **Answer:** Non-fatal fallback execution.
    *   **What it does:** In [profile_service.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/services/profile_service.py#L183-L228), calls to the Ollama client are wrapped in a `try/except` block. If it times out or fails, we assign `ai_summary = null` and continue.
    *   **Why it was chosen:** Generating summaries is an optional feature. The core profile lookup and cache flow should continue to work even if the LLM container is unavailable.
    *   **Alternatives:** Crashing the profile fetch request, which would make the entire application fail when the LLM service is offline.

---

### Q4.4: What happens if a language fetch call fails for a single repository?
*   **Answer:** Graceful degradation.
    *   **What it does:** If the request to `/repos/{owner}/{repo}/languages` fails, the client logs a warning, returns an empty dictionary, and falls back to the repository's primary language.
    *   **Why it was chosen:** It ensures that a minor error on a single repository does not fail the entire profile query.
    *   **Alternatives:** Crashing the entire request, which would make the user lookup fail if any repository returns a temporary API error.

---

## Category 5: Production Scaling & Future Refactoring

### Q5.1: If this project were deployed to production with thousands of users, how would you resolve the N+1 language fetching bottleneck?
*   **Answer:** We would migrate to the **GitHub GraphQL API v4**.
    *   **What it does:** Instead of fetching the repository list and making separate language requests for each repository (N+1 queries), we can fetch all repositories and their language details in a single GraphQL query.
    *   **Why it's useful:** It reduces network latency, minimizes resource usage, and helps prevent rate-limiting.
    *   **Alternatives:** Running language requests in parallel using thread pools. This would speed up requests but would still use the same number of API calls, increasing the risk of hitting rate limits.

---

### Q5.2: How would you scale the LLM summary feature in a production environment?
*   **Answer:** We would offload Ollama calls to background tasks.
    *   **What it does:** Instead of generating summaries inside the request thread, the backend would use a message queue (like Celery) to run these tasks in the background. The API would return the profile data immediately, and the frontend would poll for the summary.
    *   **Why it's useful:** It prevents slow LLM inference times from blocking user requests.
    *   **Alternatives:** Increasing client timeouts, which causes slow page load times and blocks web server threads.
