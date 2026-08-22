import json

import boto3
from botocore.exceptions import ClientError


class BedrockService:
    """
    Service wrapper for Amazon Bedrock.
    """

    def __init__(self, region_name: str = "us-east-1") -> None:

        self.client = boto3.client(
            service_name="bedrock-runtime", region_name=region_name
        )

    def invoke_model(self, prompt: str) -> str:
        """
        Generic Bedrock invocation.
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
                modelId="amazon.nova-lite-v1:0",
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

    def classify_text(self, text: str) -> dict:
        """
        Perform text classification.
        """

        prompt = f"""
Classify the following text sentiment.

Possible labels:
positive
negative
neutral

Return ONLY valid JSON.

Example:
{{
    "label": "negative",
    "confidence": 0.91
}}

Do not include explanations.
Do not include markdown.
Do not include extra text.

Text:
{text}
"""

        response = self.invoke_model(prompt)

        cleaned_response = response.replace("```json", "").replace("```", "").strip()

        start_index = cleaned_response.find("{")
        end_index = cleaned_response.rfind("}")

        if start_index == -1 or end_index == -1:
            raise ValueError("No valid JSON found in model response.")

        json_content = cleaned_response[start_index : end_index + 1]

        return json.loads(json_content)

    def summarize_text(self, text: str) -> str:
        """
        Summarize input text.
        """

        prompt = f"""
Summarize the following text in 2-3 concise sentences.

Text:
{text}
"""

        return self.invoke_model(prompt)
