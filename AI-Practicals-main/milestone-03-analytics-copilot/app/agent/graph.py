"""
LangGraph workflow: classifier → SQL, RAG, or hybrid path.
"""

from __future__ import annotations

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.agent.nodes import classifier_node, hybrid_agent_node, rag_agent_node, sql_agent_node
from app.agent.state import AgentState

_checkpointer = MemorySaver()
_compiled_graph = None


def _route_after_classifier(state: AgentState) -> str:
    if state.get("route") == "sql":
        return "sql_agent"
    if state.get("route") == "hybrid":
        return "hybrid_agent"
    return "rag_agent"


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("classifier", classifier_node)
    workflow.add_node("sql_agent", sql_agent_node)
    workflow.add_node("rag_agent", rag_agent_node)
    workflow.add_node("hybrid_agent", hybrid_agent_node)

    workflow.add_edge(START, "classifier")
    workflow.add_conditional_edges(
        "classifier",
        _route_after_classifier,
        {"sql_agent": "sql_agent", "rag_agent": "rag_agent", "hybrid_agent": "hybrid_agent"},
    )
    workflow.add_edge("sql_agent", END)
    workflow.add_edge("rag_agent", END)
    workflow.add_edge("hybrid_agent", END)

    return workflow.compile(checkpointer=_checkpointer)


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph
