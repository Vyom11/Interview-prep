"""LangChain agent implementation with tools, memory, and safety limits."""

from __future__ import annotations

from typing import Optional
from uuid import uuid4

from app.agent.memory import ConversationMemory
from app.agent.tools import CalculatorTool, RAGRetrieverTool, WebSearchTool
from app.core.aws_clients import bedrock_client
from app.core.config import BEDROCK_LLM_MODEL
from langchain.agents.factory import create_agent
from langchain.agents.middleware.tool_call_limit import (
    ToolCallLimitExceededError,
    ToolCallLimitMiddleware,
)
from langchain_aws import ChatBedrock

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful assistant that can use tools to answer questions. "
    "If the user asks for calculations, use the calculator tool. "
    "If the user asks about ingested documents, use the document_retriever tool. "
    "If the user asks for a general web-style answer, use the web_search tool. "
    "Always provide the best answer using tools when appropriate."
)

agent_memory = ConversationMemory()


def _build_agent(max_iterations: int = 6, system_prompt: Optional[str] = None):
    """Build a LangChain agent with a tool call limit middleware."""
    model = ChatBedrock(client=bedrock_client, model_id=BEDROCK_LLM_MODEL)
    tools = [CalculatorTool(), WebSearchTool(), RAGRetrieverTool()]
    middleware = [
        ToolCallLimitMiddleware(run_limit=max_iterations, exit_behavior="error")
    ]

    return create_agent(
        model,
        tools=tools,
        system_prompt=system_prompt or DEFAULT_SYSTEM_PROMPT,
        middleware=middleware,
        name="rag-agent",
    )


def _extract_agent_answer(response: object) -> str:
    """Extract the final assistant text from the agent graph response."""
    if isinstance(response, dict) and "messages" in response:
        for message in reversed(response["messages"]):
            if hasattr(message, "content"):
                return message.content
        return ""
    if hasattr(response, "content"):
        return response.content
    return str(response)


def ask_agent(
    question: str,
    conversation_id: Optional[str] = None,
    max_iterations: int = 6,
) -> str:
    """Ask the agent a question while maintaining conversation memory."""
    conversation_id = conversation_id or str(uuid4())
    agent_memory.add_message(conversation_id, "user", question)

    history = agent_memory.get_context(conversation_id)
    system_prompt = DEFAULT_SYSTEM_PROMPT
    if history:
        system_prompt = (
            f"{DEFAULT_SYSTEM_PROMPT}\n\nConversation history:\n{history}\n\n"
            "Continue the conversation with awareness of prior user questions and answers."
        )

    agent = _build_agent(max_iterations=max_iterations, system_prompt=system_prompt)

    try:
        response = agent.invoke({"messages": [{"role": "user", "content": question}]})
    except ToolCallLimitExceededError:
        answer = (
            "The agent stopped safely after reaching the configured max_iterations limit. "
            "If you need a longer run, increase max_iterations."
        )
        agent_memory.add_message(conversation_id, "assistant", answer)
        return answer

    answer = _extract_agent_answer(response)
    agent_memory.add_message(conversation_id, "assistant", answer)
    return answer
