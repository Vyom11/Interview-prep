# SQLAlchemy Unified Tutorial

-----

## 🌟 What is this tutorial about?

The SQLAlchemy Unified Tutorial teaches you how to use SQLAlchemy by combining its two main parts:

- **Core**
- **ORM (Object Relational Mapping)**

Instead of learning them separately, this tutorial explains them together so you understand the full picture.

-----

## 🧩 Two Main Parts of SQLAlchemy

### 1. Core (the foundation)

Think of Core as the basic toolkit:

- Connects to the database
- Runs SQL queries
- Builds SQL statements using Python

👉 You work closer to SQL here.

### 2. ORM (higher-level layer)

The ORM builds on top of Core and makes things easier:

- Lets you use Python classes instead of SQL tables
- Handles saving and retrieving data automatically
- Uses objects instead of raw SQL queries

👉 You work more with Python objects than SQL.

-----

## 🔗 How Core and ORM Work Together

- ORM uses Core internally
- In SQLAlchemy 2.0, both are more integrated
- Even ORM queries now use Core-style syntax (`select()`)

👉 So learning Core helps you understand ORM better.

-----

## 📘 What You’ll Learn in This Tutorial

The tutorial is structured step-by-step:

1. **Connecting to the Database** — Create an Engine (starting point of any app)
1. **Transactions & Queries** — How to run queries and handle results
1. **Database Structure (Metadata)** — Define tables using Python
1. **Working with Data (CRUD)** — Create, Read, Update, Delete data
1. **ORM Data Handling** — Use ORM to manage data more easily
1. **Relationships** — Link tables (like foreign keys) using ORM
1. **Further Reading** — Deep dive into advanced topics

-----

## 🎯 Who Should Read What?

- **Beginners** → Read everything
- **Core users** → Focus on Core sections
- **ORM users** → Focus on ORM sections, but understand Core basics

-----

## 🧪 Code Examples

- The tutorial includes real working code
- You can try them in Python yourself
- Make sure you’re using SQLAlchemy 2.0

**Example:**

```python
import sqlalchemy
print(sqlalchemy.__version__)
```

-----

## 🧠 Key Idea to Remember

> 👉 Core = low-level control (SQL-like)  
> 👉 ORM = high-level convenience (Python objects)  
> 👉 Both are connected, not separate

-----

# Establishing Connectivity – the Engine

-----

## 🌟 1. What is an Engine? (Simple Understanding)

👉 In SQLAlchemy, the **Engine** is the starting point of your application.

Think of it like:

> 🔌 A bridge between your Python code and PostgreSQL database

It:

- Connects to PostgreSQL
- Manages connections (connection pool)
- Sends SQL queries
- Receives results

### 🧠 Important Rule

👉 You usually create **ONE Engine** per database and reuse it everywhere.

-----

## 🛠 2. Setup in pgAdmin (Step-by-Step)

Before writing Python code, you must create a database in pgAdmin.

### ✅ Step 1: Open pgAdmin

- Launch pgAdmin
- Enter your master password

### ✅ Step 2: Create a Database

1. In left panel → Right-click **Databases**
1. Click **Create** → **Database**
1. Enter:
- Database name: `mydb`
1. Click **Save**

### ✅ Step 3: Note Your Credentials

You’ll need:

|Field   |Value                        |
|--------|-----------------------------|
|Username|usually `postgres`           |
|Password|(you set during installation)|
|Host    |`localhost`                  |
|Port    |`5432`                       |
|Database|`mydb`                       |

-----

## 📦 3. Install Required Python Packages

```bash
pip install sqlalchemy psycopg2-binary
```

-----

