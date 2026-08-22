import boto3
import json

client = boto3.client("bedrock")

response = client.list_foundation_models()

print(json.dumps(response, indent=2, default=str))
