# Senior-Level Database Questions and Answers

## Section 1: Database Management Systems (DBMS)

### 1.1 ACID Properties and Transactions

**Q1: Explain the difference between ACID and BASE consistency models, and when would you choose one over the other?**

A: ACID (Atomicity, Consistency, Isolation, Durability) ensures strong consistency and is ideal for applications requiring strict data integrity like banking systems. BASE (Basically Available, Soft state, Eventually consistent) prioritizes availability and partition tolerance, suitable for distributed systems like social media feeds. Choose ACID for financial transactions and BASE for high-throughput, distributed systems where eventual consistency is acceptable.

**Q2: Can you explain why dirty reads, non-repeatable reads, and phantom reads occur, and how isolation levels prevent them?**

A: These anomalies occur due to concurrent transactions without proper isolation:

- **Dirty reads**: Reading uncommitted data (prevented at READ_COMMITTED and above)
- **Non-repeatable reads**: Same query returns different results within a transaction (prevented at REPEATABLE_READ and above)
- **Phantom reads**: New rows appear during a transaction’s range query (prevented at SERIALIZABLE)

Isolation levels trade off consistency with performance: READ_UNCOMMITTED (fastest, unsafe) → READ_COMMITTED → REPEATABLE_READ → SERIALIZABLE (slowest, safest).

**Q3: What happens if you have a distributed transaction across multiple databases and one fails after the other has committed?**

A: This violates ACID properties. Use Two-Phase Commit (2PC) to ensure atomicity: in phase 1, all participants vote to commit/abort; in phase 2, the coordinator broadcasts the final decision. However, 2PC is a blocking protocol that reduces availability. Modern systems use compensating transactions (saga pattern) to handle failures gracefully.

-----

### 1.2 Concurrency Control

**Q4: Compare optimistic vs pessimistic locking and discuss their trade-offs.**

A:

- **Pessimistic locking**: Locks resources before modification, preventing conflicts entirely. High locking overhead, risk of deadlocks, but guarantees consistency.
- **Optimistic locking**: Assumes conflicts are rare; uses version numbers to detect conflicts on commit. Lower overhead, better concurrency, but requires retry logic.

Choose pessimistic for high-contention workloads; optimistic for low-contention scenarios.

**Q5: How does MVCC (Multi-Version Concurrency Control) improve concurrency compared to traditional locking?**

A: MVCC maintains multiple versions of data. Readers see snapshot versions while writers create new versions, eliminating read-write conflicts. This allows concurrent reads and writes without blocking. PostgreSQL uses this extensively with tuple versioning (xmin/xmax). Tradeoff: increased storage requirements and complexity in garbage collection.

**Q6: What is a deadlock and how can you prevent or recover from it?**

A: A deadlock occurs when transactions wait circularly for locks. Prevention strategies:

- Maintain consistent lock ordering across transactions
- Use timeouts to detect and abort long-running transactions
- Break cycles through rollback and retry
- Use wait-for graphs to detect and resolve deadlocks

Database engines automatically detect deadlocks and abort one transaction to break the cycle.

-----

### 1.3 Query Optimization and Execution Plans

**Q7: How does a query optimizer decide between nested loops, hash joins, and merge joins? What factors influence this decision?**

A: The optimizer considers:

- **Table sizes**: Nested loops for small tables, hash joins for larger datasets
- **Join selectivity**: How many rows will the join produce?
- **Available indexes**: Merge joins work well with pre-sorted data
- **Available memory**: Hash joins need enough memory for the hash table
- **Cardinality estimates**: Accuracy of row count predictions

The query optimizer uses statistics on columns (histograms, n_distinct) to make decisions.

**Q8: Why might a query with no WHERE clause sometimes run faster than one with a WHERE clause that filters out most rows?**

A: This can happen due to:

- **Suboptimal index usage**: The WHERE clause might prevent index utilization
- **Cardinality miscalculation**: If the optimizer underestimates filtered rows, it chooses a suboptimal plan
- **Cache effects**: Full table scans can exploit CPU cache better than random index lookups
- **Cost miscalculation**: The optimizer’s cost model might not reflect actual I/O patterns

Use EXPLAIN ANALYZE to investigate and consider query hints if the optimizer makes poor choices.

**Q9: What is the difference between lazy evaluation and eager evaluation in query execution, and which is generally preferred?**

A: **Eager evaluation** processes all data immediately, while **lazy evaluation** (streaming/iterator model) processes data on-demand. Lazy evaluation is generally preferred because:

- Reduces memory usage
- Enables early termination (LIMIT clauses)
- Better for pipelined execution
- Allows parallel processing of pipelines

Modern databases use lazy evaluation with streaming operators.

-----

### 1.4 Indexing Strategies

**Q10: When would you choose a B-tree index over a hash index, and what are the implications?**

A:

- **B-tree**: Supports range queries, sorts, partial matches, inequalities. Self-balancing, good for general-purpose use. Slower than hash for equality checks.
- **Hash**: O(1) equality lookups, but doesn’t support range queries or sorting. Cannot use for inequality operators.

Use B-tree by default; hash only for specific high-cardinality equality lookups.

**Q11: What is index fragmentation, why does it happen, and how does it affect performance?**

A: Fragmentation occurs when index pages become scattered on disk due to inserts and deletes. This increases page reads, slowing down queries. Monitor with `SHOW INDEX SIZE` commands. Rebuild or reorganize indexes periodically:

- **Reorganize**: Physically reorders pages (cheaper, online possible)
- **Rebuild**: Recreates the index from scratch (slower, requires exclusive lock)

Fragmentation above 10-15% typically warrants reorganization.

