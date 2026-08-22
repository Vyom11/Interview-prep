"""
LangGraph nodes: classifier, SQL agent, RAG agent, and hybrid agent.
"""

from __future__ import annotations

import re

from langchain_aws import ChatBedrock
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.agent import db as sql_db
from app.agent.state import AgentState
from app.core.aws_clients import bedrock_client
from app.core.config import AGENT_MAX_STEPS, BEDROCK_LLM_MODEL
from app.core.safety import check_step_limit
from app.rag.chain import rag_answer_with_history

_llm = ChatBedrock(client=bedrock_client, model_id=BEDROCK_LLM_MODEL)


def _latest_user_text(state: AgentState) -> str:
    for message in reversed(state["messages"]):
        if isinstance(message, HumanMessage):
            return message.content
        if isinstance(message, dict) and message.get("role") == "user":
            return message["content"]
    return ""


def _conversation_snippet(state: AgentState, max_turns: int = 6) -> str:
    lines: list[str] = []
    for message in state["messages"][-max_turns:]:
        if isinstance(message, HumanMessage):
            lines.append(f"User: {message.content}")
        elif isinstance(message, AIMessage):
            lines.append(f"Assistant: {message.content}")
        elif isinstance(message, dict):
            role = message.get("role", "unknown")
            lines.append(f"{role.capitalize()}: {message.get('content', '')}")
    return "\n".join(lines)


def _run_sql_path(state: AgentState) -> dict:
    """Run the SQL branch and return a structured result."""
    check_step_limit(state.get("step_count", 0), AGENT_MAX_STEPS)
    question = _latest_user_text(state)

    try:
        schema = sql_db.get_schema()
    except Exception as exc:
        safe = f"I could not complete your request. SQL agent error: Database connection failed: {exc}"
        return {"answer": safe, "error": f"Database connection failed: {exc}"}

    sql_system = SystemMessage(
        content=(
            "You are a PostgreSQL analyst. Given the schema and question, write ONE "
            "read-only SELECT query (WITH/CTE allowed). Output ONLY the SQL, no markdown."
        )
    )
    sql_human = HumanMessage(
        content=f"Schema:\n{schema}\n\nQuestion: {question}\n\nConversation:\n{_conversation_snippet(state)}"
    )

    generated_sql = ""
    try:
        sql_response = _llm.invoke([sql_system, sql_human])
        generated_sql = (sql_response.content or "").strip()
        generated_sql = re.sub(
            r"^```(?:sql)?\s*|\s*```$", "", generated_sql, flags=re.I
        ).strip()
        rows_json = sql_db.run_readonly_query(generated_sql)
    except Exception as exc:
        safe = f"I could not complete your request. SQL agent error: {exc}"
        return {
            "answer": safe,
            "error": f"SQL agent error: {exc}",
            "generated_sql": generated_sql,
        }

    answer_system = SystemMessage(
        content=(
            "Summarize query results for the user in clear natural language. "
            "If results are empty, say so. Do not invent data not in the results."
        )
    )
    answer_human = HumanMessage(
        content=(
            f"Question: {question}\n\nSQL executed:\n{generated_sql}\n\nResults:\n{rows_json}"
        )
    )

    try:
        answer_response = _llm.invoke([answer_system, answer_human])
        answer = answer_response.content or "No answer generated."
    except Exception as exc:
        safe = (
            f"I could not complete your request. Failed to summarize SQL results: {exc}"
        )
        return {
            "answer": safe,
            "error": f"Failed to summarize SQL results: {exc}",
            "generated_sql": generated_sql,
        }

    return {
        "answer": answer,
        "error": None,
        "generated_sql": generated_sql,
        "rows_json": rows_json,
    }


def _run_rag_path(state: AgentState) -> dict:
    """Run the RAG branch and return a structured result."""
    check_step_limit(state.get("step_count", 0), AGENT_MAX_STEPS)
    question = _latest_user_text(state)

    try:
        answer = rag_answer_with_history(question, state["messages"])
    except Exception as exc:
        safe = f"I could not complete your request. RAG agent error: {exc}"
        return {"answer": safe, "error": f"RAG agent error: {exc}"}

    return {"answer": answer, "error": None}


