# Phase 11 — System Design & Architecture

## Introduction: The Senior Engineer's Mindset
In system design, a junior engineer asks, *"How do we build this?"* A senior engineer asks, *"What happens when this fails? How does it scale? What are the trade-offs?"* 

There are no silver bullets in architecture. Every decision (e.g., choosing microservices over a monolith, or Kafka over RabbitMQ) introduces new complexities. Your job is to align the architecture with the business requirements (Cost, Time-to-Market, Reliability, Scalability).

---

## 1. Architecture Patterns: Monolith vs. Microservices

### The Concepts
*   **Monolith:** A single, unified unit. The UI, business logic, and data access layers reside in one codebase and are deployed together.
*   **Microservices:** An architectural style that structures an application as a collection of loosely coupled, independently deployable services organized around business domains.

### Why we use them & Trade-offs
*   **Why Monolith?** Excellent for startups and greenfield projects. Easy to debug, simple deployments, and no network latency between internal function calls.
*   **Why Microservices?** When the organization scales. It solves *people* scaling problems (teams can work independently) and *technical* scaling problems (scaling a specific bottleneck service rather than the whole app).
*   **Alternatives:** **Modular Monolith** (a monolith with strictly enforced domain boundaries) or **Serverless** (AWS Lambda-based micro-functions).

### Code Example: The Transition (API Gateway Pattern)
When breaking a monolith, we don't expose 50 microservices to the client. We use an API Gateway to route traffic.

```python
# API Gateway Example using FastAPI
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Internal microservice URLs (in reality, fetched via Service Discovery like Consul/Etcd)
USER_SERVICE_URL = "http://internal-user-service:8001"
ORDER_SERVICE_URL = "http://internal-order-service:8002"

@app.get("/api/v1/users/{user_id}/orders")
async def get_user_orders(user_id: int):
    """
    The Gateway aggregates data from multiple microservices so the 
    client only makes one network call.
    """
    async with httpx.AsyncClient() as client:
        # 1. Fetch user data (Auth/Profile)
        user_response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
        if user_response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
        
        # 2. Fetch orders for this user
        order_response = await client.get(f"{ORDER_SERVICE_URL}/orders?user_id={user_id}")
        
        # 3. Aggregate and return
        return {
            "user": user_response.json(),
            "orders": order_response.json()
        }
```

---

## 2. Distributed Systems & The CAP Theorem

### The Concept
A distributed system is a network of independent computers that appears to the user as a single coherent system. 

**The CAP Theorem** states that a distributed data store can only provide TWO of the following THREE guarantees simultaneously:
1.  **Consistency (C):** Every read receives the most recent write or an error.
2.  **Availability (A):** Every request receives a non-error response (but without the guarantee that it contains the most recent write).
3.  **Partition Tolerance (P):** The system continues to operate despite an arbitrary number of messages being dropped by the network.

### Why it matters
Because networks *always* fail (switches die, cables are cut), **Partition Tolerance (P) is a given**. Therefore, when a failure occurs, you must choose between:
*   **CP (Consistency + Partition Tolerance):** E.g., MongoDB, HBase. If a node loses connection, it will reject requests rather than serve stale data.
*   **AP (Availability + Partition Tolerance):** E.g., Cassandra, DynamoDB. If a node loses connection, it will still serve requests, meaning you might read stale data (Eventual Consistency).

---

## 3. Scalability & Load Balancing

### Scalability Types
*   **Vertical Scaling (Scale Up):** Adding more CPU/RAM to a single machine. (Easy, but has a hard hardware limit and creates a single point of failure).
*   **Horizontal Scaling (Scale Out):** Adding more machines to the pool of resources. (Infinite scaling, but requires a load balancer and stateless applications).

### Tool: Load Balancers (Nginx / HAProxy)
*   **Why we use it:** To distribute incoming network traffic across a group of backend servers, ensuring no single server bears too much demand.
*   **Algorithms:** Round Robin, Least Connections, IP Hash.
*   **Alternatives:** Cloud Managed LBs (AWS ALB/NLB), Client-side Load Balancing (gRPC).