## 🔗 4. Create Engine (PostgreSQL Version)

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:password@localhost:5432/mydb",
    echo=True
)
```

-----

## 🔍 5. Understanding the Connection URL

```
postgresql+psycopg2://username:password@host:port/database
```

|Part        |Meaning                               |
|------------|--------------------------------------|
|`postgresql`|Database type                         |
|`psycopg2`  |Driver (Python → PostgreSQL connector)|
|`postgres`  |Username                              |
|`password`  |Your password                         |
|`localhost` |Database location                     |
|`5432`      |Default PostgreSQL port               |
|`mydb`      |Database name                         |

-----

## ⚡ 6. What is `echo=True`?

```python
echo=True
```

👉 This shows SQL queries in your terminal.

**Example output:**

```sql
SELECT 1;
```

- ✔ Useful for learning
- ❌ Turn off in production

-----

## 💤 7. What is Lazy Connecting?

```python
engine = create_engine(...)
```

👉 At this point:

- ❌ No connection is made yet
- ✔ Connection happens only when needed:
  - Running a query
  - Opening a connection

👉 This is called **Lazy Initialization**

-----

## 🧪 8. Test the Connection (IMPORTANT)

```python
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:password@localhost:5432/mydb",
    echo=True
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchone())
```

### ✅ Expected Output

```
(1,)
```

✔ This means your connection is successful

### 🔍 Step-by-Step Explanation

**1️⃣ Import required things**

```python
from sqlalchemy import create_engine, text
```

- `create_engine` → used to connect to database
- `text` → used to safely write raw SQL queries (important in SQLAlchemy 2.0)

**2️⃣ Create the Engine**

```python
engine = create_engine(...)
```

👉 This sets up the connection details  
❗ But still does NOT connect yet (lazy connection)

**3️⃣ Open a Connection**

```python
with engine.connect() as conn:
```

👉 Now SQLAlchemy:

- Actually connects to PostgreSQL
- Gives you a connection object → `conn`

👉 `with` ensures:

- Connection automatically closes after use (very important)

**4️⃣ Execute a Simple Query**

```python
result = conn.execute(text("SELECT 1"))
```

👉 This runs SQL directly on PostgreSQL:

```sql
SELECT 1;
```

**Why `SELECT 1`?**

- It doesn’t need any table
- Works on any database
- Just returns the number 1
- 👉 It’s the simplest possible test query

**5️⃣ Get the Result**

```python
print(result.fetchone())
```

👉 This fetches one row from the result

Expected output:

```
(1,)
```

### 📦 What is `(1,)`?

👉 It’s a **tuple** (Python format)

- `1` → value returned by database
- `,` → means it’s a tuple with one element

### ✅ What Success Means

If you see `(1,)`, it means:

- Connection is successful ✅
- Database is reachable ✅
- Credentials are correct ✅

### ❌ If Something Goes Wrong

|Error                           |Cause                   |
|--------------------------------|------------------------|
|`authentication failed`         |🔴 Wrong password        |
|`database "mydb" does not exist`|🔴 Database not found    |
|`connection refused`            |🔴 PostgreSQL not running|

-----

## 🎯 Why This Step is Important

👉 Think of it like: *“Checking WiFi before opening a website”*

Before:

- Creating tables
- Inserting data
- Running queries

👉 You must confirm connection works

### 🧠 Simple Analogy

|Thing      |Analogy                 |
|-----------|------------------------|
|`engine`   |📱 Phone                 |
|`connect()`|☎️ Dialing number        |
|`SELECT 1` |👋 Saying “Hello?”       |
|`(1,)`     |✅ “Yes, I can hear you!”|

-----

## ✅ Final Summary

👉 This step:

- Opens a connection
- Runs a simple query
- Confirms everything is working

-----

## 🏗 9. What Engine Does Internally

When you create an Engine:

- It creates a **connection pool**
- Reuses connections
- Improves performance

👉 You don’t need to manage connections manually

-----

## 🔁 10. SQLite vs PostgreSQL (Why Different Code?)

Original tutorial used:

```
sqlite+pysqlite:///:memory:
```

👉 That:

- Uses SQLite
- No server needed
- Temporary database

But **you** are using PostgreSQL:

```
postgresql+psycopg2://postgres:password@localhost:5432/mydb
```

👉 Requires:

- Running PostgreSQL server
- Database created in pgAdmin

-----

## 🎯 Final Summary

👉 Engine is:

- The entry point to SQLAlchemy
- Responsible for connecting to PostgreSQL
- Created using `create_engine()`

👉 Key concepts:

- Uses a connection URL
- Supports lazy connection
- Can log SQL using `echo=True`
- Works with connection pooling

-----

## 🚀 Ready-to-Use Starter Code

```python
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/mydb"

engine = create_engine(DATABASE_URL, echo=True)

# Test connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())
```

-----

# Working with Transactions and the DBAPI

-----

## 🌟 1. Big Picture (What this section is about)

Now that you have an Engine, the next step is learning:

- How to connect to the database
- How to run queries
- How to handle transactions (commit/rollback)
- How to get results

**Main objects you’ll use:**

|Object      |Description                             |
|------------|----------------------------------------|
|`Connection`|Talks to database                       |
|`Result`    |Holds query output                      |
|`Session`   |(ORM) Higher-level version of Connection|

-----

## 🔌 2. What is a Connection?

👉 A **Connection** is an active link to your PostgreSQL database.

You get it from the Engine:

```python
with engine.connect() as conn:
```

**Important:**

- It opens a real database connection
- Should be used temporarily
- Automatically closes after the block (`with`)

-----

## 🧾 3. Writing SQL using `text()`

Since we are not yet using advanced SQLAlchemy features, we write raw SQL using:

```python
from sqlalchemy import text
```

**Example:**

```python
text("SELECT 1")
```

👉 This lets you write normal PostgreSQL SQL inside Python.

-----

## 🧪 4. Running a Simple Query

```python
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT 'hello world'"))
    print(result.all())
```

**What happens:**

1. Connection opens
1. Query runs on PostgreSQL
1. Result is returned
1. Connection closes

**Output:**

```
[('hello world',)]
```

-----

## 🔁 5. What is a Transaction?

👉 A **transaction** is a group of database operations.

PostgreSQL automatically starts one when you run a query.

You must:

- **Commit** → save changes, OR
- **Rollback** → cancel changes

### ⚠️ Important Rule (PostgreSQL + SQLAlchemy)

👉 By default:

- Changes are **NOT** saved automatically
- You **must** call `.commit()`

-----

## 💾 6. Committing Changes (“commit as you go”)

```python
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x INT, y INT)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    conn.commit()
```

### 🔍 Explanation

1. **Create table:**
   
   ```sql
   CREATE TABLE some_table (x INT, y INT);
   ```
1. **Insert data:**
   
   ```sql
   INSERT INTO some_table (x, y) VALUES (1,1), (2,4);
   ```
1. **Commit:**
   
   ```python
   conn.commit()
   ```

👉 Without commit → data will be lost (rolled back)

-----

## 🔄 7. Alternative: “begin once” (Recommended)

```python
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )
```

**What happens:**

- Transaction starts automatically
- If success → `COMMIT`
- If error → `ROLLBACK`

👉 Cleaner and safer

-----

## ❓ 8. What is BEGIN (implicit)?

When you see:

```
BEGIN (implicit)
```

👉 It means:

- PostgreSQL started a transaction automatically
- SQLAlchemy did not explicitly send `BEGIN`

-----

## 📊 9. What is Result?

```python
result = conn.execute(text("SELECT x, y FROM some_table"))
```

👉 `Result` contains query output

-----

## 📥 10. Reading Data from Result

**Option 1: Loop through rows**

```python
for row in result:
    print(row.x, row.y)
```

**Option 2: Get all rows**

```python
rows = result.all()
```

**Option 3: Tuple unpacking**

```python
for x, y in result:
    print(x, y)
```

**Option 4: Index access**

```python
for row in result:
    print(row[0], row[1])
```

**Option 5: Dictionary-style**

```python
for row in result.mappings():
    print(row["x"], row["y"])
```

-----

## 🔐 11. Sending Parameters (VERY IMPORTANT)

**❌ Don’t do this:**

```python
text(f"SELECT * FROM table WHERE y > {value}")
```

**✅ Do this instead:**

```python
result = conn.execute(
    text("SELECT x, y FROM some_table WHERE y > :y"),
    {"y": 2}
)
```

**Why?**

- Prevents **SQL Injection**
- Safe and recommended
- PostgreSQL handles values correctly

-----

## 📦 12. Sending Multiple Rows (executemany)

```python
conn.execute(
    text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
    [{"x": 11, "y": 12}, {"x": 13, "y": 14}]
)
conn.commit()
```

👉 This inserts multiple rows efficiently

-----

## 🧠 13. What is DBAPI?

👉 **DBAPI** is the driver layer between Python and PostgreSQL

In your case:

- Driver = `psycopg2`

**Flow:**

```
SQLAlchemy → psycopg2 → PostgreSQL
```

-----

## 🗃 14. ORM Version (Session)

Instead of `Connection`, ORM uses `Session`:

```python
from sqlalchemy.orm import Session
from sqlalchemy import text

with Session(engine) as session:
    result = session.execute(
        text("SELECT x, y FROM some_table WHERE y > :y"),
        {"y": 6}
    )
    for row in result:
        print(row.x, row.y)
```

**Commit with Session:**

```python
with Session(engine) as session:
    session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}]
    )
    session.commit()
