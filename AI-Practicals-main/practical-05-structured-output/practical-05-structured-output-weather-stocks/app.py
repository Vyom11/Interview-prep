from datetime import datetime
from dotenv import load_dotenv

from models.tool_schema import ToolDecision
from services.bedrock_client import BedrockService
from tools.weather_tool import get_weather
from tools.stock_tool import get_stock_price
from utils.file_handler import save_output


load_dotenv()


def execute_tool(
    tool_name: str,
    tool_input: str
) -> str:
    """
    Execute selected tool.
    """

    if tool_name == "get_weather":
        return get_weather(tool_input)

    if tool_name == "get_stock_price":
        return get_stock_price(tool_input)

    return "Unknown tool selected."


def main() -> None:
    """
    Main application loop.
    """

    service = BedrockService()

    print("\nInteractive Tool Calling Demo")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Enter your query: ")

        if query.lower() == "exit":
            print("\nExiting application.")
            break

        try:
            decision = service.decide_tool(query)

            validated_decision = ToolDecision(
                **decision
            )

            result = execute_tool(
                validated_decision.tool,
                validated_decision.input
            )

            output_data = {
                "timestamp": str(datetime.now()),
                "query": query,
                "selected_tool": validated_decision.tool,
                "tool_input": validated_decision.input,
                "response": result
            }

            save_output(
                output_data,
                "outputs/tool_calling_results.json"
            )

            print("\n--------------------------------")
            print(
                f"Selected Tool: "
                f"{validated_decision.tool}"
            )

            print(
                f"Tool Input: "
                f"{validated_decision.input}"
            )

            print("\nResponse:")
            print(result)
            print("--------------------------------\n")

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()