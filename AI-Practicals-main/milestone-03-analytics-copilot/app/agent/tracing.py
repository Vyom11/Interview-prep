"""
LangFuse tracing integration for LangGraph / LangChain (SDK v3+ / v4+).
"""

from __future__ import annotations

import os
from typing import Any, Optional

from app.core.config import (
    LANGFUSE_ENABLED,
    LANGFUSE_HOST,
    LANGFUSE_PUBLIC_KEY,
    LANGFUSE_SECRET_KEY,
)


def _ensure_langfuse_env() -> None:
    """Langfuse v4 reads credentials from environment variables."""
    if LANGFUSE_PUBLIC_KEY:
        os.environ.setdefault("LANGFUSE_PUBLIC_KEY", LANGFUSE_PUBLIC_KEY)
    if LANGFUSE_SECRET_KEY:
        os.environ.setdefault("LANGFUSE_SECRET_KEY", LANGFUSE_SECRET_KEY)
    if LANGFUSE_HOST:
        os.environ.setdefault("LANGFUSE_BASE_URL", LANGFUSE_HOST.rstrip("/"))


def langfuse_callbacks(
    session_id: str,
    user_id: Optional[str] = None,
    tags: Optional[list[str]] = None,
) -> list[Any]:
    """
    Return LangChain callback handlers for LangFuse tracing.
    Returns an empty list when tracing is disabled, keys are missing, or init fails.
    """
    if not LANGFUSE_ENABLED or not LANGFUSE_PUBLIC_KEY or not LANGFUSE_SECRET_KEY:
        return []

    try:
        _ensure_langfuse_env()
        try:
            from langfuse.langchain import CallbackHandler
        except ImportError:
            from langfuse.callback import CallbackHandler

        # Langfuse 4.x: credentials via env; session/user/tags via run metadata
        return [CallbackHandler(public_key=LANGFUSE_PUBLIC_KEY)]
    except Exception:
        return []


def langfuse_run_metadata(
    session_id: str,
    user_id: Optional[str] = None,
    tags: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Metadata keys read by Langfuse LangChain callback handler."""
    meta: dict[str, Any] = {
        "langfuse_session_id": session_id,
        "langfuse_tags": tags or ["routing-agent"],
    }
    if user_id:
        meta["langfuse_user_id"] = user_id
    return meta


def flush_langfuse() -> None:
    """Flush pending LangFuse events (call after graph invocation)."""
    if not LANGFUSE_ENABLED:
        return
    try:
        _ensure_langfuse_env()
        from langfuse import get_client

        get_client(public_key=LANGFUSE_PUBLIC_KEY or None).flush()
    except Exception:
        pass
