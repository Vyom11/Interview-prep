# Technical Walkthrough & Interview Preparation Guide
**Project:** GitHub Developer Profile Analyser  
**Audience:** Candidate for live technical walkthrough with a Senior AI/ML Engineer  
**Document Goal:** Prepare you to explain, defend, and justify every single design, algorithm, and architectural decision in the codebase.

---

## 1. System Architecture Deep Dive

The project follows a **Layered Clean Architecture** style, separating pure business logic from external frameworks, databases, and APIs. This makes the codebase highly testable and modular.

### High-Level Architecture Diagram
```
┌────────────────────────────────────────────────────────┐
│                        BROWSER                         │
│             Streamlit Web Application UI               │
│                     (Port 8501)                        │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP (REST + JSON)
                           ▼
┌────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                     │
│                      (Port 8000)                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │                    API Layer                     │  │ (routes, schemas, middleware)
│  ├──────────────────────────────────────────────────┤  │
│  │                  Service Layer                   │  │ (fetch-or-cache orchestrator)
│  ├──────────────────────────────────────────────────┤  │
│  │                Aggregation Engine                │  │ (pure business logic - NO I/O)
│  ├──────────────────────────────────────────────────┤  │
│  │                 Repository Layer                 │  │ (database interface/base class)
│  └──────────────────────────────────────────────────┘  │
└───────┬───────────────────┬───────────────────┬────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  GitHub API  │    │   MongoDB    │    │  Ollama API  │
│  (External)  │    │ (Container)  │    │  (Container) │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Component Breakdown
1. **Frontend (Streamlit):** Located in `frontend/`. It renders inputs, visualizes data via Plotly, and maps actions (like lookup or refresh) to HTTP calls.
2. **API Layer (`src/api/`):** Exposes HTTP endpoints (`/profiles/{username}`, `/profiles/{username}/refresh`, `/health`). Wires request correlation middleware and maps domain exceptions to HTTP statuses.
3. **Service Layer (`src/services/`):** Wires the core logic. Orchestrates the flow: check cache $\rightarrow$ if missing, fetch from GitHub $\rightarrow$ aggregate statistics $\rightarrow$ generate AI personas/summary $\rightarrow$ save in MongoDB $\rightarrow$ return.
4. **Aggregation Engine (`src/domain/aggregation.py`):** Pure python functions that perform math (e.g. calculate language percentages and push frequencies) with no knowledge of databases or HTTP clients.
5. **Persistence Layer (`src/repositories/`):** Interacts with MongoDB using `motor` (an async MongoDB library).
6. **Clients (`src/clients/`):** Connects to external services (GitHub HTTP REST v3 and local Ollama server).

---

## 2. Requirement Coverage Map

This table maps every project requirement to its implementation in the codebase so you can easily reference them during the walkthrough.

| Requirement ID | Description | Code / Module Implementation | How it works |
|---|---|---|---|
| **FR-1** | User enters GitHub username in UI | [frontend/app.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/frontend/app.py#L50-L56) | Renders a standard Streamlit form input and submit button. |
| **FR-2** | Validate username exists | [src/clients/github_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/github_client.py#L26-L51) | Backend runs username regex validation and triggers a fetch. If GitHub returns a `404 Not Found`, the backend throws `UserNotFoundError`. |
| **FR-3** | Fetch user profile metadata | [src/clients/github_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/github_client.py#L154-L168) | Calls `/users/{username}` endpoint and extracts the user's public metadata (followers, location, avatar, etc.). |
| **FR-4** | Fetch and paginate all public repos | [src/clients/github_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/github_client.py#L208-L236) | Calls `/users/{username}/repos` paginating through pages (100 items per page) until an empty array is received. |
| **FR-5** | Capture specific repository fields | [src/clients/github_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/github_client.py#L170-L191) | Maps repository attributes into a strict, validated domain `Repository` dataclass. |
| **FR-6** | Aggregate repository statistics | [src/domain/aggregation.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/aggregation.py#L88-L120) | Takes raw data and aggregates byte counts, topics, monthly activity, account age, and description-less repository stats. |
| **FR-7** | Single MongoDB document per user | [src/repositories/profile_repository.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/repositories/profile_repository.py#L50-L66) | Performs a MongoDB `replace_one` command with `upsert=True` using the username as the primary key (`_id`). |
| **FR-8** | Cached lookup first | [src/services/profile_service.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/services/profile_service.py#L77-L86) | Checks the database repository first. If it finds a record, it returns it instantly, avoiding API calls. |
| **FR-9** | Explicit "Refresh" action | [frontend/app.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/frontend/app.py#L78-L87) | Streamlit button maps to `/refresh` which invokes the service with `refresh=True`, bypassing cache lookup. |
| **FR-10**| Return 404 on missing user | [src/api/middleware/error_handler.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/middleware/error_handler.py) | Catches `UserNotFoundError` in the request pipeline and yields a clean `404` status with JSON error. |
| **FR-11**| Gracefully handle zero public repos | [src/domain/aggregation.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/tests/unit/domain/test_aggregation.py#L59-L73) | Math operations return neutral values (e.g. `0`, `{}`, `None`) and are fully validated by unit tests. |
| **FR-12**| Detect API rate limits | [src/clients/github_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/github_client.py#L92-L110) | Inspects the HTTP headers (`X-RateLimit-Remaining`). If `0`, throws `RateLimitExceededError` before blocking. |
| **FR-13**| Generate natural-language summary | [src/clients/ollama_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/ollama_client.py#L88-L105) | Converts aggregated metrics into a compact CSV and sends it to local Ollama requesting a summary. |
| **FR-14**| Save summary in MongoDB and show in UI | [src/services/profile_service.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/services/profile_service.py#L164-L174) | Saves the LLM summary response under `ai_summary` in the document, rendered via [ai_summary.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/frontend/components/ai_summary.py). |
| **FR-15**| Render stats, details, and tables | [frontend/app.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/frontend/app.py#L89-L94) | Wires individual UI modules for the profile header, metric badges, charts, and repository lists. |

---

## 3. Implementation Decisions & Justifications

During your interview, you must justify *why* you chose specific technologies and patterns instead of alternatives. Use the structured format below to defend your design.

### Decision 1: FastAPI for the Backend
* **What does it do?** It provides a high-performance, asynchronous web server framework with automatic Pydantic request/response validation.
* **Why was it chosen?** It supports asynchronous Python execution out of the box. Since this application performs multiple I/O calls (querying MongoDB, paginating the GitHub API, calling Ollama), an async backend allows it to handle concurrent tasks without blocking the main event thread.
* **What alternatives were available?** 
  * *Flask:* A lightweight synchronous micro-framework.
  * *Django:* A full-featured synchronous web framework with its own built-in ORM.
* **Why are those alternatives better or worse?** Flask and Django are synchronous by default. Handling multiple concurrent, slow HTTP requests to external APIs would require multithreading or run-in-executor loops. This is complex and resource-intensive compared to FastAPI's native async event handling.

### Decision 2: MongoDB as the Database
* **What does it do?** It acts as a document database storing each developer's raw profile metadata, repository configurations, aggregated calculations, and AI insights in a single document.
* **Why was it chosen?** A developer profile is highly hierarchical (a user profile contains a list of repositories, each containing language lists and topic arrays). Storing this as a single nested document matches the application's access pattern: we always write and read the *entire* profile together.
* **What alternatives were available?** 
  * *PostgreSQL (Relational):* Structured relational database.
  * *Redis (Key-Value):* Fast, in-memory storage.
* **Why are those alternatives better or worse?** 
  * In *PostgreSQL*, this schema would require three tables (`users`, `repositories`, `languages`) joined together on every lookup. Since profile refreshes replace the entire data tree, we would have to delete child tables and write many individual insert statements, introducing transactional complexity.
  * In *Redis*, while lookups would be fast, documents could exceed Redis memory configurations on large profiles, and Redis lacks rich native query capabilities for analytics or fields indexing should the application scale.

### Decision 3: Streamlit for the Frontend
* **What does it do?** It serves as the user-facing web dashboard displaying metrics, Plotly charts, and tables.
* **Why was it chosen?** It allows us to build complex, responsive, data-rich layouts entirely in Python. We do not need to build a separate JavaScript SPA (Single Page Application) frontend, enabling rapid prototyping of dashboards, data visualization, and forms.
* **What alternatives were available?**
  * *React.js / Next.js:* Node-based modern JavaScript frameworks.
  * *Dash:* A Python framework by Plotly for analytics.
* **Why are those alternatives better or worse?**
  * *React / Next.js* would require setting up state management, writing custom API clients, maintaining a compilation environment, and writing CSS. Streamlit achieves standard dashboards in under 100 lines of Python.
  * *Dash* has a steeper learning curve and a more complex callback layout, whereas Streamlit's top-down execution flow makes it easier to write and maintain for internal utility tools.

### Decision 4: Local Ollama & Mistral 7B
* **What does it do?** It executes a local 7B-parameter Large Language Model (LLM) inside a Docker container to generate developer summaries and fun personas.
* **Why was it chosen?** It keeps the application fully self-contained. It requires no external API keys (like OpenAI), incurs no usage costs, and runs completely locally.
* **What alternatives were available?**
  * *OpenAI GPT-4o API:* Cloud-hosted LLM endpoint.
  * *HuggingFace Transformers:* Loading model weights directly in Python.
* **Why are those alternatives better or worse?**
  * *OpenAI API* requires internet access, an active API key, and billing setup. If you do not have a paid token, the app would fail.
  * *HuggingFace Transformers* would require loading model weights directly inside the FastAPI memory heap, which increases startup times, introduces heavy GPU dependencies, and blocks backend request execution. Ollama runs as a decoupled service, keeping the backend lightweight.

---

## 4. Core Algorithms and Logic

### 1. The Fetch-and-Persist Pipeline
The primary workflow follows this sequence:
```
User Lookup ──► Check MongoDB ──► (Hit) ──► Return JSON Response
                    │
                 (Miss)
                    ▼
           Fetch User Metadata (GitHub API)
                    │
           Fetch Repos (Paginated Loop)
                    │
      ┌──── Loop: Get Language Byte Breakdown per Repo
      ▼
           Run Aggregation Engine (Pure Math Calculations)
                    │
           Derive Persona Hints & Generate Profile CSV
                    │
           Invoke Ollama (AI Summary & Personas)
                    │
           Upsert (replace_one) to MongoDB
                    │
           Return Fresh JSON Response