**Q12: How would you design an optimal composite index for queries like `SELECT * FROM users WHERE age > 30 AND city = 'NYC' AND salary DESC LIMIT 10`?**

A: Use the **ESL rule**:

- **E (Equality)**: Index on city first (constant filter)
- **S (Sort)**: Index on salary next (for ORDER BY)
- **L (Range/Less than)**: Index on age last (range condition)

Composite index: `CREATE INDEX idx_users ON users(city, salary, age)`. This allows:

- Filtering by city efficiently
- Sorting by salary within that partition
- Range filtering on age using already-sorted data

-----

### 1.5 Replication and High Availability

**Q13: Compare master-slave, master-master, and multi-master replication architectures.**

A:

- **Master-slave**: One write node, multiple read-only replicas. Simple, clear consistency model. Single point of failure for writes.
- **Master-master**: Two write nodes, each replicates to the other. Higher availability but complex conflict resolution.
- **Multi-master**: Multiple write nodes. Highest availability but most complex; requires distributed consensus (CRDT, operational transformation, or custom conflict logic).

PostgreSQL supports streaming replication (master-slave); use Postgres-XL or Citus for distributed writes.

**Q14: What is the difference between synchronous and asynchronous replication, and what are the trade-offs?**

A:

- **Synchronous**: Master waits for replica acknowledgment before confirming write. Guarantees data durability but adds latency.
- **Asynchronous**: Master confirms immediately; replication happens in background. Low latency but risk of data loss if master fails before replication completes.

Hybrid approach: use synchronous for critical data, asynchronous for less critical data.

-----

### 1.6 Consistency Models

**Q15: What is eventual consistency, and how does it differ from strong consistency?**

A: **Strong consistency**: All reads return the latest written value. Requires synchronization, limiting performance.

**Eventual consistency**: Reads may return stale values temporarily, but all replicas converge to the same state eventually. Enables high availability and partition tolerance (CAP theorem).

In practice, use **causal consistency** (if A depends on B, they’re always observed in order) or **read-your-own-writes** consistency (users see their own updates immediately but others might see stale data) as a middle ground.

-----

## Section 2: SQL and PostgreSQL

### 2.1 Query Execution and Optimization

**Q16: Explain the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN at a fundamental level. Can you write a query that uses all four?**

A: These differ in which rows from each table are retained:

- **INNER**: Only matching rows
- **LEFT**: All left rows, matched right rows (nulls if no match)
- **RIGHT**: All right rows, matched left rows (nulls if no match)
- **FULL OUTER**: All rows from both tables

Example combining all:

```sql
SELECT 
  COALESCE(a.id, b.id) as id,
  a.name as a_name,
  b.name as b_name,
  CASE 
    WHEN a.id IS NOT NULL AND b.id IS NOT NULL THEN 'INNER'
    WHEN a.id IS NOT NULL AND b.id IS NULL THEN 'LEFT_ONLY'
    WHEN a.id IS NULL AND b.id IS NOT NULL THEN 'RIGHT_ONLY'
  END as join_type
FROM table_a a
FULL OUTER JOIN table_b b ON a.id = b.id;
```

**Q17: What is the difference between a subquery in the SELECT clause vs WHERE vs FROM, and how do they affect query performance?**

A:

- **SELECT clause**: Scalar subquery, executed for each row. Can be slow if it returns one row per outer row.
- **WHERE clause**: Filter subquery, executed before outer query filtering. Can be optimized with semi-joins.
- **FROM clause**: Derived table/CTE, executed once and joined. Generally most efficient.

Example:

```sql
-- Slower: scalar subquery in SELECT
SELECT id, name, (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) as order_count
FROM users;

-- Better: JOIN with GROUP BY
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

**Q18: What is the N+1 query problem and how would you solve it?**

A: N+1 occurs when fetching a parent and then executing N additional queries for each child. Example:

```sql
-- BAD: N+1 queries
SELECT * FROM users; -- 1 query
// For each user:
SELECT * FROM orders WHERE user_id = ?; -- N queries
```

Solutions:

- **JOIN**: Fetch all data in one query
- **Subquery/CTE**: Use IN clause with all IDs
- **Query batching**: Load all children in one query with filtering
- **ORM eager loading**: Use `.include()` or `.with()` methods

-----

### 2.2 Advanced SQL Concepts

**Q19: Explain window functions and provide a complex example showing their power.**

A: Window functions perform calculations across a set of rows related to the current row, without collapsing groups. Key functions:

- `ROW_NUMBER()`: Unique rank per row
- `RANK()`: Rank with ties
- `LAG()/LEAD()`: Access previous/next row values
- `SUM()/AVG() OVER (...)`: Running totals

Complex example - find the top 3 products by revenue for each region, with running total:

```sql
WITH product_revenue AS (
  SELECT 
    region,
    product_id,
    SUM(quantity * price) as revenue,
    ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(quantity * price) DESC) as rank
  FROM sales
  GROUP BY region, product_id
)
SELECT 
  region,
  product_id,
  revenue,
  SUM(revenue) OVER (PARTITION BY region ORDER BY revenue DESC) as running_total
FROM product_revenue
WHERE rank <= 3
ORDER BY region, revenue DESC;
```

**Q20: What is a CTE (Common Table Expression) and how does it differ from a subquery? When would you prefer one over the other?**

A: CTEs (WITH clause) are named temporary result sets, more readable than subqueries. They support recursion, unlike subqueries.

```sql
-- CTE: More readable
WITH region_sales AS (
  SELECT region, SUM(amount) as total
  FROM sales
  GROUP BY region
)
SELECT * FROM region_sales WHERE total > 10000;

