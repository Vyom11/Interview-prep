"""
PostgreSQL connection, schema introspection, and read-only query execution.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any

import psycopg2
import psycopg2.extras

from app.core.safety import SQL_TOOL_WHITELIST, assert_tool_allowed, validate_readonly_sql
from app.core.config import AGENT_MAX_SQL_ROWS, postgres_dsn


@contextmanager
def _connection():
    conn = psycopg2.connect(postgres_dsn())
    try:
        yield conn
    finally:
        conn.close()


def get_schema() -> str:
    """Return a human-readable schema summary for the LLM."""
    assert_tool_allowed("get_schema", SQL_TOOL_WHITELIST)

    query = """
    SELECT
        c.table_schema,
        c.table_name,
        c.column_name,
        c.data_type,
        c.is_nullable
    FROM information_schema.columns c
    WHERE c.table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY c.table_schema, c.table_name, c.ordinal_position;
    """

    with _connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

    if not rows:
        return "No user tables found in the database."

    tables: dict[str, list[str]] = {}
    for row in rows:
        key = f"{row['table_schema']}.{row['table_name']}"
        col = f"  - {row['column_name']} ({row['data_type']}, nullable={row['is_nullable']})"
        tables.setdefault(key, []).append(col)

    lines = ["Database schema:"]
    for table, columns in tables.items():
        lines.append(f"\nTable: {table}")
        lines.extend(columns)
    return "\n".join(lines)


def run_readonly_query(sql: str) -> str:
    """Execute a validated read-only query and return JSON rows."""
    assert_tool_allowed("run_readonly_query", SQL_TOOL_WHITELIST)

    safe_sql = validate_readonly_sql(sql)
    limited_sql = f"SELECT * FROM ({safe_sql}) AS _agent_subq LIMIT {AGENT_MAX_SQL_ROWS}"

    with _connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(limited_sql)
            rows: list[dict[str, Any]] = cur.fetchall()

    return json.dumps(rows, default=str, indent=2)
