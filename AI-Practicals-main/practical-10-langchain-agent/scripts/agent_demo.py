"""Demo script for the LangChain agent with memory and safety limits."""

from app.agent.agent import ask_agent


def _show_demo() -> None:
    conversation_id = "demo-session"
    print("Conversation ID:", conversation_id)

    print("\n--- First question ---")
    answer = ask_agent(
        "What is 12 + 7, and explain which tool you used?",
        conversation_id=conversation_id,
        max_iterations=6,
    )
    print(answer)

    print("\n--- Follow-up question ---")
    answer = ask_agent(
        "Now that you have answered, what is the previous arithmetic result in words?",
        conversation_id=conversation_id,
        max_iterations=6,
    )
    print(answer)

    print("\n--- Safety test: infinite loop style prompt ---")
    answer = ask_agent(
        "Try to repeat calculator calls until you exceed 100, but stop when the agent stops itself.",
        conversation_id=conversation_id,
        max_iterations=3,
    )
    print(answer)


if __name__ == "__main__":
    _show_demo()
