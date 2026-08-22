# Practical 5 — Interactive Tool Calling Flow

This project demonstrates an interactive AI tool-calling workflow
using Amazon Bedrock and Amazon Nova Lite.

The LLM dynamically decides whether to:
- call `get_weather`
- call `get_stock_price`

based on user input.

## Features

- Interactive CLI
- Amazon Bedrock integration
- Amazon Nova Lite routing
- Dynamic tool execution
- Structured JSON validation
- Persistent output storage
- Modular architecture

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

If using AWS Academy or temporary credentials,
include `AWS_SESSION_TOKEN`.

### 5. Run Application

```bash
python app.py
```

## Example Queries

```text
What's the weather in Ahmedabad?
Show Tesla stock analysis.
What's Apple's stock outlook?
Weather in Mumbai today.
```

## Exit

```text
exit
```