import json

import boto3
from botocore.exceptions import ClientError


class BedrockService:
    """
    Service wrapper for Amazon Bedrock model invocation.
    """

    def __init__(self, region_name: str = "us-east-1") -> None:
        self.client = boto3.client(
            service_name="bedrock-runtime", region_name=region_name
        )

    def invoke_model(self, prompt: str) -> str:
        """
        Generic Bedrock model invocation.
        """

        body = {
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {
                "max_new_tokens": 300,
                "temperature": 0.1,
                "top_p": 0.9,
            },
        }

        try:
            response = self.client.invoke_model(
                modelId="us.amazon.nova-2-lite-v1:0",
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json",
            )

            response_body = json.loads(response["body"].read())

            output_content = (
                response_body.get("output", {}).get("message", {}).get("content", [])
            )

            if not output_content:
                raise ValueError("No content returned from model.")

            return output_content[0].get("text", "").strip()

        except ClientError as error:
            raise RuntimeError(f"Bedrock invocation failed: {error}") from error

        except Exception as error:
            raise RuntimeError(f"Unexpected error occurred: {error}") from error

    def decide_tool(self, query: str) -> dict:
        """
        Decide which tool should handle the query.
        """

        prompt = f"""
You are an AI routing assistant.

Available tools:

1. get_weather
   - Use for weather-related queries

2. get_stock_price
   - Use for stock/company/market queries

Return ONLY valid JSON.

Example:
{{
    "tool": "get_weather",
    "input": "Ahmedabad"
}}

Query:
{query}
"""

        response = self.invoke_model(prompt)

        cleaned_response = response.replace("```json", "").replace("```", "").strip()

        return json.loads(cleaned_response)