-- Recursive CTE: Only possible with CTE
WITH RECURSIVE hierarchy AS (
  SELECT id, parent_id, name, 0 as level
  FROM categories
  WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.parent_id, c.name, h.level + 1
  FROM categories c
  INNER JOIN hierarchy h ON c.parent_id = h.id
)
SELECT * FROM hierarchy;
```

Prefer CTEs for readability and recursion; subqueries for one-off usage.

**Q21: How do aggregate functions behave with NULL values, and how would you handle NULLs in aggregations?**

A: Most aggregate functions (SUM, AVG, COUNT) ignore NULLs:

- `COUNT(*)` includes NULLs; `COUNT(column)` excludes them
- `SUM()` and `AVG()` skip NULL values
- `MAX()` and `MIN()` ignore NULLs

Example:

```sql
SELECT 
  COUNT(*) as total_rows,           -- 10
  COUNT(age) as non_null_ages,       -- 8 (2 NULLs)
  AVG(age) as avg_age,              -- Ignores 2 NULLs
  AVG(COALESCE(age, 0)) as misleading -- Treats NULL as 0
FROM users;
```

Use `COALESCE()` carefully - it changes aggregation semantics.

-----

### 2.3 PostgreSQL-Specific Features

**Q22: Explain the difference between PostgreSQL’s EXPLAIN ANALYZE output and EXPLAIN. How would you use this to optimize a slow query?**

A:

- **EXPLAIN**: Shows the planned execution, estimated rows/costs
- **EXPLAIN ANALYZE**: Actually executes the query, showing real rows/timing

Key metrics to watch:

- **Row estimate vs actual**: Large discrepancies indicate stale statistics; run ANALYZE
- **Sequential scans on large tables**: Consider adding indexes
- **Hash/Sort operations**: Memory-intensive; might be spilling to disk
- **Planning time vs execution time**: High planning suggests complex query

Example workflow:

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '1 day';
-- If rows vastly underestimated:
ANALYZE orders;
-- If sequential scan on large table, add index:
CREATE INDEX idx_orders_created_at ON orders(created_at);
```

**Q23: What are PostgreSQL extensions, and how would you use them to extend database functionality?**

A: Extensions add capabilities without core database changes. Common ones:

- **uuid-ossp**: UUID generation
- **hstore**: Key-value storage
- **json/jsonb**: JSON support
- **pg_trgm**: Trigram indexing for fuzzy search
- **PostGIS**: Geospatial queries
- **citext**: Case-insensitive text

```sql
CREATE EXTENSION IF NOT EXISTS uuid-ossp;
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT
);

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_users_name_trgm ON users USING gist (name gist_trgm_ops);
-- Now can do fuzzy search: WHERE name % 'Jon'
```

**Q24: How does VACUUM work in PostgreSQL, and why is it critical for performance?**

A: PostgreSQL uses MVCC, creating new tuple versions on UPDATE/DELETE. Dead tuples (old versions) must be cleaned up by VACUUM:

- Removes dead tuples and reclaims space
- Updates the visibility map for faster scans
- Updates statistics for the query optimizer
- Prevents transaction ID wraparound (every tuple has xmin/xmax)

```sql
-- Manual vacuum
VACUUM ANALYZE table_name;

-- Configure automatic vacuuming
ALTER TABLE table_name SET (autovacuum_vacuum_scale_factor = 0.05);
```

Without vacuum, tables bloat, performance degrades, and risk of wraparound occurs (database halts).

**Q25: Explain the difference between Materialized Views and regular Views in PostgreSQL. When would you use each?**

A:

- **Views**: Virtual tables, query recomputed every time. No storage overhead, always fresh data.
- **Materialized Views**: Results stored as physical tables. Stale data but fast access.

```sql
-- Regular view: always fresh, slower
CREATE VIEW user_order_summary AS
SELECT u.id, COUNT(o.id) as order_count, SUM(o.amount) as total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- Materialized view: needs refresh, faster
CREATE MATERIALIZED VIEW mv_user_order_summary AS
SELECT u.id, COUNT(o.id) as order_count, SUM(o.amount) as total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- Refresh when data changes
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_user_order_summary;
```

Use regular views for correctness; materialized views for complex aggregations with acceptable staleness.

-----

### 2.4 Advanced PostgreSQL Features

**Q26: How do triggers work in PostgreSQL, and what are the performance implications of using them?**

A: Triggers execute before/after INSERT/UPDATE/DELETE. They can enforce business logic at the database level.

```sql
CREATE OR REPLACE FUNCTION update_user_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_user_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_user_updated_at();
```

Performance implications:

- Triggers add latency to every write operation
- Can cause cascading updates (trigger fires another trigger)
- Make debugging harder; logic is hidden in the database
- Harder to test and version control

Use sparingly; prefer application-level logic when possible.

**Q27: What is the difference between a PRIMARY KEY constraint and a UNIQUE constraint in PostgreSQL?**

A:

- **PRIMARY KEY**: Uniqueness + NOT NULL, implicit index, only one per table
- **UNIQUE**: Allows NULLs (multiple NULLs are considered distinct), multiple per table, creates index

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,          -- Unique + not null
  email VARCHAR UNIQUE,           -- Unique, allows 1 NULL
  ssn VARCHAR UNIQUE NOT NULL     -- Unique, not null
);
```

Gotcha: In PostgreSQL, `UNIQUE` allows multiple NULLs (they’re not considered duplicates). Use `UNIQUE NOT NULL` to match PRIMARY KEY strictness.

**Q28: Explain the concept of partitioning in PostgreSQL. How would you partition a large table?**

A: Partitioning divides a large table into smaller chunks (partitions) to improve performance. Types:

- **Range**: By date ranges
- **List**: By discrete values
- **Hash**: By hash function

Example - partition large sales table by month:

```sql
CREATE TABLE sales (
  id SERIAL,
  sale_date DATE,
  amount DECIMAL
) PARTITION BY RANGE (EXTRACT(YEAR FROM sale_date), EXTRACT(MONTH FROM sale_date));

