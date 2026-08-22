# Practical 5 — Structured Output & Tool Calling

This project demonstrates structured data extraction from product reviews
using Amazon Bedrock and Amazon Nova Lite.

## Features

- Batch review processing
- Synthetic review generation
- Structured JSON extraction
- Pydantic validation
- Logging support
- JSON export
- Error handling and retries

## Project Structure

```text
practical-05-structured-output-tool-calling/
```

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS Credentials

Create a `.env` file using `.env.example`.

## Generate Synthetic Reviews

```bash
python scripts/generate_reviews.py
```

## Run the Application

```bash
python app.py
```

## Example Output

```json
{
    "review_id": 1,
    "sentiment": "positive",
    "key_topics": [
        "battery life",
        "display"
    ],
    "rating_estimate": 5
}
```