# Phase 08 — Network & API Engineering (Interview Q&A)

### Q1: Compare HTTP/1.1, HTTP/2, and HTTP/3. If you were building a modern API, why might you care about these protocol differences?
**Expected Answer:**
*   **HTTP/1.1:** Uses plaintext and persistent TCP connections (Keep-Alive). Its biggest flaw is **Head-of-Line (HOL) Blocking at the application layer**—if a client pipelines 3 requests, the server must respond in order. If request 1 is slow, 2 and 3 are blocked.
*   **HTTP/2:** Fixes application-level HOL blocking by introducing **Binary Framing and Multiplexing**. Multiple requests and responses can interleave concurrently over a *single* TCP connection. It also compresses headers (HPACK). However, it suffers from **TCP-level HOL blocking** (if one packet drops, the OS halts all multiplexed streams until the packet is retransmitted).
*   **HTTP/3:** Replaces TCP entirely with **QUIC (built on UDP)**. It handles packet loss per-stream, meaning a dropped packet on Stream A does not block Stream B. It also combines the cryptographic TLS handshake with the protocol connection, making connection establishment much faster.

### Q2: You are building a real-time dashboard for a stock exchange. The frontend needs live price updates. How do you choose between standard HTTP Polling, Long Polling, Server-Sent Events (SSE), and WebSockets?
**Expected Answer:**
*   **Standard Polling:** The client requests data every 1 second. High overhead (HTTP headers + TCP handshakes) and wastes server resources if data hasn't changed.
*   **Long Polling:** The client makes a request, but the server holds the connection open until data changes. Better, but still requires re-establishing the connection after every update.
*   **WebSockets:** A full-duplex, persistent TCP connection. Both client and server can send messages at any time. Ideal for multiplayer games or chat apps, but overkill for a dashboard since the client only *listens* and rarely sends data back.
*   **Server-Sent Events (SSE):** The correct choice for this scenario. SSE is a unidirectional (Server-to-Client) stream over standard HTTP. It benefits from HTTP/2 multiplexing, traverses corporate firewalls easily, and has built-in browser support for automatic reconnections.

### Q3: Explain the TLS (HTTPS) Handshake. How does a client know it is securely talking to your API and not a Man-in-the-Middle?
**Expected Answer:**
When a client connects to an HTTPS API, the following happens after the TCP 3-way handshake:
1.  **ClientHello:** Client sends supported cipher suites and a random byte string.
2.  **ServerHello & Certificate:** Server responds with its chosen cipher suite, its random byte string, and its **SSL Certificate** (which contains its Public Key).
3.  **Verification:** The client verifies the certificate against a trusted Root Certificate Authority (CA) pre-installed in the OS/Browser. This guarantees the server's identity.
4.  **Key Exchange (e.g., Diffie-Hellman):** The client and server use math to independently generate the exact same **Symmetric Session Key** without ever transmitting it over the wire.
5.  **Encrypted Traffic:** The asymmetric public/private keys are discarded, and all further HTTP traffic is encrypted using the fast symmetric session key.

### Q4: In FastAPI, what happens if you declare an endpoint with `def` instead of `async def`? 
**Expected Answer:**
This is a critical architectural feature of FastAPI (via Starlette). 
If you define an endpoint with `async def`, FastAPI runs it directly on the main Asyncio Event Loop. If you put a blocking operation (like `time.sleep()` or a synchronous SQLAlchemy query) inside an `async def` function, it will freeze the entire web server.
However, if you define the endpoint with a standard synchronous `def`, FastAPI is smart enough to know it might block. It automatically offloads the execution of that function to an external **Thread Pool** (using `loop.run_in_executor`). This keeps the main event loop spinning and responsive, effectively saving junior developers from accidentally taking down the server.

### Q5: What is Idempotency in REST APIs? Contrast POST, PUT, and PATCH. How do you handle a scenario where a client sends a POST request to charge a credit card, but their network drops before receiving the response?
**Expected Answer:**
**Idempotency** means that making multiple identical requests has the same effect on the server state as making a single request.
*   **POST:** Non-idempotent. Creating a resource. Sending it twice creates two resources.
*   **PUT:** Idempotent. Fully replaces a resource. Sending it twice leaves the resource in the exact same state.
*   **PATCH:** Non-idempotent mathematically, but usually implemented idempotently to partially update a resource.
*   **The Network Drop Scenario:** To prevent charging the user twice when they retry, we implement an **Idempotency Key**. The client generates a unique UUID (e.g., `Idempotency-Key: 1234`) and sends it in the header. The server checks a fast cache (Redis). If the key doesn't exist, it processes the payment and caches the result. If the client retries with the same key, the server skips processing and simply returns the cached 200 OK response.

### Q6: How does JSON Web Token (JWT) Authentication work? What is its most significant security flaw, and how do you architect a solution for it?
**Expected Answer:**
A JWT is a stateless token containing three parts: Header, Payload, and a Cryptographic Signature. When the client sends the JWT, the server verifies the signature using its secret key. If valid, the server trusts the payload (e.g., `user_id = 5`) without querying the database.
*   **The Flaw:** Because it is stateless, **a JWT cannot be easily invalidated (logged out) before its expiration time.** If a token is stolen, the attacker has free access until the token expires.
*   **The Solution:** Implement a **Short-lived Access Token / Long-lived Refresh Token** pattern. The JWT Access token expires in 15 minutes. To "logout", the frontend deletes the tokens, and the backend adds the Refresh Token to a Redis Denylist (or deletes it from a database). If an access token is stolen, it is only valid for a few minutes. Alternatively, maintain a distributed Redis cache of "revoked" access token IDs (JTI), though this compromises pure statelessness.

