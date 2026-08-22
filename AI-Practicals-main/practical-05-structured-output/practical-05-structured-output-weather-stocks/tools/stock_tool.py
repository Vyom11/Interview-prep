from services.bedrock_client import BedrockService


def get_stock_price(company: str) -> str:
    """
    Generate realistic stock summary using Nova Lite.
    """

    service = BedrockService()

    prompt = f"""
Provide a concise stock market summary for {company}.

Include:
- likely stock trend
- investor sentiment
- concise analysis

Keep the response short.
"""

    return service.invoke_model(prompt)