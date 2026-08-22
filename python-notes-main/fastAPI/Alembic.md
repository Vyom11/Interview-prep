# Complete Mastery Guide: Alembic with PostgreSQL
### The Definitive Internal Engineering Manual

> **Audience:** Backend engineers and DBAs working with Python, SQLAlchemy, and PostgreSQL.  
> **Version:** Alembic 1.13+, SQLAlchemy 2.0+, PostgreSQL 15+
---

## Table of Contents

1. [Project Setup & Directory Structure](#1-project-setup--directory-structure)
2. [Architectural Deep Dive — Under the Hood](#2-architectural-deep-dive--under-the-hood)
3. [PostgreSQL-Specific Configuration](#3-postgresql-specific-configuration)
4. [The Developer Workflow & Reflection](#4-the-developer-workflow--reflection)
5. [Troubleshooting & Edge Cases — The War Room Guide](#5-troubleshooting--edge-cases--the-war-room-guide)
6. [Advanced Mechanics](#6-advanced-mechanics)
7. [PostgreSQL Type Intricacies](#7-postgresql-type-intricacies)
8. [Quick Reference Cheat Sheet](#8-quick-reference-cheat-sheet)

---

## Introduction

When building a FastAPI application, managing database schema changes is essential as the application grows and evolves. Your database schema needs to keep pace with new features, bug fixes, and changing requirements.

Alembic is a lightweight, powerful, and flexible tool that streamlines the process of managing database migrations. With Alembic, you can track changes to your schema, roll back to previous versions, and maintain a clear history of modifications. This enables effective collaboration within your team and provides a structured way to handle schema updates, ensuring your database evolves in step with your application.

---

## Analogy — Alembic as “Git for Your Database”

Think of Alembic as the **Git for your database schema**.

Just as Git tracks changes in your codebase, Alembic tracks changes in your database schema. When you modify code, you commit changes in Git to save a snapshot of that version. Similarly, when you update your database schema (such as adding a new column or table), Alembic creates a migration file to capture that change. This migration file serves as a versioned snapshot of the database structure at a specific point in time.

### How the Analogy Maps

- **Version Control:**  
  Just like Git keeps track of code versions, Alembic keeps a history of schema changes, allowing you to move backward or forward in time (e.g., rollback).

- **Migrations as Commits:**  
  Each Alembic migration file is like a Git commit, representing a specific change to the database schema. You can apply or roll back these migrations as needed.

- **Branching and Collaboration:**  
  In a collaborative environment, developers work on different features. Each developer can create migration files, which are later applied sequentially to maintain consistency.

- **Schema Consistency:**  
  Just as Git synchronizes codebases, Alembic ensures your database schema stays consistent across development, testing, and production environments.

> Alembic gives your database both a **history** and a **roadmap**, making it easier to evolve safely as your application grows.


## 1. Project Setup & Directory Structure

### Installation

```bash
pip install alembic sqlalchemy psycopg2-binary python-dotenv
```

### Initialize Alembic

```bash
alembic init alembic
```

This produces the canonical layout:

```
project_root/
├── alembic/
│   ├── env.py                  # Execution environment — the orchestrator
│   ├── script.py.mako          # Jinja2 template for new migration files
│   ├── README
│   └── versions/               # All migration scripts live here
│       ├── 3a1f8b2c_initial_schema.py
│       └── 9e4d7c1a_add_users_index.py
├── alembic.ini                 # Configuration file (commit this)
├── models.py                   # Your SQLAlchemy ORM models
└── .env                        # Secrets — NEVER commit this
```

> [!IMPORTANT]
> Never hardcode database credentials in `alembic.ini`. The `sqlalchemy.url` key in that file should be treated as a placeholder only. See [Section 3](#3-postgresql-specific-configuration) for the correct approach using environment variables.

---

## 2. Architectural Deep Dive — Under the Hood

### 2.1 The `alembic_version` Table — The Single Source of Truth

When Alembic first runs against a database, it creates a tiny but critical table:

```sql
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
```

**This table does exactly one thing:** it stores the revision ID of the *currently applied* migration head. Everything Alembic does is oriented around reading and writing this single row.

| State | `alembic_version` contents |
|---|---|
| Fresh database, no migrations run | Empty (0 rows) |
| After first `alembic upgrade head` | `{ version_num: "3a1f8b2c" }` |
| After second migration applied | `{ version_num: "9e4d7c1a" }` |
| Multiple heads (branch scenario) | Two rows exist simultaneously |

When you run `alembic upgrade head`, Alembic:
1. Connects to the DB and reads `SELECT version_num FROM alembic_version`.
2. Walks the **revision DAG** (directed acyclic graph) of your `versions/` directory to find the path from the current revision to `head`.
3. Executes each `upgrade()` function in order.
4. Updates `alembic_version` after **each successful migration step**.

### 2.2 The `upgrade()` and `downgrade()` Execution Model

Every migration file is a plain Python module with two required functions:

```python
# versions/9e4d7c1a_add_users_index.py

revision = "9e4d7c1a"
down_revision = "3a1f8b2c"  # The parent — this forms the DAG edge
branch_labels = None
depends_on = None

def upgrade() -> None:
    # All op.* calls here translate to DDL executed against the live DB
    op.create_index("ix_users_email", "users", ["email"], unique=True)

def downgrade() -> None:
    # The exact inverse — must restore the DB to the state before upgrade()
    op.drop_index("ix_users_email", table_name="users")
```

**Key mechanics:**

- `down_revision` is what builds the **revision chain**. Alembic uses this to determine upgrade/downgrade order. It is the parent pointer in the DAG.
- `op.*` functions (from `alembic.operations`) are **lazy** — they are collected and sent to the database via the active connection managed by `env.py`, not executed immediately inline.
- After a successful `upgrade()`, Alembic executes: `UPDATE alembic_version SET version_num = '9e4d7c1a'`.
- After a successful `downgrade()`, it executes: `UPDATE alembic_version SET version_num = '3a1f8b2c'` (the `down_revision`).

### 2.3 The Full Execution Flow: `env.py` → `alembic.ini` → Engine → DDL

Understanding how these pieces connect prevents hours of debugging.

```
alembic upgrade head
        │
        ▼
   alembic.ini          ← Parsed first for script_location, file_template, etc.
        │
        ▼
    env.py               ← Your code. Runs in two modes (online / offline).
        │
        ├─ Reads sqlalchemy.url (or overrides it via os.environ)
        ├─ Creates a SQLAlchemy Engine
        ├─ Calls context.configure(connection=conn, target_metadata=metadata)
        │
        ▼
  MigrationContext       ← Alembic internal: wraps the connection
        │
        ├─ Queries alembic_version to find current head
        ├─ Resolves revision path using versions/*.py DAG
        │
        ▼
  upgrade() / downgrade() ← Your migration function executes
        │
        ├─ op.create_table(), op.add_column(), etc.
        ├─ Each op translates to a DDL string via the dialect (postgresql)
        │
        ▼
  PostgreSQL Engine       ← Raw SQL sent over psycopg2 connection
        │
        ▼
  alembic_version updated ← Committed as part of the same transaction (DDL)
```

### 2.4 The `script.py.mako` Template

When you run `alembic revision`, Alembic renders this Mako template to produce a new migration file. You can customize it for your team:

```mako
## script.py.mako — customized for our team
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
Reviewed By: <engineer_name>
Ticket: <jira_ticket>
"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
```

> **Pro Tip:** Add `Reviewed By` and `Ticket` fields to your template. Every migration touching production should be traceable to a code review and a ticket.

---

## 3. PostgreSQL-Specific Configuration

### 3.1 Secure `sqlalchemy.url` via Environment Variables

**`alembic.ini`** — Keep the placeholder, never a real URL:

```ini
[alembic]
script_location = alembic
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s
prepend_sys_path = .
version_path_separator = os

# This is intentionally left as a placeholder.
# The real URL is injected in env.py from environment variables.
sqlalchemy.url = postgresql+psycopg2://user:pass@localhost/dbname
```

**`.env`** — Your secrets file:

```dotenv
DB_USER=myapp_user
DB_PASSWORD=supersecretpassword
DB_HOST=db.internal.company.com
DB_PORT=5432
DB_NAME=myapp_production
```

**`env.py`** — The correct, production-grade pattern:

```python
import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your models' metadata
from models import Base  

load_dotenv()

config = context.config

# Build the URL from environment variables — never from alembic.ini directly
def get_url() -> str:
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    host = os.environ["DB_HOST"]
    port = os.environ.get("DB_PORT", "5432")
    name = os.environ["DB_NAME"]
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

# Override whatever is in alembic.ini
config.set_main_option("sqlalchemy.url", get_url())

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (generates SQL, no DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,          # Detect column type changes
        compare_server_defaults=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (direct DB connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Critical for migration scripts — no connection pooling
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_defaults=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

> [!IMPORTANT]
> Always use `poolclass=pool.NullPool` in migration scripts. Migration processes are short-lived; connection pooling adds no benefit and can cause connection leaks or lock contention in CI/CD environments.

### 3.2 Naming Conventions — The Single Most Important PostgreSQL Configuration

PostgreSQL requires that **every constraint has a unique name**. SQLAlchemy's autogenerate will detect constraint changes only if it can match them by name. Without a naming convention, Alembic generates unnamed constraints, and `--autogenerate` becomes **blind** to them — it cannot detect they exist and cannot drop or modify them.

**Define this in your `models.py` base and never deviate:**

```python
# models.py
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# The canonical PostgreSQL naming convention
POSTGRES_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=POSTGRES_NAMING_CONVENTION)
```

**What this prevents:**

```sql
-- Without naming convention (Alembic can't track this):
ALTER TABLE orders ADD CONSTRAINT unnamed_1234 FOREIGN KEY (user_id) REFERENCES users(id);

-- With naming convention (Alembic knows exactly what this is):
ALTER TABLE orders ADD CONSTRAINT fk_orders_user_id_users FOREIGN KEY (user_id) REFERENCES users(id);
```

When you add `render_as_batch=False` (or leave it default for PostgreSQL) and these conventions, Alembic's `--autogenerate` will correctly detect additions, modifications, and removals of **all** constraint types.

### 3.3 Transactional DDL — PostgreSQL's Superpower

**PostgreSQL is one of the few databases that wraps DDL in transactions.** This is a fundamental safety guarantee that most databases (MySQL, Oracle) do not provide.

What this means in practice:

```sql
BEGIN;
    ALTER TABLE users ADD COLUMN phone VARCHAR(20);
    ALTER TABLE users ADD CONSTRAINT uq_users_phone UNIQUE (phone);
    UPDATE alembic_version SET version_num = 'abc123';
COMMIT;  -- All three succeed atomically, or NONE of them do.
```

If the second `ALTER TABLE` fails (e.g., duplicate constraint name), PostgreSQL **rolls back the entire transaction** — the column addition is also undone, and `alembic_version` is never updated. Your database is left in a clean state.

**How Alembic leverages this:**

In `env.py`, the `with context.begin_transaction():` block is what opens this wrapping transaction. Each migration step runs inside a single transaction by default.

> [!IMPORTANT]
> Some DDL operations in PostgreSQL **cannot run inside a transaction**. These include:
> - `CREATE INDEX CONCURRENTLY`
> - `DROP INDEX CONCURRENTLY`
> - `VACUUM`
> - Some `ALTER TYPE` operations (adding values to ENUM)
>
> For these operations, you **must** use `op.execute()` with explicit transaction management and set `transaction_per_migration = False` or use separate migration files with `execute_timeout`. See [Section 7](#7-postgresql-type-intricacies) for the ENUM and Concurrent Index patterns.

---

## 4. The Developer Workflow & Reflection

### 4.1 Code-to-DB: The `--autogenerate` Workflow

This is the primary day-to-day workflow. You change your models, then ask Alembic to diff them against the live DB.

**The correct workflow:**

```bash
# Step 1: Make changes to your SQLAlchemy models in models.py

# Step 2: Generate the migration (Alembic diffs models against DB state)
alembic revision --autogenerate -m "add_phone_to_users"

# Step 3: ALWAYS inspect the generated file before applying
# Open alembic/versions/20240115_1030_abc123_add_phone_to_users.py
# Verify the upgrade() and downgrade() match your intent

# Step 4: Apply to your local dev database
alembic upgrade head

# Step 5: Commit BOTH the model changes AND the migration file together
git add models.py alembic/versions/20240115_1030_abc123_add_phone_to_users.py
git commit -m "feat: add phone field to users (migration included)"
```

> [!IMPORTANT]
> **Always review the autogenerated migration.** Autogenerate is smart but not perfect. It commonly misses or mis-generates:
> - Changes to stored procedures, triggers, and views
> - `CHECK` constraints if not reflected in the metadata
> - Server-side default value changes (partial support)
> - Renamings (it sees a drop + create, not a rename)
> - PostgreSQL-specific types like `JSONB`, `ARRAY`, custom `ENUM`

**What `--autogenerate` compares:**

| Detected | Not Detected by Default |
|---|---|
| Table additions/removals | Stored procedures |
| Column additions/removals | Triggers |
| Column type changes (`compare_type=True`) | Views |
| Index additions/removals | Sequences |
| Constraint additions/removals (with naming convention) | `GRANT`/`REVOKE` |
| Server defaults (`compare_server_defaults=True`) | Row-level security policies |

### 4.2 DB-to-Code (Reflection) — Handling an Existing Database

> **This is the most commonly misunderstood Alembic concept.**

**Alembic does NOT automatically update your SQLAlchemy models from the database.** The `--autogenerate` flag only works in one direction: it reads your **Python models** and compares them against the **live database schema**.

The workflow for onboarding an existing database:

#### Scenario: Your team has a live PostgreSQL DB with no Alembic migrations yet.

**Step 1: Reflect the existing schema into SQLAlchemy models manually** (or use a tool like `sqlacodegen`):

```bash
pip install sqlacodegen
sqlacodegen postgresql+psycopg2://user:pass@host/dbname > models_reflected.py
```

Review and clean up the output into your `models.py`.

**Step 2: Create an initial "baseline" migration that does nothing.**
This tells Alembic "the DB already looks like this; don't re-create anything."

```bash
alembic revision -m "baseline_existing_schema"
```

Edit the generated file to have **empty** `upgrade()` and `downgrade()`:

```python
def upgrade() -> None:
    pass  # DB already exists; this migration is a sync point only.

def downgrade() -> None:
    pass
```

**Step 3: Stamp the database with this revision.**

```bash
alembic stamp head
```

This inserts the revision ID into `alembic_version` without running any DDL. Now Alembic thinks the DB is at `head`.

**Step 4: All future changes follow the normal Code-to-DB workflow.**

```
models.py changed → alembic revision --autogenerate → review → alembic upgrade head
```

---

## 5. Troubleshooting & Edge Cases — The War Room Guide

### 5.1 The "Multiple Heads" Crisis

**How it happens:**

```
main branch: ... → rev_A (head)
                         \
developer-1 branch:       → rev_B  (merged to main)
developer-2 branch:       → rev_C  (merged to main)
```

After both developers merge to `main`, you now have **two heads**: `rev_B` and `rev_C`. Running `alembic upgrade head` will **fail** with:

```
alembic.util.exc.CommandError: Multiple head revisions are present for given argument 'head'
```

**Diagnosis:**

```bash
alembic heads
# Output:
# rev_B (head)
# rev_C (head)

alembic history --verbose
# Shows the branching in the DAG
```

**Resolution — The `alembic merge` command:**

```bash
alembic merge -m "merge_revB_and_revC" rev_B rev_C
```

This generates a new migration file:

```python
# versions/20240115_1100_rev_D_merge_revB_and_revC.py

revision = "rev_D"
down_revision = ("rev_B", "rev_C")  # Two parents — this is the merge node
branch_labels = None
depends_on = None

def upgrade() -> None:
    pass  # Merge migrations are typically no-ops

def downgrade() -> None:
    pass
```

```bash
alembic upgrade head   # Now resolves cleanly through rev_D
```

> **Prevention:** Establish a team convention. Assign each developer a migration "slot" time at the end of their PR, or use a migration number coordinator in your CI/CD pipeline that detects head conflicts before merge.

### 5.2 The "Failed Head" / Dirty State

**How it happens:** A migration runs, partially applies some DDL, then crashes (e.g., Python exception, OOM, network drop). Because of PostgreSQL's Transactional DDL, the DDL is rolled back — but `alembic_version` may or may not be updated depending on where the crash occurred.

**Diagnosis — Always start here:**

```bash
# Check what Alembic thinks the state is
alembic current

# Check what the DB actually contains
psql -c "SELECT version_num FROM alembic_version;"

# Check the actual schema to see what was applied
psql -c "\d users"
```

**Case 1: `alembic_version` has the new revision but the DDL partially failed (extremely rare with PostgreSQL's Transactional DDL, but possible with CONCURRENT operations).**

```sql
-- Manually revert alembic_version to the previous revision
UPDATE alembic_version SET version_num = 'rev_A';  -- The last known-good revision
```

Then manually reverse any partial DDL that was applied outside a transaction (e.g., a concurrent index), and re-run the migration.

**Case 2: `alembic_version` shows an old revision but you know you've applied some changes manually to the DB.**

```bash
# Stamp the DB to the correct revision without running any DDL
alembic stamp rev_B
```

**Case 3: `alembic_version` table is missing entirely.**

```bash
# Re-stamp from scratch
alembic stamp head
```

> [!IMPORTANT]
> **Never edit `alembic_version` in production without a documented rollback plan and team sign-off.** Incorrect stamps lead to Alembic re-running already-applied migrations or skipping required ones. Always take a DB snapshot before manual intervention.

### 5.3 NOT NULL Column on a Populated Production Table

Adding `NOT NULL` to a column with existing data is one of the most dangerous migrations you can run. **A naive migration will lock the entire table and fail if any row has a NULL in that column.**

> [!IMPORTANT]
> Never do this as a single step in production:
> ```python
> # ❌ DANGEROUS — will lock the table for the duration of the backfill
> op.add_column("orders", sa.Column("status", sa.String(), nullable=False))
> ```

**The correct multi-step, zero-downtime pattern:**

#### Migration 1: Add the column as nullable with a server default

```python
def upgrade() -> None:
    op.add_column(
        "orders",
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=True,              # Start nullable
            server_default="pending",   # Default for new rows
        ),
    )

def downgrade() -> None:
    op.drop_column("orders", "status")
```

Deploy this. Your application can now write `status` to new rows.

#### Migration 2: Backfill existing NULL rows in batches (application-level or via migration)

```python
def upgrade() -> None:
    # Use batched updates to avoid long-running transactions / table locks
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            UPDATE orders
            SET status = 'legacy_pending'
            WHERE status IS NULL
        """)
    )
    # For very large tables, do this in a separate script with:
    # UPDATE orders SET status = 'x' WHERE id BETWEEN :start AND :end AND status IS NULL

def downgrade() -> None:
    pass  # Backfill is non-reversible; downgrade is a no-op
```

#### Migration 3: Add the NOT NULL constraint

```python
def upgrade() -> None:
    # At this point, all rows have a value — safe to enforce NOT NULL
    op.alter_column("orders", "status", nullable=False)

def downgrade() -> None:
    op.alter_column("orders", "status", nullable=True)
```

> **For extremely large tables:** Use `ALTER TABLE orders ALTER COLUMN status SET NOT NULL` only after you've validated 0 NULLs remain with `SELECT COUNT(*) FROM orders WHERE status IS NULL`. PostgreSQL 12+ has an optimization: if you add a `CHECK (status IS NOT NULL)` constraint as `NOT VALID`, then `VALIDATE CONSTRAINT`, it takes a lighter lock.

---

## 6. Advanced Mechanics

### 6.1 Batch Operations

`op.batch_alter_table()` is primarily a workaround for **SQLite**, which cannot `ALTER TABLE` to drop or modify columns. However, in PostgreSQL it can also be useful for **grouping multiple column alterations into a single ALTER TABLE statement**, reducing the number of table rewrites.

```python
def upgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("age", sa.Integer(), nullable=True))
        batch_op.alter_column(
            "email",
            existing_type=sa.VARCHAR(length=100),
            type_=sa.VARCHAR(length=255),
            existing_nullable=False,
        )
        batch_op.drop_constraint("uq_users_username", type_="unique")
        batch_op.create_unique_constraint("uq_users_email_phone", ["email", "phone"])
```

> **PostgreSQL note:** PostgreSQL can handle multiple column alterations in one `ALTER TABLE` natively, which batch mode facilitates. However, some operations (like changing a column type) still require a table rewrite regardless.

### 6.2 Offline Mode (`--sql`) — The DBA Review Pattern

In regulated environments, DBAs must review all SQL before it touches production. Alembic's offline mode generates the raw SQL without connecting to a database.

```bash
# Generate SQL for all pending migrations
alembic upgrade head --sql > migration_$(date +%Y%m%d).sql

# Generate SQL for a specific range of revisions
alembic upgrade rev_A:rev_C --sql > migration_range.sql

# Generate downgrade SQL
alembic downgrade -1 --sql > rollback_last.sql
```

The output file contains the exact DDL plus the `UPDATE alembic_version` statement. DBAs can review, modify if needed, and apply using `psql`:

```bash
psql -h prod-db.internal -U admin -d myapp -f migration_20240115.sql
```

> **Workflow for regulated teams:** The CI/CD pipeline should automatically generate this SQL artifact for every migration PR. The artifact is attached to the pull request and linked from the deployment ticket.

### 6.3 Stairway Testing — Ensuring Reversible Migrations

Every migration should be tested with the full upgrade → downgrade → upgrade cycle. This validates:
1. `upgrade()` applies cleanly.
2. `downgrade()` fully reverses the changes.
3. `upgrade()` can be re-applied after a downgrade (idempotency check).

**The canonical test structure using `pytest`:**

```python
# tests/test_migrations.py
import pytest
from sqlalchemy import create_engine, text
from alembic.config import Config
from alembic import command


@pytest.fixture(scope="session")
def alembic_config():
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", "postgresql+psycopg2://test:test@localhost/test_db")
    return cfg


def get_current_head(config: Config) -> str:
    """Helper to get the current alembic_version from the test DB."""
    engine = create_engine(config.get_main_option("sqlalchemy.url"))
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version_num FROM alembic_version"))
        row = result.fetchone()
        return row[0] if row else None


def test_stairway_migrations(alembic_config):
    """
    Stairway test: for each revision, run upgrade, verify, downgrade, verify, upgrade again.
    This ensures all migrations are fully reversible and re-applicable.
    """
    # Start from a clean state
    command.downgrade(alembic_config, "base")

    # Get all revisions in order
    from alembic.script import ScriptDirectory
    script = ScriptDirectory.from_config(alembic_config)
    revisions = list(script.walk_revisions("base", "heads"))
    revisions.reverse()  # From oldest to newest

    for revision in revisions:
        rev_id = revision.revision

        # Step 1: Upgrade to this revision
        command.upgrade(alembic_config, rev_id)
        assert get_current_head(alembic_config) == rev_id, \
            f"After upgrade, expected head={rev_id}"

        # Step 2: Downgrade one step
        command.downgrade(alembic_config, "-1")
        # After downgrade, we should be at the parent revision
        expected_down = revision.down_revision if not isinstance(
            revision.down_revision, tuple
        ) else revision.down_revision[0]
        if expected_down:
            assert get_current_head(alembic_config) == expected_down, \
                f"After downgrade from {rev_id}, expected head={expected_down}"

        # Step 3: Re-upgrade
        command.upgrade(alembic_config, rev_id)
        assert get_current_head(alembic_config) == rev_id, \
            f"After re-upgrade, expected head={rev_id}"

    print("✅ Stairway test passed — all migrations are reversible.")
```

> **Run this in CI against a dedicated test PostgreSQL instance, not production or staging.** Use Docker Compose to spin up a fresh Postgres for each test run.

---

## 7. PostgreSQL Type Intricacies

### 7.1 PostgreSQL ENUM Types

PostgreSQL `ENUM` types are **first-class database objects**, not inline constraints. This makes them tricky:

```python
# Defining a PostgreSQL ENUM in a migration
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM

order_status_enum = PG_ENUM(
    "pending", "processing", "shipped", "delivered", "cancelled",
    name="order_status_enum",
    create_type=False,  # We'll create it manually below
)

def upgrade() -> None:
    # Create the ENUM type first (outside a transaction if adding to existing ENUM)
    op.execute("CREATE TYPE order_status_enum AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled')")
    op.add_column("orders", sa.Column("status", order_status_enum, nullable=False))

def downgrade() -> None:
    op.drop_column("orders", "status")
    op.execute("DROP TYPE order_status_enum")
```

**Adding a value to an existing ENUM (PostgreSQL 9.1+):**

```python
# ⚠️ ALTER TYPE ... ADD VALUE cannot run inside a transaction in PostgreSQL < 12
# For PostgreSQL 12+, it can run inside a transaction in most cases.

def upgrade() -> None:
    op.execute("ALTER TYPE order_status_enum ADD VALUE IF NOT EXISTS 'refunded'")

def downgrade() -> None:
    # ❌ You CANNOT remove values from a PostgreSQL ENUM.
    # Downgrade must recreate the type if removal is critical.
    # This is often left as a no-op with a comment.
    pass  # ENUM value removal requires recreating the type and all dependent columns
```

> [!IMPORTANT]
> You **cannot remove values** from a PostgreSQL ENUM type using `ALTER TYPE`. If you need to remove an ENUM value, you must: drop all columns using the type, drop the type, recreate it without the value, and recreate the columns. This is a destructive operation requiring careful data migration.

### 7.2 JSONB Columns

```python
from sqlalchemy.dialects.postgresql import JSONB

def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column(
            "metadata",
            JSONB,
            nullable=True,
            server_default=sa.text("'{}'::jsonb"),  # Empty JSON object default
        ),
    )
    # Add a GIN index for fast JSONB queries
    op.create_index(
        "ix_products_metadata_gin",
        "products",
        ["metadata"],
        postgresql_using="gin",
    )

def downgrade() -> None:
    op.drop_index("ix_products_metadata_gin", table_name="products")
    op.drop_column("products", "metadata")
```

### 7.3 Concurrent Index Creation — Zero-Downtime Indexing

`CREATE INDEX` in PostgreSQL takes a `ShareLock` on the table, blocking writes. For large production tables, use `CREATE INDEX CONCURRENTLY`.

> [!IMPORTANT]
> `CREATE INDEX CONCURRENTLY` **cannot run inside a transaction**. You must use a special migration pattern that disables Alembic's transaction wrapping for that specific operation.

```python
# The correct pattern for zero-downtime index creation

def upgrade() -> None:
    # Disable the Alembic transaction wrapper for this migration
    op.execute("COMMIT")  # Close the outer transaction
    
    op.create_index(
        "ix_orders_created_at",
        "orders",
        ["created_at"],
        postgresql_concurrently=True,  # Generates CREATE INDEX CONCURRENTLY
        if_not_exists=True,
    )

def downgrade() -> None:
    op.execute("COMMIT")
    op.drop_index(
        "ix_orders_created_at",
        table_name="orders",
        postgresql_concurrently=True,  # Generates DROP INDEX CONCURRENTLY
    )
```

Alternatively, configure the migration file to opt out of transaction wrapping entirely:

```python
# At the module level in the migration file:

# This disables the wrapping transaction for the entire migration file.
# Use ONLY when the migration contains non-transactional DDL.

from alembic import context

def upgrade() -> None:
    if not context.is_offline_mode():
        # Get the raw connection and disable autocommit wrapper
        conn = op.get_bind()
        conn.execution_options(isolation_level="AUTOCOMMIT")
    
    op.create_index(
        "ix_orders_created_at",
        "orders",
        ["created_at"],
        postgresql_concurrently=True,
    )
```

### 7.4 Partial Indexes

```python
def upgrade() -> None:
    # Index only active users — dramatically smaller index, faster queries
    op.create_index(
        "ix_users_email_active",
        "users",
        ["email"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )

def downgrade() -> None:
    op.drop_index("ix_users_email_active", table_name="users")
```

### 7.5 Table Partitioning

Alembic does not natively generate partitioned table DDL. Use `op.execute()` with raw SQL:

```python
def upgrade() -> None:
    op.execute("""
        CREATE TABLE events (
            id          BIGSERIAL,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            event_type  TEXT NOT NULL,
            payload     JSONB
        ) PARTITION BY RANGE (created_at)
    """)
    op.execute("""
        CREATE TABLE events_2024_q1 PARTITION OF events
        FOR VALUES FROM ('2024-01-01') TO ('2024-04-01')
    """)
    op.execute("""
        CREATE TABLE events_2024_q2 PARTITION OF events
        FOR VALUES FROM ('2024-04-01') TO ('2024-07-01')
    """)

def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS events_2024_q2")
    op.execute("DROP TABLE IF EXISTS events_2024_q1")
    op.execute("DROP TABLE IF EXISTS events")
```

---

## 8. Quick Reference Cheat Sheet

### Essential Commands

| Command | Description |
|---|---|
| `alembic init alembic` | Initialize a new Alembic environment |
| `alembic revision -m "msg"` | Create a blank migration file |
| `alembic revision --autogenerate -m "msg"` | Auto-generate migration from model diff |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic upgrade +2` | Apply the next 2 migrations |
| `alembic downgrade -1` | Revert the last migration |
| `alembic downgrade base` | Revert ALL migrations |
| `alembic current` | Show the current revision in the DB |
| `alembic history --verbose` | Show full migration history with details |
| `alembic heads` | Show all current head revisions |
| `alembic merge -m "msg" rev1 rev2` | Merge two divergent heads |
| `alembic stamp rev_id` | Mark a revision as current without running DDL |
| `alembic upgrade head --sql` | Generate SQL without executing (offline mode) |
| `alembic show rev_id` | Show details of a specific revision |

### Common `op.*` Operations Reference

```python
# Tables
op.create_table("name", sa.Column(...), ...)
op.drop_table("name")
op.rename_table("old_name", "new_name")

# Columns
op.add_column("table", sa.Column("col", sa.Integer()))
op.drop_column("table", "col")
op.alter_column("table", "col", nullable=False, new_column_name="new_col",
                type_=sa.String(255), server_default="default_val")

# Indexes
op.create_index("ix_name", "table", ["col1", "col2"], unique=True)
op.drop_index("ix_name", table_name="table")

# Constraints
op.create_foreign_key("fk_name", "source", "referent", ["col"], ["id"],
                      ondelete="CASCADE")
op.drop_constraint("fk_name", "table", type_="foreignkey")
op.create_unique_constraint("uq_name", "table", ["col1", "col2"])
op.create_check_constraint("ck_name", "table", "amount > 0")

# Raw SQL (escape hatch for PostgreSQL-specific DDL)
op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
op.execute(sa.text("UPDATE users SET status = 'active' WHERE status IS NULL"))
```
## sqlacodegen
sqlacodegen is a command-line tool that performs "reverse engineering" on your database. While Alembic usually goes from Code → Database, sqlacodegen goes from Database → Code. [1] 
## Commands:

pip install sqlacodegen psycopg2
sqlacodegen postgresql+psycopg2://user:password@localhost:5432/dbname > models.py

### Pre-Merge Checklist

- [ ] Migration file reviewed by at least one other engineer
- [ ] `alembic heads` shows only one head after your addition
- [ ] Stairway test (upgrade → downgrade → upgrade) passes in CI
- [ ] `alembic upgrade head --sql` output has been attached to the PR
- [ ] Migration has a corresponding `downgrade()` that fully reverses the changes
- [ ] Column naming follows the team convention
- [ ] Constraint naming convention is applied (via MetaData)
- [ ] NOT NULL additions on populated tables use the 3-step pattern
- [ ] CONCURRENT index operations are in their own migration file

---

*This document is a living standard. Update it as the team discovers new patterns, edge cases, or PostgreSQL version-specific behaviors. Every section should map to a real incident or engineering decision.*
