# The Principal Engineer’s Complete Guide to APIs

https://apidog.com/blog/know-about-apis/?gad_source=1&gad_campaignid=23405649492&gbraid=0AAAAA-gKXrAd9JTjyYGvUkVXKGTepVGci&gclid=Cj0KCQjwqPLOBhCiARIsAKRMPZqrnHkf_fpkZuoWehibnJ4P9-olx7TfKYu34G-JjRykbWiH0jnu1F4aApjOEALw_wcB

https://blog.dreamfactory.com/rest-apis-an-overview-of-basic-principles

https://www.opslevel.com/resources/api-protocols-picking-the-right-protocol-for-your-use-case



### From Foundational Concepts to Protocol-Level Architecture

> *A synthesis of foundational API theory, REST architectural constraints, and modern protocol trade-offs — written for engineers who want to understand the **why** behind every design decision.*

-----

## Table of Contents

1. [What Is an API? The Contract Model](#1-what-is-an-api-the-contract-model)
1. [The Request/Response Lifecycle](#2-the-requestresponse-lifecycle)
1. [HTTP Methods & Idempotency](#3-http-methods--idempotency)
1. [The Six REST Architectural Constraints](#4-the-six-rest-architectural-constraints)
1. [Serialization & Data Formats](#5-serialization--data-formats)
1. [Status Codes: The Machine’s Vocabulary](#6-status-codes-the-machines-vocabulary)
1. [Protocol Comparison: REST vs. GraphQL vs. gRPC](#7-protocol-comparison-rest-vs-graphql-vs-grpc)
1. [Decision Framework: Choosing Your Protocol](#8-decision-framework-choosing-your-protocol)

-----

## 1. What Is an API? The Contract Model

### Technical Deep-Dive

An **Application Programming Interface (API)** is a formally defined communication contract between two software systems. At the machine level, this contract specifies three things: the **interface** (what endpoints or methods are exposed), the **data schema** (the shape and type of data exchanged), and the **protocol** (the transport and encoding rules governing transmission).

The key architectural insight is that an API creates a **boundary of abstraction**. The caller (client) never needs to know how the server implements its logic — it only needs to know *what* to ask for and *what format* the answer will arrive in. This separation is what makes distributed systems composable and independently deployable.

From a systems-design perspective, this abstraction boundary enables **loose coupling**: a mobile client, a web frontend, a third-party partner, and an internal microservice can all consume the same API without any of them affecting each other’s internal implementation. The API acts as the single stable surface area. This is why companies like Stripe, Google, and Twilio are able to expose powerful capabilities to millions of developers without granting them any access to internal systems.

### The Analogy

Think of a restaurant. You, the customer (client), interact only with the **menu** (the API contract) and the **waiter** (the API endpoint). You order a dish by name — you don’t walk into the kitchen, you don’t care which chef makes it, and you don’t need to know where the ingredients came from. The kitchen (server) fulfills the request and the waiter returns a plate (response). If the restaurant changes its chef, kitchen layout, or supplier, *your experience of ordering doesn’t change at all*. The menu is the contract; everything behind it is an implementation detail.

### Types of APIs

There are four major access models, and understanding them shapes how you design security and governance:

**Open (Public) APIs** are available to any external developer, often with simple API key authentication. The GitHub REST API and the OpenWeatherMap API are canonical examples. They optimize for discoverability and ease of integration.

**Partner APIs** are exposed only to vetted external organizations under formal agreements. The Stripe Connect API, used by platforms to move money on behalf of their users, operates in this model. They require stronger authentication (OAuth 2.0, mutual TLS) and carry contractual SLAs.

**Internal APIs** are consumed exclusively by teams within the same organization. Because the client and server are co-owned, teams can afford tighter coupling and move faster. DreamFactory, for example, is a platform purpose-built for auto-generating governed internal REST APIs from any database without writing backend code.

**Composite APIs** aggregate calls to multiple underlying services into a single endpoint. The client makes one call, and the API layer fans out to N services and assembles the result. This pattern is especially powerful in microservice architectures and is the conceptual foundation of GraphQL and the “Backend for Frontend” (BFF) pattern.

-----

## 2. The Request/Response Lifecycle

### Technical Deep-Dive

Every API interaction follows the same fundamental lifecycle. Understanding it at the protocol level removes the mystery from debugging and performance tuning.

**Step 1 — DNS Resolution.** The client converts a human-readable hostname (e.g., `api.example.com`) into an IP address by querying a DNS resolver. This lookup can be cached by the OS or a CDN, which is why DNS TTL (time-to-live) settings matter for service reliability.

**Step 2 — TCP Handshake.** The client initiates a TCP (Transmission Control Protocol) connection to the server’s IP address on port 443 (HTTPS) or 80 (HTTP). TCP uses a three-way handshake (`SYN` → `SYN-ACK` → `ACK`) to establish a reliable, ordered byte stream. This is fundamentally different from UDP, which provides no delivery guarantees but is faster — a distinction that becomes critical when evaluating gRPC over HTTP/2 vs. WebSockets.

**Step 3 — TLS Negotiation.** For HTTPS, a TLS handshake occurs on top of the TCP connection. The client and server agree on a cipher suite, exchange certificates for identity verification, and derive a shared symmetric encryption key. This is the overhead that connection pooling is designed to amortize — re-using an existing connection skips steps 2 and 3.

**Step 4 — HTTP Request Transmission.** The client serializes its request into an HTTP message and transmits it over the established connection. An HTTP/1.1 request has a strictly defined structure:

```
METHOD /path HTTP/1.1           ← Request Line: verb + resource identifier + protocol version
Host: api.example.com           ← Required header: identifies the virtual host
Authorization: Bearer <token>   ← Auth credential carried in the header, not the URL
Content-Type: application/json  ← Tells the server how to deserialize the body
Accept: application/json        ← Content negotiation: tells server what format client wants back

{                               ← Message body (only for POST/PUT/PATCH)
  "name": "Ada Lovelace"
}
```

**Step 5 — Server Processing.** The server’s web framework (e.g., FastAPI, Express, Django) parses the raw HTTP bytes, routes the request to the correct handler function based on the method and path, executes application logic (database queries, business rules), and serializes a response.

**Step 6 — HTTP Response Transmission.** The response follows the same structure: a status line, headers, and an optional body.

```
HTTP/1.1 201 Created            ← Status Line: protocol version + status code + reason phrase
Content-Type: application/json  ← Tells the client how to deserialize the body
Location: /users/42             ← Convention: where to find the newly created resource
Cache-Control: no-store         ← Caching directive for this specific response

{
  "id": 42,
  "name": "Ada Lovelace"
}
```

**Step 7 — Client Deserialization.** The client reads the `Content-Type` header, deserializes the body (e.g., parses JSON string into a native Python dict), checks the status code to determine success or failure, and acts accordingly.

### The Analogy

The lifecycle is like sending a certified letter. You write the letter (request body), put it in an envelope with a destination address (URL), and hand it to the postal service (TCP/IP network). The postal service guarantees delivery (TCP handshake). The recipient opens it, reads it, writes a reply, and sends it back. The status code is like the tone of the reply — “Got it, here’s what you asked for” (200 OK), “I couldn’t find what you’re looking for” (404 Not Found), or “I dropped the ball on my end” (500 Internal Server Error).

-----

## 3. HTTP Methods & Idempotency

### Technical Deep-Dive

HTTP methods (also called “verbs”) are not arbitrary labels — they carry precise semantic contracts defined in the HTTP specification (RFC 7231). Two properties are critical for building reliable distributed systems: **safety** and **idempotency**.

A **safe** method is one that does not modify server state. It is a read-only operation. `GET` and `HEAD` are safe. This property is what allows browsers, CDNs, and proxies to cache `GET` responses without concern for side effects.

An **idempotent** method is one where making the same call N times produces the same final state as making it once. `GET`, `PUT`, `DELETE`, and `HEAD` are all idempotent. `POST` is *not*. This distinction is architecturally crucial: if your network drops a `DELETE /users/42` request mid-flight, you can safely retry it because whether the server received it the first time or not, the end state is identical — the user is gone. If you retry a `POST /orders`, you may create duplicate orders.

|Method   |Safe|Idempotent|Typical Use Case                             |
|---------|----|----------|---------------------------------------------|
|`GET`    |✅   |✅         |Read a resource or collection                |
|`POST`   |❌   |❌         |Create a new resource, trigger a process     |
|`PUT`    |❌   |✅         |Replace a resource entirely (full update)    |
|`PATCH`  |❌   |⚠️ Depends |Partially update a resource                  |
|`DELETE` |❌   |✅         |Remove a resource                            |
|`HEAD`   |✅   |✅         |Check existence/headers without fetching body|
|`OPTIONS`|✅   |✅         |CORS preflight; discover allowed methods     |

`PATCH` deserves a special note. Its idempotency is implementation-defined. If `PATCH` means “set the `name` field to X,” it is idempotent. If it means “increment the `counter` field by 1,” it is not. Always document which semantic your implementation uses.

### The Analogy

`GET` is reading a book in a library — you leave it exactly as you found it. `POST` is filling out a government form — each submission creates a new record, so submitting twice means two records. `PUT` is replacing every page of a notebook with new content. `PATCH` is making a correction on a specific page. `DELETE` is shredding the notebook — do it once, or a hundred times, the result is the same.

-----

## 4. The Six REST Architectural Constraints

REST (Representational State Transfer) was defined by Roy Fielding in his 2000 doctoral dissertation. It is not a protocol or a specification — it is an **architectural style** described by six constraints. A system that satisfies all six is called “RESTful.” Each constraint exists for a specific engineering reason.

### 4.1 Client-Server Separation

**What it means:** The user interface (client) and the data storage/business logic (server) must be separated behind a uniform interface. Neither side should know or care about the internal implementation of the other.

**Why it exists:** This constraint enables independent evolvability. The frontend team can migrate from React to a native mobile app without touching the backend. The backend team can switch from PostgreSQL to a distributed NoSQL store without the client knowing. This separation of concerns is the prerequisite for the modern microservices pattern and is what makes it possible for a single REST API to serve web browsers, mobile apps, IoT devices, and other services simultaneously.

**System design implication:** This is why REST discourages server-side rendering or any pattern where the server generates UI. The server should return data (representations of resources), not presentation logic.

### 4.2 Statelessness

**What it means:** Each request from client to server must contain *all* the information necessary for the server to understand and process it. The server must not store any client session state between requests. Authentication credentials, context about what the client did last, preference settings — all of it must be re-sent with every single request.

**Why it exists (and why it’s brilliant for scale):** Statelessness is the architectural cornerstone of horizontal scalability. If the server holds no session state, then *any server in a load-balanced cluster can handle any request*. You can add 100 more server instances and your load balancer can distribute traffic freely using round-robin or least-connections algorithms, with no need for “sticky sessions” or session affinity. You can also kill any server at any time without losing user sessions.

**The common implementation:** Rather than storing a session in server memory, the client receives a signed **JWT (JSON Web Token)** after authenticating. The JWT is a self-contained, cryptographically signed object that encodes the user’s identity and permissions. On every subsequent request, the client sends this token in the `Authorization: Bearer <token>` header. The server validates the signature and reads the claims — no database lookup required.

**The trade-off:** The downside is increased payload size per request (you’re re-sending auth credentials every time) and the inability to trivially invalidate a token before it expires. This is why JWT expiration windows and refresh token rotation patterns exist.

### The Analogy

Imagine calling a customer support line where each agent has amnesia. Every time you call, you must re-explain your name, your account number, and the full context of your issue from scratch. Frustrating for humans, but liberating for distributed systems — it means any agent (server) can handle any call (request) because they don’t rely on remembered context.


### 4.3 Cacheability

**What it means:** Every response must explicitly declare whether it can be cached, for how long, and under what conditions. Responses that are cacheable can be stored and re-served by intermediate proxies (CDN edge nodes, reverse proxies) or the client itself, without hitting the origin server.

**Why it exists:** Caching is one of the most impactful performance and scalability optimizations in distributed systems. A CDN node in Singapore serving a cached response to a user is orders of magnitude faster and cheaper than routing that request all the way to an origin server in Virginia. Well-managed caching can eliminate 80–90% of read traffic from your origin servers.

**The mechanism:** HTTP cache control is orchestrated entirely through response headers. The most important ones are `Cache-Control` (primary directive: `max-age`, `no-cache`, `no-store`, `public`, `private`), `ETag` (a fingerprint of the resource content, used for conditional GET revalidation), and `Last-Modified` (timestamp used for `If-Modified-Since` conditional requests).

**System design implication:** This is one of REST’s biggest advantages over GraphQL. Because REST uses distinct URLs for distinct resources and `GET` requests are semantically read-only, CDNs and reverse proxies can transparently cache them. GraphQL, which tunnels all operations over `POST /graphql`, cannot use standard HTTP caching without custom middleware.

### 4.4 Uniform Interface

**What it means:** This is the central feature that distinguishes REST from other API styles. The interface between client and server must follow a standardized, uniform contract. Fielding defined four sub-constraints:

The interface must be **resource-based** — every “thing” in the system is identified by a URI (Uniform Resource Identifier) using nouns, not verbs. `/users/42` is correct; `/getUser?id=42` is not RESTful because the action is in the URI rather than the HTTP method.

Resources must have **multiple representations** — the same resource (e.g., a user record) can be returned as JSON, XML, or CSV, depending on what the client requests via the `Accept` header. This is called content negotiation.

Messages must be **self-descriptive** — each message contains enough information to describe how to process it. A `Content-Type: application/json` header, for example, tells the receiver exactly how to deserialize the body.

The interface must support **HATEOAS** (Hypermedia As The Engine Of Application State) — responses should contain links to related actions and resources, allowing a client to navigate the API dynamically without hardcoding URLs. This is the most mature and least commonly implemented of the four sub-constraints.

### 4.5 Layered System

**What it means:** A client should not be able to tell whether it is communicating directly with the origin server or with an intermediary. The system must be composed of hierarchical layers — and each layer must only know about the immediate layer it is interacting with.

**Why it exists:** This constraint is what allows the entire ecosystem of API infrastructure to exist. Load balancers, API gateways, reverse proxies, CDN edge nodes, authentication middleware, rate-limiting services, observability sidecars — all of these are layers that can be inserted between client and server without either end knowing. This is the architectural foundation of the modern API gateway pattern (Kong, AWS API Gateway, Apigee).

**System design implication:** DreamFactory is a concrete example of this constraint in action. It sits as an intermediary layer that intercepts requests, validates API keys, enforces RBAC policies, translates between protocols (e.g., converting REST requests to SQL queries or SOAP calls), and logs audit trails — all transparently, without the client needing to know the database engine behind the scenes.

### 4.6 Code on Demand (Optional)

**What it means:** Servers can optionally send executable code to clients that extends their functionality. The canonical example is a web server returning JavaScript, which the browser executes. This is the only optional constraint in REST.

**Why it exists:** It provides post-deployment flexibility. A server can send a JavaScript widget or validation script that changes client behavior without the client needing to be updated. The trade-off is reduced visibility — the client is now running code it didn’t have at compile time.

-----

## 5. Serialization & Data Formats

### Technical Deep-Dive

**Serialization** is the process of converting an in-memory data structure (e.g., a Python dict, a Java object) into a sequence of bytes suitable for transmission over a network. **Deserialization** is the reverse. The format chosen for serialization has profound implications for bandwidth consumption, CPU overhead, and interoperability.

**JSON (JavaScript Object Notation)** is the dominant format for REST APIs. It is text-based, human-readable, and has native parsing support in every modern language. Its downside is verbosity: field names are repeated in every record, whitespace is included, and numbers are encoded as characters. A JSON payload carrying a list of 10,000 user records will be substantially larger than the equivalent binary encoding.

**XML** was the dominant format before JSON (especially with SOAP). It is even more verbose due to closing tags, but offers mature tooling for validation (XML Schema), transformation (XSLT), and querying (XPath). It is still prevalent in financial systems, healthcare (HL7 FHIR), and enterprise integrations.

**Protocol Buffers (Protobuf)** is Google’s binary serialization format, used natively by gRPC. Fields are identified by integer tags (not string names), and data is encoded in a compact binary representation. A protobuf message is typically 3–10x smaller than the equivalent JSON, and encoding/decoding is significantly faster because there is no string parsing. The downside is that binary messages are not human-readable — you cannot `curl` an endpoint and read the raw response.

### The Analogy

Imagine sending a table of data. JSON is like writing out a CSV where every single row repeats the column headers: `{"name": "Ada", "age": 36}, {"name": "Grace", "age": 85}` — every record restates “name” and “age.” Protocol Buffers is like a pre-agreed codebook where field 1 means “name” and field 2 means “age” — you just send `1: Ada, 2: 36` in binary. Much shorter, but you need the codebook (`.proto` file) to decode it.

-----

## 6. Status Codes: The Machine’s Vocabulary

### Technical Deep-Dive

HTTP status codes are the server’s primary mechanism for communicating the outcome of a request. They are grouped into five classes, and using them correctly is essential for building clients that handle errors gracefully.

**2xx — Success.** The request was received, understood, and processed successfully. The most important ones are `200 OK` (general success), `201 Created` (a new resource was created; pair with a `Location` header), `204 No Content` (success, but there is no body to return — common for `DELETE`), and `206 Partial Content` (used for ranged requests and streaming).

**3xx — Redirection.** The client must take further action to complete the request. `301 Moved Permanently` tells clients and crawlers to update their bookmarks. `302 Found` is a temporary redirect. `304 Not Modified` is the critical caching response: the server is telling the client “your cached version is still current; no need to re-transmit the body.”

**4xx — Client Error.** The request was malformed or cannot be fulfilled as written. `400 Bad Request` means the syntax was wrong (invalid JSON, missing required field). `401 Unauthorized` means “you didn’t provide credentials.” `403 Forbidden` means “you provided valid credentials, but you don’t have permission.” `404 Not Found` means the resource doesn’t exist at this URI. `409 Conflict` means the request conflicts with current state (e.g., creating a user with a duplicate email). `429 Too Many Requests` signals rate limiting.

**5xx — Server Error.** The server received a valid request but failed to process it. `500 Internal Server Error` is a catch-all for unhandled exceptions. `502 Bad Gateway` means an upstream service returned an invalid response. `503 Service Unavailable` means the server is overloaded or down for maintenance. `504 Gateway Timeout` means an upstream request timed out.

The architectural importance of distinguishing 4xx from 5xx cannot be overstated. A `4xx` error means “retry is pointless without changing the request.” A `5xx` error means “retry with exponential backoff may succeed.” Clients that implement this distinction are dramatically more resilient in production.

-----

## 7. Protocol Comparison: REST vs. GraphQL vs. gRPC

### Technical Deep-Dive

The choice of API protocol is one of the most consequential architectural decisions you will make. Each protocol embodies a different philosophy about where the intelligence should live (client vs. server), how data should be shaped (resource vs. query vs. procedure), and what the performance constraints of the system are.

### REST

REST treats the system as a collection of **resources**, each identified by a URI. The client navigates the resource graph using standard HTTP methods. It is the dominant standard for public APIs because it is universally understood, natively supported by every HTTP client ever written, and naturally compatible with CDN and browser caching.

The classic weakness of REST is **over-fetching** and **under-fetching**. Over-fetching is when an endpoint returns more data than the client needs — a `GET /users/42` endpoint might return 30 fields when the client only needs `name` and `avatar_url`. Under-fetching is the opposite: to display a user’s profile page with their posts and comments, the client must make separate requests to `/users/42`, `/users/42/posts`, and `/users/42/comments`. This is the “N+1 request” problem, and it can seriously degrade mobile client performance on high-latency networks.

**Transport:** HTTP/1.1 or HTTP/2. **Serialization:** JSON (primary), XML, others. **Schema enforcement:** Optional (OpenAPI spec). **Caching:** Native HTTP caching.

### GraphQL

GraphQL was created by Facebook in 2012 to solve the over/under-fetching problem at scale across a heterogeneous collection of client apps (iOS, Android, web, each with different data needs). It introduces a **query language**: the client sends a query that precisely describes the shape of the data it needs, and the server returns exactly that — nothing more, nothing less.

The single most important architectural feature of GraphQL is **declarative data fetching**. Instead of the server deciding what data to return, the client specifies it. This moves the “data shaping” intelligence from the server to the client, dramatically reducing both bandwidth waste and round trips.

GraphQL uses a **single endpoint** (`POST /graphql`) for all operations. This simplifies the API surface but breaks standard HTTP caching, since CDNs cache based on URL and caching `POST` requests is non-trivial. It also complicates rate limiting (you can’t limit by endpoint when there’s only one) and requires server-side query complexity analysis to prevent abuse.

**Transport:** HTTP. **Serialization:** JSON. **Schema:** Mandatory (typed schema definition). **Caching:** Complex; requires custom solutions (persisted queries, query hashing).

### gRPC

gRPC, developed by Google (originally as “Stubby”), is optimized for one thing above all else: **high-performance service-to-service communication in distributed systems**. It treats communication as **remote procedure calls** — the client calls a method on the server as if it were a local function call, with full type safety.

gRPC uses **Protocol Buffers** for serialization (binary, 3–10x more compact than JSON) and **HTTP/2** for transport. HTTP/2 brings several critical advantages over HTTP/1.1: **multiplexing** (multiple concurrent requests over a single TCP connection, eliminating head-of-line blocking), **header compression** (HPACK reduces repeated header overhead), **server push**, and native **bidirectional streaming**. This streaming capability means gRPC can handle patterns that REST simply cannot: a single long-lived connection where both client and server push data asynchronously in real time.

The key trade-off is ecosystem maturity and developer friction. Protocol Buffers require a compilation step (running `protoc` to generate client and server stubs), and the binary format is not human-readable. Browser support is limited — a `grpc-web` proxy layer is required. gRPC is therefore the right choice for internal microservice communication but a poor choice for public-facing APIs.

### The Analogy

REST is like a restaurant with a fixed menu — the kitchen decides what comes on each plate. GraphQL is like a custom salad bar — you tell the server exactly which ingredients you want and they assemble it precisely. gRPC is like a direct intercom between two chefs in different restaurants — extremely fast, strictly structured, but requires both sides to agree on a detailed shared protocol in advance.

### Side-by-Side Comparison

|Dimension          |REST                  |GraphQL                       |gRPC                                           |
|-------------------|----------------------|------------------------------|-----------------------------------------------|
|**Paradigm**       |Resource-oriented     |Query language                |Remote procedure call                          |
|**Transport**      |HTTP/1.1 or HTTP/2    |HTTP (usually 1.1)            |HTTP/2                                         |
|**Serialization**  |JSON / XML (text)     |JSON (text)                   |Protocol Buffers (binary)                      |
|**Schema**         |Optional (OpenAPI)    |Mandatory                     |Mandatory (.proto files)                       |
|**Over-fetching**  |Common                |Solved by design              |Controlled via proto                           |
|**Caching**        |Native (HTTP headers) |Complex / custom              |Not built-in                                   |
|**Browser support**|Native                |Native                        |Requires `grpc-web` proxy                      |
|**Streaming**      |Limited (chunked)     |Subscriptions (WebSockets)    |Native bidirectional                           |
|**Performance**    |Good                  |Good (better E2E)             |Excellent (5–10x REST)                         |
|**Learning curve** |Low                   |Medium                        |High                                           |
|**Best for**       |Public APIs, CRUD apps|Mobile/web clients, dashboards|Internal microservices, ML inference, real-time|


-----

## 8. Decision Framework: Choosing Your Protocol

Every protocol choice involves trade-offs. Here is a structured way to think through the decision:

**Choose REST when** you are building a public-facing API, when your consumers are unknown or heterogeneous (browsers, mobile apps, third-party developers), when HTTP caching is important to your performance strategy (read-heavy, relatively static data), and when your team needs a low learning-curve solution. REST is the safest default for most web and mobile API work, and it is what the entire ecosystem of API gateways, documentation tools, and client libraries is built around.

**Choose GraphQL when** you have multiple types of clients (iOS, Android, web) that need meaningfully different subsets of the same data, and round-trip latency or bandwidth is a real constraint (e.g., mobile apps on 4G). GraphQL shines when a single screen or feature requires data aggregated from multiple backend services — what would be N REST calls becomes 1 GraphQL query. The trade-offs in caching complexity and query abuse protection are worth it in this scenario.

**Choose gRPC when** you are building internal service-to-service communication in a microservices architecture where performance is critical — particularly when latency is measured in milliseconds and throughput is in the tens of thousands of requests per second. Google, Netflix, and Cloudflare all rely heavily on gRPC for their internal RPC layers. It is also the right choice when you need bidirectional streaming (real-time telemetry, ML inference pipelines, live collaborative features).

A final, important observation: **these protocols are not mutually exclusive**. Production systems frequently use all three simultaneously. A common architecture uses gRPC for communication between backend microservices, a GraphQL layer as the “API gateway” that aggregates gRPC service responses for frontend clients, and REST endpoints for public third-party integrations and webhooks. The skill is not choosing one and using it everywhere — it is knowing which tool to apply to which layer of the system.

-----

## Further Reading

- Roy Fielding’s original REST dissertation: *Architectural Styles and the Design of Network-based Software Architectures* (2000)
- [OpenAPI Specification (Swagger)](https://swagger.io/specification/) — the standard for documenting REST APIs
- [gRPC Documentation](https://grpc.io/docs/) — official guide to Protocol Buffers and gRPC service definitions
- [GraphQL Specification](https://spec.graphql.org/) — formal specification of the GraphQL query language
- [HTTP Semantics — RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) — the authoritative specification for HTTP methods, status codes, and headers

-----

*Synthesized from: Apidog — Know About APIs · DreamFactory — REST API Overview · OpsLevel — API Protocols Guide*