```

-----

## 🔁 Connection vs Session (Simple Difference)

|Feature        |Connection (Core)|Session (ORM)     |
|---------------|-----------------|------------------|
|Level          |Low-level        |High-level        |
|Used for       |Direct SQL       |Object-based work |
|Commit         |`conn.commit()`  |`session.commit()`|
|Internally uses|DBAPI            |Connection        |

-----

## 🎯 Final Summary

- **Connection** → used to execute SQL
- **Transaction** → group of operations (must commit)
- **Result** → holds query output
- **`text()`** → write raw SQL
- **Parameters** → safe query inputs
- **Session** → ORM version of Connection
- **DBAPI (psycopg2)** → connects Python to PostgreSQL

-----

# Working with Database Metadata

-----

## 🌟 1. Big Picture (What is this section about?)

Before writing queries, SQLAlchemy needs to understand your database structure.

👉 This structure (tables, columns, relationships) is called: **Database Metadata**

-----

## 🧠 2. What is Database Metadata?

👉 **Metadata** = “data about your data”

In PostgreSQL, you have:

- Tables
- Columns
- Data types
- Relationships

SQLAlchemy represents all of this using **Python objects**

-----

## 🧩 3. Core Building Blocks

There are 3 main objects:

### ✅ 1. MetaData

👉 A container that stores all your tables

```python
from sqlalchemy import MetaData

metadata_obj = MetaData()
```

Think of it like: **A folder that holds all tables**

### ✅ 2. Table

👉 Represents a PostgreSQL table

```python
from sqlalchemy import Table
```

### ✅ 3. Column

👉 Represents a column inside a table

```python
from sqlalchemy import Column
```

-----

## 🏗 4. Creating Tables in Python (Core Style)

```python
from sqlalchemy import Table, Column, Integer, String, MetaData

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)
```

### 🔍 Explanation

- `"user_account"` → Name of table in PostgreSQL
- `metadata_obj` → Stores this table

|Column    |Meaning              |
|----------|---------------------|
|`id`      |Integer, primary key |
|`name`    |String (max 30 chars)|
|`fullname`|String               |

-----

## 📌 5. Accessing Columns

```python
user_table.c.name
```

👉 `.c` means columns

**Get all column names:**

```python
user_table.c.keys()
```

-----

## 🔑 6. Important Terms (New Definitions)

### 🔹 Primary Key

```python
Column("id", Integer, primary_key=True)
```

👉 Unique identifier for each row  
👉 Cannot be null

PostgreSQL equivalent:

```sql
PRIMARY KEY (id)
```

### 🔹 Constraint

👉 Rules applied to columns. Examples:

- Primary Key
- Foreign Key
- NOT NULL

### 🔹 NOT NULL

```python
Column("email", String, nullable=False)
```

👉 Value must be provided

### 🔹 Foreign Key

👉 Links one table to another

-----

## 🔗 7. Creating Related Tables

```python
from sqlalchemy import ForeignKey

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)
```

### 🔍 Explanation

- `user_id` refers to `user_account.id`
- Creates relationship between tables

PostgreSQL equivalent:

```sql
FOREIGN KEY (user_id) REFERENCES user_account(id)
```

-----

## 🏗 8. Creating Tables in PostgreSQL (DDL)

👉 **DDL** = Data Definition Language

Commands like:

- `CREATE TABLE`
- `DROP TABLE`

**Create tables in database:**

```python
metadata_obj.create_all(engine)
```

**What happens internally:**

- SQLAlchemy generates SQL
- Sends it to PostgreSQL
- Creates tables

**PostgreSQL output (simplified):**

```sql
CREATE TABLE user_account (...);
CREATE TABLE address (...);
```

**Important:**

👉 Order matters:

- `user_account` created first
- Then `address` (because of foreign key)

-----

## 🗑 9. Dropping Tables

```python
metadata_obj.drop_all(engine)
```

👉 Deletes tables (reverse order)

-----

## ⚠️ 10. Important Note (Real Projects)

👉 For real applications, use: **Alembic** (migration tool)

**Why?**

- Tracks database changes
- Updates schema safely

-----

## 🗃 11. ORM Way (Declarative Approach)

Instead of writing tables manually, ORM lets you use Python classes.

**Step 1: Create Base**

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

**Step 2: Create Models**

```python
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
```

### 🔍 Explanation

|Part             |Meaning              |
|-----------------|---------------------|
|`User`           |Python class         |
|`__tablename__`  |PostgreSQL table name|
|`Mapped[int]`    |Column type          |
|`mapped_column()`|Creates column       |

-----

## 🔗 12. Relationships in ORM

```python
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user = relationship("User")
```

**What is `relationship()`?**

👉 Connects two tables at Python level

- User ↔ Address
- Makes querying easier

-----

## 🧠 13. What is Declarative Base?

👉 A base class that:

- Stores metadata
- Registers all models
- Connects ORM with database

-----

## 📦 14. Creating Tables using ORM

```python
Base.metadata.create_all(engine)
```

👉 Same as Core version

-----

## 🔄 15. Table Reflection (Advanced)

👉 Instead of defining tables manually, SQLAlchemy can **read existing PostgreSQL tables**:

```python
some_table = Table(
    "some_table",
    metadata_obj,
    autoload_with=engine
)
```

### 🔍 Explanation of Parameters

- `some_table = Table(...)` — Creates a Python object that represents your database table. You will use this object later to run queries (like selecting or inserting data).
- `"some_table"` — This is the actual name of the table as it exists inside your database (e.g., in MySQL or PostgreSQL).
- `metadata_obj` — Think of this as a “catalog” or folder. It’s a container that holds information about all the tables your script knows about.
- `autoload_with=engine` — This is the “magic” part. `engine` is your active connection to the database. `autoload_with` tells SQLAlchemy to reach out through that connection, scan the table in the database, and automatically fill in all the column details for you.

### 💡 In Simple Terms

Imagine you have a spreadsheet with 50 columns. Instead of writing a Python script that lists all 50 columns by hand, you are saying: *“Hey Python, connect to the database using this engine, find the table called `some_table`, and just copy its structure into this metadata catalog for me.”*

**What happens:**

- Reads table from PostgreSQL
- Creates Python object automatically

-----

## 📘 16. When to Use Reflection?

**Use when:**

- Database already exists
- You don’t want to rewrite schema

### ⚠️ Important

👉 Reflection is optional  
👉 Most apps define schema in Python

-----

## 🎯 Final Summary

|Concept          |Description                         |
|-----------------|------------------------------------|
|Metadata         |Container for tables                |
|Table            |Represents PostgreSQL table         |
|Column           |Represents column                   |
|Constraints      |Rules (PK, FK, NOT NULL)            |
|`create_all()`   |Creates tables                      |
|ORM (Declarative)|Use Python classes instead of tables|
|Reflection       |Load tables from existing database  |

-----

# Working with Data

-----

## 🌟 1. Big Picture

Now that:

- You can connect to PostgreSQL
- You have tables defined (metadata/ORM)

👉 Next step is: **Working with actual data**

This includes:

- **INSERT** → add data
- **SELECT** → read data
- **UPDATE** → modify data
- **DELETE** → remove data

-----

## 🧾 2. INSERT (Adding Data)

### ✅ What is `insert()`?

👉 A function used to insert rows into a table

**Example:**

```python
from sqlalchemy import insert