CREATE TABLE sales_2024_01 PARTITION OF sales
  FOR VALUES FROM (2024, 1) TO (2024, 2);
CREATE TABLE sales_2024_02 PARTITION OF sales
  FOR VALUES FROM (2024, 2) TO (2024, 3);
```

Benefits: Faster queries on subsets, easier VACUUM, parallel scans. Overhead: added complexity, index management.

**Q29: What is a prepared statement, and why should you always use them?**

A: Prepared statements separate SQL structure from data, preventing SQL injection and improving performance.

```sql
-- Vulnerable to SQL injection
SELECT * FROM users WHERE id = ' + user_input + ';

-- Safe with prepared statement
PREPARE get_user AS SELECT * FROM users WHERE id = $1;
EXECUTE get_user(123);
DEALLOCATE get_user;
```

Benefits:

- SQL injection prevention
- Better performance: parse once, execute multiple times
- Cleaner code, better readability

Always use prepared statements in application code (parameterized queries).

-----

### 2.5 Data Types and Storage

**Q30: Compare storage and query performance of storing data as VARCHAR vs JSON/JSONB in PostgreSQL. When would you use each?**

A:

- **VARCHAR**: Rigid schema, fast queries, excellent indexing support
- **JSON**: Flexible schema, slower queries, limited indexing
- **JSONB**: Flexible schema, fast queries (parsed, indexed), best of both worlds

```sql
-- VARCHAR: Rigid
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  email VARCHAR
);

-- JSONB: Flexible
CREATE TABLE users_flexible (
  id SERIAL PRIMARY KEY,
  data JSONB
);

-- Query JSONB
SELECT * FROM users_flexible 
WHERE data->>'email' = 'john@example.com';

-- Index JSONB for performance
CREATE INDEX idx_users_email ON users_flexible USING GIN ((data->'email'));
```

Use VARCHAR for structured data; JSONB for semi-structured (mixed attributes per row).

-----

## Section 3: MongoDB

### 3.1 Document Model and Design

**Q31: How does MongoDB’s document model differ fundamentally from relational databases, and what are the implications for application design?**

A: MongoDB stores data as documents (JSON-like), not rows. Key differences:

- **Schema flexibility**: Each document can have different fields
- **Denormalization**: Embed related data instead of joining
- **No atomic transactions across documents** (until 4.0, but still per-document atomicity is native)

Relational: Normalize, use JOINs

```sql
SELECT u.*, o.* FROM users u JOIN orders o ON u.id = o.user_id;
```

MongoDB: Denormalize, embed

```javascript
db.users.findOne({ _id: 1 }, {
  name: "John",
  orders: [
    { id: 1, amount: 100 },
    { id: 2, amount: 200 }
  ]
})
```

Trade-offs: Denormalization causes data duplication, harder to update related data, but faster reads.

**Q32: What is MongoDB’s _id field, and how should you design it?**

A: `_id` is the mandatory primary key, unique per collection. Default is ObjectId (12 bytes: timestamp + machine + process + counter), but you can specify custom values.

```javascript
// Default ObjectId
db.users.insertOne({ name: "John" });
// { _id: ObjectId("..."), name: "John" }

// Custom _id
db.users.insertOne({ _id: "user:123", name: "John" });

// Composite _id
db.user_sessions.insertOne({
  _id: { user_id: 123, session_id: "abc" },
  created_at: new Date()
});
```

Design considerations:

- **ObjectId**: Good default, includes timestamp for sorting
- **Custom string**: Better semantics (user_123), but no automatic ordering
- **Composite**: For compound uniqueness

**Q33: Explain the concept of embedding vs referencing in MongoDB. How do you decide which to use?**

A:

- **Embedding**: Store related data inside a document
- **Referencing**: Store document IDs and fetch separately (like foreign keys)

```javascript
// Embedding: Fast reads, data duplication on updates
db.users.insertOne({
  _id: 1,
  name: "John",
  addresses: [
    { street: "123 Main", city: "NYC" },
    { street: "456 Oak", city: "LA" }
  ]
});

// Referencing: Normalized, slower reads (requires multiple queries)
db.users.insertOne({ _id: 1, name: "John" });
db.addresses.insertOne({ _id: 1, user_id: 1, street: "123 Main", city: "NYC" });
```

Decision matrix:

- **Embed if**: One-to-few relationship, data accessed together, read performance critical
- **Reference if**: One-to-many/many-to-many, data changes independently, write optimization needed

**Q34: What are the risks of unbounded embedding, and how would you mitigate them?**

A: Unbounded embedding (arrays that grow infinitely) causes:

- Document size limits (16 MB per document)
- Memory bloat
- Slower queries (entire array fetched even if you need 1 item)

Example problem:

```javascript
// BAD: Orders array grows infinitely
db.users.insertOne({
  _id: 1,
  name: "John",
  orders: [{ id: 1, amount: 100 }, { id: 2, amount: 200 }, ...]
});

