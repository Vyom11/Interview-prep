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

    def analyze_review(self, review: str) -> dict:
        """
        Analyze a product review using Amazon Nova Lite.
        """

        prompt = f"""
You are an AI assistant that extracts structured information from product reviews.

Return ONLY valid JSON.

Example:
{{
    "sentiment": "positive",
    "key_topics": ["battery", "display"],
    "rating_estimate": 4
}}

Rules:
sentiment must be one of: positive, negative, neutral
key_topics must be a JSON array of strings
rating_estimate must be an integer between 1 and 5
DO NOT include markdown
DO NOT include explanations
DO NOT include extra text

Review:
{review}
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

            text_output = output_content[0].get("text", "").strip()

            cleaned_output = (
                text_output.replace("```json", "").replace("```", "").strip()
            )

            return json.loads(cleaned_output)

        except json.JSONDecodeError as error:
            raise ValueError(f"Failed to parse model response: {error}") from error

        except ClientError as error:
            raise RuntimeError(f"Bedrock invocation failed: {error}") from error

        except Exception as error:
            raise RuntimeError(f"Unexpected error occurred: {error}") from error
