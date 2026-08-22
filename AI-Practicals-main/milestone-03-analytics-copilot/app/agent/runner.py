"""
Public entry point for the routing agent with memory and tracing.
"""

from __future__ import annotations

from typing import Any, Optional

from langchain_core.messages import HumanMessage

from app.agent.graph import get_graph
from app.agent.tracing import flush_langfuse, langfuse_callbacks, langfuse_run_metadata
from app.agent.state import AgentState


def run_agent(
    question: str,
    session_id: str = "default",
    user_id: Optional[str] = None,
) -> dict[str, Any]:
    """
    Run the routing agent for one user turn.
    Conversation history is persisted per session_id via LangGraph checkpointer.
    """
    graph = get_graph()
    config = {
        "configurable": {"thread_id": session_id},
        "callbacks": langfuse_callbacks(session_id=session_id, user_id=user_id),
        "run_name": "routing-agent",
        "metadata": langfuse_run_metadata(session_id=session_id, user_id=user_id),
    }

    input_state: AgentState = {
        "messages": [HumanMessage(content=question)],
        "route": "",
        "answer": "",
        "error": None,
        "step_count": 0,
    }

    try:
        result = graph.invoke(input_state, config=config)
    finally:
        flush_langfuse()

    return {
        "answer": result.get("answer", ""),
        "route": result.get("route", ""),
        "error": result.get("error"),
        "session_id": session_id,
    }