stmt = insert(user_table).values(
    name="john",
    fullname="John Doe"
)
```

**Execute it:**

```python
with engine.connect() as conn:
    conn.execute(stmt)
    conn.commit()
```

### 🔍 What SQLAlchemy generates (PostgreSQL)

```sql
INSERT INTO user_account (name, fullname)
VALUES ('john', 'John Doe');
```

### 🧠 Key Point

👉 You don’t need to write `VALUES` manually — SQLAlchemy generates it automatically

-----

### 🔁 INSERT with Multiple Rows

```python
conn.execute(
    insert(user_table),
    [
        {"name": "a", "fullname": "A"},
        {"name": "b", "fullname": "B"},
    ]
)
conn.commit()
```

-----

### 🔙 INSERT…RETURNING (PostgreSQL Feature)

👉 PostgreSQL supports `RETURNING`

```python
stmt = insert(user_table).values(name="sam").returning(user_table.c.id)

with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.fetchone())
```

**SQL Generated:**

```sql
INSERT INTO user_account (name)
VALUES ('sam')
RETURNING id;
```

👉 Useful to get inserted ID

-----

### 🔄 INSERT…FROM SELECT

👉 Insert data from another query

```python
stmt = insert(address_table).from_select(
    ["user_id", "email_address"],
    select(user_table.c.id, user_table.c.name)
)
```

**Explanation:**

- `insert(address_table)` — Identifies the “target.” You are telling the code: “I want to add new rows into the `address_table`.”
- `.from_select(...)` — This is the source of the data. Instead of typing in values manually, you are saying: “Get the data from a search (`SELECT`) instead.”
- `["user_id", "email_address"]` — These are the specific columns in the target table (`address_table`) that you want to fill.
- `select(user_table.c.id, user_table.c.name)` — This is the actual data you are grabbing from the source table (`user_table`). It takes the `id` from the user table and puts it into the `user_id` column. It takes the `name` from the user table and puts it into the `email_address` column.

> **Note:** `stmt` is a common shorthand for “Statement.” Developers use this name to show that the variable holds a SQL statement (like an instruction) that is ready to be executed.

-----

## 📖 3. SELECT (Reading Data)

### ✅ What is `select()`?

👉 Used to fetch data from PostgreSQL

**Basic Example:**

```python
from sqlalchemy import select

