"""Conversation memory for the LangChain agent."""

from typing import Dict, List


class ConversationMemory:
    """Simple in-memory conversation history store."""

    def __init__(self) -> None:
        self._history: Dict[str, List[dict[str, str]]] = {}

    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        conversation_id = conversation_id or "default"
        self._history.setdefault(conversation_id, []).append(
            {"role": role, "content": content}
        )

    def get_history(self, conversation_id: str) -> List[dict[str, str]]:
        return self._history.setdefault(conversation_id or "default", [])

    def get_context(self, conversation_id: str, max_messages: int = 8) -> str:
        history = self.get_history(conversation_id)[-max_messages:]
        if not history:
            return ""

        return "\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in history
        )
