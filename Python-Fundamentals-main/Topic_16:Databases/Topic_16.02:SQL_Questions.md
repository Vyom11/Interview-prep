# Level 1: Beginner (DBMS & PostgreSQL Basics)

**Q1: What is a DBMS, and why use it over a standard file system?**
* **Answer:** A Database Management System (DBMS) is software used to store, retrieve, and manage data securely and efficiently. Unlike standard file systems, a DBMS provides data integrity, concurrency control (multiple users accessing data simultaneously without conflict), security, crash recovery, and a standardized querying language (like SQL) to manipulate data easily.

**Q2: What is PostgreSQL, and what makes it different from other databases like MySQL?**
* **Answer:** PostgreSQL is an open-source Object-Relational Database Management System (ORDBMS) known for its robustness, extensibility, and strict SQL compliance. Unlike MySQL, which historically focused primarily on speed for read-heavy web apps, PostgreSQL was designed with complex queries, data integrity, and advanced data types (like JSONB, arrays, and custom types) in mind. It supports advanced features like table inheritance and custom functions in multiple languages (PL/pgSQL, Python, etc.).

**Q3: Explain the differences between DDL, DML, DCL, and TCL in SQL.**
* **Answer:** 
  * **DDL (Data Definition Language):** Defines the database structure. (*CREATE, ALTER, DROP, TRUNCATE*)
  * **DML (Data Manipulation Language):** Manipulates the data inside the tables. (*INSERT, UPDATE, DELETE*)
  * **DCL (Data Control Language):** Controls access to the data. (*GRANT, REVOKE*)
  * **TCL (Transaction Control Language):** Manages transactions. (*COMMIT, ROLLBACK, SAVEPOINT*)

**Q4: What are Primary Keys and Foreign Keys?**
* **Answer:** 
  * A **Primary Key** is a column (or set of columns) that uniquely identifies each row in a table. It cannot contain NULL values.
  * A **Foreign Key** is a column that creates a relationship between two tables. It references the Primary Key of another table, ensuring referential integrity (meaning you cannot add a record to a table that refers to a non-existent record in the referenced table).

---

# Level 2: Intermediate (SQL Mastery & Relational Concepts)

**Q5: What are the ACID properties? How does PostgreSQL ensure them?**
* **Answer:** ACID stands for Atomicity, Consistency, Isolation, and Durability.
  * **Atomicity:** All parts of a transaction succeed, or none do. PostgreSQL ensures this via the Write-Ahead Log (WAL).
  * **Consistency:** Data must meet all defined rules (constraints, cascades). PostgreSQL enforces this via constraints and triggers.
  * **Isolation:** Concurrent transactions don't interfere with each other. PostgreSQL handles this via MVCC (Multi-Version Concurrency Control).
  * **Durability:** Committed data is permanently saved, even in a crash. PostgreSQL achieves this by writing to the WAL before returning a success signal to the user.

**Q6: What is an index? What is the default index type in PostgreSQL?**
* **Answer:** An index is a database object that improves the speed of data retrieval operations at the cost of additional storage and slower write operations (since the index must be updated on INSERT/UPDATE/DELETE). The default index type in PostgreSQL is the **B-Tree** (Balanced Tree), which is highly optimized for sorting, equality (`=`), and range queries (`<`, `>`, `BETWEEN`).

**Q7: Explain the difference between `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and `FULL OUTER JOIN`.**
* **Answer:**
  * **INNER JOIN:** Returns only the rows that have matching values in both tables.
  * **LEFT JOIN:** Returns all rows from the left table, and the matched rows from the right table. Unmatched right rows return NULL.
  * **RIGHT JOIN:** Returns all rows from the right table, and the matched rows from the left. Unmatched left rows return NULL.
  * **FULL OUTER JOIN:** Returns all rows when there is a match in either the left or right table. Unmatched rows on either side return NULL.

**Q8: What are Views and Materialized Views in PostgreSQL?**
* **Answer:** 
  * A **View** is a virtual table representing the result of a saved query. It does not store data itself; it runs the underlying query every time the view is accessed.
  * A **Materialized View** physically stores the result of the query on disk. It allows for much faster read performance but must be manually refreshed (`REFRESH MATERIALIZED VIEW`) when the underlying base tables change.

---

# Level 3: Advanced (Internals, Performance Tuning & DBA)

**Q9: Explain MVCC (Multi-Version Concurrency Control) in PostgreSQL.**
* **Answer:** MVCC is how PostgreSQL handles database concurrency. Instead of locking a table or row when reading/writing, PostgreSQL creates a new version of the row for an `UPDATE` and marks the old row as dead. Readers continue to read the old version of the row until the transaction commits. This means "readers never block writers, and writers never block readers," allowing high throughput.

**Q10: What is the purpose of `VACUUM` and `ANALYZE`?**
* **Answer:** 
  * **VACUUM:** Because of MVCC, updated or deleted rows leave behind "dead tuples" on the disk. `VACUUM` reclaims the storage space occupied by these dead tuples so it can be reused. `VACUUM FULL` aggressively rewrites the table to return space to the OS (requiring a full table lock).
  * **ANALYZE:** Collects statistics about the contents of tables and stores them in the system catalogs. The Query Planner uses these statistics to determine the most efficient execution plan (e.g., whether to use an index scan or a sequential scan).

**Q11: How do you interpret an `EXPLAIN ANALYZE` output?**
* **Answer:** `EXPLAIN` shows the execution plan the query optimizer generated. Adding `ANALYZE` actually executes the query and compares the estimated costs with actual execution times. 
  Key things to look for:
  * **Sequential Scans (Seq Scan):** If this occurs on a large table, an index might be missing.
  * **Cost:** Shown as `cost=startup_cost..total_cost`. It’s an arbitrary unit of computation.
  * **Actual Time:** `time=startup_time..total_time`. Shows real milliseconds taken.
  * **Loops:** How many times a specific node was executed.
  * Look for "Filter" rows discarding massive amounts of data, indicating poor index usage.

**Q12: Describe Table Partitioning in PostgreSQL and its benefits.**
* **Answer:** Table partitioning is the splitting of one large logical table into smaller physical tables (partitions). PostgreSQL supports Range, List, and Hash partitioning. 
  * **Benefits:** Query performance drastically improves due to "partition pruning" (the planner skips scanning partitions that don't match the query condition). Bulk deletes become as simple and fast as `DROP TABLE` on a partition. It is highly beneficial for time-series data.

---

# Level 4: Senior AI/ML Engineer Level (Vector DBs, Scaling, RAG, and ML Pipelines)

**Q13: What is `pgvector`, and how does it fit into a Retrieval-Augmented Generation (RAG) pipeline?**
* **Answer:** `pgvector` is an open-source extension for PostgreSQL that allows it to store, query, and index high-dimensional vector embeddings (generated by models like OpenAI's `text-embedding-ada-002` or HuggingFace transformers). 
  In a RAG pipeline, LLMs need contextual data to answer questions accurately without hallucination. An AI engineer will chunk documents, generate embeddings, and store them in PostgreSQL via `pgvector`. When a user asks a question, the query is embedded, and `pgvector` performs a similarity search (using Cosine Similarity, Euclidean distance, or Inner Product) to retrieve the most contextually relevant chunks from the database to feed into the LLM prompt.

**Q14: Explain the difference between IVFFlat and HNSW indexes in `pgvector`. When would you use which?**
* **Answer:** 
  * **IVFFlat (Inverted File with Flat Compression):** Divides the vector space into clusters (lists). During a search, it only compares the query vector to the centroids of the clusters, and then searches within the nearest clusters. It is fast to build and uses less memory, but suffers in recall (accuracy) and requires the table to be populated before building the index to calculate good centroids.
  * **HNSW (Hierarchical Navigable Small World):** A graph-based index that builds multiple layers of interconnected vectors. It offers vastly superior query speed and recall compared to IVFFlat, and handles dynamic data (inserts/updates) without degrading performance. 
  * **Usage:** As a Senior AI Engineer, you almost always default to **HNSW** for modern production RAG applications because of its high recall and query speed, tolerating the trade-off that HNSW consumes more RAM and takes longer to build.

**Q15: How do you handle unstructured/semi-structured feature data and model metadata in PostgreSQL efficiently?**
* **Answer:** PostgreSQL’s `JSONB` data type is highly effective for storing semi-structured metadata (e.g., dynamic model hyperparameters, experiment tracking configs, or sparse feature dictionaries). 
  To do this efficiently at scale:
  * Use **GIN (Generalized Inverted Index)** indexes on the `JSONB` columns to allow sub-millisecond querying of keys/values inside the JSON (e.g., `CREATE INDEX idx_metadata ON models USING GIN (metadata);`).
  * Combine `JSONB` with relational data. Keep highly queried, structured features as native relational columns, and relegate flexible, sparse, or changing schemas to `JSONB`.

**Q16: Design a feature-serving layer using PostgreSQL for a low-latency real-time ML inference system.**
* **Answer:** For real-time inference (e.g., fraud detection), features must be served in milliseconds. A robust architecture involves:
  * **Connection Pooling:** Use PgBouncer to manage thousands of concurrent connections from stateless inference microservices without overwhelming Postgres.
  * **Read Replicas:** Route heavy analytical training queries to a replica database, reserving the primary database for fast writes and real-time read traffic.
  * **Materialized Views / Pre-computation:** Use materialized views to aggregate batch features (e.g., "user's total spend in 30 days") overnight. 
  * **Caching:** Put Redis in front of Postgres. When the model requests a feature vector, it checks Redis. If there's a cache miss, it queries Postgres, returns the data, and populates Redis.
  * **Indexing:** Ensure all lookup keys (e.g., `user_id`) have B-Tree indexes.

**Q17: How would you use PostgreSQL’s `LISTEN` and `NOTIFY` in an asynchronous ML pipeline?**
* **Answer:** `LISTEN`/`NOTIFY` enables lightweight, real-time event-driven architectures without needing external message brokers like Kafka or RabbitMQ for simpler pipelines.
  * **Architecture:** Suppose an application inserts an image path into a `raw_images` table. You can attach a database Trigger that executes `NOTIFY process_image, '{"id": 123}'` upon `INSERT`.
  * **ML Worker:** A Python worker (using `psycopg2` or `asyncpg`) maintains a persistent connection with a `LISTEN process_image` command. It instantly receives the payload, pulls the image, runs inference (e.g., object detection), and writes the bounding boxes back to an `inference_results` table. This drastically reduces latency compared to the worker constantly polling the database with `SELECT * FROM images WHERE processed = false`.

---

# Level 5: Real-World Scenarios (Applied Knowledge)

**Q18: (Beginner/Intermediate Scenario) You are building an e-commerce checkout. A customer pays for an item, but the database crashes right before the query runs to decrement the item's inventory count. How do you ensure the customer isn't charged for an item that wasn't removed from inventory?**
* **Answer:** This is a classic TCL (Transaction Control Language) scenario. Both the payment logging and the inventory update must be wrapped in a single database **transaction** block using `BEGIN;` and `COMMIT;`. If the database crashes or an error occurs halfway through, PostgreSQL uses its Write-Ahead Log (WAL) to automatically `ROLLBACK` the incomplete transaction. This guarantees the **Atomicity** property of ACID—either all steps succeed, or none of them are applied to the database.

**Q19: (Intermediate/Advanced Scenario) A marketing dashboard features a query: `SELECT * FROM orders WHERE status = 'pending' AND created_at > '2025-01-01'`. The table has 50 million rows, and the dashboard is taking 15 seconds to load. How would you troubleshoot and optimize this?**
* **Answer:** 
  1. **Troubleshoot:** Run `EXPLAIN ANALYZE` on the query. I would likely see a `Seq Scan` (Sequential Scan), meaning PostgreSQL is reading all 50 million rows to find the matches.
  2. **Optimize:** I would create a **Composite B-Tree Index** on both columns: `CREATE INDEX idx_orders_status_date ON orders (status, created_at);`.
  3. **Alternative (Partial Index):** If we only ever query for 'pending' orders on this dashboard, a highly efficient partial index would be better: `CREATE INDEX idx_pending_orders ON orders (created_at) WHERE status = 'pending';`. This takes up a fraction of the disk space and makes the query virtually instantaneous.

**Q20: (Advanced Scenario) Your application logs user events into a `user_activity` table. It currently generates 5 million rows daily. After 6 months, inserts are slowing down, disks are filling up, and running analytical queries times out. Deleting old data locks the table. What architectural changes do you make?**
* **Answer:** The table has grown too large for a single logical structure. 
  1. **Table Partitioning:** I would implement declarative time-based partitioning (e.g., partitioning by day or month on the `created_at` column). 
  2. **Automated Maintenance:** Use extensions like `pg_partman` to automatically create partitions for upcoming months.
  3. **Data Lifecycle:** Instead of running heavy `DELETE` statements (which create dead tuples and trigger massive `VACUUM` loads), I can simply `DROP TABLE` on partitions older than 6 months. This instantly frees up OS disk space with zero locking overhead. 
  4. **Archiving:** Before dropping, old partitions can be backed up to cheaper object storage (like AWS S3) for historical analytical needs.

**Q21: (Senior AI/ML Scenario) You deployed a RAG chatbot using `pgvector`. It was lightning fast during testing with 10,000 document chunks. However, in production with 10 million chunks, the exact nearest neighbor (KNN) vector searches are taking 3 seconds and causing LLM timeouts. What steps do you take to fix this?**
* **Answer:** The system is struggling because it's doing an exact KNN search (calculating the distance between the user's query vector and *all* 10 million vectors). To fix this:
  1. **Add an Approximate Nearest Neighbor (ANN) Index:** I would create an HNSW index on the vector column (`CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);`). HNSW searches a multi-layer graph instead of scanning all rows, dropping latency from seconds to milliseconds.
  2. **Tune Index Parameters:** I would adjust `m` (max connections per layer) and `ef_construction` during index creation based on the recall-vs-speed trade-off needed. 
  3. **Pre-filtering / Hybrid Search:** If the user is querying a specific document, I would filter by relational metadata *before* doing vector math. *Note:* In `pgvector` > 0.5.0, HNSW supports efficient pre-filtering, so combining a standard B-Tree index on `document_id` with the HNSW index will massively speed up the query.

**Q22: (Senior AI/ML Scenario) You have an overnight batch ML pipeline that predicts user churn scores for 5 million active users. Writing the predictions back to the live `user_features` table using standard `UPDATE` statements is taking hours, locking rows, and causing production latency. How do you optimize this massive bulk update?**
* **Answer:** Doing 5 million individual `UPDATE` statements incurs massive network round-trip overhead and transaction logging. I would refactor the pipeline as follows:
  1. **Temporary Staging Table:** Have the ML worker use PostgreSQL's `COPY` command (via `psycopg2.extras.execute_values` or similar) to bulk-insert all 5 million predictions into an unlogged temporary staging table (`temp_churn_predictions`). `COPY` bypasses much of the standard SQL overhead and is blazing fast.
  2. **Bulk Update / Upsert:** Execute a single, massive SQL statement that updates the live table by joining it to the staging table: 
     `UPDATE user_features uf SET churn_score = tmp.score FROM temp_churn_predictions tmp WHERE uf.user_id = tmp.user_id;`
  3. **Alternative (Partition Swapping):** If the feature table is completely rewritten nightly, I would write the new predictions to a brand new table, build the indexes on the new table, and then do a virtually instant table rename (e.g., `ALTER TABLE user_features RENAME TO user_features_old; ALTER TABLE new_features RENAME TO user_features;`) to avoid updates altogether.
