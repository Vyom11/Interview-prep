# Mock Interview Preparation Guide (Simplified)
## GitHub Developer Profile Analyser (Live Code Walkthrough)

This guide contains project-specific mock interview questions and answers rewritten in simple, conversational language. It focuses on the actual codebase structure, execution flows, and key design choices.

---

## Table of Contents
1. [Request Flow (UI to API to DB)](#1-request-flow-ui-to-api-to-db)
2. [Cache-First Strategy & Refresh Mechanism](#2-cache-first-strategy--refresh-mechanism)
3. [GitHub Client & Pagination](#3-github-client--pagination)
4. [GitHub API Rate Limit Handling](#4-github-api-rate-limit-handling)
5. [Pure Aggregation Engine](#5-pure-aggregation-engine)
6. [Developer Persona Hints](#6-developer-persona-hints)
7. [LLM Context Serialization (CSV Generation)](#7-llm-context-serialization-csv-generation)
8. [Ollama Client & Resilience/Parsing](#8-ollama-client--resilianceparsing)
9. [MongoDB Schema Design](#9-mongodb-schema-design)
10. [Global Exception Handling Middleware](#10-global-exception-handling-middleware)
11. [Request ID Middleware & Log Redaction](#11-request-id-middleware--log-redaction)
12. [Health Checks & Dependency Verification](#12-health-checks--dependency-verification)
13. [Handling Large Accounts (System Scale & Limits)](#13-handling-large-accounts-system-scale--limits)

---

### 1. Request Flow (UI to API to DB)

#### The Interview Question
> "Walk me through how a request flows through the app from start to finish. What happens when a user submits a username?"

#### Spoken Answer
> "When a user types a username in the UI and clicks 'Analyse Profile', the Streamlit frontend sends a GET request to our backend API at `/api/v1/profiles/{username}`.
>
> On the backend, FastAPI assigns a unique request ID for tracing and routes the request to our profile route handler. The handler builds our `ProfileService` and passes the username to it.
>
> The service first validates the username structure, then checks MongoDB to see if we already have a cached profile. If we do, we return it immediately.
>
> If it is a cache miss, we call the `GithubClient` to fetch the user's profile details and loop through all their public repos. We run this data through our Aggregation Engine to calculate metrics like language percentages. We then call the `OllamaClient` to generate an AI summary, save the full profile to MongoDB, and return it back to the UI."

#### Code References
* **Frontend Controller:** [app.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/frontend/app.py#L50-L64) (captures form submissions)
* **Frontend API Caller:** [api_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/frontend/utils/api_client.py#L16-L35) (`get_profile` HTTP call)
* **Backend Router:** [profile.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/routes/profile.py#L51-L73) (profile endpoint)
* **Service Coordinator:** [profile_service.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/services/profile_service.py#L52-L95) (`get_profile` workflow)

#### Internal Walkthrough
1. The user hits submit in `app.py`, which triggers `get_profile(username)` in `api_client.py`.
2. `api_client.py` makes a GET request to `/api/v1/profiles/{username}`.
3. Backend middleware (`request_id.py`) generates a tracking UUID.
4. The route handler in `profile.py` calls `ProfileService.get_profile()`.
5. The service checks the database. If found, it returns the cache.
6. If not found, it fetches the user details and repos from GitHub, runs the metrics calculations, calls Ollama, saves the result to MongoDB, and sends the final JSON back to the frontend.

#### Why the implementation was written this way
We separated the service, repository, and client layers so that each class does only one job. This makes the code much cleaner and lets us test the business logic easily without spinning up a database or hitting the live GitHub network.

#### Common Follow-Up Questions
* *What is the request timeout, and why is it so high?* (We set it to 900 seconds in the frontend client because fetching repos and waiting for a local AI model response can take time).
* *How is the response validated?* (We use Pydantic models in `src/schemas/profile.py` to enforce the exact JSON format returned by the API).

---

### 2. Cache-First Strategy & Refresh Mechanism

#### The Interview Question
> "How does the cache-first check work, and how does the user bypass it when they click 'Refresh'?"

#### Spoken Answer
> "We use a cache-first approach to speed up lookups and avoid hitting GitHub's API rate limits.
>
> When you look up a profile, our `ProfileService` first checks MongoDB using the lowercased username. If the document exists, we return it right away with the source labeled as `cache`.
>
> If the user wants fresh data and clicks the 'Refresh' button in the UI, the frontend calls a POST request to `/api/v1/profiles/{username}/refresh`. This endpoint calls the same service method but sets the `refresh` flag to `True`. The service then skips the MongoDB check, calls the GitHub API directly to get the latest data, updates MongoDB with the new details, and returns the response labeled as `fresh`."

#### Code References
* **Service Entry Point:** [profile_service.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/services/profile_service.py#L77-L95) (handles the `refresh` flag logic)
* **Router Binding:** [profile.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/routes/profile.py#L76-L98) (the POST refresh route)
* **UI Refresh Action:** [app.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/frontend/app.py#L77-L87) (handles clicking the refresh button)

#### Internal Walkthrough
1. The frontend requests a profile. If `refresh` is `False`, the service runs `repository.find_by_username(username)`.
2. If database returns data, the service returns it with `source: "cache"`.
3. If the refresh button is clicked, the router calls `service.get_profile(username, refresh=True)`.
4. The service skips the database read check and runs `_fetch_and_persist()`.
5. It fetches new data from GitHub, overwrites the existing record in MongoDB, and returns it with `source: "fresh"`.

#### Why the implementation was written this way
Using the same `get_profile` function with a simple boolean flag avoids repeating the fetch-and-save code. We used a POST request for the refresh endpoint because it updates state inside our database.

#### Common Follow-Up Questions
* *What happens if the username has uppercase letters?* (We lowercase all usernames during validation so `OctoCat` and `octocat` point to the same database document).
* *How does the frontend reload after a refresh?* (We update the session state variables in Streamlit and call `st.rerun()` to update the view).

---

### 3. GitHub Client & Pagination

#### The Interview Question
> "Where do you communicate with the GitHub API, and how do you handle paginating through a user's repositories?"

#### Spoken Answer
> "We have a `GithubClient` class in `github_client.py` that makes async requests to the GitHub REST API using `httpx`.
>
> When we fetch repositories, GitHub limits the results per response, so we paginated the requests. We request the maximum limit of 100 repositories per page. We loop and request page after page until we get back an empty list or a list with fewer than 100 items, which tells us there are no more repos left to fetch.
>
> We also make a request for each repository to get the language byte breakdown. If the language endpoint returns empty, we fall back to using the repository's primary language as a default so it's not left out of the statistics."

#### Code References
* **GitHub Client:** [github_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/github_client.py#L61-L284)
* **Pagination Loop:** [github_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/github_client.py#L208-L236) (`fetch_repositories`)
* **Languages Endpoint:** [github_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/github_client.py#L238-L259) (`fetch_languages`)

#### Internal Walkthrough
1. `fetch_user_profile` validates the username and queries `/users/{username}` for metadata.
2. In `fetch_repositories`, we query `/users/{username}/repos?per_page=100&page=1`.
3. If we get 100 repositories, we increment the page count and call the endpoint again. We repeat this until the response has fewer than 100 repositories.
4. For each repository retrieved, we call `/repos/{username}/{repo_name}/languages` to get byte-level language counts.
5. If the languages object is empty, we default to the primary language with a count of 1.

#### Why the implementation was written this way
We fetch data asynchronously using `httpx` so we don't block the backend application. The language fallback check ensures that repositories with tiny codebases or unidentified files are still counted in our language stats.

#### Common Follow-Up Questions
* *Isn't making a separate language call for each repo slow?* (Yes, it is the slowest part of the fetch. This is why our caching mechanism is so important. In a production environment, we could speed this up by fetching languages in parallel).
* *What happens if a single repository language call fails?* (We catch the network exception, log a warning, and return an empty dictionary so that a single failure doesn't ruin the whole process).

---

### 4. GitHub API Rate Limit Handling

#### The Interview Question
> "How does the backend handle GitHub's API rate limits, and how is this shown to the user?"

#### Spoken Answer
> "We inspect the HTTP headers on every response from GitHub inside the `_check_rate_limit()` helper.
>
> If the `X-RateLimit-Remaining` header is `0`, or if we get an HTTP 403 error due to an exhausted rate limit, we extract the `X-RateLimit-Reset` timestamp and raise a custom `RateLimitExceededError`.
>
> Our backend error middleware catches this exception and returns an HTTP 429 status code with a JSON message containing the exact reset time.
>
> On the frontend, Streamlit checks the status code and displays a user-friendly warning message showing when the rate limit will reset and explaining how to set up a `GITHUB_TOKEN` in the environment files to raise their limit."

#### Code References
* **Rate Limit Check:** [github_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/github_client.py#L92-L110) (`_check_rate_limit`)
* **Custom Exception:** [exceptions.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/exceptions.py#L24-L42) (`RateLimitExceededError`)
* **API Handler:** [error_handler.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/middleware/error_handler.py#L61-L73) (`rate_limit_handler`)

#### Internal Walkthrough
1. The client sends a request.
2. The client checks `X-RateLimit-Remaining` in the response headers. If it reads `"0"`, it parses the Unix reset timestamp from the header.
3. The client raises `RateLimitExceededError`.
4. Our exception handler maps this to an HTTP 429 status response.
5. The frontend displays the error message inside a standard `st.warning` box in the UI.

#### Why the implementation was written this way
Checking the headers inside our client wrapper ensures we handle rate limits immediately, before sending any more useless requests. Using standard HTTP 429 errors allows the frontend to easily detect and handle the rate limit message.

#### Common Follow-Up Questions
* *What are the GitHub rate limits?* (Unauthenticated requests are limited to 60 per hour per IP. Authenticated requests using a personal token get 5,000 per hour).
* *Where is the token loaded?* (It is loaded from the environment variables in `src/config.py`).

---

### 5. Pure Aggregation Engine

#### The Interview Question
> "How does the Aggregation Engine compute metrics? Why doesn't it have any database or network dependencies?"

#### Spoken Answer
> "Our Aggregation Engine is in `aggregation.py`. It is a collection of pure Python functions that take raw user and repository data and return an `AggregatedProfile` object.
>
> To compute the language breakdown, we sum the byte counts of each language across all repositories using Python's `Counter`. We then divide each language's bytes by the total bytes to get a percentage.
>
> To find the active months, we format the repository push dates into `YYYY-MM` strings and count which month has the most push activity.
>
> We kept this engine completely free of database and network calls to separate our calculations from our storage and API logic. This makes the aggregation logic simple to test with unit tests because we can feed it mock dictionaries without setting up mock databases or API clients."

#### Code References
* **Aggregation Functions:** [aggregation.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/aggregation.py#L1-L121)
* **Language Calculation:** [aggregation.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/aggregation.py#L26-L40) (`_compute_language_breakdown`)
* **Activity Logic:** [aggregation.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/aggregation.py#L59-L78) (`_compute_activity_by_month`)

#### Internal Walkthrough
1. The service passes the user profile and repository list to `aggregate_profile`.
2. Language percentages are calculated by dividing each language's sum of bytes by the overall total bytes.
3. The most active month is determined by finding the most common `YYYY-MM` push timestamp.
4. Account age is calculated using the user's `created_at` timestamp relative to the current time.
5. The statistics are returned as an `AggregatedProfile` model.

#### Why the implementation was written this way
Separating the calculations from the database and network layers is a core practice of clean design. It ensures that our tests run quickly and reliably, and keeps the code easy to maintain.

#### Common Follow-Up Questions
* *What happens if the user has no repositories?* (The calculation defaults are handled gracefully. Language bytes sum to 0, return an empty dictionary, and no error is raised).
* *How is the account age calculated?* (We divide the date delta in days by 365.25 to account for leap years).

---

### 6. Developer Persona Hints

#### The Interview Question
> "How are the developer personas calculated? How do the rule-based hints help the LLM?"

#### Spoken Answer
> "We use a hybrid approach to create personas. We first calculate standard 'hints' in our Python code, and then pass those hints to the local LLM to generate the final, creative persona titles.
>
> The rules are defined in `persona_rules.py` within `derive_persona_hints()`. We evaluate the user's statistics against specific rules. For example, if a user has under 5 repositories, they get a `novice` hint. If their repositories have over 1,000 total stars, they get a `megastar` hint. If they have three or more languages representing at least 5% of their total byte share, they get a `polyglot` hint.
>
> We limit these hints to a maximum of three and append them to the profile data we send to the LLM. The LLM then uses these hints to generate creative titles, like turning `polyglot` into `'Language Collector'`."

#### Code References
* **Persona Logic:** [persona_rules.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/persona_rules.py#L32-L79) (`derive_persona_hints`)
* **CSV Prompt Insertion:** [profile_csv.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/profile_csv.py#L103-L104) (appends hints to the LLM payload)

#### Internal Walkthrough
1. The service calls `derive_persona_hints(aggregated)`.
2. The rules inspect total repositories, stars, languages, account age, and forks.
3. If conditions are met, matching labels (like `novice`, `polyglot`, `veteran`, or `oss_contributor`) are added to the list.
4. We slice the list to return a maximum of three hints.
5. The hints are output as row data in the profile CSV passed to the LLM prompt.

#### Why the implementation was written this way
Using rule-based hints prevents the LLM from hallucinating or making up incorrect developer characteristics. The rules establish factual constraints, while the LLM handles generating creative names.

#### Common Follow-Up Questions
* *Why is the "Other" language slice ignored in the polyglot check?* (Because "Other" is a catch-all group for minor languages, and counting it would lead to inaccurate polyglot labels).
* *Where are the badge styles configured?* (They are styled using custom CSS gradients and emojis in [personas.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/frontend/components/personas.py#L6-L10)).

---

### 7. LLM Context Serialization (CSV Generation)

#### The Interview Question
> "How do you format the profile data before sending it to the LLM? Why did you choose CSV instead of JSON?"

#### Spoken Answer
> "We format the profile metrics and repository list into a single, compact CSV string using the code in `profile_csv.py`.
>
> The CSV contains two main sections:
> First, a table listing the user's profile statistics and persona hints.
> Second, a table listing their repositories, with columns for the repo name, primary language, star counts, forks, topics, description, and archived status.
>
> We chose CSV instead of JSON because it uses far fewer tokens. JSON has a lot of extra formatting like curly braces, quotes, and repeating key names. For profiles with many repositories, this extra formatting can easily exceed the LLM's context limit. A CSV file strips away this syntax, allowing us to send more repository data while using fewer tokens."

#### Code References
* **CSV Builder:** [profile_csv.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/profile_csv.py#L109-L131) (`build_full_profile_csv`)
* **Stats Serialization:** [profile_csv.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/profile_csv.py#L59-L106) (`build_profile_stats_csv`)
* **Table Serialization:** [profile_csv.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/profile_csv.py#L38-L56) (`build_repos_table_csv`)

#### Internal Walkthrough
1. The service calls `build_full_profile_csv` to prepare the data.
2. `build_profile_stats_csv` writes flat rows containing section, field, and value columns.
3. `build_repos_table_csv` loops through the repositories and writes rows with columns for names, languages, stars, forks, topics, and descriptions.
4. The two CSV strings are joined together with a header separator.
5. The combined CSV text is inserted directly into the Ollama prompt template.

#### Why the implementation was written this way
We only select specific fields to include in the CSV, leaving out raw fields like `created_at` and `size_kb` to save tokens. Languages that represent less than 1% of the codebase are grouped into an "Other" category to keep the prompt clean.

#### Common Follow-Up Questions
* *How do you handle commas or quotes inside repository descriptions?* (We use Python's built-in `csv.writer()`, which handles escaping quotes and commas automatically to keep the CSV valid).
* *Where is the language grouping defined?* (In [ai_context.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/ai_context.py#L11) using the `MIN_SLICE_PERCENT = 1.0` constant).

---

### 8. Ollama Client & Resilience/Parsing

#### The Interview Question
> "How does the Ollama client generate insights? What happens if Ollama is offline or returns invalid text?"

#### Spoken Answer
> "Our `OllamaClient` makes async HTTP POST requests to the local Ollama `/api/generate` endpoint using the `mistral` model.
>
> Because running a local LLM can be slow or fail on machines with limited hardware, we designed the client to be resilient:
> First, we set a 20-second request timeout on the HTTP client.
> Second, we wrap our requests in try-except blocks. If Ollama is offline or times out, we catch the exception, log a warning, and return `None` so that the main request still succeeds.
> Third, we request a JSON response matching a specific schema. If the model returns markdown code blocks or invalid JSON, our custom parsing function strips the markdown formatting and uses a regex pattern to extract the persona array. If all parsing attempts fail, the service layer defaults the AI summary fields to null, and the UI displays the rest of the profile normally."

#### Code References
* **Ollama Client:** [ollama_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/ollama_client.py#L67-L159)
* **Response Parsing:** [ollama_client.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/clients/ollama_client.py#L160-L196) (`_parse_insights_response`)
* **Service Fallback:** [profile_service.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/services/profile_service.py#L221-L228) (handles failed summaries gracefully)

#### Internal Walkthrough
1. The client formats the CSV data into the prompt template and sends a POST request to `/api/generate`.
2. If the request fails or times out, the client logs a warning and returns `None`.
3. If it succeeds, `_parse_insights_response` strips any triple backticks or leading `"json"` text.
4. It attempts to parse the response using `json.loads`.
5. If that fails, it runs a regex search `\[[\s\S]*?\]` to extract the array of personas.
6. The client returns the parsed insights, and the service saves them to MongoDB.

#### Why the implementation was written this way
Using regex parsing as a backup ensures we can still extract personas even if the model prefixes its response with conversational text. Making Ollama errors non-fatal ensures that the app remains functional even if the optional AI service is offline.

#### Common Follow-Up Questions
* *What model does the client use?* (It defaults to `mistral` but can be configured in the settings).
* *How is the output length capped?* (We limit the request to 300 tokens to speed up the response time).

---

### 9. MongoDB Schema Design

#### The Interview Question
> "Explain your MongoDB schema. Why did you choose to store the user and repository details in a single document?"

#### Spoken Answer
> "We store each developer profile as a single document in the `profiles` collection, using the user's lowercased GitHub username as the primary key (`_id`).
>
> The document contains the raw user metadata, an array of repositories (including their language breakdowns), the aggregated stats, the AI personas, the AI summary text, and a fetch timestamp.
>
> We chose this single-document design because it matches our app's access patterns. We always retrieve and display all profile details at the same time. Storing everything in one document allows us to retrieve a profile in a single database read without using joins. It also makes updating data simple, as we can replace the entire document using a single atomic `replace_one` upsert operation keyed by username."

#### Code References
* **Repository Implementation:** [profile_repository.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/repositories/profile_repository.py#L19-L86)
* **Upsert Operation:** [profile_repository.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/repositories/profile_repository.py#L50-L66) (`upsert`)
* **Document Model:** [models.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/domain/models.py#L87-L112) (`ProfileDocument`)

#### Internal Walkthrough
1. On application startup, the repository runs `ensure_indexes()` to set a unique index on `username`.
2. When query runs, `find_by_username` executes `find_one({"_id": username.lower()})`.
3. If found, the BSON document is mapped to a `ProfileDocument` instance.
4. When saving, `upsert` replaces the existing document or inserts a new one if it doesn't exist, using `upsert=True` keyed by the lowercased username.

#### Why the implementation was written this way
We included a `schema_version` field in the document schema. This allows us to handle future updates or changes to the database structure without needing to rewrite the existing database.

#### Common Follow-Up Questions
* *Can the document exceed MongoDB's 16MB limit if a user has many repos?* (No, because we cap the stored repositories list at 2,000, which keeps the document size well under 1MB).
* *Where is the repository cap defined?* (In [profile_service.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/services/profile_service.py#L25) using the `MAX_REPOS_STORED = 2000` constant).

---

### 10. Global Exception Handling Middleware

#### The Interview Question
> "How does the backend handle exceptions globally, and how do they map to HTTP status codes?"

#### Spoken Answer
> "We use a global error handler middleware in `error_handler.py` to catch exceptions. This allows us to keep our route handlers clean and free of repetitive try-except blocks.
>
> We register exception handlers on our FastAPI app to catch specific errors and map them to HTTP status codes:
> * `UserNotFoundError` maps to HTTP 404.
> * `InvalidUsernameError` maps to HTTP 422.
> * `RateLimitExceededError` maps to HTTP 429.
> * `UpstreamServiceError` maps to HTTP 502.
>
> For any unhandled exceptions, we catch them, log the stack trace, and return a clean HTTP 500 internal server error. All errors return a consistent JSON response containing an error code and a descriptive message."

#### Code References
* **Registration:** [main.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/main.py#L67) (registers the handlers on startup)
* **Error Handlers:** [error_handler.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/middleware/error_handler.py#L32-L106)
* **JSON Helper:** [error_handler.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/middleware/error_handler.py#L25-L29) (`_error_body`)

#### Internal Walkthrough
1. During startup, `register_exception_handlers` attaches handlers to the FastAPI app.
2. During a request, if the GitHub API returns a 404, the client raises `UserNotFoundError`.
3. FastAPI intercepts the exception and routes it to `user_not_found_handler`.
4. The handler builds a JSON response containing `user_not_found` and returns an HTTP 404 status.
5. The frontend API client detects the 404 response and displays an error message to the user.

#### Why the implementation was written this way
Decoupling exception handling from the route handlers keeps our API code clean. The business logic only needs to raise errors, and the middleware handles formatting the HTTP responses.

#### Common Follow-Up Questions
* *What happens during database connection failures?* (They are caught by the general `Exception` handler, which logs the error details for debugging and returns a clean HTTP 500 error to the client).
* *Where is the error schema defined?* (In [profile.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/schemas/profile.py) as the `ErrorResponse` model).

---

### 11. Request ID Middleware & Log Redaction

#### The Interview Question
> "How do you track logs for a specific request, and how do you prevent authorization tokens from leaking in the logs?"

#### Spoken Answer
> "We use a custom `RequestIdMiddleware` to generate a unique UUID4 for every incoming request. We store this request ID in the request state and return it in the response as an `X-Request-Id` header.
>
> We pass this request ID to our logging helper `log_event()`, which includes the ID in every log statement so we can easily trace logs for a specific request.
>
> To make sure we don't leak secret tokens in our logs, we created a custom `RedactingJsonFormatter` in `logging_config.py`. This formatter checks our logs for authorization token strings like `Bearer ghp_...` and replaces the token values with `[REDACTED]` before writing them to the log."

#### Code References
* **Request ID Middleware:** [request_id.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/middleware/request_id.py#L16-L35)
* **Log Formatter Redaction:** [logging_config.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/utils/logging_config.py#L18-L26) (`RedactingJsonFormatter`)
* **Event Logger:** [logging_config.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/utils/logging_config.py#L48-L74) (`log_event`)

#### Internal Walkthrough
1. `RequestIdMiddleware` intercepts an incoming request, generates a UUID, and saves it in `request.state.request_id`.
2. The router passes this request ID to the profile service.
3. The service uses `log_event()` to log activities, passing along the request ID.
4. Before printing to the console, `RedactingJsonFormatter` checks the log message and redacts matching token strings.
5. The middleware appends the request ID to the HTTP response header.

#### Why the implementation was written this way
We use structured JSON logs because they are easy to search in log management tools. We redact authorization tokens at the formatter level to ensure that credentials are never written to the logs, even if someone accidentally logs a raw request object.

#### Common Follow-Up Questions
* *What library does the log formatter extend?* (It extends `python-json-logger`'s `JsonFormatter` to format log outputs as JSON).
* *Where is the formatter registered?* (It is configured and registered on the root logger inside `configure_logging()`).

---

### 12. Health Checks & Dependency Verification

#### The Interview Question
> "How does the health check endpoint verify downstream dependencies like MongoDB and Ollama?"

#### Spoken Answer
> "We implement health checks at the `/api/v1/health` endpoint in `health.py`. This endpoint verifies the health of our two main downstream dependencies: MongoDB and Ollama.
>
> To check MongoDB, we run a ping command: `await db.command("ping")`. If the database responds without an error, we mark it as `connected`.
>
> To check Ollama, we see if it is enabled in our settings. If it is, we make a quick GET request to `/api/tags` with a 5-second timeout. If the request succeeds, we mark it as `reachable`.
>
> The overall health status returns `"ok"` if MongoDB is connected, and `"degraded"` if it isn't. This endpoint is used by Docker to monitor our backend container and ensure it is ready to handle traffic."

#### Code References
* **Health Check Endpoint:** [health.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/routes/health.py#L74-L91) (`health_check`)
* **Mongo Ping Check:** [health.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/routes/health.py#L21-L29) (`_check_mongodb`)
* **Ollama Ping Check:** [health.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/api/routes/health.py#L32-L71) (`_check_ollama`)

#### Internal Walkthrough
1. The orchestrator calls the `/health` endpoint.
2. `_check_mongodb` retrieves the database client and runs a ping check.
3. `_check_ollama` checks if Ollama is enabled and makes a GET request to `/api/tags`.
4. If MongoDB is connected, the overall status is set to `"ok"`; otherwise, it returns `"degraded"`.
5. The endpoint returns the status dictionary.

#### Why the implementation was written this way
We keep the health status checks for MongoDB and Ollama separate. If Ollama is offline or disabled, the endpoint still returns an overall status of `"ok"` as long as MongoDB is connected. This prevents the application from being marked as unhealthy if the optional AI features are offline.

#### Common Follow-Up Questions
* *What happens if the check to Ollama times out?* (We catch the connection error, log a health check failure warning, and return `"unreachable"` without failing the request).
* *Where is this check configured?* (It is configured in the healthcheck section of the `docker-compose.yml` file to monitor the container status).

---

### 13. Handling Large Accounts (System Scale & Limits)

#### The Interview Question
> "If you search for a GitHub user with 5,000 public repositories, where will the current implementation run into limitations? How would you modify the system to handle this?"

#### Spoken Answer
> "If we search for a user with 5,000 repositories, we will run into a few key bottlenecks:
> 
> * **API Call Overhead:** Since we fetch languages for every repository, we would make 5,000 separate HTTP requests. This would take several minutes and cause the request to time out.
> * **Storage Limits:** Storing all 5,000 repository records in a single MongoDB document could approach MongoDB's 16MB document limit.
> 
> To resolve these bottlenecks:
> * **Repository Capping:** We already implement a cap in `profile_service.py` using the `MAX_REPOS_STORED = 2000` constant. If a user exceeds this limit, we sort their repositories by stars and only store the top 2,000, which keeps our database documents small.
> * **Parallel Requests:** We could speed up language fetches by making requests in parallel using `asyncio.gather()`, batching the calls to avoid overloading the connection pool.
> * **Background Tasks:** For large accounts, we should process the request as a background task. The backend would return an HTTP 202 status code immediately, compile the profile in the background, and update the UI once the profile is ready."

#### Code References
* **Repository Limit Cap:** [profile_service.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/services/profile_service.py#L25) (`MAX_REPOS_STORED = 2000`)
* **Cap Sorting Logic:** [profile_service.py](file:///Users/vyompandya/Downloads/Practical%20Assessment/src/services/profile_service.py#L140-L144) (sorts and slices repos by stars)

#### Internal Walkthrough
1. In `profile_service.py`, after fetching repositories, we check if the count exceeds `MAX_REPOS_STORED`.
2. If it does, we sort the repositories in descending order based on star counts.
3. We slice the list to keep only the top 2,000 repositories.
4. Only these top repositories are stored in MongoDB.

#### Why the implementation was written this way
Sorting and slicing the repositories by star count ensures we still capture the developer's most popular projects for our stats, even if we drop some of their less active repositories. This approach provides a good compromise, keeping MongoDB document sizes small and ensuring fast loading times while still gathering useful data.

#### Common Follow-Up Questions
* *How is the LLM prompt adjusted for large repo lists?* (We limit the repository table input to fit within the model context window by using compact CSV formats).
* *Where would you modify the code to fetch languages in parallel?* (In `fetch_user_profile()` within `github_client.py`, where we loop over the repository list to fetch languages).