```

### 2. Aggregation Engine Calculations
* **Language percentage breakdown:** Sums language byte sizes across all repositories and computes percentages:
  $$\text{Language \%} = \left( \frac{\text{Bytes of Language } X}{\text{Total Bytes of All Languages}} \right) \times 100$$
* **Time Complexity:** $\mathcal{O}(R \times L)$ where $R$ is the number of repositories and $L$ is the average number of languages per repository. Because we fetch data beforehand and process it in memory, this runs in milliseconds.
* **Space Complexity:** $\mathcal{O}(L_{\text{total}})$ where $L_{\text{total}}$ is the total number of unique languages, which is extremely small (typically $<30$).

---

## 5. Database Schema & Data Flow

MongoDB stores each developer profile as a single document in the `profiles` collection. Below is the schema structure.

```json
{
  "_id": "octocat", // Lowercased username (enforces uniqueness)
  "username": "octocat",
  "github_user": {
    "id": 583231,
    "name": "The Octocat",
    "bio": "Developer advocate",
    "avatar_url": "https://...",
    "followers": 12345,
    "following": 9,
    "public_repos": 8,
    "created_at": "2011-01-25T18:44:36Z",
    "location": "San Francisco",
    "blog": "https://github.blog"
  },
  "repositories": [
    {
      "name": "Hello-World",
      "description": "My first repository",
      "primary_language": "Python",
      "languages": { "Python": 12345, "Shell": 234 },
      "topics": ["example", "tutorial"],
      "stars": 120,
      "forks": 30,
      "watchers": 120,
      "open_issues": 2,
      "is_fork": false,
      "is_archived": false,
      "license": "MIT",
      "created_at": "2011-01-26T19:01:12Z",
      "pushed_at": "2020-05-14T10:00:00Z",
      "size_kb": 108
    }
  ],
  "aggregated_profile": {
    "total_repos": 8,
    "total_stars": 450,
    "total_forks": 88,
    "language_breakdown": { "Python": 61.2, "JavaScript": 25.4, "Shell": 13.4 },
    "most_used_language": "Python",
    "top_topics": ["tutorial", "api"],
    "most_active_month": "2020-05",
    "activity_by_month": { "2020-05": 6, "2020-06": 2 },
    "account_age_years": 15.4,
    "repos_with_no_description_pct": 12.5,
    "archived_repos_count": 1,
    "fork_repos_count": 2
  },
  "ai_summary": "Octocat is a versatile developer...",
  "developer_personas": ["Code Nomad", "Star Magnet"],
  "last_fetched_at": "2026-07-09T12:00:00Z",
  "schema_version": 1
}
```

### Schema Design Decisions
1. **Uniqueness:** The document uses `_id: username.lower()` rather than MongoDB's default `ObjectId`. GitHub usernames are unique and case-insensitive. By mapping the lowercase username to `_id`, we let MongoDB enforce username uniqueness at the database level and index lookups instantly without requiring secondary index scans.
2. **Pre-aggregation:** The `aggregated_profile` subdocument is calculated once on write, rather than recalculated every time the user loads the page. This shifts CPU-intensive work to the fetch stage and keeps reads very fast.

---

## 6. Edge Cases & Robust Error Handling

| Edge Case Scenario | Impact | How the Code Manages It |
|---|---|---|
| **Non-existent user** | Backend crashes or returns empty data | `GithubClient` raises `UserNotFoundError` when it gets an HTTP 404 from GitHub. The error handler middleware catches this and returns a clean HTTP 404 JSON response. |
| **GitHub rate limit reached** | Fetches fail with incomplete data | The client inspects the HTTP headers (`X-RateLimit-Remaining`). If it is `0`, the client raises `RateLimitExceededError`. The API middleware catches this and returns a clear `429 Too Many Requests` error, indicating when the limit resets. |
| **User with zero public repositories** | Division by zero or Null errors | Math aggregations check if lists are empty (e.g., `if not repositories: return 0.0`). The system still creates, persists, and displays the profile, showing neutral or empty states in the UI instead of crashing. |
| **Ollama container is down or starting up** | Profile lookup crashes | Caught inside the service layer. A warning is logged, `ai_summary` and `developer_personas` are set to `null`, and the response is returned. The app remains fully functional. |
| **Extremely large user profiles (e.g. 2,000+ repos)** | MongoDB document exceeds the 16MB limit | The service layer trims stored repositories: if repository count exceeds `2,000`, it sorts repositories by star count and stores only the top `2,000` repositories, preventing write failures. |

---

## 7. Additional Features (Implemented Beyond Requirements)

1. **Rule-Based AI Prompts ("Persona Hints"):**
   * *What it does:* The backend analyzes the aggregated metrics (like stars or account age) and assigns preliminary tags (e.g. `novice`, `polyglot`, `veteran`, `legend_of_python`). These are appended as hints to the LLM prompt.
   * *Why it's useful:* Local 7B models can struggle to follow complex reasoning. Providing these preliminary hints guides the model, ensuring it generates relevant and high-quality personas.
2. **CSV-formatted Prompts:**
   * *What it does:* Instead of sending raw JSON to the LLM, we compile user stats and repository lists into structured CSV text.
   * *Why it's useful:* CSV formatting is highly compact. It uses fewer tokens than verbose JSON structures, reducing the prompt's footprint and speeding up local LLM inference times.
3. **Streamlit Persona Badges:**
   * *What it does:* The UI renders AI personas using custom HTML cards styled with vibrant CSS linear gradients and drop shadows.
   * *Why it's useful:* It improves the visual appeal of the dashboard, making it look like a modern web application instead of a basic tool.

---

## 8. Potential Project Weaknesses & Interview Red Flags

A senior interviewer will identify potential issues. Review the table below so you can proactively explain these trade-offs and suggest how they could be improved.

| Identified Weakness / Flag | Engineering Impact | How to Address / Refactor |
|---|---|---|
| **N+1 Request Bottleneck during Language Fetching** | Fetching a user with $N$ repositories requires 1 request to list them, and $N$ additional HTTP requests to get the language breakdown for each repo. If a user has 100 repos, this requires 101 requests, risking rate-limiting. | We can use a thread pool to execute language calls in parallel, or migrate to the GitHub GraphQL API, which can fetch a user's repositories and their language data in a single request. |
| **Ruff Format Deviations** | Code style formatting checks fail for 12 files in the project directory, which is a minor code quality concern. | Run `.venv/bin/ruff format .` to format the files. |
| **No UI pagination** | If a developer profile has 1,000 repositories, the UI attempts to load all of them into a single Streamlit dataframe widget, causing browser latency. | Implement pagination in the repository table component. |
| **Synchronous client logic in Streamlit** | The Streamlit client makes blocking HTTP calls (`httpx.get` / `httpx.post`) to the backend. If a request is slow, the Streamlit session thread blocks. | Use async requests in Streamlit or show a progress bar. |

---

## 9. Interview Preparation: Q&A Bank

### Q1: Why did you decide to aggregate the user's data on fetch/write time rather than computation-on-read?
**Answer:** This is a classic write-heavy versus read-heavy optimization trade-off. We chose write-time aggregation. Recalculating metrics like language byte percentages, topic frequencies, and push counts on every read would require fetching raw repository arrays from MongoDB and calculating them in memory on every page load. This wastes CPU cycles. Since profile lookups happen frequently but data updates only occur when a user clicks the "Refresh" button, it makes sense to compute the aggregates once during the fetch phase and save them in the document, keeping read queries fast.

### Q2: What is the time complexity of the aggregation engine? How does it scale if a user has thousands of repositories?
**Answer:** The time complexity is $\mathcal{O}(R \times L)$ where $R$ is the number of repositories and $L$ is the number of languages per repository. Space complexity is $\mathcal{O}(L_{\text{total}})$ where $L_{\text{total}}$ is the total number of unique languages. If a developer has thousands of repositories, the processing loop will scale linearly, which takes only a few milliseconds in Python. The bottleneck is not the aggregation math, but the N+1 network calls needed to query each repository's language breakdown via the REST API.

### Q3: How do you handle transient connection issues or downtime when calling Ollama? Why is it non-fatal?
**Answer:** Calling a local LLM is a secondary feature. In the service layer, we wrap the Ollama call in a `try/except` block. If the Ollama server is down, timed out, or returning errors, we catch the exception, log it as a warning, and assign `ai_summary = null` and `developer_personas = null`. The document is still saved to MongoDB, and the response is returned to the user. This ensures that a failure in the LLM feature does not impact the core functionality of the profile lookup.

---

### Follow-up Questions and Answers

#### Interviewer: "I see you have a custom regex for username validation. What security risk does this prevent?"
*   **Answer:** It prevents path traversal and injection attacks on the backend. When we call the GitHub API, we interpolate the username directly into the request path: `f"/users/{username}"`. If we did not validate the username, an attacker could input values like `../` to attempt to query other API endpoints. By enforcing alphanumeric and hyphen characters matching GitHub's naming conventions, we ensure that only valid usernames are processed.

#### Interviewer: "What is a major limitation of using a local Ollama container in a production docker-compose context?"
*   **Answer:** The major limitation is hardware resource constraints. Local LLMs require significant CPU and RAM (typically 8GB+ for a quantized 7B model) and benefit from GPU acceleration. In a production environment, running Ollama inside a container without access to a host GPU will result in slow inference times. In production, it is better to deploy the LLM behind an independent scaling service (like AWS ECS with GPU access) or use a managed service like AWS Bedrock or OpenAI.

#### Interviewer: "How would you migrate this architecture to support horizontal scaling if thousands of users accessed the tool concurrently?"
*   **Answer:** 
    1.  **Introduce an API Gateway / Load Balancer** to distribute requests across multiple backend app instances.
    2.  **Add a Message Queue (like Celery or RabbitMQ)**: Currently, fetches and Ollama calls run in the request thread, causing long request times. We should offload the fetch, aggregate, and AI generation tasks to background worker nodes, returning a task ID to the frontend and polling for updates.
    3.  **Deploy a MongoDB replica set** or use a distributed database (like DocumentDB) to scale reads and writes.
