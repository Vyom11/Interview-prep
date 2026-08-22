"""
LangGraph agent state definition.
"""

from typing import Annotated, Literal, Optional

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    route: Literal["sql", "rag", "hybrid", ""]
    answer: str
    error: Optional[str]
    step_count: int