// GOOD: Reference orders, embed only recent ones
db.users.insertOne({
  _id: 1,
  name: "John",
  recent_orders: [{ id: 1, amount: 100 }],  // Limited size
  order_count: 1000
});
db.orders.find({ user_id: 1 });  // Fetch as needed
```

-----

### 3.2 Querying and Aggregation

**Q35: Explain the MongoDB aggregation pipeline and why it’s superior to fetching and filtering in application code.**

A: Aggregation pipeline processes data through stages (like Unix pipes), each transforming data. Stages:

- `$match`: Filter documents
- `$group`: Aggregate by field
- `$sort`: Sort results
- `$project`: Select/transform fields
- `$lookup`: Join with other collections
- `$unwind`: Flatten arrays
- `$skip`/`$limit`: Pagination

```javascript
db.orders.aggregate([
  { $match: { created_at: { $gt: new Date("2024-01-01") } } },
  { $group: { _id: "$user_id", total: { $sum: "$amount" } } },
  { $sort: { total: -1 } },
  { $limit: 10 }
]);
```

Why it’s superior to application code:

- **Filtering at source**: Reduces data transfer
- **Pushdown operations**: Database optimizes execution
- **Server-side processing**: No network overhead
- **Memory efficient**: Streaming processing

**Q36: What is $lookup and how does it compare to embedding for handling relationships?**

A: `$lookup` performs a JOIN in MongoDB:

```javascript
db.users.aggregate([
  {
    $lookup: {
      from: "orders",
      localField: "_id",
      foreignField: "user_id",
      as: "user_orders"
    }
  }
]);
// Result: [{ _id: 1, name: "John", user_orders: [{...}, {...}] }]
```

Comparison:

- **Embedding**: Fast reads, denormalized, data duplication
- **$lookup**: Normalized, slower than embedding, extra stage in aggregation, allows filtering post-join

Use embedding for one-to-few; $lookup for complex queries needing recent data.

**Q37: How would you implement pagination in MongoDB efficiently for large result sets?**

A:

- **Skip/Limit**: Simple but slow for large offsets (skips N documents)
- **Range-based pagination**: Use an indexed field for efficient navigation

```javascript
// BAD: Skip-based pagination
db.users.find().skip(1000000).limit(10);  // Skips 1 million docs!

// GOOD: Range-based pagination
// Client stores last_id from previous page
db.users.find({ _id: { $gt: last_id } })
  .sort({ _id: 1 })
  .limit(10);

// Or use timestamp-based
db.users.find({ created_at: { $lt: last_timestamp } })
  .sort({ created_at: -1 })
  .limit(10);
```

Range-based is O(n) for last item, not O(n*pageSize), much faster.

-----

### 3.3 Indexing in MongoDB

**Q38: How do compound indexes work in MongoDB, and how does field order affect query performance?**

A: Compound indexes index multiple fields together. Field order matters for query optimization:

```javascript
// Create compound index
db.users.createIndex({ country: 1, age: -1, name: 1 });

// This index is BEST for queries using country first
db.users.find({ country: "USA", age: { $gt: 30 } });

// This uses the index but less efficiently
db.users.find({ age: { $gt: 30 } });  // Can't use country

// This query needs its own index (doesn't use compound)
db.users.find({ name: "John" });
```

**ESR rule** (Equality, Sort, Range) for optimal compound indexes:

```javascript
// Query: find(age: {$gt: 30}, country: "USA").sort(salary: -1)
// Optimal index: country (equality), salary (sort), age (range)
db.users.createIndex({ country: 1, salary: -1, age: 1 });
```

**Q39: What is the difference between a sparse index and a partial index in MongoDB?**

A:

- **Sparse index**: Omits documents where the indexed field is missing/null
- **Partial index**: Includes documents matching a filter condition

```javascript
// Sparse: Only index documents with email field
db.users.createIndex({ email: 1 }, { sparse: true });
// Documents without email field are excluded

// Partial: Index only active users
db.users.createIndex(
  { email: 1 },
  { partialFilterExpression: { status: "active" } }
);
// Smaller index, faster inserts on inactive docs
```

Use sparse for optional fields; partial for subsets of data.

**Q40: How do you analyze query performance in MongoDB using explain()?**

A: The `explain()` method shows execution statistics:

```javascript
db.users.find({ email: "john@example.com" }).explain("executionStats");
// Returns:
// {
//   executionStats: {
//     executionStages: {
//       stage: "COLLSCAN",  // Full collection scan = bad
//       nReturned: 1,
//       executionTimeMillis: 50,
//       totalDocsExamined: 1000000
//     }
//   }
// }
```

Key metrics:

- **Stage**: COLLSCAN (bad), IXSCAN (good), FETCH
- **nReturned vs totalDocsExamined**: Should be close (ratio ~1)
- **executionTimeMillis**: Time to execute

If COLLSCAN appears, add an index:

```javascript
db.users.createIndex({ email: 1 });
```

-----

### 3.4 Transactions and Atomicity

**Q41: How do multi-document transactions work in MongoDB, and what are their limitations compared to relational databases?**

A: MongoDB 4.0+ supports ACID transactions across multiple documents using sessions:

```javascript
const session = db.getMongo().startSession();
session.startTransaction();
try {
  db.users.updateOne({ _id: 1 }, { $inc: { balance: -100 } }, { session });
  db.users.updateOne({ _id: 2 }, { $inc: { balance: +100 } }, { session });
  session.commitTransaction();
} catch (error) {
  session.abortTransaction();
  throw error;
}
session.endSession();
```

Limitations:

- **Only on replica sets**: Not available on sharded clusters (MongoDB 4.0)
- **Slower than relational**: No decades of optimization
- **Oplog size**: Large transactions can exceed oplog
- **Blocking**: Like 2PC in relational databases
- **Limited to 16 MB**: Transaction data size limit

Prefer embedding/denormalization to avoid multi-document transactions.

**Q42: What is the difference between implicit and explicit transactions in MongoDB?**

A:

- **Implicit**: Single document is atomic by default (within MongoDB 4.0)
- **Explicit**: Multi-document transactions with session control

```javascript
// Implicit: Atomic by default
db.users.updateOne({ _id: 1 }, {
  $set: { name: "John" },
  $inc: { age: 1 },
  $push: { tags: "admin" }
});  // All operations atomic

