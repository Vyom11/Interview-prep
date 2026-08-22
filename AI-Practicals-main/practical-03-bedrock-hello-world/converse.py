import boto3

client = boto3.client("bedrock-runtime", region_name='us-east-1')

# FIXED: Use inference profile ID
MODEL_ID = "us.amazon.nova-2-lite-v1:0"  # Cross-region inference profile

response = client.converse(
    modelId=MODEL_ID,
    messages=[
        {
            "role": "user",
            "content": [{"text": "Explain AWS Bedrock in simple words."}]
        }
    ],
    inferenceConfig={
        "temperature": 1.0,
        "topP": 1.0,
        "maxTokens": 200
    }
)

output_text = response["output"]["message"]["content"][0]["text"]
print("\nModel Response:\n", output_text)
