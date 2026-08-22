"""
RAG chain implementation.
"""

from __future__ import annotations

import re
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.core.safety import RAG_TOOL_WHITELIST, assert_tool_allowed
from app.core.aws_clients import bedrock_client
from app.core.config import BEDROCK_LLM_MODEL
from app.rag.retriever import retriever
from langchain_aws import ChatBedrock

llm = ChatBedrock(client=bedrock_client, model_id=BEDROCK_LLM_MODEL)


def _doc_label(doc: Any, index: int) -> str:
    metadata = getattr(doc, "metadata", {}) or {}
    source = metadata.get("source", "unknown-source")
    page = metadata.get("page")
    page_label = f", page {page}" if page is not None else ""
    return f"[{index}] source={source}{page_label}"


def _format_docs(docs: list[Any]) -> str:
    parts: list[str] = []
    for index, doc in enumerate(docs, start=1):
        parts.append(f"{_doc_label(doc, index)}\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def _retrieve_documents(query: str) -> list[Any]:
    docs = retriever.invoke(query)
    if not docs:
        return []
    unique_docs: list[Any] = []
    seen: set[str] = set()
    for doc in docs:
        content = getattr(doc, "page_content", "").strip()
        if not content or content in seen:
            continue
        seen.add(content)
        unique_docs.append(doc)
    return unique_docs[:5]


def search_documents(query: str) -> str:
    """Whitelisted RAG tool: retrieve relevant document chunks."""
    assert_tool_allowed("search_documents", RAG_TOOL_WHITELIST)
    docs = _retrieve_documents(query)
    if not docs:
        return "No relevant documents found."
    return _format_docs(docs)


def _format_history(messages: list[Any], max_turns: int = 6) -> str:
    lines: list[str] = []
    for message in messages[-max_turns:]:
        if isinstance(message, HumanMessage):
            lines.append(f"User: {message.content}")
        elif isinstance(message, AIMessage):
            lines.append(f"Assistant: {message.content}")
        elif isinstance(message, dict):
            role = message.get("role", "unknown")
            lines.append(f"{role.capitalize()}: {message.get('content', '')}")
    return "\n".join(lines) if lines else "(no prior turns)"


def rag_answer_with_history(question: str, messages: list[Any]) -> str:
    """RAG answer using retrieved context and conversation memory."""
    docs = _retrieve_documents(question)
    if not docs:
        return (
            "I could not find enough relevant information in the retrieved document "
            "passages to answer confidently."
        )

    context = _format_docs(docs)
    history = _format_history(messages)

    answer_system = SystemMessage(
        content=(
            "You are a careful document QA assistant.\n"
            "Use ONLY the retrieved context and the conversation history if it helps "
            "interpret the question.\n"
            "Do not use outside knowledge.\n"
            "If the retrieved context does not clearly support the answer, say you do "
            "not have enough information.\n"
            "When you answer, prefer explicit facts from the passages and cite the "
            "relevant chunk labels like [1] or [2].\n"
            "Do not guess the document topic if the evidence is weak."
        )
    )
    answer_human = HumanMessage(
        content=(
            f"Conversation history:\n{history}\n\n"
            f"Retrieved context:\n{context}\n\n"
            f"Question:\n{question}"
        )
    )
    response = llm.invoke([answer_system, answer_human])
    draft_answer = response.content or "I do not have enough information."

    verifier_system = SystemMessage(
        content=(
            "You are a strict grounding checker.\n"
            "Decide whether the candidate answer is fully supported by the retrieved "
            "context.\n"
            "If the answer adds facts that are not explicit in the context, return "
            "NOT_GROUNDED.\n"
            "If it is fully supported, return GROUNDED.\n"
            "Reply with only one word: GROUNDED or NOT_GROUNDED."
        )
    )
    verifier_human = HumanMessage(
        content=(
            f"Retrieved context:\n{context}\n\n"
            f"Candidate answer:\n{draft_answer}\n\n"
            f"Question:\n{question}"
        )
    )

    try:
        verdict_response = llm.invoke([verifier_system, verifier_human])
        verdict = re.sub(r"[^A-Z_]", "", (verdict_response.content or "").upper())
    except Exception:
        verdict = "NOT_GROUNDED"

    if verdict != "GROUNDED":
        return (
            "I do not have enough information in the retrieved passages to answer "
            "confidently without guessing."
        )

    return draft_answer


def ask_question(question: str) -> str:
    """
    Ask question using RAG.
    """

    return rag_answer_with_history(question, [])