// Explicit: Control across multiple documents
session.startTransaction();
db.users.updateOne({ _id: 1 }, { $inc: { balance: -100 } }, { session });
db.audit.insertOne({ action: "transfer", amount: 100 }, { session });
session.commitTransaction();
```

For most use cases, implicit (single document) atomicity is sufficient if you denormalize properly.

-----

### 3.5 Data Validation and Schema Design

**Q43: How do you enforce schema validation in MongoDB despite its schema-less nature?**

A: Use JSON schema validation:

```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["_id", "name", "email"],
      properties: {
        _id: { bsonType: "objectId" },
        name: { bsonType: "string" },
        email: { bsonType: "string", pattern: "^[^@]+@[^@]+$" },
        age: {
          bsonType: "int",
          minimum: 0,
          maximum: 150
        },
        addresses: {
          bsonType: "array",
          items: {
            bsonType: "object",
            properties: {
              street: { bsonType: "string" },
              city: { bsonType: "string" }
            }
          }
        }
      }
    }
  },
  validationAction: "error"  // Reject invalid documents
});
```

Validation modes:

- **strict**: Apply to all inserts/updates
- **moderate**: Apply to existing valid documents

**Q44: What is the difference between schema design in MongoDB vs relational databases, and what anti-patterns should you avoid?**

A: MongoDB schema design principles:

- **Normalize by default**: Don’t automatically embed
- **Embed for read performance**: Only if accessed together
- **Denormalize for write safety**: Reduce need for transactions
- **Consider update patterns**: Embedding causes duplicate updates

Common anti-patterns:

1. **Over-embedding**: Creating 16 MB+ documents
1. **Always embedding**: Not everything should be embedded
1. **Unbounded arrays**: No growth controls
1. **Ignoring data types**: Everything is a string
1. **Not indexing frequently queried fields**: No filters are slow

**Example**: E-commerce system

```javascript
// GOOD: Separate concerns
db.users.insertOne({
  _id: 1,
  name: "John",
  email: "john@example.com"
});

db.orders.insertOne({
  _id: "order:123",
  user_id: 1,
  items: [
    { product_id: "prod:456", quantity: 2, price: 50 }
  ],
  total: 100
});

// BAD: Over-normalized
// db.users.insertOne({
//   _id: 1,
//   name: "John",
//   orders: [{ _id: "order:123", items: [...], total: 100 }]  // Unbounded growth
// });
```

-----

### 3.6 Performance and Scalability

**Q45: How does sharding work in MongoDB, and what are the implications of shard key selection?**

A: Sharding distributes data across multiple servers. A shard key determines how documents are distributed:

```javascript
// Enable sharding
sh.enableSharding("myapp");

// Create shard key
db.users.createIndex({ user_id: 1 });
sh.shardCollection("myapp.users", { user_id: 1 });
```

Good shard key characteristics:

- **High cardinality**: Many unique values (avoid small ranges)
- **Distributed writes**: Avoid hot shards
- **Queryable**: Queries can target specific shards efficiently

Bad shard key selection:

```javascript
// BAD: Status has only 3 values (hot shards, uneven distribution)
sh.shardCollection("myapp.users", { status: 1 });

// GOOD: user_id has high cardinality
sh.shardCollection("myapp.users", { user_id: 1 });

// GOOD: Compound shard key (status + timestamp)
sh.shardCollection("myapp.logs", { severity: 1, timestamp: 1 });
```

Shard key impacts:

- **Query performance**: Queries not on shard key are scattered-gathered (slow)
- **Write distribution**: Good key balances loads; bad key causes hot shards
- **Immutability**: Shard key cannot be changed

**Q46: How would you handle querying across shards efficiently?**

A: Sharded queries can be:

- **Targeted**: Shard key in filter (fast, hits one shard)
- **Scattered-gathered**: No shard key, hits all shards (slow)

```javascript
// GOOD: Targeted query, uses shard key
db.users.find({ user_id: 123 });  // Fast, hits one shard

// BAD: Scattered-gathered, hits all shards
db.users.find({ email: "john@example.com" });  // Slow, scans all shards

// SOLUTION: Add secondary index and maintain reference
db.users.createIndex({ email: 1, user_id: 1 });
// Query becomes: find({ email: "john@example.com" }) -> extract user_id -> find({ user_id })
```

For scattered queries, options:

- Add shard key to query filter
- Denormalize shard key into query path
- Accept slower performance or redesign queries

**Q47: How do replica sets and shards differ, and when would you use each?**

A:

- **Replica sets**: Replication for HA, all data available on each node
- **Shards**: Partitioning for scale, data distributed across nodes

```javascript
// Replica set: 3 nodes, all have full data
// Primary: Accepts writes
// Secondary: Read-only, replicate from primary
// Arbiter: Votes in elections, no data