### Code Example: Simulating a Weighted Round Robin
To understand how load balancers route traffic under the hood:

```python
import itertools

class WeightedRoundRobin:
    def __init__(self, servers):
        # servers is a dict of {"server_ip": weight}
        self.servers = servers
        self.server_pool = self._build_pool()
        # itertools.cycle creates an infinite iterator over the pool
        self.iterator = itertools.cycle(self.server_pool)

    def _build_pool(self):
        pool = []
        for server, weight in self.servers.items():
            # If server A has weight 3, it appears in the pool 3 times
            pool.extend([server] * weight)
        return pool

    def get_next_server(self):
        return next(self.iterator)

# Usage: 
# Server 1 is twice as powerful as Server 2 and 3.
lb = WeightedRoundRobin({
    "192.168.1.10": 2, 
    "192.168.1.11": 1, 
    "192.168.1.12": 1
})

# Simulating 4 incoming requests
for _ in range(4):
    print(f"Routing request to: {lb.get_next_server()}")
# Output: .10, .10, .11, .12, (then repeats)
```

---

## 4. Event-Driven Architecture & Message Queues

### The Concept
Instead of Service A calling Service B synchronously (waiting for a response), Service A emits an "Event" to a Message Broker. Service B listens to the broker and processes the event asynchronously. 

### Tools: RabbitMQ vs. Apache Kafka
*   **RabbitMQ (Smart Broker / Dumb Consumer):** 
    *   *Why use it:* Traditional queueing. When a consumer reads a message, it is deleted from the queue. Great for task distribution (e.g., Celery, sending emails, processing payments).
*   **Apache Kafka (Dumb Broker / Smart Consumer):**
    *   *Why use it:* Event Streaming. It is essentially an append-only distributed log. Messages are *not* deleted when read; consumers track their own "offset". Great for high-throughput analytics, log aggregation, and Event Sourcing.
*   **Alternatives:** AWS SQS, Google Pub/Sub, Redis Streams.