def _node_response(state: AgentState, result: dict) -> dict:
    return {
        "answer": result["answer"],
        "messages": [AIMessage(content=result["answer"])],
        "step_count": state.get("step_count", 0) + 1,
        "error": result.get("error"),
    }


def classifier_node(state: AgentState) -> dict:
    """Route the question to SQL, RAG, or a hybrid path."""
    check_step_limit(state.get("step_count", 0), AGENT_MAX_STEPS)
    question = _latest_user_text(state)

    system = SystemMessage(
        content=(
            "You are a query router. Classify the user's latest question as exactly "
            "one of: sql, rag, hybrid.\n"
            "- sql: questions about structured data, metrics, counts, aggregates, "
            "tables, sales, orders, customers, revenue, database records.\n"
            "- rag: questions about documents, policies, PDF content, manuals, "
            "procedures, or anything requiring unstructured document retrieval.\n"
            "- hybrid: questions that need both database facts and document facts, "
            "or that explicitly ask to combine both sources.\n"
            "Reply with only the single word: sql, rag, or hybrid."
        )
    )
    human = HumanMessage(
        content=f"Conversation:\n{_conversation_snippet(state)}\n\nLatest question: {question}"
    )

    try:
        response = _llm.invoke([system, human])
        raw = (response.content or "").strip().lower()
        if "hybrid" in raw or ("sql" in raw and "rag" in raw):
            route = "hybrid"
        else:
            match = re.search(r"\b(sql|rag)\b", raw)
            route = match.group(1) if match else "rag"
    except Exception:
        route = "rag"

    return {
        "route": route,
        "step_count": state.get("step_count", 0) + 1,
        "error": None,
    }


def sql_agent_node(state: AgentState) -> dict:
    """Introspect schema, generate read-only SQL, execute, and summarize."""
    return _node_response(state, _run_sql_path(state))


def rag_agent_node(state: AgentState) -> dict:
    """Answer using the OpenSearch-backed RAG pipeline."""
    return _node_response(state, _run_rag_path(state))


def hybrid_agent_node(state: AgentState) -> dict:
    """Answer using both SQL and RAG, then synthesize a combined response."""
    check_step_limit(state.get("step_count", 0), AGENT_MAX_STEPS)
    question = _latest_user_text(state)

    sql_result = _run_sql_path(state)
    rag_result = _run_rag_path(state)

    if sql_result.get("error") and rag_result.get("error"):
        return _error_response(
            state,
            f"Hybrid agent error: {sql_result['error']} ; {rag_result['error']}",
        )

    synthesis_system = SystemMessage(
        content=(
            "You are an analytics assistant. Combine structured database findings and "
            "document evidence into one concise answer. Use both sources when relevant. "
            "Do not invent facts, and if one source failed, mention that gently without "
            "masking the successful source."
        )
    )
    synthesis_human = HumanMessage(
        content=(
            f"Question: {question}\n\n"
            f"SQL result:\n{sql_result['answer']}\n\n"
            f"RAG result:\n{rag_result['answer']}\n\n"
            "Write a single user-facing answer that combines the two sources."
        )
    )

    try:
        synthesis_response = _llm.invoke([synthesis_system, synthesis_human])
        answer = synthesis_response.content or "No answer generated."
    except Exception:
        parts: list[str] = []
        if sql_result.get("error"):
            parts.append(f"SQL: {sql_result['answer']}")
        else:
            parts.append(sql_result["answer"])
        if rag_result.get("error"):
            parts.append(f"RAG: {rag_result['answer']}")
        else:
            parts.append(rag_result["answer"])
        answer = "\n\n".join(parts)

    return {
        "answer": answer,
        "messages": [AIMessage(content=answer)],
        "step_count": state.get("step_count", 0) + 1,
        "error": None,
    }


def _error_response(state: AgentState, message: str) -> dict:
    safe = f"I could not complete your request. {message}"
    return {
        "answer": safe,
        "messages": [AIMessage(content=safe)],
        "error": message,
        "step_count": state.get("step_count", 0) + 1,
    }
