# MongoDB Interview Questions & Answers  
## From Beginner to Senior Engineer Level

***

## Table of Contents

1. [Beginner Level Questions](#beginner-level-questions)
2. [Intermediate Level Questions](#intermediate-level-questions)
3. [Senior Engineer Level Questions](#senior-engineer-level-questions)
4. [Real-World Scenario-Based Questions](#real-world-scenario-based-questions)
5. [System Design & Architecture Questions](#system-design--architecture-questions)
6. [Troubleshooting & Operational Questions](#troubleshooting--operational-questions)

***

## Beginner Level Questions

### Q1: What is MongoDB and how is it different from SQL databases?

**Answer:**  
MongoDB is a **NoSQL, document-oriented database** that stores data in flexible, JSON-like documents called **BSON** (Binary JSON). [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

**Key differences:**

| Aspect | SQL Database | MongoDB |
|--------|--------------|---------|
| **Data Model** | Tables with rows and columns | Collections with documents  [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA) |
| **Schema** | Fixed schema (must define beforehand) | Dynamic schema (flexible)  [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA) |
| **Scaling** | Vertical (bigger server) | Horizontal (add more servers via sharding)  [codecademy](https://www.codecademy.com/learn/learn-mongodb) |
| **Relationships** | JOINs across tables | Embedding and referencing documents  [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA) |
| **Query Language** | SQL | MongoDB Query Language (MQL) |

**When to use MongoDB:** Unstructured/semi-structured data, rapid development, horizontal scaling needs. [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
**When to use SQL:** Structured data, complex relationships, strict ACID requirements.

***

### Q2: What are databases, collections, and documents in MongoDB?

**Answer:**

- **Database**: A container for collections (like a database in SQL) [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
- **Collection**: A group of MongoDB documents (like a table in SQL) [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
- **Document**: A single record stored in BSON format (like a row in SQL) [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

**Example:**
```javascript
// Database: "myApp"
// Collection: "users"
// Document:
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "Vyom Pandya",
  "age": 25,
  "city": "Ahmedabad"
}
```

**Key point:** Documents in the same collection can have different fields (schema-less). [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

***

### Q3: What is BSON and why does MongoDB use it instead of JSON?

**Answer:**  
**BSON** (Binary JSON) is how MongoDB stores data internally. [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

**Why BSON over JSON:**
- **Extends JSON** with additional data types: `Date`, `ObjectId`, `BinData`, etc.
- **More efficient** for storage and traversal
- **Supports hierarchical data** with nested documents
- **Faster** to encode/decode than pure JSON

**Example:**
```javascript
// JSON would represent this as a string
// BSON stores it as actual Date type
{
  "createdAt": Date("2026-05-29T10:00:00Z"),
  "userId": ObjectId("507f1f77bcf86cd799439011")
}
```

***

### Q4: Write a query to insert, find, update, and delete a document.

**Answer:**

```javascript
// INSERT
db.users.insertOne({
  name: "Alice",
  age: 28,
  city: "Mumbai"
});

// FIND
db.users.find({ city: "Mumbai" });
db.users.findOne({ name: "Alice" });

// UPDATE
db.users.updateOne(
  { name: "Alice" },
  { $set: { age: 29 } }
);

// DELETE
db.users.deleteOne({ name: "Alice" });
```

**Key operators:**
- `$set`: Update specific field
- `$inc`: Increment value
- `$push`: Add to array
- `$pull`: Remove from array [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

***

### Q5: What are MongoDB indexes and why are they important?

**Answer:**  
**Indexes** are special data structures that speed up query operations by allowing MongoDB to find documents without scanning the entire collection. [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

**Without index:** Collection scan (COLLSCAN) → Slow  
**With index:** Index scan (IXSCAN) → Fast

**Example:**
```javascript
// Create index on "city" field
db.users.createIndex({ city: 1 });

// Query will use the index
db.users.find({ city: "Ahmedabad" });
```

**Types of indexes:**
- Single-field: `{ name: 1 }`
- Compound: `{ city: 1, age: -1 }`
- Text: `{ name: "text" }` for full-text search [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
- Geospatial: `{ location: "2dsphere" }`
- Unique: Prevents duplicate values [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

**Trade-off:** Indexes speed up reads but slow down writes (each index must be updated).

***

### Q6: What is the difference between `find()` and `findOne()`?

**Answer:**

| Method | Returns | Use Case |
|--------|---------|----------|
| `find()` | **Cursor** (list of documents) | Multiple matches |
| `findOne()` | **Single document** (first match) | Single match expected |

**Example:**
```javascript
// Returns cursor (can iterate)
const cursor = db.users.find({ city: "Ahmedabad" });

// Returns single document (or null)
const user = db.users.findOne({ name: "Alice" });
```

***

### Q7: What are query operators? Give examples.

**Answer:**  
**Query operators** allow you to filter documents based on conditions. [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

**Comparison operators:**
```javascript
{ age: { $gt: 25 } }       // Greater than
{ age: { $gte: 25 } }      // Greater than or equal
{ age: { $lt: 30 } }       // Less than
{ age: { $lte: 30 } }      // Less than or equal
{ age: { $eq: 25 } }       // Equal
{ age: { $ne: 25 } }       // Not equal
```

**Logical operators:**
```javascript
{ $and: [ { age: { $gt: 25 } }, { city: "Ahmedabad" } ] }
{ $or: [ { city: "Mumbai" }, { city: "Delhi" } ] }
{ $not: { age: { $gt: 30 } } }
```

**Array operators:**
```javascript
{ skills: "Python" }           // Contains "Python"
{ skills: { $all: ["Python", "MongoDB"] } }  // Contains all
```

***

### Q8: What is an aggregation pipeline?

**Answer:**  
The **aggregation framework** processes documents through a **pipeline** of stages, transforming data into aggregated results. [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

**Example:**
```javascript
db.orders.aggregate([
  { $match: { status: "completed" } },     // Filter
  { $group: {                              // Group
      _id: "$customerId",
      total: { $sum: "$amount" }
  }},
  { $sort: { total: -1 } },                // Sort
  { $limit: 10 }                           // Limit
]);
```

**Common stages:**
- `$match`: Filter documents [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
- `$group`: Group by field [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
- `$sort`: Sort results [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
- `$limit`: Limit number of documents [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
- `$project`: Reshape documents [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
- `$lookup`: Join collections [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
- `$unwind`: Deconstruct array [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

***

## Intermediate Level Questions

### Q9: What is the difference between embedding and referencing in MongoDB?

**Answer:**

**Embedding** (store related data in one document):
```javascript
{
  "_id": ObjectId("..."),
  "name": "Vyom Pandya",
  "addresses": [
    { "type": "home", "city": "Ahmedabad" },
    { "type": "work", "city": "Mumbai" }
  ]
}
```

**Referencing** (store documents separately with references):
```javascript
// User document
{ "_id": ObjectId("user123"), "name": "Vyom Pandya" }

// Address document
{ "_id": ObjectId("addr456"), "userId": ObjectId("user123"), "city": "Ahmedabad" }
```

| Factor | Embedding | Referencing |
|--------|-----------|-------------|
| **Read speed** | Faster (single query) | Slower (multiple queries or `$lookup`) |
| **Write atomicity** | Atomic (all in one document) | Not atomic across documents |
| **Document size** | Limited (16MB) | No limit |
| **Best for** | One-to-few, accessed together | One-to-many, independent access  [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA) |

**When to embed:** Data accessed together, one-to-few relationships, read-heavy. [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
**When to reference:** Large or independent data, one-to-many/many-to-many, write-heavy.

***

### Q10: How do you optimize a slow query in MongoDB?

**Answer:**

**Steps to optimize:**

1. **Check query execution plan:**
   ```javascript
   db.users.find({ city: "Ahmedabad" }).explain("executionStats");
   ```
   - Look for `IXSCAN` (good) vs `COLLSCAN` (bad) [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)
   - Check `totalDocsExamined` vs `nReturned` (should be close)

2. **Add appropriate indexes:**
   ```javascript
   db.users.createIndex({ city: 1 });
   ```

3. **Use covered queries** (all fields in index):
   ```javascript
   db.users.createIndex({ name: 1, email: 1 });
   db.users.find({ name: "Alice" }, { name: 1, email: 1, _id: 0 });
   ```

4. **Optimize aggregation:**
   - Put `$match` early in pipeline
   - Avoid `$sort` before `$match`
   - Use `$project` to limit fields early

5. **Check indexes:**
   ```javascript
   db.users.getIndexes();
   db.users.aggregate([{ $indexStats: {} }]);
   ```

***

### Q11: What is a compound index and when would you use it?

**Answer:**  
A **compound index** indexes multiple fields together.

**Example:**
```javascript
// Compound index on city and age
db.users.createIndex({ city: 1, age: -1 });
```

**When to use:**
- Queries filter by **multiple fields** together
- Queries need **sorted results** on multiple fields
- Query pattern matches index order

**Important:** Index order matters!
```javascript
// This query uses the index
db.users.find({ city: "Ahmedabad", age: { $gt: 25 } });

// This query may NOT use the index efficiently (equality on second field)
db.users.find({ age: { $gt: 25 } });
```

**Rule of thumb:** Put equality fields first, then range fields.

***

### Q12: What is `$lookup` and how is it different from SQL JOINs?

**Answer:**  
**`$lookup`** performs a **left outer join** between collections in MongoDB. [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

**Example:**
```javascript
db.users.aggregate([
  {
    $lookup: {
      from: "orders",           // Collection to join
      localField: "_id",        // Field from users
      foreignField: "userId",   // Field from orders
      as: "orders"              // Output array field
    }
  }
]);
```

**Differences from SQL JOINs:**

| Aspect | SQL JOIN | MongoDB `$lookup` |
|--------|----------|-------------------|
| **Performance** | Optimized for joins | Slower (no indexes on joined field by default) |
| **Use case** | Normalized data | Denormalized/embedded preferred |
| **Complexity** | Multiple tables | Usually avoid if possible |
| **Best practice** | Use JOINs | Embed or reference instead |

**Best practice:** Use `$lookup` sparingly; prefer embedding for frequently joined data.

***

### Q13: What are multi-document ACID transactions in MongoDB?

**Answer:**  
**Multi-document transactions** allow multiple write operations to succeed or fail together as a single atomic unit. [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

**Example:**
```javascript
const session = db.getMongo().startSession();
session.startTransaction();

try {
  // Transfer money from A to B
  db.accounts.updateOne(
    { _id: "A", balance: { $gte: 1000 } },
    { $inc: { balance: -1000 } },
    { session: session }
  );
  
  db.accounts.updateOne(
    { _id: "B" },
    { $inc: { balance: 1000 } },
    { session: session }
  );
  
  session.commitTransaction();
} catch (error) {
  session.abortTransaction();
  throw error;
} finally {
  session.endSession();
}
```

**When to use:**
- Financial transfers
- Inventory updates across locations
- Consistency across multiple documents [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

**When NOT to use:**
- Single-document updates (already atomic)
- High-throughput systems (transactions add overhead)
- When application-level consistency is sufficient [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

***

### Q14: What is replication and how does it provide high availability?

**Answer:**  
**Replication** maintains multiple copies of data across servers (replica set). [blog.stackademic](https://blog.stackademic.com/mongodb-architecture-a-complete-senior-engineer-grade-guide-0f7cd97521f6)

**Replica set architecture:**
```
Primary (writes) → Secondaries (reads/replication)
```

**Benefits:**
- **High availability**: If primary fails, secondary becomes primary
- **Data redundancy**: Protects against data loss
- **Read scaling**: Distribute reads across secondaries

**Node types:**
- **Primary**: Handles all writes
- **Secondary**: Replicates from primary, can handle reads
- **Arbiter**: Votes in elections, no data

**Failover:** When primary fails, secondaries elect a new primary automatically. [blog.stackademic](https://blog.stackademic.com/mongodb-architecture-a-complete-senior-engineer-grade-guide-0f7cd97521f6)

***

### Q15: What is sharding and when should you use it?

**Answer:**  
**Sharding** distributes data across multiple servers (shards) for horizontal scaling. [codecademy](https://www.codecademy.com/learn/learn-mongodb)

**When to shard:**
- Dataset exceeds single server capacity
- Write throughput exceeds single server capability
- Need horizontal scaling [codecademy](https://www.codecademy.com/learn/learn-mongodb)

**When NOT to shard:**
- Data fits on single server
- Complexity not justified
- Start with replica set first

**Shard key selection (critical!):**
- ✅ High cardinality (many unique values)
- ✅ Even distribution
- ✅ Often used in queries

**Bad shard keys:**
- ❌ Monotonically increasing (e.g., timestamp) → Hot shards
- ❌ Low cardinality (e.g., gender)

***

### Q16: What is write concern and read preference?

**Answer:**

**Write concern**: How many nodes must acknowledge a write: [blog.stackademic](https://blog.stackademic.com/mongodb-architecture-a-complete-senior-engineer-grade-guide-0f7cd97521f6)
```javascript
// Wait for majority of nodes
{ w: "majority" }

// Wait for specific number
{ w: 2 }

// Wait for majority + journal
{ w: "majority", j: true }
```

**Read preference**: Which replica set member serves reads: [blog.stackademic](https://blog.stackademic.com/mongodb-architecture-a-complete-senior-engineer-grade-guide-0f7cd97521f6)
- `primary`: Read from primary only (strong consistency)
- `primaryPreferred`: Primary preferred, fallback to secondary
- `secondary`: Read from secondary only (read scaling)
- `secondaryPreferred`: Secondary preferred
- `nearest`: Read from nearest member (global apps)

***

## Senior Engineer Level Questions

### Q17: Explain the WiredTiger storage engine and how it works.

**Answer:**  
**WiredTiger** is MongoDB's default storage engine (since v3.2). [blog.stackademic](https://blog.stackademic.com/mongodb-architecture-a-complete-senior-engineer-grade-guide-0f7cd97521f6)

**Key features:**
- **MVCC (Multi-Version Concurrency Control)**: Allows concurrent reads/writes without locking
- **Document-level locking**: Only locks the document being modified (not entire collection)
- **Checkpointing**: Periodic snapshots to disk
- **Cache**: In-memory cache (50% of RAM + 1GB by default)
- **Journaling**: Write-ahead log for durability

**How it works:**
1. Writes go to **cache** first
2. Periodically **checkpointed** to disk
3. **Journal** records changes for crash recovery
4. **Compression**: Snappy or zlib for storage efficiency

**Monitoring:**
```javascript
db.serverStatus().wiredTiger.cache;

// Key metrics:
// - "bytes currently in the cache"
// - "tracked dirty bytes in the cache"
// - Cache hit ratio (>99% is good)
```

***

### Q18: How do you design a schema for a social media platform with millions of users?

**Answer:**

**Design considerations:**
- High write volume (posts, likes, comments)
- High read volume (timelines, profiles)
- Scaling horizontally
- Fast query performance

**Schema design:**

```javascript
// User (embedded profile, referenced friends)
{
  "_id": ObjectId("..."),
  "username": "vyom_pandya",
  "profile": {
    "bio": "AI/ML Engineer",
    "location": "Ahmedabad"
  },
  "followers": [ObjectId("user1"), ObjectId("user2")], // Bounded array
  "followingCount": 150
}

// Post (referenced user, embedded metadata)
{
  "_id": ObjectId("..."),
  "userId": ObjectId("vyom_user"),
  "content": "Hello MongoDB!",
  "images": ["url1", "url2"],
  "metadata": {
    "likeCount": 150,
    "commentCount": 23
  },
  "createdAt": ISODate("2026-05-29")
}

// Comment (referenced post, embedded user info)
{
  "_id": ObjectId("..."),
  "postId": ObjectId("post123"),
  "userId": ObjectId("user456"),
  "userName": "Alice",          // Denormalized for fast reads
  "content": "Great post!",
  "createdAt": ISODate("2026-05-29")
}
```

**Indexing strategy:**
```javascript
db.posts.createIndex({ userId: 1, createdAt: -1 });  // User's timeline
db.posts.createIndex({ createdAt: -1 });             // Global timeline
db.comments.createIndex({ postId: 1, createdAt: 1 }); // Comments for post
```

**Sharding strategy:**
- Shard by `userId` (hashed) for even distribution
- User timeline queries target specific shard

**Optimizations:**
- Denormalize frequently accessed fields
- Use count fields instead of counting on every request
- Implement pagination with `skip`/`limit` or cursor-based
- Use change streams for real-time notifications

***

### Q19: How would you handle a scenario where your database is running out of memory?

**Answer:**

**Diagnosis:**
```javascript
// Check cache usage
db.serverStatus().wiredTiger.cache;

// Check working set size
db.stats();

// Check for slow queries
db.currentOp({ "secs_running": { $gt: 1 } });
```

**Solutions (in order of priority):**

1. **Add indexes** to reduce collection scans:
   ```javascript
   db.collection.createIndex({ frequentlyQueriedField: 1 });
   ```

2. **Optimize queries** to return fewer fields:
   ```javascript
   db.collection.find({ field: "value" }, { importantField: 1, _id: 0 });
   ```

3. **Increase RAM** on the server

4. **Reduce working set** by:
   - Archiving old data
   - Using TTL collections for temporary data
   ```javascript
   db.logs.createIndex({ createdAt: 1 }, { expireAfterSeconds: 2592000 }); // 30 days
   ```

5. **Shard the collection** to distribute data across servers [codecademy](https://www.codecademy.com/learn/learn-mongodb)

6. **Tune WiredTiger cache** (if using dedicated instance):
   ```bash
   # mongod.conf
   storage:
     wiredTiger:
       engineConfig:
         cacheSizeGB: 16  # Adjust based on available RAM
   ```

7. **Monitor and alert** on memory usage

**Prevention:**
- Regular monitoring of cache hit ratio
- Query performance testing before deployment
- Capacity planning based on growth projections

***

### Q20: How do you ensure data consistency across multiple collections in a distributed system?

**Answer:**

**Approaches (in order of preference):**

1. **Single-document atomicity** (preferred):
   - Embed related data in one document
   - MongoDB guarantees atomicity at document level

2. **Multi-document transactions** (if necessary):
   ```javascript
   const session = db.getMongo().startSession();
   session.startTransaction();
   try {
     // Multiple updates
     session.commitTransaction();
   } catch (e) {
     session.abortTransaction();
   }
   ```
   - Use sparingly (performance overhead) [linkedin](https://www.linkedin.com/posts/ibraheem-omikunle-is-a-software-engineer_mongodb-learning-roadmap-from-basics-to-activity-7333372358201651200-MjiA)

3. **Application-level consistency**:
   - Retry logic with idempotency
   - Two-phase commit pattern
   - Saga pattern for distributed transactions

4. **Eventual consistency with change streams**:
   ```javascript
   db.orders.watch().on('change', change => {
     // Update inventory, send notification, etc.
   });
   ```

5. **Read/write concern configuration**:
   ```javascript
   // Strong consistency
   { writeConcern: { w: "majority", j: true } }
   { readPreference: "primary" }
   ```

**Best practices:**
- Design schema to minimize cross-document operations
- Use transactions only when absolutely necessary
- Implement compensating transactions for rollbacks
- Monitor transaction duration and conflicts

***

### Q21: How do you plan and execute a MongoDB migration from a monolith to microservices?

**Answer:**

**Migration strategy:**

1. **Assessment phase:**
   - Analyze current data model and query patterns
   - Identify service boundaries
   - Determine which collections belong to which service

2. **Parallel run (Strangler Fig pattern):**
   - Run old and new systems simultaneously
   - Gradually route traffic to new services
   - Monitor for discrepancies

3. **Data migration approaches:**

   **A. Dual-write (while migrating):**
   ```javascript
   // Write to both old and new
   await oldCollection.insertOne(data);
   await newCollection.insertOne(data);
   ```

   **B. Backfill (after migration):**
   ```javascript
   // Copy historical data
   db.oldCollection.find().forEach(doc => {
     newCollection.insertOne(transform(doc));
   });
   ```

   **C. Change streams (real-time sync):**
   ```javascript
   db.oldCollection.watch().on('change', change => {
     syncToNewService(change);
   });
   ```

4. **Per-collection migration:**
   - Migrate one collection/service at a time
   - Validate data consistency after each migration
   - Rollback plan ready

5. **Validation:**
   - Compare record counts
   - Spot-check random documents
   - Run integration tests

6. **Cutover:**
   - Switch read traffic first (read-only)
   - Switch write traffic after validation
   - Monitor for issues

**Key considerations:**
- Maintain data consistency during migration
- Handle schema differences between services
- Plan for downtime (minimize)
- Have rollback strategy ready

***

### Q22: What are your strategies for handling MongoDB backups in production?

**Answer:**

**Backup strategies:**

1. **Automated snapshots (Atlas or mongodump):**
   ```bash
   # Automated daily backups (Atlas)
   # Or manual script:
   mongodump --db production --out /backup/$(date +%Y%m%d)
   ```

2. **Point-in-time recovery (PITR):**
   - Enable oplog retention (Atlas: up to 24 hours)
   - Restore to any second within retention window

3. **Cross-region backups:**
   - Replicate backups to another region
   - Protect against regional failures

4. **Backup types:**
   | Type | Tool | Pros | Cons |
   |------|------|------|------|
   | Logical | `mongodump` | Granular, version-independent | Slower, larger |
   | Physical | File snapshots | Fast, smaller | Requires filesystem |
   | Oplog-based | `mongodump --oplog` | Point-in-time | Requires oplog |

5. **Testing recovery:**
   - **Test restore monthly** (never assume it works)
   - Document restoration procedure
   - Measure RTO (Recovery Time Objective) and RPO (Recovery Point Objective)

6. **Automation:**
   ```bash
   # Example backup script
   #!/bin/bash
   BACKUP_DIR="/backup/$(date +%Y%m%d_%H%M%S)"
   mongodump --archive="$BACKUP_DIR/archive.gz" --gzip
   aws s3 cp $BACKUP_DIR s3://my-bucket/backups/
   ```

7. **Monitoring:**
   - Alert on backup failures
   - Monitor backup size and duration
   - Verify backup integrity

**Best practices:**
- Test restores regularly
- Keep backups in multiple locations
- Encrypt backups at rest
- Rotate old backups (retention policy)
- Document disaster recovery runbook

***

### Q23: How do you optimize MongoDB for high-write workloads (e.g., IoT sensor data)?

**Answer:**

**Optimization strategies:**

1. **Use Time-Series Collections** (MongoDB 5.0+):
   ```javascript
   db.createCollection("sensorData", {
     timeseries: {
       timeField: "timestamp",
       metaField: "sensorId",
       granularity: "minutes"
     }
   });
   ```
   - 5-10x compression
   - Optimized for time-range queries

2. **Batch writes:**
   ```javascript
   // Instead of individual inserts
   const batch = [];
   for (let i = 0; i < 1000; i++) {
     batch.push({ timestamp: new Date(), value: sensorValue });
   }
   db.sensorData.insertMany(batch);
   ```

3. **Optimize write concern:**
   ```javascript
   // Faster, less durability (acceptable for sensor data)
   { writeConcern: { w: 1 } }

   // Balanced
   { writeConcern: { w: "majority" } }
   ```

4. **Minimize indexes:**
   - Only index fields needed for queries
   - Avoid indexes on high-write fields

5. **Sharding strategy:**
   - Shard by `sensorId` (hashed)
   - Distribute writes evenly

6. **TTL for automatic expiration:**
   ```javascript
   db.sensorData.createIndex({ timestamp: 1 }, { expireAfterSeconds: 2592000 });
   ```

7. **WiredTiger cache tuning:**
   - Increase cache size for write buffering

8. **Consider coarse-grained aggregation:**
   - Pre-aggregate sensor data (e.g., 1-minute averages)
   - Store raw data separately for detailed analysis

***

### Q24: How do you secure MongoDB in a production environment?

**Answer:**

**Security layers:**

1. **Authentication:**
   ```javascript
   // Enable in mongod.conf
   security:
     authorization: enabled
   ```
   - Use SCRAM (password-based) or X.509 (certificates)
   - Never use default `admin` user

2. **Authorization (RBAC):**
   ```javascript
   // Create least-privilege user
   db.createUser({
     user: "appUser",
     pwd: "securePassword",
     roles: [{ role: "readWrite", db: "production" }]
   });
   ```

3. **Encryption in transit:**
   ```bash
   # mongod.conf
   net:
     ssl:
       mode: requireTLS
       PEMKeyFile: /etc/ssl/mongodb/server.pem
   ```

4. **Encryption at rest:**
   - TDE (Enterprise) or filesystem encryption (LUKS/BitLocker)

5. **Network security:**
   ```bash
   # Bind to specific IPs
   net:
     bindIp: 127.0.0.1,192.168.1.100
   
   # Use firewall rules
   # AWS: Security groups
   # Azure: NSG
   ```

6. **Audit logging:**
   ```bash
   # Enable audit (Enterprise)
   auditLog:
     destination: file
     format: JSON
     filter: '{ "atype": { "$in": [ "login", "logout" ] } }'
   ```

7. **Regular security practices:**
   - Rotate credentials periodically
   - Monitor for unauthorized access
   - Keep MongoDB updated
   - Regular security audits

**Checklist:**
- ✅ Authentication enabled
- ✅ TLS/SSL configured
- ✅ Least-privilege roles
- ✅ Network isolation
- ✅ Audit logging enabled
- ✅ Regular backups encrypted

***

## Real-World Scenario-Based Questions

### Scenario 1: Your e-commerce site's product search is slow during Black Friday. How do you troubleshoot and fix it?

**Answer:**

**Step 1: Diagnosis**
```javascript
// Check slow queries
db.currentOp({ "secs_running": { $gt: 1 } });

// Analyze search query
db.products.find({ 
  $text: { $search: "laptop" }
}).explain("executionStats");
```

**Step 2: Immediate fixes**
```javascript
// Add text index (if not exists)
db.products.createIndex({ name: "text", description: "text", category: "text" });

// Add compound index for filtering
db.products.createIndex({ category: 1, price: 1, inStock: 1 });
```

**Step 3: Aggregation optimization**
```javascript
// Before: Sort before match (slow)
db.products.aggregate([
  { $sort: { price: 1 } },
  { $match: { category: "Electronics" } },
  { $limit: 20 }
]);

// After: Match before sort (fast)
db.products.aggregate([
  { $match: { category: "Electronics", inStock: true } },
  { $sort: { price: 1 } },
  { $limit: 20 }
]);
```

**Step 4: Scaling**
- Enable read preference `secondary` for search (read scaling)
- Consider sharding by `category` if still slow
- Use Atlas Search for advanced search features

**Step 5: Monitoring**
- Set up alerts for query latency
- Monitor CPU and memory during peak
- Cache frequent search results

***

### Scenario 2: A customer reports that their order was charged twice. How do you investigate and prevent this?

**Answer:**

**Investigation:**

1. **Check transactions:**
   ```javascript
   db.orders.find({ 
     userId: customerId, 
     status: "completed" 
   }).sort({ createdAt: -1 }).limit(10);
   
   db.transactions.find({ 
     orderId: orderId 
   });
   ```

2. **Check for duplicate orders:**
   ```javascript
   db.orders.aggregate([
     { $group: { _id: "$userId", count: { $sum: 1 } } },
     { $match: { count: { $gt: 1 } } }
   ]);
   ```

3. **Check application logs** for retry logic

**Root causes:**
- Network timeout causing client retry
- Lack of idempotency in payment processing
- Race condition in concurrent requests

**Prevention:**

1. **Implement idempotency keys:**
   ```javascript
   // Store idempotency key
   db.paymentRequests.insertOne({
     idempotencyKey: "unique-key-123",
     userId: customerId,
     amount: 75000,
     status: "processing"
   });
   
   // Check before processing
   const existing = db.paymentRequests.findOne({ idempotencyKey: "unique-key-123" });
   if (existing && existing.status === "completed") {
     return existing.result; // Return cached result
   }
   ```

2. **Use transactions for order + payment:**
   ```javascript
   const session = db.getMongo().startSession();
   session.startTransaction();
   try {
     db.orders.insertOne(order, { session });
     db.payments.insertOne(payment, { session });
     session.commitTransaction();
   } catch (e) {
     session.abortTransaction();
   }
   ```

3. **Add unique constraint:**
   ```javascript
   db.orders.createIndex({ userId: 1, orderId: 1 }, { unique: true });
   ```

4. **Implement retry logic with exponential backoff**

***

### Scenario 3: Your social media app needs to show a user's timeline (posts from followed users) with 10 million users. How do you design this?

**Answer:**

**Design approach:**

**Option A: Pull model (query on request)**
```javascript
// Query posts from followed users
db.posts.aggregate([
  { $match: { userId: { $in: followingList } } },
  { $sort: { createdAt: -1 } },
  { $limit: 20 }
]);
```
- ✅ Simple
- ❌ Slow for many followers (large `$in` query)

**Option B: Push model (pre-generate timeline)**
```javascript
// Store timeline in user document
{
  "_id": ObjectId("user123"),
  "timeline": [
    { postId: ObjectId("post1"), author: "Alice", content: "...", createdAt: ... },
    { postId: ObjectId("post2"), author: "Bob", content: "...", createdAt: ... }
  ],
  "timelineLastUpdated": ISODate("2026-05-29")
}
```
- ✅ Fast read (single query)
- ❌ Complex write (update all followers when posting)

**Option C: Hybrid (recommended for scale)**
```javascript
// 1. Store posts separately
db.posts.insertOne({
  "_id": ObjectId("post123"),
  "userId": ObjectId("alice"),
  "content": "Hello!",
  "createdAt": ISODate("2026-05-29")
});

// 2. Pre-generate timeline for recent posts only
db.userTimelines.updateOne(
  { userId: ObjectId("user123") },
  { $push: { timeline: { post: postId, ... } } },
  { upsert: true }
);

// 3. For older posts, fallback to pull model
```

**Indexing:**
```javascript
db.posts.createIndex({ userId: 1, createdAt: -1 });  // User's posts
db.posts.createIndex({ createdAt: -1 });             // Global feed
db.userTimelines.createIndex({ userId: 1 });         // User's timeline
```

**Sharding:**
- Shard `posts` by `userId` (hashed)
- Shard `userTimelines` by `userId`

**Optimizations:**
- Cache recent timelines in Redis
- Use pagination (cursor-based, not `skip`)
- Limit timeline size (e.g., 100 posts max)
- Implement fan-out-on-write for popular users

***

### Scenario 4: Your IoT platform receives 1 million sensor readings per minute. How do you store and query this data?

**Answer:**

**Storage design:**

1. **Use Time-Series Collections** (best for this use case):
   ```javascript
   db.createCollection("sensorReadings", {
     timeseries: {
       timeField: "timestamp",
       metaField: "sensorId",
       granularity: "minutes"
     }
   });
   ```

2. **Data model:**
   ```javascript
   {
     "timestamp": ISODate("2026-05-29T10:00:00Z"),
     "sensorId": "sensor_001",
     "temperature": 25.5,
     "humidity": 60,
     "batteryLevel": 85
   }
   ```

3. **Ingestion (optimized):**
   ```javascript
   // Batch inserts
   const batch = [];
   for (let i = 0; i < 1000; i++) {
     batch.push({
       timestamp: new Date(),
       sensorId: `sensor_${i}`,
       temperature: Math.random() * 30,
       humidity: Math.random() * 100
     });
   }
   db.sensorReadings.insertMany(batch);
   ```

4. **Query patterns:**
   ```javascript
   // Last hour of data for a sensor
   db.sensorReadings.find({
     sensorId: "sensor_001",
     timestamp: { $gte: new Date(Date.now() - 3600000) }
   }).sort({ timestamp: -1 });
   
   // Aggregate temperature averages
   db.sensorReadings.aggregate([
     { $match: { timestamp: { $gte: startOfWeek } } },
     { $group: {
         _id: "$sensorId",
         avgTemp: { $avg: "$temperature" },
         maxTemp: { $max: "$temperature" }
     }}
   ]);
   ```

5. **Retention policy:**
   ```javascript
   // Auto-delete old data
   db.sensorReadings.createIndex(
     { timestamp: 1 },
     { expireAfterSeconds: 7776000 }  // 90 days
   );
   ```

6. **Sharding (if needed):**
   - Shard by `sensorId` (hashed)
   - Or use zone sharding by geographic region

7. **Pre-aggregation:**
   - Store 1-minute, 1-hour, 1-day aggregates separately
   - Query aggregates for long-term trends

***

### Scenario 5: Your startup is building a real-time chat app. How do you design message storage and delivery?

**Answer:**

**Design:**

1. **Data model:**
   ```javascript
   // Messages collection
   {
     "_id": ObjectId("msg123"),
     "conversationId": ObjectId("conv456"),
     "senderId": ObjectId("user1"),
     "content": "Hello!",
     "type": "text",  // or "image", "file"
     "timestamp": ISODate("2026-05-29T10:00:00Z"),
     "readBy": [ObjectId("user2"), ObjectId("user3")]
   }
   ```

2. **Conversation collection:**
   ```javascript
   {
     "_id": ObjectId("conv456"),
     "participants": [ObjectId("user1"), ObjectId("user2")],
     "lastMessage": "Hello!",
     "lastMessageAt": ISODate("2026-05-29T10:00:00Z"),
     "unreadCounts": { "user1": 0, "user2": 2 }
   }
   ```

3. **Indexing:**
   ```javascript
   db.messages.createIndex({ conversationId: 1, timestamp: 1 });
   db.messages.createIndex({ conversationId: 1, senderId: 1 });
   db.conversations.createIndex({ participants: 1 });
   ```

4. **Real-time delivery (change streams):**
   ```javascript
   // Server-side
   const changeStream = db.messages.watch([
     { $match: { operationType: "insert" } }
   ]);
   
   changeStream.on('change', change => {
     // Send to WebSocket clients in conversation
     io.to(change.fullDocument.conversationId.toString())
       .emit('newMessage', change.fullDocument);
   });
   ```

5. **Pagination:**
   ```javascript
   // Cursor-based pagination (better than skip/limit)
   db.messages.find({
     conversationId: ObjectId("conv456"),
     timestamp: { $lt: lastTimestamp }  // Before last seen message
   }).sort({ timestamp: -1 }).limit(50);
   ```

6. **Scaling:**
   - Shard by `conversationId` (hash)
   - Use read preference `secondary` for message history
   - Cache active conversations in Redis

7. **Message retention:**
   - TTL for message archival
   - Separate "hot" (recent) and "cold" (archive) collections

***

## System Design & Architecture Questions

### Q25: How would you design a URL shortener service using MongoDB?

**Answer:**

**Data model:**
```javascript
// URLs collection
{
  "_id": ObjectId("..."),
  "shortCode": "abc123",           // Unique, 6-7 chars
  "originalUrl": "https://...",
  "createdAt": ISODate("2026-05-29"),
  "clickCount": 0,
  "userId": ObjectId("user1"),     // Optional
  "expiresAt": ISODate("2026-06-29") // Optional
}
```

**Indexing:**
```javascript
db.urls.createIndex({ shortCode: 1 }, { unique: true });
db.urls.createIndex({ originalUrl: 1 });  // Check for duplicates
```

**Short code generation:**
```javascript
// Option A: Base62 encoding of ObjectId
function generateShortCode() {
  const objectId = new ObjectId().toString();
  return base62.encode(objectId);
}

// Option B: Random string with collision check
function generateShortCode() {
  let code;
  do {
    code = randomString(6);
  } while (db.urls.findOne({ shortCode: code }));
  return code;
}
```

**Redirect flow:**
```javascript
// 1. Lookup (fast, indexed)
const url = db.urls.findOne({ shortCode: "abc123" });

// 2. Update click count (atomic)
db.urls.updateOne(
  { shortCode: "abc123" },
  { $inc: { clickCount: 1 } }
);

// 3. Redirect to originalUrl
```

**Scaling:**
- Shard by `shortCode` (hashed)
- Use CDN for redirects (cache shortCode → URL mapping)
- Batch click counter updates (reduce write load)

***

### Q26: How do you design a recommendation engine using MongoDB vector search?

**Answer:**

**Data model:**
```javascript
// Products collection with embeddings
{
  "_id": ObjectId("prod123"),
  "name": "Laptop",
  "category": "Electronics",
  "embeddings": {
    "text": [0.12, -0.45, 0.78, ...],  // 1536-dim BERT embedding
    "image": [0.34, 0.56, -0.23, ...]   // Image embedding
  },
  "price": 75000
}
```

**Vector index:**
```javascript
db.products.createCollection("products", {
  vectorSearch: {
    index: {
      name: "text_embeddings",
      path: "embeddings.text",
      numDimensions: 1536,
      similarity: "cosine"
    }
  }
});
```

**Similarity search:**
```javascript
// Find similar products
db.products.aggregate([
  {
    $vectorSearch: {
      queryVector: userInputEmbedding,  // User's query embedding
      path: "embeddings.text",
      limit: 10,
      numCandidates: 100
    }
  },
  {
    $project: {
      name: 1,
      price: 1,
      score: { $meta: "vectorSearchScore" }
    }
  }
]);
```

**Hybrid search (text + vector):**
```javascript
db.products.aggregate([
  {
    $search: {
      text: { query: "laptop", path: "name" }
    }
  },
  {
    $vectorSearch: {
      queryVector: userPreferencesEmbedding,
      path: "embeddings.text",
      limit: 50,
      numCandidates: 100
    }
  },
  { $limit: 10 }
]);
```

***

## Troubleshooting & Operational Questions

### Q27: Your replica set has high replication lag. How do you diagnose and fix it?

**Answer:**

**Diagnosis:**
```javascript
// Check replica set status
rs.status();

// Look for:
// - "syncingTo" field
// - "lag" in seconds
// - "stateStr": "SECONDARY" vs "RECOVERING"
```

**Common causes:**

1. **Network latency:**
   - Check network between primary and secondary
   - Verify bandwidth

2. **Slow secondaries:**
   - Secondary hardware is weaker than primary
   - Check disk I/O on secondary

3. **Large index builds:**
   ```javascript
   db.currentOp({ 
     "prog": "indexBuilds",
     "secs_running": { $gt: 10 }
   });
   ```

4. **High write load:**
   - Primary is overwhelmed
   - Optimize writes or shard

**Solutions:**

1. **Add secondary resources:**
   - Upgrade secondary hardware
   - Use SSDs for faster replication

2. **Optimize oplog:**
   ```javascript
   // Check oplog size
   use local
   db.oplog.rs.stats();
   ```

3. **Pause non-critical operations:**
   - Pause index builds on secondary
   - Delay heavy queries

4. **Check for lock contention:**
   ```javascript
   db.currentOp({ "locks": { $exists: true } });
   ```

5. **Add more secondaries** for read scaling

***

### Q28: How do you monitor MongoDB in production? What metrics do you track?

**Answer:**

**Key metrics to monitor:**

| Category | Metrics | Alert Threshold |
|----------|---------|-----------------|
| **Performance** | Query latency, QPS | >100ms p99 latency |
| **Memory** | Cache hit ratio, used memory | <99% hit ratio |
| **Disk** | IOPS, disk usage | >80% disk used |
| **Replication** | Replication lag | >5 seconds lag |
| **Connections** | Connection count | >80% max connections |
| **Operations** | Insert/update/delete rate | Sudden spikes |

**Monitoring tools:**
- **Atlas Monitor** (built-in)
- **Cloud Manager** / **Ops Manager**
- **Prometheus + Grafana** (custom)
- **DataDog**, **New Relic**

**Example monitoring queries:**
```javascript
// Replica set status
rs.status();

// Current operations
db.currentOp({ "secs_running": { $gt: 1 } });

// Index usage
db.collection.aggregate([{ $indexStats: {} }]);

// Server status
db.serverStatus();

// Oplog status
use local
db.oplog.rs.find().sort({ $natural: -1 }).limit(1);
```

**Alerts to set up:**
- Disk usage >80%
- Replication lag >5s
- Query latency >100ms (p99)
- Connection count >80% of max
- Backup failures
- Node down (primary/secondary)

***

### Q29: Your MongoDB instance is running out of disk space. How do you free up space?

**Answer:**

**Step 1: Diagnose**
```javascript
// Check database sizes
db.stats();

// Check collection sizes
db.getCollectionNames().forEach(collection => {
  print(collection + ": " + db[collection].stats().size + " bytes");
});

// Check indexes
db.collection.getIndexes();
```

**Step 2: Free up space**

1. **Delete unnecessary data:**
   ```javascript
   // Delete old documents
   db.logs.deleteMany({ createdAt: { $lt: new Date("2025-01-01") } });
   ```

2. **Compact collection (defragments):**
   ```javascript
   db.collection.reIndex();  // Rebuild indexes
   db.collection.runCommand({ compact: "collectionName" });
   ```

3. **Drop unused indexes:**
   ```javascript
   db.collection.dropIndex("unused_index_name");
   ```

4. **Archive old data:**
   ```javascript
   // Move to archive collection
   db.archive.insertMany(db.collection.find({ createdAt: { $lt: ... } }).toArray());
   db.collection.deleteMany({ createdAt: { $lt: ... } });
   ```

5. **Remove spare files:**
   ```bash
   # MongoDB creates pre-allocated files (jumbo files)
   # Run compact to reclaim space
   db.collection.runCommand({ compact: "collectionName" });
   ```

**Step 3: Prevent future issues**
- Set up disk usage alerts (>80%)
- Implement TTL indexes for auto-expiration
- Plan capacity growth
- Use sharding to distribute data

***

### Q30: How do you handle a MongoDB cluster with a failed node?

**Answer:**

**Scenario: Primary node failed**

1. **Automatic failover (replica set):**
   - Secondaries detect failure (after timeout)
   - Election starts
   - New primary elected automatically
   - Application reconnects to new primary

2. **Manual intervention (if needed):**
   ```javascript
   // Check replica set status
   rs.status();
   
   // If no primary exists, force election
   rs.stepUp();  // On a secondary
   ```

3. **Replace failed node:**
   ```bash
   # Stop MongoDB on failed node
   sudo systemctl stop mongod
   
   # Replace hardware or VM
   
   # Start fresh MongoDB (without data)
   sudo systemctl start mongod
   
   # Add to replica set
   rs.add("new-node:27017");
   ```

4. **Data sync:**
   - New node automatically syncs from primary
   - Monitor sync progress:
   ```javascript
   rs.status().members.forEach(m => {
     print(m.name + " - syncing: " + m.syncSourceHost);
   });
   ```

**Scenario: Shard failed in sharded cluster**

1. **Balancer stops** (chunks won't migrate)
2. **Queries to failed shard** will timeout
3. **Remove failed shard:**
   ```javascript
   sh.removeShard("failed-shard");
   ```
   - Data redistributes to remaining shards
   - May take hours/days depending on data size

4. **Add replacement shard:**
   ```javascript
   sh.addShard("new-shard:27017");
   ```

**Prevention:**
- Use at least 3 nodes (odd number for elections)
- Place nodes in different availability zones
- Monitor node health
- Test failover regularly
- Have runbook for node replacement

***

## Quick Reference Cheat Sheet

| Topic | Key Command/Concept |
|-------|---------------------|
| **CRUD** | `insertOne`, `find`, `updateOne`, `deleteOne` |
| **Indexes** | `createIndex({ field: 1 })`, `explain()` |
| **Aggregation** | `aggregate([{ $match }, { $group }, { $sort }])` |
| **Transactions** | `session.startTransaction()`, `commitTransaction()` |
| **Replica Set** | `rs.initiate()`, `rs.status()`, `rs.add()` |
| **Sharding** | `sh.enableSharding()`, `sh.shardCollection()` |
| **Backup** | `mongodump`, `mongorestore` |
| **Profiler** | `db.setProfilingLevel(1, { slowms: 100 })` |
| **Current Ops** | `db.currentOp()` |
| **Stats** | `db.stats()`, `collection.stats()` |
| **Change Stream** | `db.collection.watch()` |
| **Vector Search** | `$vectorSearch` aggregation stage |

***

**Good luck with your MongoDB interview!** 🚀 Remember: Understanding the "why" behind each concept is more important than memorizing commands.