### Code Example: Idempotent Consumer (RabbitMQ / Pika)
In distributed systems, messages might be delivered more than once (At-Least-Once delivery). Consumers **must** be idempotent (processing the same message twice doesn't break the system).

```python
import pika
import redis
import json

# Redis used to track processed messages
cache = redis.Redis(host='localhost', port=6379, db=0)

def process_order(ch, method, properties, body):
    event = json.loads(body)
    order_id = event.get("order_id")
    
    # 1. Idempotency Check: Have we seen this order before?
    if cache.exists(f"processed_order:{order_id}"):
        print(f"Order {order_id} already processed. Skipping.")
        # Acknowledge message so RabbitMQ removes it from the queue
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # 2. Process Business Logic (e.g., charge credit card)
    print(f"Charging card for order: {order_id}")
    
    # 3. Mark as processed in Redis (Store for 24 hours)
    cache.setex(f"processed_order:{order_id}", 86400, "1")
    
    # 4. Acknowledge message only AFTER successful processing
    ch.basic_ack(delivery_tag=method.delivery_tag)

# (Connection boilerplate omitted for brevity)
# channel.basic_consume(queue='order_queue', on_message_callback=process_order)
```

---

## 5. Service Communication (REST vs gRPC vs GraphQL)

When microservices talk to each other, HTTP/REST is often too slow and bulky.

### Tool: gRPC (Google Remote Procedure Call)
*   **Why we use it:** Uses **HTTP/2** (multiplexing, lower latency) and **Protocol Buffers (Protobuf)**. Instead of JSON (which requires heavy parsing and is text-based), Protobuf serializes data into a dense, strongly-typed binary format.
*   **Alternatives:** 
    *   **REST:** Ubiquitous, easy to test (cURL), best for external-facing APIs.
    *   **GraphQL:** Best when clients (mobile/web) need highly specific, nested data without over-fetching (getting fields you don't need) or under-fetching (requiring multiple API calls).

### Code Example: gRPC Protobuf Definition
```protobuf
// save as user.proto
syntax = "proto3";

// Define the payload structure
message UserRequest {
  int32 user_id = 1;
}

message UserResponse {
  int32 user_id = 1;
  string name = 2;
  string role = 3;
}

// Define the Service
service UserService {
  // A standard unary RPC call
  rpc GetUser(UserRequest) returns (UserResponse);
}
```
*(Senior context: In Python, you use `grpcio-tools` to compile this `.proto` file into Python classes, ensuring strict schema contracts between microservices).*

---

## 6. Senior-Level Interview Questions on System Design

Expect these to be open-ended. The interviewer is evaluating your thought process, not looking for a single correct word.

### Q1: We have a massive legacy Monolith that is slowing down our release cycle. How do you migrate it to Microservices without downtime?
**Expected Answer:**
I would use the **Strangler Fig Pattern**. We do not rewrite the monolith from scratch. Instead, we put an API Gateway in front of the monolith. We identify a single, highly decoupled domain (e.g., the Notification Service) and rewrite it as a microservice. We configure the API Gateway to route notification requests to the new service, and all other requests to the monolith. Over months/years, we "strangle" the monolith by migrating domain by domain until the monolith disappears.

### Q2: Service A processes an order, Service B deducts inventory, and Service C processes payment. If Service C fails, how do you rollback Service A and B in a distributed system?
**Expected Answer:**
We cannot use standard ACID database transactions across multiple microservices. Instead, I would implement the **Saga Pattern**. 
Specifically, I would use Choreography (events) or Orchestration (a central controller). If Payment (Service C) fails, it publishes a `PaymentFailed` event. Services A and B listen for this event and execute **Compensating Transactions** (e.g., Service B runs a function to add the inventory back, Service A marks the order as "Cancelled").

### Q3: How do you prevent a failing microservice from bringing down the entire system (Cascading Failures)?
**Expected Answer:**
I would implement the **Circuit Breaker Pattern** (using tools like Resilience4j or a Python equivalent). 
If Service A calls Service B, and Service B times out or fails repeatedly, the Circuit Breaker "opens." Once open, Service A stops calling Service B immediately and returns a fallback response (or an error) to prevent resource exhaustion (like thread pool depletion). After a timeout, it transitions to "half-open," allowing a few test requests through. If they succeed, it closes the circuit and resumes normal operations.

### Q4: We are building a high-frequency trading platform or a real-time multiplayer game. Should we use TCP or UDP? Why?
**Expected Answer:**
We should use **UDP (User Datagram Protocol)**. 
TCP is reliable, orders packets, and performs error-checking/retransmissions. However, this creates overhead and "Head-of-line blocking." In a real-time game or trading platform, if a packet containing the player's position from 50ms ago is dropped, we don't want TCP to pause everything to retransmit it—the data is already obsolete. UDP is connectionless and fires data as fast as possible, leaving the application layer to handle interpolation or missing data.

### Q5: What is a Dead Letter Queue (DLQ) and why is it essential in Event-Driven Architecture?
**Expected Answer:**
A DLQ is a secondary queue used to store messages that could not be processed successfully by a consumer after a certain number of retries. 
It is essential because without it, a "poison pill" message (e.g., a malformed JSON payload that causes an unhandled exception in the consumer) would be continuously re-read and crashed on, blocking all subsequent messages in the queue. The DLQ isolates the bad message so developers can inspect and debug it manually without stopping the entire pipeline.

### Q6: You are designing a system like Twitter. How do you handle generating the timeline for a user like Justin Bieber who has 100 million followers?
**Expected Answer:**
This is a classic "Fan-out" problem. 
For normal users, we can use a **Fan-out on Write (Push)** model: When a user tweets, we asynchronously push that tweet into the pre-computed timeline caches of all their followers (e.g., via Redis). 
However, for celebrities, a single tweet would require 100 million cache writes, overloading the system. For them, we use a **Fan-out on Read (Pull)** model: We don't push their tweets to followers. Instead, when a user loads their timeline, the system merges their pre-computed feed of normal friends with a live query pulling the latest tweets from the celebrities they follow.

### Q7: Explain the difference between Database Replication and Database Sharding. When do you use which?
**Expected Answer:**
*   **Replication:** Copying the entire database to multiple servers (Master-Slave or Primary-Replica). All writes go to the Primary, while Reads are distributed across Replicas. I use this when the system is **Read-Heavy** (e.g., a blog or standard CMS).
*   **Sharding:** Partitioning a single dataset across multiple databases. E.g., Users A-M on DB1, Users N-Z on DB2. I use this when the system is extremely **Write-Heavy** or the dataset is simply too large to fit on a single machine's disk. Sharding is highly complex (joining data across shards is difficult) and is a last resort.

### Q8: What is Event Sourcing, and how does it relate to CQRS (Command Query Responsibility Segregation)?
**Expected Answer:**
**Event Sourcing** means we don't store the *current state* of an entity in the database; instead, we store an append-only log of every *event* that mutated it. To get the current state, we replay the events (like a bank ledger). 
Because querying an event log for current state is slow, it is almost always paired with **CQRS**. CQRS separates the application into a Command side (which writes to the Event Store) and a Query side (which listens to the Event Store and constantly updates a highly-optimized Read Database, often a NoSQL cache).

### Q9: In an AP system (from the CAP theorem) like DynamoDB, how do you handle resolving data conflicts when eventual consistency results in two different values for the same key?
**Expected Answer:**
Conflict resolution can be handled in a few ways:
1.  **Last Write Wins (LWW):** Using a timestamp, the system arbitrarily picks the newest write and discards the older one. (Risks data loss).
2.  **Application-level resolution:** The database returns *both* conflicting versions to the application layer (like Git conflict). The application uses business logic to merge them (e.g., a shopping cart merging two sets of items).
3.  **Vector Clocks:** A tracking mechanism attached to data that determines the causal history of events, allowing the system to logically determine which version precedes the other.

### Q10: How do you ensure high availability and scale for a WebSocket server used for a real-time chat application?
**Expected Answer:**
WebSockets maintain long-lived, persistent TCP connections. Standard HTTP load balancers struggle with this.
1. I would configure a Layer 7 Load Balancer (like Nginx/HAProxy) to support WebSocket upgrades (`Connection: Upgrade`).
2. Because connections are sticky, standard horizontal scaling won't broadcast messages to users connected to different servers.
3. I would introduce a **Pub/Sub Backplane** (e.g., Redis Pub/Sub). When Server A receives a chat message for User 2 (who is connected to Server B), Server A publishes the message to Redis. Server B is subscribed to Redis, receives the event, and pushes it down the WebSocket to User 2.

---

### Q11: The client is hitting one of our API endpoints, but it takes an unacceptably long time for them to receive a response. How do you investigate and architect a solution to reduce this latency end-to-end?
**Expected Answer:**
To reduce latency, I must look at the entire lifecycle of the request—from the client's network to our database—and eliminate bottlenecks layer by layer:
1.  **Network/Edge Layer:** Are they downloading too much data? I would enable **GZIP/Brotli compression** on the Load Balancer/Gateway. If the data is static or rarely changes, I would put a **CDN (Content Delivery Network)** in front to serve requests directly from an edge server geographically closer to the client.
2.  **Application Layer (Synchronous vs. Asynchronous):** If the API is doing heavy processing (e.g., generating a PDF, sending an email, complex calculations), I would offload this. The API should instantly return a `202 Accepted` status with a Job ID, while a background worker (like **Celery** or an **AWS SQS** consumer) processes the task asynchronously.
3.  **Database Layer:** Is the DB query taking seconds? I would check for missing indexes, fix ORM N+1 issues (using Eager Loading), and implement **Pagination** so we aren't fetching 10,000 rows when the user only sees 20.
4.  **Caching:** If the query is expensive but the data is requested frequently, I would wrap the DB call in a **Redis cache** (Cache-Aside pattern).

### Q12: Your service heavily relies on a Third-Party API (e.g., a payment gateway or a shipping provider). Suddenly, their API becomes very slow or starts timing out. How do you design your system so their outage doesn't cause your system to crash?
**Expected Answer:**
If we make synchronous calls to a degraded external service, our internal application threads will hang, waiting for a response. Eventually, we will run out of threads/memory and our entire system will crash. To prevent this:
1.  **Strict Timeouts:** Never make an HTTP call without a timeout. Set a realistic timeout (e.g., 3 seconds) to ensure our app "fails fast".
2.  **Circuit Breaker:** I would implement a circuit breaker. If the 3rd-party API fails 5 times in a row, the circuit "opens" and we immediately return a fallback response (e.g., "Payment provider unavailable, try again later") without even attempting to make the external network call, giving their system time to recover.
3.  **Asynchronous Queuing:** If the task isn't time-sensitive (e.g., syncing a CRM), I wouldn't call the API synchronously at all. I would push the task to a message queue (RabbitMQ). If the 3rd-party is down, the messages safely pile up in the queue and we process them later when they recover.

### Q13: Users need to upload and download massive files (e.g., 5GB 4K videos) through your web application. If they upload them via your Python backend APIs, the servers crash due to Memory (OOM) and connection timeouts. How do you architect this?
**Expected Answer:**
Routing massive files through the application server is a major anti-pattern. It eats up server memory, ties up worker threads, and costs double in network bandwidth (Client -> App -> Storage). 
Instead, I would use the **Pre-Signed URL Pattern**:
1.  The client requests an upload from our backend.
2.  Our backend securely asks the cloud storage provider (e.g., AWS S3) for a temporary, short-lived "Pre-Signed URL".
3.  The backend returns this URL to the client.
4.  The client uploads the 5GB file **directly** to S3, completely bypassing our application servers. We can also use multipart uploads for reliability.
5.  Once the upload finishes, S3 triggers an event (via SNS/SQS) that tells our backend "File X is successfully uploaded," and we update our database.

### Q14: During a huge marketing campaign, traffic spikes 100x. Your API servers auto-scale horizontally perfectly, but suddenly your Relational Database (PostgreSQL/MySQL) crashes with "Too many connections" errors. How do you solve this?
**Expected Answer:**
When the app horizontally scales, each new container opens its own pool of connections to the database. RDBMS architectures are notoriously bad at handling thousands of idle/active connections because each connection consumes significant RAM.
1.  **Connection Pooling Proxy:** I would place a proxy like **PgBouncer** (for Postgres) or **ProxySQL** between the application and the database. The app opens thousands of connections to PgBouncer, but PgBouncer multiplexes them down to a small, manageable number (e.g., 100) of actual database connections.
2.  **Read Replicas:** If the traffic is mostly reads, I would spin up DB Read Replicas and route all `SELECT` queries to them, taking the load off the Primary database.
3.  **Caching & Rate Limiting:** Introduce Redis to absorb the read spike before it hits the DB, and configure the API Gateway to rate-limit users so the backend isn't overwhelmed by excessive requests.

### Q15: Users are complaining that searching for products on your e-commerce site is timing out. You look at the logs and see queries like `SELECT * FROM products WHERE name LIKE '%query%' OR description LIKE '%query%'`. How do you architect a scalable search solution?
**Expected Answer:**
A standard relational database uses B-Tree indexes, which are completely useless for wildcard queries that start with a `%`. The database is forced to do a "Full Table Scan," which becomes exponentially slower as the table grows.
1.  I would introduce a dedicated full-text search engine like **Elasticsearch**, **Apache Solr**, or a managed service like **Algolia**. These tools use an *Inverted Index* (similar to the index at the back of a book), making text search lightning-fast ($O(1)$ lookup times for terms).
2.  To keep the data in sync, I would implement **Change Data Capture (CDC)** using a tool like Debezium. Whenever a product is added or updated in the main Postgres DB, Debezium reads the transaction log and asynchronously streams that change via Kafka to update the Elasticsearch index, without adding any overhead to the main database writes.