// Sharded cluster: Data partitioned
// Shard 1: user_id 1-1000000
// Shard 2: user_id 1000001-2000000
// Each shard can be a replica set (shard + HA)
```

Use cases:

- **Replica set alone**: Dataset fits on one machine, HA needed
- **Sharding**: Dataset too large for one machine, distributed load needed
- **Both**: Large dataset + HA (sharded cluster where each shard is a replica set)

-----

### 3.7 Advanced MongoDB Concepts

**Q48: What are bulk operations in MongoDB, and when should you use them?**

A: Bulk operations group writes for efficiency:

```javascript
// Individual inserts: Slow
for (let i = 0; i < 1000; i++) {
  db.users.insertOne({ name: `User ${i}` });
}

// Bulk insert: Much faster
db.users.insertMany([
  { name: "User 1" },
  { name: "User 2" },
  // ...
]);

// Bulk with mixed operations
const bulk = db.users.initializeUnorderedBulkOp();
bulk.insert({ name: "User 1" });
bulk.find({ _id: 1 }).update({ $set: { status: "active" } });
bulk.find({ _id: 2 }).removeOne();
bulk.execute();
```

Benefits:

- **Reduced round-trips**: One network request per batch
- **Server-side optimization**: Database processes batch efficiently
- **Ordered vs unordered**: Ordered stops on first error; unordered continues

Use for bulk imports/updates; not for real-time operations.

**Q49: How do you implement full-text search in MongoDB efficiently?**

A: MongoDB supports full-text search indexes:

```javascript
// Create full-text index
db.articles.createIndex({ title: "text", content: "text" });

// Simple search
db.articles.find({ $text: { $search: "mongodb" } });

// Complex search with weights
db.articles.createIndex(
  { title: "text", content: "text" },
  { weights: { title: 10, content: 1 } }  // title matches weighted 10x
);

// Phrase search
db.articles.find({ $text: { $search: "\"machine learning\"" } });

// Exclude terms
db.articles.find({ $text: { $search: "mongodb -python" } });  // Has mongodb, not python
```

Limitations:

- Doesn’t support fuzzy matching
- Not optimized for large text (use Elasticsearch for serious full-text search)
- One text index per collection only

**Q50: What is geospatial indexing in MongoDB, and how would you query location-based data?**

A: MongoDB supports geospatial queries with 2dsphere indexes:

```javascript
// Create geospatial index
db.restaurants.createIndex({ location: "2dsphere" });

// Insert data with GeoJSON
db.restaurants.insertOne({
  name: "Pizza Place",
  location: {
    type: "Point",
    coordinates: [-73.97, 40.77]  // [longitude, latitude]
  }
});

// Find restaurants near a point
db.restaurants.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [-73.9, 40.7]
      },
      $maxDistance: 5000  // 5000 meters
    }
  }
});

// Find within a polygon (city boundary)
db.restaurants.find({
  location: {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [[...coordinates...]]
      }
    }
  }
});
```

Query operators:

- `$near`: Within distance, returns sorted by distance
- `$geoWithin`: Within region
- `$geoIntersects`: Overlaps geometry

-----

## Section 4: Cross-Database Concepts

### 4.1 Comparative Questions

**Q51: When would you choose PostgreSQL over MongoDB, and vice versa?**

A:
**PostgreSQL for:**

- Highly structured data (users, orders, transactions)
- Complex queries with multiple JOINs
- ACID transactions critical
- Data consistency paramount
- Relational integrity (foreign keys)
- Complex reporting/analytics

**MongoDB for:**

- Semi-structured data (varied documents)
- Rapid schema evolution
- High write throughput
- Simple queries on single collections
- Flexible/evolving data model
- Horizontal scaling (sharding)

Example: A bank uses PostgreSQL (transactions critical); a social network uses MongoDB (flexible post format, massive scale).

**Q52: What is polyglot persistence, and how would you design a system using multiple databases?**

A: Polyglot persistence means using different databases for different concerns:

```
User Service: PostgreSQL (relational, consistent)
  ↓
Product Service: MongoDB (flexible catalog)
  ↓
Search Service: Elasticsearch (full-text, analytics)
  ↓
Cache Layer: Redis (sessions, real-time)
```

Design principles:

- **Choose per concern**: Each DB optimized for its use case
- **Data synchronization**: Keep systems in sync (event streaming, dual-writes with care)
- **Consistency model**: Accept eventual consistency across systems
- **Operational complexity**: More databases = more to operate

Example architecture:

```
Orders (PostgreSQL) → Order Events (Kafka) 
  → Analytics (Redshift) 
  → Search (Elasticsearch)
  → Cache (Redis)
```

**Q53: How do you handle cross-database transactions in a polyglot system?**

A: No distributed transactions across different databases. Use saga pattern:

```javascript
// Choreography: Each service listens to events
// Place Order (PostgreSQL):
orders.insertOne({ user_id: 1, amount: 100 });
emit("order.placed", { user_id: 1, amount: 100 });

// Payment Service listens:
kafka.on("order.placed", async (event) => {
  try {
    await paymentDB.charge(event.user_id, event.amount);
    emit("payment.completed", { order_id: event.order_id });
  } catch (error) {
    emit("payment.failed", { order_id: event.order_id });
  }
});