stmt = select(user_table)

with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(row)
```

### 🎯 Selecting Specific Columns

```python
stmt = select(user_table.c.name, user_table.c.fullname)
```

### 🔍 WHERE Clause (Filtering)

```python
stmt = select(user_table).where(user_table.c.name == "john")
```

**SQL:**

```sql
SELECT * FROM user_account WHERE name = 'john';
```

### 🔗 JOIN (Combining Tables)

```python
stmt = select(user_table.c.name, address_table.c.email_address).join(
    address_table,
    user_table.c.id == address_table.c.user_id
)
```

**SQL:**

```sql
SELECT user_account.name, address.email_address
FROM user_account
JOIN address ON user_account.id = address.user_id;
```

### 📊 ORDER BY, GROUP BY, HAVING

**ORDER BY:**

```python
stmt = select(user_table).order_by(user_table.c.name)
```

**GROUP BY:**

```python
from sqlalchemy import func

stmt = select(user_table.c.name, func.count()).group_by(user_table.c.name)
```

**HAVING:**

```python
stmt = stmt.having(func.count() > 1)
```

### 🧩 Using Aliases

👉 Temporary table name

```python
user_alias = user_table.alias()
stmt = select(user_alias.c.name)
```

### 🔄 Subqueries

**What is a Subquery?**

👉 Query inside another query

**Example:**

```python
subq = select(user_table.c.id).where(user_table.c.name == "john")
stmt = select(address_table).where(address_table.c.user_id.in_(subq))
```

### 📌 CTE (Common Table Expression)

👉 Named subquery

```python
cte = select(user_table).cte("user_cte")
stmt = select(cte)
```

### 🔗 UNION (Combine Results)

**UNION:**

```python
stmt = select(user_table.c.name).union(
    select(address_table.c.email_address)
)
```

**UNION ALL** (includes duplicates):

```python
stmt = select(...).union_all(select(...))
```

### 🔍 EXISTS (Check if data exists)

```python
from sqlalchemy import exists

stmt = select(user_table).where(
    exists().where(address_table.c.user_id == user_table.c.id)
)
```

### 🧮 SQL Functions

```python
from sqlalchemy import func

stmt = select(func.count(user_table.c.id))
```

**PostgreSQL Functions Examples:**

- `COUNT()`
- `MAX()`
- `MIN()`
- `AVG()`

-----

## ✏️ 4. UPDATE (Modify Data)

**Basic Example:**

```python
from sqlalchemy import update

stmt = update(user_table).where(
    user_table.c.name == "john"
).values(fullname="John Updated")
```

**Execute:**

```python
with engine.connect() as conn:
    conn.execute(stmt)
    conn.commit()
```

**SQL:**

```sql
UPDATE user_account
SET fullname = 'John Updated'
WHERE name = 'john';
```

-----

## 🗑 5. DELETE (Remove Data)

```python
from sqlalchemy import delete

