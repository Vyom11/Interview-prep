"""
Safety utilities: SQL validation, step limits, tool whitelists.
"""

import re
from typing import FrozenSet

SQL_TOOL_WHITELIST: FrozenSet[str] = frozenset({"get_schema", "run_readonly_query"})
RAG_TOOL_WHITELIST: FrozenSet[str] = frozenset({"search_documents"})

_BLOCKED_SQL_PATTERN = re.compile(
    r"\b("
    r"insert|update|delete|drop|alter|truncate|create|grant|revoke|"
    r"merge|replace|call|execute|copy|vacuum|reindex|attach|detach|"
    r"pragma|lock|unload|install|load|into\s+outfile"
    r")\b",
    re.IGNORECASE,
)


def assert_tool_allowed(tool_name: str, whitelist: FrozenSet[str]) -> None:
    if tool_name not in whitelist:
        raise PermissionError(f"Tool '{tool_name}' is not allowed for this agent path.")


def validate_readonly_sql(sql: str) -> str:
    if not sql or not sql.strip():
        raise ValueError("Empty SQL query.")

    normalized = sql.strip().rstrip(";")
    lower = normalized.lower()

    if ";" in normalized:
        raise ValueError("Multiple SQL statements are not allowed.")

    if not (lower.startswith("select") or lower.startswith("with")):
        raise ValueError("Only SELECT queries (including WITH/CTE) are permitted.")

    if _BLOCKED_SQL_PATTERN.search(lower):
        raise ValueError("Query contains forbidden SQL keywords.")

    return normalized


def check_step_limit(step_count: int, max_steps: int) -> None:
    if step_count >= max_steps:
        raise RuntimeError(f"Agent exceeded maximum steps ({max_steps}).")