// Inventory Service listens:
kafka.on("payment.completed", async (event) => {
  try {
    await inventoryDB.reserveItems(event.items);
    emit("order.confirmed", { order_id: event.order_id });
  } catch (error) {
    emit("inventory.failed", { order_id: event.order_id });
    // Compensating transaction: reverse payment
    emit("payment.refund", { order_id: event.order_id });
  }
});
```

Challenges:

- **Complexity**: Hard to reason about distributed flows
- **No atomicity**: Partial failures require compensating transactions
- **Eventual consistency**: Accepts temporary inconsistency

-----

## Section 5: Architecture and System Design Questions

**Q54: How would you design a database schema for a social media platform supporting 1 billion users?**

A: Consider:

- **Sharding strategy**: User-based sharding for locality
- **Denormalization**: Store frequently accessed data together
- **Time-series data**: Separate hot (recent) from cold (old) data

```
Tables/Collections:
├── Users (PostgreSQL)
│   ├── PK: user_id (shard key)
│   ├── name, email, profile
│   └── Recent activity summary
│
├── Posts (MongoDB sharded on user_id)
│   ├── _id: post_id
│   ├── user_id (shard key)
│   ├── content, media_urls
│   ├── like_count (denormalized)
│   └── recent_comments (embedded, limited size)
│
├── Likes (Time-series, partitioned by date)
│   ├── post_id, user_id
│   ├── created_at
│   └── Partitioned: likes_2024_01, likes_2024_02...
│
├── Comments (MongoDB or PostgreSQL)
│   ├── post_id (shard key/partition key)
│   ├── comment_id
│   └── content
│
└── Feeds (Redis cache + async computation)
    ├── user_id:feed → List of recent post_ids
    └── Computed periodically from Posts/Follows
```

Optimization techniques:

- **Caching**: Redis for feeds, sessions
- **Async**: Compute feeds offline
- **Partitioning**: Hot/cold data separation
- **Eventual consistency**: Accept feed staleness

**Q55: Design a database for a real-time messaging/chat application with billions of messages.**

A: Handle real-time, massive scale:

```
Architecture:
├── User metadata (PostgreSQL)
│   ├── user_id, name, avatar
│   └── Single master, replicated
│
├── Messages (MongoDB sharded on room_id)
│   ├── _id: message_id
│   ├── room_id (shard key)
│   ├── user_id, content
│   ├── created_at (index for sorting)
│   ├── TTL index: Auto-delete old messages
│   └── Shard by room_id for locality
│
├── Room metadata (Redis + PostgreSQL)
│   ├── room_id, name, participants
│   └── Redis for in-memory access
│
├── Unread counts (Redis)
│   ├── user_id:unread:room_id → count
│   └── Efficient increments
│
└── Real-time layer (WebSocket + message queue)
    ├── Active connections (Redis Pub/Sub)
    └── Message delivery (Kafka/RabbitMQ)
```

Challenges and solutions:

- **Pagination**: Use timestamp-based (efficient for billions)
- **Unread counts**: Use Redis for fast increments
- **Sorting/ordering**: Index on created_at in MongoDB
- **Room presence**: Redis for online status
- **Message delivery**: Kafka/RabbitMQ for reliability

```javascript
// Message insertion
db.messages.insertOne({
  _id: ObjectId(),
  room_id: "room:123",  // shard key
  user_id: "user:456",
  content: "Hello!",
  created_at: new Date()
});

// Create TTL index to auto-delete after 30 days
db.messages.createIndex({ created_at: 1 }, { expireAfterSeconds: 2592000 });

// Get recent messages (timestamp-based pagination)
db.messages.find({
  room_id: "room:123",
  created_at: { $lt: last_timestamp }
})
.sort({ created_at: -1 })
.limit(50);
```

**Q56: Design a database schema for an e-commerce platform with product catalog, inventory, and orders.**

A:

```
Structure:
├── Products (MongoDB, denormalized for reads)
│   ├── _id: product_id
│   ├── name, description, price
│   ├── category, tags
│   ├── inventory: { available: 100, reserved: 10 }
│   ├── ratings (embedded, aggregated)
│   └── Indexed: category, tags, price
│
├── Orders (PostgreSQL, transactional)
│   ├── PK: order_id
│   ├── user_id (FK)
│   ├── status, total, created_at
│   ├── Indexed: user_id, created_at
│   └── Replicated for HA
│
├── Order Items (PostgreSQL)
│   ├── PK: (order_id, product_id)
│   ├── quantity, unit_price
│   └── product_id (denormalized snapshot)
│
├── Inventory (PostgreSQL, transactional)
│   ├── PK: product_id
│   ├── total, available, reserved
│   └── Version for optimistic locking
│
├── Cart (Redis)
│   ├── user_id:cart → { product_id: quantity, ... }
│   └── Session-based, auto-expiring
│
├── Search (Elasticsearch)
│   ├── Synced from product database
│   └── Full-text + faceted search
│
└── Reviews (MongoDB or PostgreSQL)
    ├── product_id (index)
    ├── user_id, rating, comment
    └── created_at (for sorting)
```

Transaction flow (Order):

```sql
-- PostgreSQL transaction
BEGIN;
-- 1. Deduct inventory
UPDATE inventory SET available = available - 1, reserved = reserved + 1 
WHERE product_id = 123 AND available >= 1;

-- 2. Create order
INSERT INTO orders (user_id, status, total, created_at)
VALUES (1, 'pending', 99.99, NOW());

-- 3. Add order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (1, 123, 1, 99.99);

-- 4. Clear cart
-- DELETE FROM cart WHERE user_id = 1;  -- Or use Redis

COMMIT;
```

-----

## Summary

This comprehensive Q&A covers:

- **DBMS foundations**: ACID, transactions, concurrency, indexing
- **PostgreSQL expertise**: Query optimization, window functions, replication
- **MongoDB mastery**: Document design, sharding, aggregation
- **System design**: Real-world architecture decisions

Key takeaways:

1. Understand trade-offs (consistency vs availability, normalization vs denormalization)
1. Know your tools intimately (EXPLAIN ANALYZE, explain(), query plans)
1. Design for scale (sharding, partitioning, replication)
1. Choose the right database for the use case (polyglot persistence)
1. Always optimize for your specific workload patterns