stmt = delete(user_table).where(user_table.c.name == "john")
```

**SQL:**

```sql
DELETE FROM user_account WHERE name = 'john';
```

-----

## 📊 6. Rows Affected

```python
result = conn.execute(stmt)
print(result.rowcount)
```

👉 Shows how many rows were updated/deleted

-----

## 🔙 RETURNING with UPDATE/DELETE (PostgreSQL)

```python
stmt = (
    update(user_table)
    .where(user_table.c.name == "john")
    .values(fullname="New Name")
    .returning(user_table.c.id)
)
```

👉 PostgreSQL returns affected rows

-----

## 🧠 7. Important Terms (New)

### 🔹 DML (Data Manipulation Language)

👉 Commands that change data:

- `INSERT`
- `UPDATE`
- `DELETE`

### 🔹 Clause

👉 Part of SQL:

- `WHERE`
- `ORDER BY`
- `GROUP BY`

### 🔹 Expression Language

👉 SQLAlchemy’s way of writing SQL using Python

### 🔹 Function (`func`)

👉 Represents SQL functions like `COUNT`, `SUM`

### 🔹 Alias

👉 Temporary name for a table/query

### 🔹 Subquery

👉 Query inside another query

### 🔹 CTE

👉 Named subquery (`WITH` clause in PostgreSQL)

-----

## 🎯 Final Summary

You now know how to:

- `INSERT` data into PostgreSQL
- `SELECT` and filter data
- `JOIN` tables
- `GROUP` and sort data
- `UPDATE` existing rows
- `DELETE` rows
- Use PostgreSQL features like `RETURNING`

-----

# ORM Data Handling

-----

## 🌟 1. Big Idea (ORM vs Core)

Earlier you used:

- `insert()`, `select()` → Core (SQL-like)

Now with ORM:

**You work with Python objects instead of SQL**

-----

## 🧱 2. Setup (Models + Session)

### ✅ Step 1: Define Models

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
```

### ✅ Step 2: Create Tables

```python
Base.metadata.create_all(engine)
```

### ✅ Step 3: Create Session

```python
from sqlalchemy.orm import Session
```

-----

## ➕ 3. INSERT (Add Data using ORM)

**Example:**

```python
with Session(engine) as session:
    user = User(name="john", fullname="John Doe")
    session.add(user)
    session.commit()
```

### 🔍 What happens:

- You create a Python object → `User(...)`
- ORM converts it to SQL:

```sql
INSERT INTO user_account ...
```

### Insert Multiple Rows

```python
with Session(engine) as session:
    users = [
        User(name="a", fullname="A"),
        User(name="b", fullname="B")
    ]
    session.add_all(users)
    session.commit()
```

### 🔗 Insert with Relationship

```python
with Session(engine) as session:
    user = User(
        name="alice",
        fullname="Alice Smith",
        addresses=[
            Address(email_address="alice@example.com"),
            Address(email_address="alice@gmail.com")
        ]
    )
    session.add(user)
    session.commit()
```

👉 ORM automatically handles foreign keys

-----

## 📖 4. SELECT (Read Data)

### Get All Users

```python
from sqlalchemy import select

with Session(engine) as session:
    result = session.execute(select(User))
    for user in result.scalars():
        print(user.name, user.fullname)
```

### ⚠️ Important: Why `.scalars()` Matters

If you do **not** use `.scalars()`, the loop will iterate over `Row` objects, which behave like Python tuples.

Instead of receiving a single ORM object (e.g., `User`), you will receive a tuple containing that object as its first element: `(<User object>,)`.

**Consequences:**

- **Attribute Error:** Your code will fail. Since `user` is now a tuple, attempting to access `user.name` will raise an `AttributeError` because tuples do not have a `.name` attribute.

```python
scalars()
```

👉 Extracts actual objects from result

### 🔎 Filter Data (WHERE)

```python
stmt = select(User).where(User.name == "john")

with Session(engine) as session:
    result = session.execute(stmt)
    for user in result.scalars():
        print(user)
```

### 🔗 JOIN (Related Tables)

```python
stmt = select(User).join(User.addresses)

with Session(engine) as session:
    result = session.execute(stmt)
    for user in result.scalars():
        print(user.name)
```

**Breakdown of the Code:**

- `select(User)` — Prepares a SQL query to fetch all columns mapped to the `User` class.
- `.join(User.addresses)` — Adds an `INNER JOIN` to the SQL statement. It tells SQLAlchemy to only include `User` records that have at least one corresponding entry in the `addresses` table, using the relationship defined in the model.

### 📊 ORDER BY

```python
stmt = select(User).order_by(User.name)  # default is ascending
```

### 📈 GROUP BY + COUNT

```python
from sqlalchemy import func

stmt = select(User.name, func.count()).group_by(User.name)
```

-----

## ✏️ 5. UPDATE (Modify Data)

### Method 1: Change Object

```python
with Session(engine) as session:
    user = session.get(User, 1)  # get by primary key
    user.fullname = "Updated Name"
    session.commit()
```

### 🔍 What happens:

- ORM tracks changes
- Automatically runs:

```sql
UPDATE user_account SET fullname = ...
```

### Method 2: Using Query

```python
from sqlalchemy import update

stmt = update(User).where(User.name == "john").values(fullname="New Name")

with Session(engine) as session:
    session.execute(stmt)
    session.commit()
```

-----

## 🗑 6. DELETE (Remove Data)