### Q7: Explain the OAuth 2.0 "Authorization Code Flow". Why do we use an Authorization Code instead of having the Auth Server just return the Access Token directly to the client browser?
**Expected Answer:**
This flow allows a user to grant an application (Client) access to their data on a Resource Server (e.g., Google) without sharing their password.
1.  The user is redirected to the Auth Server, logs in, and approves access.
2.  The Auth Server redirects the user back to the Client's frontend with a short-lived **Authorization Code** in the URL.
3.  The frontend sends this code to the Client's Backend.
4.  The Backend securely sends the Authorization Code + a **Client Secret** to the Auth Server to exchange it for an Access Token.
*   **Why the Code?** If the Auth server returned the Access Token directly in the URL redirect (Implicit Flow), it would be exposed to the browser history, browser extensions, and XSS attacks. By using a code, the actual Access Token is only transmitted Server-to-Server, where the Client Secret can be securely validated.

### Q8: We have an API endpoint `GET /api/users` that returns millions of records. Offset/Limit pagination (`?offset=100000&limit=50`) is causing severe database performance issues. Why, and what is the alternative?
**Expected Answer:**
Offset pagination requires the database engine to scan, count, and discard the first 100,000 rows before returning the 50 requested rows. This makes the query $O(N)$, causing severe CPU/I/O strain on deep pages.
*   **Alternative:** **Cursor-based (Keyset) Pagination.** Instead of an offset, the client sends the ID of the last item they received (`?last_id=100000&limit=50`). The backend executes `SELECT * FROM users WHERE id > 100000 LIMIT 50`. Because `id` is indexed, the database performs an $O(1)$ B-Tree seek directly to the start point. 
*   **Trade-off:** With cursors, you cannot allow users to "Jump to page 50" (there are no page numbers, just "Next" and "Previous").

### Q9: Your public API is being overwhelmed by a burst of traffic. What Rate Limiting algorithms do you know, and which would you implement using Redis?
**Expected Answer:**
*   **Fixed Window:** Counts requests per minute (e.g., 00:00 to 00:01). *Flaw:* A user can send 100 requests at 00:00:59 and 100 more at 00:01:01, bursting 200 requests in 2 seconds.
*   **Sliding Window Log:** Stores the exact timestamp of every request. Highly accurate but consumes massive memory.
*   **Leaky Bucket:** Requests enter a queue and are processed at a strictly constant rate. Smooths out traffic, but bursts are delayed.
*   **Token Bucket:** The industry standard. A bucket holds tokens (e.g., 100 max). Tokens are added at a fixed rate (10 per second). Each request costs 1 token. It handles bursts perfectly while maintaining a steady long-term rate.
*   **Implementation:** I would implement a Token Bucket or a Sliding Window Counter in Redis. Using a Lua script in Redis ensures the rate-limit check and token deduction are atomic operations, preventing race conditions in a distributed system.

### Q10: You need to introduce a breaking change to a REST API. What are the common strategies for API Versioning, and what are their trade-offs?
**Expected Answer:**
1.  **URI Versioning (`/v1/users` to `/v2/users`):** 
    *   *Pros:* Extremely explicit, easy to route via an API Gateway or Nginx. Highly cacheable by CDNs. 
    *   *Cons:* Can lead to code duplication and breaks the strict REST principle that a URI should represent a resource, not a version.
2.  **Header Versioning (`Accept: application/vnd.myapi.v2+json` or `X-API-Version: 2`):**
    *   *Pros:* Keeps URIs clean and truly RESTful.
    *   *Cons:* Harder to test in a browser without a tool like Postman. Caching is more complex (requires `Vary: Accept` headers).
3.  **Date-based Versioning (Stripe Model):** The URI stays the same, but the client sends a header like `Stripe-Version: 2023-10-01`. The API processes the request, and a middleware layer dynamically transforms the response payload backwards to match the requested historical schema. *Pros:* Incredible developer experience. *Cons:* Massive engineering effort to maintain the transformation middleware.

### Q11: Explain FastAPI's Dependency Injection system. Why is it considered vastly superior to the traditional middleware approach used in Express.js or Flask?
**Expected Answer:**
In traditional frameworks (Flask/Express), if you want to extract a user from a JWT, you put it in a Middleware. Middleware runs globally on *every* request, polluting the request object (`req.user`) and making it difficult to apply logic strictly to specific routes.
FastAPI's Dependency Injection allows you to inject logic exactly where it's needed at the route signature level: 
`async def get_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):`
*   **Decoupling:** The route handler only cares about business logic. `Depends()` automatically extracts headers, verifies the JWT, and provisions a database connection.
*   **Testing:** During testing, you can trivially override dependencies (`app.dependency_overrides[get_db] = get_test_db`) without modifying the application code or monkey-patching.

### Q12: How do you handle file uploads in a REST API? If a client needs to upload a 5GB video, how do you architect the system to prevent taking down your FastAPI server?
**Expected Answer:**
For small files (e.g., 5MB images), standard `multipart/form-data` in FastAPI (`UploadFile`) is fine. The file is spooled to disk, preventing memory exhaustion.
However, routing a **5GB file** through a Python application server is a major anti-pattern. It ties up worker threads, consumes network bandwidth, and leads to timeouts.
**The Architecture (Pre-signed URLs):**
1.  The client hits a lightweight FastAPI endpoint: `GET /generate-upload-url`.
2.  The API asks the cloud provider (e.g., AWS S3) for a temporary, secure "Pre-signed URL" and returns it to the client.
3.  The client uploads the 5GB file *directly* to S3 using the URL, completely bypassing the FastAPI application.
4.  Once finished, S3 triggers a webhook/event (via AWS SQS or SNS) notifying the FastAPI backend that the file was successfully uploaded so the database can be updated.