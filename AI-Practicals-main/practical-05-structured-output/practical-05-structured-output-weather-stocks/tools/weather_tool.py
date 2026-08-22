from services.bedrock_client import BedrockService


def get_weather(city: str) -> str:
    """
    Generate realistic weather response using Nova Lite.
    """

    service = BedrockService()

    prompt = f"""
Provide a realistic current weather summary for {city}.

Keep the response concise and user-friendly.
"""

    return service.invoke_model(prompt)