### Method 1: Delete Object

```python
with Session(engine) as session:
    user = session.get(User, 1)
    session.delete(user)
    session.commit()
```

### Method 2: Using Query

```python
from sqlalchemy import delete

stmt = delete(User).where(User.name == "john")

with Session(engine) as session:
    session.execute(stmt)
    session.commit()
```

-----

## 🔙 7. RETURNING (PostgreSQL Feature)

```python
from sqlalchemy import update

stmt = (
    update(User)
    .where(User.name == "john")
    .values(fullname="New Name")
    .returning(User.id)
)

with Session(engine) as session:
    result = session.execute(stmt)
    print(result.fetchall())
    session.commit()
```

-----

## 📊 8. Row Count

```python
result = session.execute(stmt)
print(result.rowcount)
```

-----

## 🧠 9. Important ORM Concepts (New)

### 🔹 Session

👉 Main object for ORM operations

- Handles transactions
- Tracks changes

### 🔹 ORM Object

👉 Python object representing a row

**Example:**

```python
user = User(name="john")
```

### 🔹 Identity Map

👉 Session remembers objects

- Same row → same Python object

### 🔹 Unit of Work

👉 ORM tracks changes and executes SQL automatically on commit

### 🔹 Lazy Loading

👉 Related data loads only when accessed

-----

## 🔄 10. Core vs ORM (Final Comparison)

|Operation|Core      |ORM               |
|---------|----------|------------------|
|Insert   |`insert()`|`session.add()`   |
|Select   |`select()`|`select(Model)`   |
|Update   |`update()`|modify object     |
|Delete   |`delete()`|`session.delete()`|
|Relations|Manual    |Automatic         |

-----

## 🎯 Final Summary

With ORM you:

- Work with Python objects instead of SQL
- Let SQLAlchemy generate SQL
- Use `Session` to manage everything
- Easily handle relationships

-----

## 🚀 What You Can Do Now

You can:

- Build full CRUD apps
- Use PostgreSQL features (`RETURNING`, `JOIN`s)
- Avoid writing raw SQL

-----

# 📊 SQLAlchemy Core vs ORM Comparison

|Operation            |Core (SQL-like)                          |ORM (Object-oriented)                   |What it Means       |
|---------------------|-----------------------------------------|----------------------------------------|--------------------|
|Insert (single)      |`conn.execute(insert(table).values(...))`|`session.add(obj)`                      |Add one row         |
|Insert (multiple)    |`conn.execute(insert(table), [dicts])`   |`session.add_all([objs])`               |Add multiple rows   |
|Select (all)         |`select(table)`                          |`select(Model)`                         |Get all rows        |
|Select (execute)     |`conn.execute(stmt)`                     |`session.execute(stmt)`                 |Run query           |
|Get results          |`result.fetchall()` / loop               |`result.scalars()`                      |Extract data        |
|Filter (WHERE)       |`.where(table.c.col == value)`           |`.where(Model.col == value)`            |Filter rows         |
|Join                 |`.join(table2, condition)`               |`.join(Model.relationship)`             |Combine tables      |
|Order By             |`.order_by(table.c.col)`                 |`.order_by(Model.col)`                  |Sort results        |
|Group By             |`.group_by(table.c.col)`                 |`.group_by(Model.col)`                  |Group data          |
|Insert with RETURNING|`.returning(table.c.id)`                 |`.returning(Model.id)`                  |Get inserted values |
|Update               |`update(table).where(...).values(...)`   |Modify object OR `update(Model)`        |Change data         |
|Delete               |`delete(table).where(...)`               |`session.delete(obj)` OR `delete(Model)`|Remove data         |
|Commit               |`conn.commit()`                          |`session.commit()`                      |Save changes        |
|Connection           |`engine.connect()`                       |`Session(engine)`                       |Start DB interaction|
|Relationships        |Manual foreign keys                      |`relationship()`                        |Link tables         |
|Access columns       |`table.c.column`                         |`Model.column`                          |Reference column    |

-----

## 🧠 Simple Understanding

|Core                    |ORM                    |
|------------------------|-----------------------|
|Closer to SQL           |Closer to Python       |
|More control            |Easier to use          |
|Manual relationships    |Automatic relationships|
|Good for complex queries|Good for applications  |

-----

## 🎯 Key Takeaway

- **Use Core when:**
  - You want full control over SQL
  - Writing complex queries
- **Use ORM when:**
  - Building applications
  - Working with objects instead of SQL
