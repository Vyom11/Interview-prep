# AWS Foundations & GenAI Study Guide
### From Absolute Beginner → AI/ML Engineer on AWS

---

## Table of Contents

1. [The Big Picture — AWS Foundations](#1-the-big-picture--aws-foundations)
   - [What is AWS?](#what-is-aws)
   - [The Cloud — The Utility Company Analogy](#the-cloud--the-utility-company-analogy)
   - [Pay-As-You-Go Infrastructure](#pay-as-you-go-infrastructure)
   - [Global Infrastructure](#global-infrastructure)
   - [Core Services — The Toolbox](#core-services--the-toolbox)
2. [The Programming Bridge — boto3](#2-the-programming-bridge--boto3)
3. [AWS Bedrock & The Converse API](#3-aws-bedrock--the-converse-api)
4. [Practical Implementation — Hands-On Lab](#4-practical-implementation--hands-on-lab)
5. [Tuning & Senior Secrets](#5-tuning--senior-secrets)

---

# 1. The Big Picture — AWS Foundations

## What is AWS?

**AWS (Amazon Web Services)** is a collection of computing services offered by Amazon over the internet. Think of it as a massive, global rental shop — but instead of renting tools or cars, you rent computing power, storage, databases, AI models, networking, and dozens of other technical services.

You never have to buy a physical server, set up a data center, or worry about hardware. You just describe what you need, and AWS provides it — instantly, on demand, and you pay only for what you use.

> 🌐 **Fun Fact:** AWS powers a huge chunk of the internet, including Netflix, Airbnb, NASA, and millions of startups and enterprises. When you stream a video or open an app, there's a good chance AWS is involved somewhere.

---

## The Cloud — The Utility Company Analogy

Before AWS and "the cloud" existed, if a company needed a computer server (a powerful machine that runs software 24/7), they had to:

1. **Buy** expensive physical hardware
2. **Set up** a room to house it (with cooling, power, security)
3. **Hire staff** to maintain it
4. **Buy more** if they needed to grow — and guess wrong on how much they'd need

This was slow, expensive, and wasteful.

### The Electricity Analogy

Imagine if, instead of plugging into a power outlet, you had to:
- Build your own power plant in your backyard
- Maintain it yourself
- Generate exactly the right amount of electricity — not too much, not too little

That would be absurd. Instead, we use a **utility company** (like the electric grid):
- The utility company runs the power plant
- You plug in and get power instantly
- You pay only for the electricity you actually use
- Need more power? The grid scales automatically

**The cloud works the same way for computing:**

| Electricity (Utility) | Cloud Computing (AWS) |
|---|---|
| Power plant | AWS Data Center |
| Wiring to your house | The Internet |
| Your appliances | Your apps / AI models |
| Monthly electric bill | Monthly AWS bill |
| Flip a light switch | Launch a new server in seconds |
| Power scales when you run more appliances | AWS scales when you get more users |

> 💡 **Intuition:** You don't need to own the power plant. You just need to know how to plug in. That's what we're learning here — how to "plug in" to AWS for AI/ML work.

---

## Pay-As-You-Go Infrastructure

Traditional computing forced companies to **over-provision** — buy hardware for their *worst-case* peak demand, even if that peak only happens once a year.

AWS uses a **pay-as-you-go** model:

- You spin up a server → you pay by the second or hour
- You shut it down → billing stops
- You process 1,000 AI requests → you pay for 1,000
- You process 0 AI requests → you pay nothing

```
Traditional Model:
[Buy Server] ──────────────────────────────────────────────────── [Pay Forever, Even When Idle]

AWS Pay-As-You-Go:
[Need resource] → [Launch] → [Use] → [Pay] → [Shut Down] → [Stop Paying]
                                                    ↑
                                          Only pay for actual usage
```

This is especially powerful for AI/ML work, where you might run a massive training job for 4 hours, then need nothing for a week. You only pay for those 4 hours.

---

## Global Infrastructure

AWS doesn't live in one place. It's a planet-spanning network of physical data centers. Understanding this geography is essential for AI/ML engineers.

### Regions

A **Region** is a distinct geographic area (like "US East Coast" or "Europe") where AWS clusters its data centers. Each Region is completely independent — if one region has a problem, others are unaffected.

**Example Regions:**
| Region Code | Location |
|---|---|
| `us-east-1` | Northern Virginia, USA |
| `us-west-2` | Oregon, USA |
| `eu-west-1` | Ireland, Europe |
| `ap-southeast-1` | Singapore, Asia Pacific |
| `us-east-2` | Ohio, USA |

### Availability Zones (AZs)

Inside each Region, there are multiple **Availability Zones (AZs)**. An AZ is one or more physically separate data centers within a Region. They are close enough to communicate very fast, but far enough apart that a flood, fire, or power outage in one won't affect another.

```
Region: us-east-1 (Northern Virginia)
┌────────────────────────────────────────────────────────┐
│                                                        │
│   ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│   │ AZ: us-east- │  │ AZ: us-east- │  │ AZ: us-    │  │
│   │    1a        │  │    1b        │  │  east-1c   │  │
│   │ (Data Center)│  │ (Data Center)│  │(DataCenter)│  │
│   └──────────────┘  └──────────────┘  └────────────┘  │
│                                                        │
│         Fast, low-latency connections between AZs      │
└────────────────────────────────────────────────────────┘
```

### Why Latency Matters

**Latency** is the time it takes for data to travel from Point A to Point B. It's measured in milliseconds (ms).

- A user in New York using a server in Northern Virginia → ~10ms latency ✅ Fast
- A user in New York using a server in Sydney, Australia → ~250ms latency ❌ Slow

For AI/ML applications where users are waiting for model responses, every millisecond matters. A chatbot with 3 seconds of latency feels broken. One with 200ms feels snappy.

> 💡 **Rule of Thumb:** Always deploy your resources in the Region closest to your users. For AI inference (running a model to get a response), latency is critical.

### Why Data Residency Matters

**Data residency** refers to the physical location where your data is stored. This matters because:

- **Legal regulations**: GDPR (Europe's data privacy law) may require that European user data stays within Europe
- **Government compliance**: Some countries require citizen data to stay within their borders
- **Corporate policy**: Some enterprises can't let data leave certain regions

> 🔐 **Senior Engineer Tip:** Always check your data residency requirements before choosing a Region. A rookie mistake is building everything in `us-east-1` and then discovering your EU customers' data legally cannot leave Europe.

### Why Your Region Matters for AI Models

Not all AI foundation models are available in every Region. Amazon Bedrock's model availability varies by Region.

- `us-east-1` and `us-west-2` typically have the broadest model availability
- Some newer models launch in limited Regions first
- Cross-region inference adds latency and potential cost

> ⚠️ **Beginner Mistake:** Calling a Bedrock model from the wrong region will give you a `ResourceNotFoundException`. Always verify your model is available in your configured region at the [Bedrock documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html).

---

## Core Services — The Toolbox

AWS has hundreds of services. As an AI/ML engineer, you'll use a specific subset regularly. Think of these as your professional toolkit.

---

### 🪣 S3 — Simple Storage Service (Your Data Warehouse)

**Intuition:** S3 is like an infinitely large, highly durable filing cabinet in the cloud. You put files in, you take files out. The files can be anything: datasets, model outputs, images, PDFs, code, logs.

**Technical definition:** S3 is AWS's **object storage** service. You store data as "objects" (files) inside "buckets" (containers). Each object can be up to 5 terabytes.

```
S3 Structure:
┌─────────────────────────────────────────────────────────┐
│  Bucket: my-ai-project-data                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │  training-data/dataset_v1.csv                      │ │
│  │  training-data/dataset_v2.csv                      │ │
│  │  model-outputs/response_logs/2025-01-15.jsonl      │ │
│  │  prompts/system_prompts/customer_service.txt       │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Why AI/ML engineers care:**
- Store training datasets
- Save model outputs and logs for analysis
- Store prompt templates
- Archive conversation histories
- Host fine-tuning data for Bedrock

---

### 🔐 IAM — Identity and Access Management (Your Security Guard)

**Intuition:** IAM is the bouncer at the door of every AWS service. It decides *who* can do *what* with *which* resources. Without IAM, anyone could access your data, run up your bill, or delete your infrastructure.

**Technical definition:** IAM is AWS's **authentication and authorization** system. It manages:
- **Users**: Individual human accounts (like your developer account)
- **Roles**: Temporary permission sets that services (like Lambda) can assume
- **Policies**: JSON documents that define what actions are allowed or denied

**Key IAM concepts for beginners:**

| Concept | Analogy | Technical Meaning |
|---|---|---|
| IAM User | A person with a key card | A permanent identity with long-term credentials |
| IAM Role | A temporary badge for a visitor | A temporary identity that services assume |
| IAM Policy | A list of what the key card can open | A JSON document defining permissions |
| Least Privilege | Only give the key to rooms the person needs | Grant minimum permissions required |

**Example Policy (Read-Only S3 Access):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": "arn:aws:s3:::my-ai-project-data/*"
    }
  ]
}
```
This policy says: "Allow only reading files from this specific S3 bucket. Nothing else."

---

### ⚡ Lambda — Serverless Compute (Your Code in the Cloud)

**Intuition:** Imagine you could write a function in Python, upload it to AWS, and say: "Run this function whenever X happens (an API call, a file upload, a scheduled time)." You don't manage any servers. AWS wakes up your code, runs it, and you pay for the milliseconds it ran.

**Technical definition:** Lambda is AWS's **serverless compute** service. You upload code (called a "function"), define a trigger, and Lambda runs it on demand — no server provisioning required.

**Why AI/ML engineers care:**
- Build serverless AI APIs: user sends a message → Lambda calls Bedrock → returns response
- Process files automatically when uploaded to S3
- Run lightweight inference pipelines without managing servers
- Schedule jobs (like daily model performance reports)

```
Serverless AI API Flow with Lambda:
[User's App] → [API Request] → [Lambda Function] → [Bedrock/Claude] → [Response] → [User]
                                      ↑
                               AWS manages the server.
                               You just write the Python.
```

---

### 📊 CloudWatch — Monitoring (Your Dashboard & Alarm System)

**Intuition:** CloudWatch is like the health monitor on a hospital patient. It tracks metrics (CPU usage, number of errors, API response times), stores logs (text records of everything that happened), and can alert you when something goes wrong.

**Technical definition:** CloudWatch is AWS's **observability** service. It collects metrics, logs, and events from your AWS resources, and lets you create alarms and dashboards.

**Why AI/ML engineers care:**
- Monitor how many Bedrock API calls you're making (and their cost)
- Set alarms if your spending exceeds a budget
- Debug why your Lambda function is failing
- Track model response latency over time
- Audit who accessed your models and when

---

### 🌐 VPC — Virtual Private Cloud (Your Private Network)

**Intuition:** Imagine renting an office in a massive shared building (AWS). A VPC is like having your own private floor in that building — your own isolated network space where only your resources live, with controlled doors in and out.

**Technical definition:** A VPC is a logically isolated virtual network within AWS. You control IP address ranges, subnets, routing, and access control for all resources inside it.

**Beginner essentials:**
- **Public Subnet**: Resources here can reach the internet (like a web server)
- **Private Subnet**: Resources here are hidden from the internet (like your database)
- **Security Group**: A virtual firewall that controls inbound/outbound traffic at the resource level

> 💡 **For Day 1:** You don't need to deeply understand VPC to call Bedrock or use S3. Most Bedrock work uses public AWS endpoints. But know that in enterprise environments, everything lives in private VPCs for security. Come back to this as you advance.

---

# 2. The Programming Bridge — boto3

## What is an SDK?

Before we define boto3, let's define an **SDK (Software Development Kit)**.

**Intuition:** Imagine you want to order food from a restaurant, but the restaurant only speaks French and uses a complex ordering system. An SDK is like a professional translator who:
1. Speaks your language (Python)
2. Knows the restaurant's entire menu and ordering system (AWS APIs)
3. Handles all the communication details for you

An SDK is a **library of pre-written code** that makes it easy to talk to an external service (like AWS) from your programming language of choice.

---

## What is boto3?

**boto3** is the **official AWS SDK for Python**. It's a Python library (a collection of reusable code) that lets you control AWS services — S3, IAM, Bedrock, Lambda, CloudWatch, and more — directly from Python code.

Without boto3, you'd have to manually craft HTTP requests (a technical communication format), handle authentication cryptography, parse raw JSON responses, and deal with error handling yourself. boto3 does all of that for you.

```
Without boto3 (painful):
  You write raw HTTP request → Sign it with AWS SigV4 cryptographic signature →
  Send to AWS endpoint → Parse JSON response → Handle errors → 😩

With boto3 (clean):
  import boto3
  client = boto3.client('s3')
  client.list_buckets()  ✅
```

---

## What is an API?

**API (Application Programming Interface)** is the way two software systems talk to each other. It's a defined set of rules for sending requests and receiving responses.

**Intuition:** An API is like a restaurant menu. The menu tells you exactly:
- What you can order (available endpoints/actions)
- How to order it (required parameters)
- What you'll receive (response format)

You don't need to know how the kitchen works — just how to read the menu and place the order.

**AWS APIs** are HTTP-based interfaces that every AWS service exposes. When you call boto3, it's translating your Python into these HTTP API calls behind the scenes.

---

## How boto3 Translates Python into AWS Actions

Here's the complete journey from your Python code to an AI model response:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     THE BOTO3 REQUEST PIPELINE                          │
│                                                                         │
│  Your Python Code                                                       │
│  ┌─────────────────────┐                                                │
│  │ client.converse(    │                                                │
│  │   modelId="claude", │  ← You write this                             │
│  │   messages=[...]    │                                                │
│  │ )                   │                                                │
│  └──────────┬──────────┘                                                │
│             │                                                           │
│             ▼                                                           │
│  boto3 SDK Layer                                                        │
│  ┌─────────────────────┐                                                │
│  │ 1. Validate inputs  │  ← boto3 checks your parameters               │
│  │ 2. Serialize to JSON│  ← converts Python dict → JSON string         │
│  │ 3. Sign request     │  ← adds your AWS credentials (SigV4 auth)    │
│  │ 4. Build HTTP req   │  ← packages everything into an HTTP request   │
│  └──────────┬──────────┘                                                │
│             │                                                           │
│             ▼                                                           │
│  Internet / AWS Network                                                 │
│  ┌─────────────────────┐                                                │
│  │ HTTPS POST request  │  ← encrypted, authenticated request           │
│  │ to AWS endpoint     │                                                │
│  └──────────┬──────────┘                                                │
│             │                                                           │
│             ▼                                                           │
│  AWS Bedrock Service                                                    │
│  ┌─────────────────────┐                                                │
│  │ 1. Verify auth      │  ← AWS checks your credentials                │
│  │ 2. Check IAM perms  │  ← are you allowed to do this?                │
│  │ 3. Route to model   │  ← sends to the specific AI model             │
│  │ 4. Run inference    │  ← model generates a response                 │
│  └──────────┬──────────┘                                                │
│             │                                                           │
│             ▼                                                           │
│  Response back to You                                                   │
│  ┌─────────────────────┐                                                │
│  │ JSON response       │  ← AWS sends back structured data             │
│  │ boto3 deserializes  │  ← boto3 converts JSON → Python dict          │
│  │ → Python dict/obj   │  ← you access response['output']['message']   │
│  └─────────────────────┘                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

### The API Client

An **API Client** is an object that boto3 creates to represent a connection to a specific AWS service. You create one like this:

```python
import boto3

# Create a client for Amazon Bedrock Runtime
# This is the service that lets you CALL models
client = boto3.client(
    service_name='bedrock-runtime',  # Which AWS service
    region_name='us-east-1'          # Which AWS region
)
```

Once you have a `client`, you call methods on it. Each method corresponds to one operation in that service's API (like sending a message, listing models, etc.).

### Authentication — How AWS Knows It's You

When boto3 makes a request, it must prove to AWS that the request is coming from a legitimate, authorized user. It does this by **signing** the request with your **AWS credentials** (a pair of keys: an Access Key ID and a Secret Access Key — think of them like a username and password).

boto3 automatically looks for credentials in this order:
1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
2. AWS credentials file (`~/.aws/credentials`)
3. IAM Role attached to the compute resource (e.g., a Lambda function)

> 🔐 **NEVER hardcode your AWS credentials in your code.** We'll cover the right way to handle them in Section 4.

---

# 3. AWS Bedrock & The Converse API

## Bedrock Fundamentals

### What is Amazon Bedrock?

**Amazon Bedrock** is AWS's fully managed service for accessing, running, and building with **foundation models** (large, powerful AI models). It's the main tool you'll use as an AI/ML engineer on AWS for generative AI work.

### The Showroom Analogy

Imagine a luxury car showroom. Inside the showroom:
- Multiple car brands are displayed (Anthropic's Claude, Meta's Llama, Mistral, Cohere, etc.)
- You don't need to build a car yourself — you choose from the available models
- The showroom handles the engine, maintenance, and infrastructure
- You just need to know how to drive (send API requests)

**Bedrock is the showroom.** The **foundation models** are the cars.

```
Amazon Bedrock "Showroom"
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  ┌─────────┐ │
│  │  Anthropic  │  │    Meta     │  │  Mistral   │  │  Cohere │ │
│  │   Claude    │  │    Llama    │  │    AI      │  │         │ │
│  │  3.5 Sonnet │  │  3.1 405B  │  │  Large     │  │ Command │ │
│  └─────────────┘  └─────────────┘  └────────────┘  └─────────┘ │
│                                                                  │
│  One API to rule them all: boto3 → Bedrock → Any Model          │
└──────────────────────────────────────────────────────────────────┘
```

### What is a Foundation Model?

A **Foundation Model (FM)** is a large AI model trained on enormous amounts of text (and sometimes images, code, etc.) that can perform many different tasks: answer questions, write code, summarize documents, translate languages, analyze data, and more.

They're called "foundation" models because they serve as a **foundation** — you can use them as-is, or customize them for specific use cases (like fine-tuning a model on your company's internal documents).

**Examples:**
- **Claude 3.5 Sonnet** (Anthropic) — Excellent for reasoning, coding, writing, analysis
- **Llama 3.1** (Meta) — Open-weights model, strong across many tasks
- **Mistral Large** (Mistral AI) — Strong coding and reasoning, European model
- **Titan** (Amazon) — AWS's own model family

---

## The Converse API

### What is the Converse API?

The **Converse API** is a unified interface provided by Amazon Bedrock for having **multi-turn conversations** with any supported foundation model. "Multi-turn" means back-and-forth conversations — like texting someone, where each message builds on the last.

**Why it's important:** Instead of writing different code for every AI model (Claude has one format, Llama has another, Mistral has another), the Converse API gives you **one consistent interface** for all of them. You change one parameter (`modelId`) to switch between models.

### Multi-Turn Conversations

A **multi-turn conversation** means the model remembers what was said earlier in the conversation. This is what makes a chatbot feel like a real conversation instead of isolated question-and-answer pairs.

**Single-turn (no memory):**
```
User: "My name is Alex."
Model: "Hello, Alex! How can I help?"

User: "What's my name?"
Model: "I don't know your name."  ← 😞 No memory
```

**Multi-turn (with memory via Converse API):**
```
User: "My name is Alex."
Model: "Hello, Alex! How can I help?"

User: "What's my name?"
Model: "Your name is Alex!"  ← ✅ Remembers context
```

### How Memory/Context Works

**Important concept:** Foundation models are **stateless** — they don't actually store memory between API calls. Instead, the Converse API works by sending the **entire conversation history** with every single request.

```
Turn 1:
  You send: [User: "My name is Alex"]
  Model responds: "Hello, Alex!"

Turn 2:
  You send: [User: "My name is Alex", Assistant: "Hello, Alex!", User: "What's my name?"]
            ↑ ENTIRE HISTORY is resent every time
  Model responds: "Your name is Alex!"
```

This means your Python code is responsible for maintaining and appending to the conversation history list. Each message has a `role` (either `"user"` or `"assistant"`) and `content` (the text).

> 💡 **Implication for Cost:** Every token in the conversation history costs money on every turn. Long conversations get expensive. In production systems, engineers implement techniques like summarization or sliding windows to manage context length and cost.

---

## Comparison — Converse API vs. InvokeModel API

Amazon Bedrock offers two main ways to call models:

| Feature | Converse API | InvokeModel API |
|---|---|---|
| **Interface** | Unified, consistent | Model-specific, varies |
| **Switching models** | Change `modelId` only | Rewrite request format |
| **Multi-turn** | Built-in `messages` list | Must implement manually |
| **Streaming** | `ConverseStream` | `InvokeModelWithResponseStream` |
| **Tool use / Function calling** | Standardized | Model-specific format |
| **Best for** | Chat apps, agents, most use cases | Specialized model features not in Converse |
| **Recommended for beginners** | ✅ YES | ❌ Only when necessary |

### Why Converse is Better for Chat Systems

```
InvokeModel approach — Claude format:
{
  "anthropic_version": "bedrock-2023-05-31",
  "messages": [{"role": "user", "content": "Hello"}]
}

InvokeModel approach — Llama format:
{
  "prompt": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\nHello",
  "max_gen_len": 512
}

Converse API — ALL models (same format!):
{
  "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",  ← just change this
  "messages": [{"role": "user", "content": [{"text": "Hello"}]}]
}
```

With Converse API, switching from Claude to Llama is **one line change**. With InvokeModel, it's a complete rewrite of the request structure.

### Model Comparison

| | **Claude 3.5 Sonnet** | **Llama 3.1 70B** |
|---|---|---|
| **Provider** | Anthropic | Meta |
| **Strengths** | Reasoning, coding, nuanced writing, safety | Open weights, cost-effective, strong at coding |
| **Context Window** | 200K tokens | 128K tokens |
| **Pricing** | Higher (premium model) | Lower |
| **Best for** | Complex analysis, customer-facing AI, agents | Cost-sensitive apps, self-hosting scenarios |

---

## Alternatives — Bedrock vs. SageMaker vs. OpenAI API

| | **Amazon Bedrock** | **Amazon SageMaker** | **OpenAI API** |
|---|---|---|---|
| **What it is** | Managed access to foundation models | Full ML platform (train, deploy, serve models) | OpenAI's direct API (GPT-4, etc.) |
| **Best for** | Using existing FMs in production | Custom model training and deployment | Accessing GPT models specifically |
| **Skill required** | Low-Medium | High | Low |
| **Infrastructure management** | None (fully managed) | High | None |
| **Model customization** | Fine-tuning via Bedrock | Full training control | Fine-tuning (limited) |
| **Data stays on AWS** | ✅ Yes | ✅ Yes | ❌ Leaves AWS |
| **Cost model** | Per token | Per instance hour + storage | Per token |

### When Would an Engineer Choose Each?

**Choose Bedrock when:**
- You want to use Claude, Llama, Mistral, or other foundation models
- You want minimal infrastructure management
- Your data must stay within AWS (compliance)
- You're building chat apps, RAG systems, or AI agents

**Choose SageMaker when:**
- You need to train a custom model from scratch on your own dataset
- You have proprietary model architectures
- You need fine-grained control over the training infrastructure
- You're doing research-grade ML work

**Choose OpenAI API when:**
- You specifically need GPT-4/GPT-4o capabilities
- You're building a prototype quickly and OpenAI's features fit
- AWS ecosystem lock-in is not a concern
- Note: If you're building on AWS, Bedrock + Claude gives you similar capabilities while keeping everything within AWS

---

# 4. Practical Implementation — Hands-On Lab

## Safe Setup

### Step 1 — Install Python

Python is the programming language we'll use. Think of it as the language we use to write instructions that boto3 understands.

**Check if you already have Python:**
```bash
# In your terminal, run this command:
python3 --version

# You want to see: Python 3.9 or higher
# Example output: Python 3.11.4
```

If you don't have Python, download it from [python.org](https://www.python.org/downloads/). Install Python 3.11 or newer.

---

### Step 2 — Create a Virtual Environment

**What is a virtual environment?**

Imagine your Python projects as different cooking recipes. Each recipe might call for different ingredients. A **virtual environment** (venv) is like a separate kitchen for each recipe — the ingredients (libraries) in one kitchen don't interfere with another.

Without virtual environments, all your Python projects share one global kitchen, and conflicting ingredient versions cause chaos.

```bash
# Create a folder for your project
mkdir aws-genai-project
cd aws-genai-project

# Create a virtual environment named "venv"
python3 -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Your terminal should now show (venv) at the beginning:
# (venv) user@computer aws-genai-project %
```

> ✅ **You'll know it worked** when `(venv)` appears at the start of your terminal prompt.

---

### Step 3 — Install boto3

With your virtual environment active, install boto3:

```bash
# pip is Python's package manager — like an app store for Python libraries
pip install boto3

# Also install python-dotenv for safe credential management (explained below)
pip install python-dotenv

# Verify installation
python3 -c "import boto3; print(boto3.__version__)"
# Should print a version number like: 1.34.0
```

---

### Step 4 — AWS Credentials and IAM Setup

Before your code can talk to AWS, AWS needs to know who you are and verify your identity.

#### Creating an IAM User (NOT root!)

> ⚠️ **CRITICAL:** Never use your AWS root account for development. The root account has unlimited power. If its credentials are leaked, an attacker can do anything — delete everything, run up a massive bill, steal your data.

1. Log into the [AWS Console](https://aws.amazon.com/console/)
2. Go to **IAM** (search for it in the top search bar)
3. Click **Users** → **Create User**
4. Name it `bedrock-dev-user`
5. Attach the policy `AmazonBedrockFullAccess` (we'll tighten this later)
6. After creation, go to **Security Credentials** tab
7. Click **Create Access Key** → choose **Local code**
8. Download the `.csv` file — **this is the only time you'll see the Secret Key**

#### Configuring aws configure

```bash
# Run this in your terminal
aws configure

# It will ask for:
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE    ← from your .csv
AWS Secret Access Key [None]: wJalrXUtn/K7MDENG   ← from your .csv
Default region name [None]: us-east-1              ← use us-east-1 for broadest model support
Default output format [None]: json                 ← press Enter to accept
```

This stores your credentials in `~/.aws/credentials` (a hidden file in your home directory). boto3 automatically reads from this file.

**What this looks like on disk:**
```ini
# File: ~/.aws/credentials
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG
```

---

### Step 5 — The Golden Rule: NEVER Hardcode Access Keys

```python
# ❌ WRONG — NEVER DO THIS
import boto3

client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id='AKIAIOSFODNN7EXAMPLE',       # ← DANGER
    aws_secret_access_key='wJalrXUtnFEMI/K7MDENG'  # ← EXTREME DANGER
)

# Why is this dangerous?
# If you push this code to GitHub (even a private repo), your keys can be scraped.
# Bots scan GitHub for AWS keys 24/7. Within minutes of exposure, attackers
# can run up tens of thousands of dollars in compute bills.
```

```python
# ✅ CORRECT — Let boto3 find credentials automatically
import boto3

# boto3 automatically checks:
# 1. Environment variables
# 2. ~/.aws/credentials file (set by aws configure)
# 3. IAM Role (for Lambda/EC2)
client = boto3.client('bedrock-runtime', region_name='us-east-1')
```

---

### Step 6 — Using .env Files and Environment Variables

For projects where you need to manage configuration values (like model IDs, region names, or other settings), use a `.env` file.

**What is an environment variable?**

An **environment variable** is a value set in your operating system's environment (outside of your code). Your program can read it, but it's not hardcoded into your source files.

**Create a `.env` file in your project folder:**
```bash
# File: .env
# ⚠️ NEVER commit this file to Git. Add it to .gitignore immediately.

AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
MAX_TOKENS=1024
```

**Create a `.gitignore` file immediately:**
```bash
# File: .gitignore
.env
venv/
__pycache__/
*.pyc
.DS_Store
```

**Read `.env` values in Python:**
```python
import os
from dotenv import load_dotenv  # from the python-dotenv library we installed

# Load the .env file into environment variables
load_dotenv()

# Read values with os.getenv()
# The second argument is a default value if the variable isn't set
region = os.getenv("AWS_REGION", "us-east-1")
model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
```

---

## Code Lab

### Lab 1 — List Available Bedrock Models

This script connects to Bedrock and retrieves a list of all available foundation models.

```python
"""
lab_01_list_models.py
======================
Purpose: Connect to Amazon Bedrock and list available foundation models.
This is the "Hello World" of Bedrock — if this works, your setup is correct.

Run with: python3 lab_01_list_models.py
"""

# ─── Imports ────────────────────────────────────────────────────────────────
import boto3       # The AWS SDK for Python — our main tool for talking to AWS
import json        # Python's built-in library for reading/writing JSON data
import sys         # Provides access to system functions like sys.exit()

# ─── Configuration ──────────────────────────────────────────────────────────
# We hardcode the region here because it's not sensitive data (not a secret).
# For production, you'd still read this from an environment variable.
REGION = "us-east-1"


def list_bedrock_models():
    """
    Lists all foundation models available in Amazon Bedrock.
    
    Note: We use 'bedrock' (not 'bedrock-runtime') here.
    - 'bedrock' client: for management tasks (listing models, managing fine-tuning jobs)
    - 'bedrock-runtime' client: for actually calling/invoking models
    """
    
    print("=" * 60)
    print("  Amazon Bedrock — Available Foundation Models")
    print("=" * 60)
    
    # ── Step 1: Create the boto3 client ──────────────────────────────────────
    # boto3.client() creates a connection to a specific AWS service.
    # It automatically uses credentials from ~/.aws/credentials (set by aws configure).
    # If credentials aren't found, it raises a NoCredentialsError.
    try:
        bedrock_client = boto3.client(
            service_name="bedrock",   # Which AWS service (management plane)
            region_name=REGION        # Which AWS region to connect to
        )
    except Exception as e:
        print(f"❌ Failed to create boto3 client: {e}")
        print("   → Make sure you've run 'aws configure' with valid credentials.")
        sys.exit(1)   # Exit the program with an error code
    
    # ── Step 2: Call the API ─────────────────────────────────────────────────
    # list_foundation_models() calls the Bedrock API and returns a response object.
    # The response is a Python dictionary containing the API's JSON response.
    try:
        response = bedrock_client.list_foundation_models(
            # Optional filter: only show models that support "TEXT" output
            # Remove this filter to see ALL models including image generation
            byOutputModality="TEXT"
        )
    except Exception as e:
        print(f"❌ API call failed: {e}")
        print("   → Common causes: wrong region, insufficient IAM permissions")
        print("   → Check that your IAM user has the 'AmazonBedrockFullAccess' policy")
        sys.exit(1)
    
    # ── Step 3: Parse and Display the Response ───────────────────────────────
    # response["modelSummaries"] is a list (array) of dictionaries.
    # Each dictionary contains information about one model.
    models = response.get("modelSummaries", [])
    
    if not models:
        print("No models found. Check your region — not all regions have all models.")
        return
    
    print(f"\n✅ Found {len(models)} text-capable models in {REGION}:\n")
    
    # Iterate over each model and print key information
    for model in models:
        # model["modelId"] is the string you use in API calls to invoke this model
        # model["modelName"] is the human-readable display name
        # model["providerName"] is the company that created the model (e.g., "Anthropic")
        
        provider = model.get("providerName", "Unknown")
        name = model.get("modelName", "Unknown")
        model_id = model.get("modelId", "Unknown")
        
        print(f"  Provider: {provider}")
        print(f"  Model:    {name}")
        print(f"  ID:       {model_id}")   # ← This is what you put in modelId when calling
        print("-" * 50)


# ─── Entry Point ─────────────────────────────────────────────────────────────
# This pattern (if __name__ == "__main__") is Python best practice.
# It means: "Only run this code if this script is run directly."
# It prevents the code from running if this file is imported by another script.
if __name__ == "__main__":
    list_bedrock_models()
```

**Expected Output:**
```
============================================================
  Amazon Bedrock — Available Foundation Models
============================================================

✅ Found 23 text-capable models in us-east-1:

  Provider: Anthropic
  Model:    Claude 3.5 Sonnet v2
  ID:       anthropic.claude-3-5-sonnet-20241022-v2:0
--------------------------------------------------
  Provider: Meta
  Model:    Llama 3.1 70B Instruct
  ID:       meta.llama3-1-70b-instruct-v1:0
--------------------------------------------------
...
```

> 🔧 **Debugging Tip:** If you get `botocore.exceptions.NoRegionError`, you forgot `region_name`. If you get `botocore.exceptions.NoCredentialsError`, run `aws configure` again.

---

### Lab 2 — Send a Single Message Using the Converse API

```python
"""
lab_02_single_message.py
=========================
Purpose: Send a single message to Claude via the Bedrock Converse API
         and display the response.

This is the fundamental building block of every GenAI app you'll build.

Run with: python3 lab_02_single_message.py
"""

# ─── Imports ─────────────────────────────────────────────────────────────────
import boto3          # AWS SDK — our bridge to Bedrock
import json           # For pretty-printing the raw response (educational)
import os             # For reading environment variables
from dotenv import load_dotenv   # For loading .env file

# ─── Load Environment Variables ──────────────────────────────────────────────
# load_dotenv() reads your .env file and makes those values available
# via os.getenv(). Call this BEFORE reading any env vars.
load_dotenv()

# ─── Configuration ───────────────────────────────────────────────────────────
# os.getenv(KEY, DEFAULT) reads an env var.
# If the variable isn't set, it uses the DEFAULT value.
REGION = os.getenv("AWS_REGION", "us-east-1")

# The model ID identifies WHICH foundation model to use.
# You got this list from Lab 1 above.
MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    "anthropic.claude-3-5-sonnet-20241022-v2:0"  # Default to Claude 3.5 Sonnet v2
)

# Max tokens = the maximum length of the model's response.
# 1 token ≈ 0.75 words. 1024 tokens ≈ ~750 words.
# Higher = longer possible responses, higher cost ceiling.
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))


def send_single_message(user_message: str) -> str:
    """
    Sends a single message to a Bedrock foundation model using the Converse API.
    
    Parameters:
        user_message (str): The text message to send to the model.
    
    Returns:
        str: The model's text response.
    
    The 'str' type hints (user_message: str) are optional but good practice.
    They document what type of data the function expects and returns.
    """
    
    # ── Step 1: Create the boto3 Bedrock Runtime client ──────────────────────
    # 'bedrock-runtime' is for CALLING models (inference).
    # 'bedrock' (without -runtime) is for management (listing models, etc.)
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=REGION
    )
    
    # ── Step 2: Build the messages list ──────────────────────────────────────
    # The Converse API expects a "messages" list.
    # Each message is a dictionary with:
    #   - "role": either "user" (you) or "assistant" (the model)
    #   - "content": a list of content blocks
    # 
    # Why is "content" a list? Because a single message can contain
    # multiple parts: text, images, documents, tool results, etc.
    # For simple text, it's a list with one item: {"text": "your text"}
    
    messages = [
        {
            "role": "user",         # This message is from the user (you)
            "content": [
                {
                    "text": user_message   # The actual text content
                }
            ]
        }
    ]
    
    # ── Step 3: Build inference configuration ────────────────────────────────
    # These parameters control HOW the model generates its response.
    # We'll explain these in depth in Section 5 (Tuning & Senior Secrets).
    inference_config = {
        "maxTokens": MAX_TOKENS,   # Max response length in tokens
        "temperature": 0.7,        # Creativity level (0.0 = deterministic, 1.0 = creative)
        "topP": 0.9                # Nucleus sampling threshold (advanced — leave at 0.9 for now)
    }
    
    # ── Step 4: Call the Converse API ────────────────────────────────────────
    print(f"\n📤 Sending message to {MODEL_ID}...")
    print(f"   Message: '{user_message[:50]}...' " if len(user_message) > 50 else f"   Message: '{user_message}'")
    
    try:
        response = client.converse(
            modelId=MODEL_ID,             # Which model to use
            messages=messages,            # The conversation history (just 1 message here)
            inferenceConfig=inference_config  # Generation parameters
        )
    except client.exceptions.ResourceNotFoundException:
        # This happens when the modelId doesn't exist in your region
        print(f"❌ Model '{MODEL_ID}' not found in region '{REGION}'.")
        print("   → Try 'us-east-1' or 'us-west-2' for broadest model availability.")
        print("   → Run Lab 1 to see which models are actually available.")
        raise
    except client.exceptions.AccessDeniedException:
        # This happens when your IAM user doesn't have permission to call this model
        print("❌ Access Denied.")
        print("   → Go to AWS Bedrock console → Model access → Request access for this model.")
        print("   → Some models require explicit approval before you can use them.")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        raise
    
    # ── Step 5: Parse the Response ───────────────────────────────────────────
    # The Converse API returns a structured response dictionary.
    # Structure:
    #   response
    #   └── "output"
    #       └── "message"
    #           ├── "role": "assistant"
    #           └── "content": [{"text": "The model's response here"}]
    
    # .get() safely retrieves a key — returns None if the key doesn't exist
    # instead of raising a KeyError (a crash).
    output_message = response.get("output", {}).get("message", {})
    content_list = output_message.get("content", [])
    
    # Extract the text from the first content block
    # In a text-only response, there's exactly one content block of type "text"
    response_text = ""
    for content_block in content_list:
        if "text" in content_block:           # Check if this block is a text block
            response_text += content_block["text"]   # Append the text
    
    # ── Step 6: Display Usage Metrics ────────────────────────────────────────
    # The 'usage' field tells us how many tokens were used.
    # This maps directly to cost — more tokens = higher bill.
    usage = response.get("usage", {})
    input_tokens = usage.get("inputTokens", 0)    # Tokens in our prompt
    output_tokens = usage.get("outputTokens", 0)  # Tokens in the response
    total_tokens = usage.get("totalTokens", 0)    # Sum of both
    
    print(f"\n📊 Token Usage:")
    print(f"   Input tokens:  {input_tokens:,}")   # :, adds thousands separator
    print(f"   Output tokens: {output_tokens:,}")
    print(f"   Total tokens:  {total_tokens:,}")
    
    return response_text


# ─── Main Execution ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    
    # Define our test prompt
    # Start with small prompts when testing — saves money and debugs faster
    test_prompt = "Explain what Amazon Bedrock is in exactly 3 bullet points. Be concise."
    
    # Call our function and get the response
    result = send_single_message(test_prompt)
    
    # Display the result
    print("\n" + "=" * 60)
    print("  🤖 Model Response:")
    print("=" * 60)
    print(result)
    print("=" * 60)
```

---

### Lab 3 — Multi-Turn Conversation

```python
"""
lab_03_multi_turn_chat.py
==========================
Purpose: Build a real multi-turn conversation with memory.
         The model will remember everything said in the session.

Key concept: We maintain a `conversation_history` list that grows
with each turn. We send the ENTIRE list on every API call.

Run with: python3 lab_03_multi_turn_chat.py
Type 'quit' or 'exit' to end the conversation.
Type 'history' to see the raw conversation log.
Type 'clear' to start a new conversation.
"""

# ─── Imports ─────────────────────────────────────────────────────────────────
import boto3
import os
from dotenv import load_dotenv

# ─── Load Config ──────────────────────────────────────────────────────────────
load_dotenv()

REGION   = os.getenv("AWS_REGION",        "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID",  "anthropic.claude-3-5-sonnet-20241022-v2:0")
MAX_TOKENS = int(os.getenv("MAX_TOKENS",  "1024"))

# The system prompt is a set of instructions that shapes the model's behavior.
# It's not part of the conversation history — it's a separate instruction layer.
# Think of it as the job description you give to an employee before they start work.
SYSTEM_PROMPT = """You are a helpful AWS and AI/ML learning assistant. 
You help beginners understand cloud computing and AI concepts.
Keep your explanations clear, use analogies, and be encouraging."""


def create_bedrock_client():
    """Creates and returns a Bedrock Runtime boto3 client."""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=REGION
    )


def send_message_with_history(client, conversation_history: list, user_message: str) -> tuple[str, dict]:
    """
    Sends a message WITH the full conversation history.
    
    Parameters:
        client: The boto3 Bedrock Runtime client
        conversation_history (list): All previous messages in this conversation
        user_message (str): The new message to send
    
    Returns:
        tuple: (response_text, usage_stats)
               - response_text: The model's response as a string
               - usage_stats: Dictionary with token counts
    
    Note on tuple: A tuple is a Python data structure that holds multiple
    values together. We return both the text and usage stats at once.
    """
    
    # Build the new user message in the correct Converse API format
    new_user_message = {
        "role": "user",
        "content": [{"text": user_message}]
    }
    
    # Create the full messages list: all history + the new message
    # The spread operator (...) equivalent in Python is list concatenation:
    # [*old_list, new_item] creates a NEW list with all old items plus the new one
    # We don't modify conversation_history yet — only add the assistant's
    # response AFTER we get it back.
    messages_to_send = conversation_history + [new_user_message]
    
    # Build the system message list
    # The Converse API takes "system" as a list of content blocks
    system = [
        {"text": SYSTEM_PROMPT}
    ]
    
    # Call the Converse API with the full conversation
    response = client.converse(
        modelId=MODEL_ID,
        system=system,                        # The system prompt (model's instructions)
        messages=messages_to_send,            # Full conversation including new message
        inferenceConfig={
            "maxTokens": MAX_TOKENS,
            "temperature": 0.7,
            "topP": 0.9
        }
    )
    
    # Extract the response text from the response structure
    output_message = response.get("output", {}).get("message", {})
    content_list = output_message.get("content", [])
    
    response_text = ""
    for block in content_list:
        if "text" in block:
            response_text += block["text"]
    
    # Extract usage statistics
    usage = response.get("usage", {})
    
    return response_text, usage


def run_chat_session():
    """
    Runs an interactive multi-turn chat session in the terminal.
    
    This function demonstrates the core pattern of all chatbot applications:
    1. Get user input
    2. Add to history
    3. Send history + new message to model
    4. Get response
    5. Add response to history
    6. Repeat
    """
    
    print("=" * 65)
    print("  🤖 AWS GenAI Chat Assistant (Multi-Turn Conversation)")
    print("=" * 65)
    print(f"  Model: {MODEL_ID}")
    print(f"  Region: {REGION}")
    print("\n  Commands: 'quit' to exit | 'history' to view log | 'clear' to reset")
    print("-" * 65)
    
    # Create the boto3 client once, reuse it for the entire session.
    # Creating a client is not free — it does a bit of setup work.
    # Don't create a new client on every message.
    client = create_bedrock_client()
    
    # The conversation history is a simple Python list.
    # It starts empty and grows as the conversation progresses.
    # Each item is a dictionary with "role" and "content" keys.
    conversation_history = []
    
    # Track total tokens used in this session for cost awareness
    total_session_tokens = 0
    
    # The main conversation loop
    while True:   # Loop forever until the user types 'quit'
        
        # Get user input from the terminal
        # '\n' prints a blank line before the prompt for readability
        print()
        user_input = input("  You: ").strip()   # .strip() removes leading/trailing whitespace
        
        # Handle special commands
        if not user_input:               # Empty input — user just hit Enter
            continue                     # Skip to next loop iteration
            
        if user_input.lower() in ["quit", "exit", "bye"]:
            print(f"\n  👋 Goodbye! Session used approximately {total_session_tokens:,} tokens total.")
            break   # Exit the while loop
            
        if user_input.lower() == "history":
            print("\n  📜 Conversation History:")
            print("  " + "-" * 40)
            for i, msg in enumerate(conversation_history):
                role = msg["role"].upper()
                # Show first 100 characters of each message
                text = msg["content"][0]["text"][:100]
                print(f"  [{i+1}] {role}: {text}...")
            continue
            
        if user_input.lower() == "clear":
            conversation_history = []   # Reset the history list
            total_session_tokens = 0
            print("  ✅ Conversation cleared. Starting fresh!")
            continue
        
        # ── Send the message ─────────────────────────────────────────────────
        try:
            print("  🤔 Thinking...", end="", flush=True)   # Show thinking indicator
            
            response_text, usage = send_message_with_history(
                client,
                conversation_history,
                user_input
            )
            
            print("\r" + " " * 20 + "\r", end="")   # Clear the "Thinking..." text
            
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
            print("  → The conversation history is preserved. Try again.")
            continue   # Don't update history on error — go back to input prompt
        
        # ── Update conversation history ───────────────────────────────────────
        # IMPORTANT: Only update history AFTER a successful response.
        # If the API call failed, we don't want partial updates in our history.
        
        # Add the user's message to history
        conversation_history.append({
            "role": "user",
            "content": [{"text": user_input}]
        })
        
        # Add the model's response to history
        # This is what gives the model "memory" — on the next turn,
        # the model will see what it said this turn.
        conversation_history.append({
            "role": "assistant",
            "content": [{"text": response_text}]
        })
        
        # Update token tracking
        turn_tokens = usage.get("totalTokens", 0)
        total_session_tokens += turn_tokens
        
        # Display the response
        print(f"\n  🤖 Assistant: {response_text}")
        print(f"\n  📊 Turn: {turn_tokens:,} tokens | Session total: {total_session_tokens:,} tokens")
        print("-" * 65)
        
        # ── Context Window Warning ────────────────────────────────────────────
        # Foundation models have a maximum context length (measured in tokens).
        # If you exceed it, the API will return an error.
        # Claude 3.5 Sonnet supports up to 200,000 tokens.
        # As a safety warning, alert if we're getting long.
        if total_session_tokens > 100_000:
            print("  ⚠️  Warning: Conversation is getting long.")
            print("     Consider typing 'clear' to start a new session.")
            print("     (Long conversations cost more and may hit context limits)")


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_chat_session()
```

---

### Lab 4 — Production-Ready Error Handling

```python
"""
lab_04_production_patterns.py
==============================
Purpose: Demonstrate production-grade error handling, retry logic,
         and logging patterns used by senior engineers.

In production (real-world deployed software), you CANNOT let errors
silently crash your application. You need to:
  1. Catch specific error types (not just all errors with "Exception")
  2. Log errors with enough context to debug them later
  3. Implement retry logic for transient (temporary) failures
  4. Provide meaningful error messages to users

Run with: python3 lab_04_production_patterns.py
"""

# ─── Imports ─────────────────────────────────────────────────────────────────
import boto3
import os
import time           # For implementing retry delays (sleep between retries)
import logging        # Python's built-in logging system
from botocore.exceptions import ClientError, BotoCoreError   # Specific AWS error types
from dotenv import load_dotenv

# ─── Configure Logging ───────────────────────────────────────────────────────
# logging is Python's professional-grade way to record what your program does.
# Better than print() because you can:
#   - Control verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#   - Send logs to files, databases, or monitoring services
#   - Include timestamps automatically
#   - Turn off debug logs in production

logging.basicConfig(
    level=logging.INFO,    # Only show INFO level and above (not DEBUG)
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    # Output: "2025-01-15 10:30:45 | INFO     | Message here"
)
logger = logging.getLogger(__name__)   # Get a logger for this module

# ─── Load Config ──────────────────────────────────────────────────────────────
load_dotenv()

REGION   = os.getenv("AWS_REGION",       "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "512"))

# Retry configuration
MAX_RETRIES = 3         # Maximum number of retry attempts
RETRY_DELAY = 2         # Seconds to wait between retries
BACKOFF_MULTIPLIER = 2  # Each retry waits 2x longer (exponential backoff)


class BedrockError(Exception):
    """
    Custom exception class for Bedrock-related errors.
    
    Creating custom exceptions is a professional practice because:
    1. Callers can catch YOUR specific error instead of all exceptions
    2. You can attach additional context (error codes, request IDs)
    3. It makes your API cleaner and more predictable
    
    'Exception' is Python's base class for all errors.
    We inherit from it to create a specialized version.
    """
    def __init__(self, message: str, error_code: str = None, request_id: str = None):
        super().__init__(message)                # Call parent class constructor
        self.error_code = error_code             # AWS error code (e.g., "ThrottlingException")
        self.request_id = request_id             # AWS request ID for support tickets


def call_bedrock_with_retry(client, messages: list, max_retries: int = MAX_RETRIES) -> dict:
    """
    Calls the Bedrock Converse API with exponential backoff retry logic.
    
    What is exponential backoff?
    If an API request fails (e.g., due to rate limiting or a temporary issue),
    we don't immediately retry — that would make things worse (like hammering
    a door that's already stuck). Instead, we wait a bit, then try again.
    Each retry waits longer than the last:
      Attempt 1: fails → wait 2 seconds
      Attempt 2: fails → wait 4 seconds
      Attempt 3: fails → wait 8 seconds
    This is "exponential" because the wait time doubles each time.
    
    Parameters:
        client: boto3 Bedrock Runtime client
        messages: List of conversation messages
        max_retries: Maximum retry attempts before giving up
    
    Returns:
        dict: The raw API response dictionary
    
    Raises:
        BedrockError: If all retries are exhausted or if the error is not retryable
    """
    
    delay = RETRY_DELAY   # Start with the base delay
    
    for attempt in range(max_retries + 1):   # +1 because range is exclusive at the end
        try:
            logger.info(f"Calling Bedrock Converse API (attempt {attempt + 1}/{max_retries + 1})")
            
            response = client.converse(
                modelId=MODEL_ID,
                messages=messages,
                inferenceConfig={
                    "maxTokens": MAX_TOKENS,
                    "temperature": 0.7,
                }
            )
            
            # If we got here, the call succeeded
            logger.info("✅ API call successful")
            return response
        
        except ClientError as e:
            # ClientError is the boto3 exception for AWS API errors.
            # It contains an error code that tells us WHY the call failed.
            
            # Extract the error code from the error response
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            
            # Extract the AWS request ID (useful for AWS support tickets)
            request_id = e.response.get("ResponseMetadata", {}).get("RequestId", "unknown")
            
            logger.error(f"AWS ClientError: {error_code} — {error_message}")
            logger.error(f"Request ID: {request_id}")
            
            # ── Decide whether to retry based on error type ───────────────────
            # Not all errors are worth retrying.
            # "Retryable" errors are temporary — the same request might succeed later.
            # "Non-retryable" errors are permanent — retrying won't help.
            
            RETRYABLE_ERRORS = [
                "ThrottlingException",        # Too many requests — slow down
                "ServiceUnavailableException",  # AWS service temporarily down
                "ModelTimeoutException",      # Model took too long — try again
                "InternalServerException",    # AWS internal error — usually transient
            ]
            
            NON_RETRYABLE_ERRORS = {
                "ResourceNotFoundException": "Model not found. Check modelId and region.",
                "AccessDeniedException":     "Permission denied. Check IAM permissions and model access.",
                "ValidationException":       "Invalid request format. Check your messages structure.",
            }
            
            if error_code in NON_RETRYABLE_ERRORS:
                # Don't retry — this will never succeed without code changes
                hint = NON_RETRYABLE_ERRORS[error_code]
                logger.error(f"Non-retryable error: {hint}")
                raise BedrockError(
                    message=f"{error_code}: {error_message}. Hint: {hint}",
                    error_code=error_code,
                    request_id=request_id
                )
            
            if error_code in RETRYABLE_ERRORS and attempt < max_retries:
                # Retry with exponential backoff
                logger.warning(f"Retryable error. Waiting {delay}s before retry...")
                time.sleep(delay)           # Wait before retrying
                delay *= BACKOFF_MULTIPLIER # Double the wait time for next retry
                continue                    # Go back to the top of the for loop
            
            # Either not a known retryable error, or we've exhausted retries
            if attempt >= max_retries:
                logger.error(f"All {max_retries + 1} attempts failed.")
            
            raise BedrockError(
                message=f"API call failed after {attempt + 1} attempts: {error_message}",
                error_code=error_code,
                request_id=request_id
            )
        
        except BotoCoreError as e:
            # BotoCoreError is for lower-level SDK errors (network issues, config problems)
            logger.error(f"BotoCoreError: {e}")
            
            if attempt < max_retries:
                logger.warning(f"Network/SDK error. Retrying in {delay}s...")
                time.sleep(delay)
                delay *= BACKOFF_MULTIPLIER
                continue
            
            raise BedrockError(f"SDK error after {attempt + 1} attempts: {e}")


def safe_chat(user_message: str) -> str:
    """
    A production-ready wrapper around the Bedrock Converse API.
    Demonstrates proper error handling, logging, and user-friendly messages.
    
    Parameters:
        user_message (str): The user's input message
    
    Returns:
        str: Either the model's response or a user-friendly error message
    """
    logger.info(f"Processing message: '{user_message[:50]}...'")
    
    # Create client
    client = boto3.client("bedrock-runtime", region_name=REGION)
    
    # Build messages
    messages = [
        {"role": "user", "content": [{"text": user_message}]}
    ]
    
    # Call the API with retry logic
    try:
        response = call_bedrock_with_retry(client, messages)
        
        # Extract response text
        response_text = response["output"]["message"]["content"][0]["text"]
        
        # Log token usage for cost monitoring
        usage = response.get("usage", {})
        logger.info(
            f"Token usage — Input: {usage.get('inputTokens', 0)}, "
            f"Output: {usage.get('outputTokens', 0)}, "
            f"Total: {usage.get('totalTokens', 0)}"
        )
        
        return response_text
    
    except BedrockError as e:
        # Our custom error with specific context
        logger.error(f"BedrockError: {e} (Code: {e.error_code}, ReqID: {e.request_id})")
        
        # Return a user-friendly message instead of crashing
        # In production, you'd also alert your monitoring system (PagerDuty, etc.)
        return f"I'm sorry, I encountered an error processing your request. Please try again. (Error: {e.error_code})"
    
    except Exception as e:
        # Catch-all for truly unexpected errors
        # In production, this should trigger an alert — unexpected means a bug
        logger.critical(f"Unexpected error: {type(e).__name__}: {e}", exc_info=True)
        return "An unexpected error occurred. Our team has been notified."


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_message = "What are the 3 most important AWS services for a beginner AI engineer to learn?"
    
    print("\n" + "=" * 65)
    print("  Production-Ready Bedrock API Call")
    print("=" * 65 + "\n")
    
    result = safe_chat(test_message)
    
    print("\n🤖 Response:")
    print("-" * 65)
    print(result)
    print("-" * 65)
```

---

# 5. Tuning & Senior Secrets

## Model Parameters

These are the knobs you turn to control *how* a model generates its response. Getting these right is the difference between a mediocre AI app and a great one.

### The Chef vs. Recipe Analogy

Imagine you've hired a world-class chef. They have a recipe (your prompt), but you can give them additional instructions about *how* to cook it:

| Parameter | Chef Instruction Equivalent |
|---|---|
| **Temperature** | "How much creative freedom do you have?" |
| **Top_p** | "Stick to ingredients from the approved list — how big is the list?" |
| **Max Tokens** | "How long should the dish take? Stop cooking after 30 minutes." |

---

### 🌡️ Temperature — The Creativity Dial

**Intuition:** Temperature controls how "adventurous" or "predictable" the model is when choosing its next word. At every step of generating text, the model calculates probabilities for all possible next words. Temperature controls whether it:
- **Always picks the most likely word** (low temperature = predictable, focused)
- **Sometimes picks surprising words** (high temperature = creative, unpredictable)

**Scale: 0.0 to 1.0** (some models go up to 2.0)

```
Temperature 0.0 (Zero):
  Question: "What is the capital of France?"
  Attempt 1: "The capital of France is Paris."
  Attempt 2: "The capital of France is Paris."
  Attempt 3: "The capital of France is Paris."
  ← Perfectly deterministic. Same answer every time.

Temperature 0.1 (Very Low):
  Great for: factual Q&A, code generation, data extraction
  Behavior: Very consistent, minimal variation, follows instructions precisely
  Use when: You need reliable, repeatable, accurate output

Temperature 0.7 (Medium — Good Default):
  Great for: general chat assistants, explanations
  Behavior: Mostly consistent, slight variation, still follows instructions
  Use when: You want helpful, natural-sounding responses

Temperature 1.0 (High):
  Great for: creative writing, brainstorming, story generation
  Behavior: High variation, surprising word choices, very creative
  Attempt 1: "Paris! The city of lights, love, and croissants..."
  Attempt 2: "Ah, Paris — a city that has captured imaginations for centuries..."
  Use when: You explicitly want creative, varied output
```

**Practical Guide:**

| Use Case | Recommended Temperature |
|---|---|
| SQL query generation | 0.0 — 0.1 |
| Code completion | 0.0 — 0.2 |
| Data extraction / classification | 0.0 — 0.2 |
| Customer support chatbot | 0.3 — 0.5 |
| General assistant | 0.5 — 0.7 |
| Creative writing | 0.8 — 1.0 |
| Brainstorming / ideation | 0.9 — 1.0 |

> 💡 **Senior Engineer Tip:** Many engineers use `temperature=0.0` for anything that requires accuracy and correctness (code, facts, data). They only increase temperature when they explicitly need variety or creativity.

---

### 🎯 Top_p — Nucleus Sampling

**Intuition:** Imagine the model has a dictionary of all possible next words, each with a probability. Top_p (also called "nucleus sampling") sets a probability mass threshold:

- **Top_p = 0.9**: "Consider only the set of top words that together account for 90% of the probability mass. Pick from those."
- **Top_p = 0.5**: "Even stricter — only the most likely words covering 50% of probability."
- **Top_p = 1.0**: "Consider all possible words."

**In practice:** Top_p and Temperature both control randomness, but differently. Most engineers adjust Temperature first and leave Top_p at 0.9 as a default. You rarely need to tune both simultaneously.

---

### 📏 Max Tokens — The Length Limit

**What is a token?**

A **token** is the basic unit of text that models process. It's roughly:
- 1 token ≈ 4 characters of English text
- 1 token ≈ ¾ of a word
- 100 tokens ≈ 75 words ≈ ~1 paragraph

Tokens are not whole words — they're chunks. "unbelievable" might be tokenized as "un", "believ", "able" (3 tokens).

**Why Max Tokens matters:**
- It limits the maximum length of the response
- It directly affects cost (you pay per token)
- If the model hits the limit mid-sentence, it stops abruptly

**Practical guide:**

| Response Type | Suggested Max Tokens |
|---|---|
| Short factual answer | 256 |
| Detailed explanation | 512 — 1024 |
| Long-form writing | 2048 — 4096 |
| Extended code generation | 4096 — 8192 |

> 🔧 **Tip:** Setting `maxTokens` high doesn't cost more — you only pay for tokens actually generated. It just sets the ceiling. But be careful: some pricing models charge for the context window allocation, not just generated tokens.

---

## Cost Control

### How Bedrock Pricing Works

Bedrock charges by the **number of tokens processed**, split into:
- **Input tokens**: Everything you send to the model (system prompt + conversation history + new message)
- **Output tokens**: Everything the model generates in response

**Formula:** `Total Cost = (Input Tokens × Input Price) + (Output Tokens × Output Price)`

Output tokens are typically more expensive than input tokens (generating text is harder than reading it).

**Example (illustrative — check current AWS pricing):**
```
Claude 3.5 Sonnet (approximate):
  Input:  $3.00 per million tokens
  Output: $15.00 per million tokens

A typical chat turn:
  Input: 500 tokens → $0.0015
  Output: 200 tokens → $0.003
  Cost per message: ~$0.0045 (less than half a cent)

1,000 conversations per day:
  ~$4.50/day → ~$135/month
  (Plus your system prompt tokens repeated every turn)
```

### The System Prompt Tax

Here's a hidden cost that surprises beginners:

```
Every API call includes:
  [System Prompt] + [All Previous Messages] + [New User Message] → Model

If your system prompt is 500 tokens and you have a 10-turn conversation:
  Turn 1:  500 (system) + 20 (messages) = 520 input tokens
  Turn 5:  500 (system) + 300 (messages) = 800 input tokens
  Turn 10: 500 (system) + 700 (messages) = 1,200 input tokens

A long conversation costs MORE per turn as history grows.
```

> 💡 **Senior Engineer Tip:** Keep your system prompts lean and specific. A 100-token system prompt instead of a 500-token one saves 400 tokens × every API call × every user × every turn. At scale, this adds up to thousands of dollars.

### Avoiding Surprise Bills

1. **Set a Budget Alarm** in AWS Billing Console:
   - Go to AWS Console → Billing → Budgets → Create Budget
   - Set a monthly dollar threshold (e.g., $50)
   - Add your email for alerts at 50%, 80%, 100% of budget

2. **Test with small prompts first:**
   ```python
   # ❌ Don't test your system with a 50,000-token document
   # ✅ Test with: "Say hello." — then confirm the plumbing works
   ```

3. **Log every API call's token usage:**
   ```python
   usage = response.get("usage", {})
   logger.info(f"Tokens: {usage}")  # Always log this
   ```

4. **Set a hard Max Tokens limit** appropriate to your use case — don't default to the maximum.

5. **Free Tier:** AWS Bedrock does NOT have a traditional free tier for model invocations. Some models offer a limited free trial period. Always check current pricing at [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/).

> 🚨 **Beginner Mistake:** Running a tight loop that calls the API hundreds of times in testing (e.g., a bug where your retry logic retries infinitely). Always add maximum retry limits. Always add delays between calls. Check CloudWatch costs after your first session.

---

## Security Basics

### The Least Privilege Principle

**The Least Privilege Principle** is one of the most important security concepts in cloud engineering:

> "Grant only the minimum permissions required to perform a specific task. Nothing more."

**Analogy:** A delivery driver needs a key to the lobby to deliver packages. They do NOT need keys to every apartment, the accounting office, or the server room. Even if giving them all keys would be convenient, it's a massive security risk.

**In AWS terms:**
```
❌ Overly permissive (BAD):
   Policy: AdministratorAccess
   → Can do literally everything in your AWS account
   → If these credentials are leaked → catastrophic

✅ Least privilege (GOOD):
   Policy: Allow bedrock:InvokeModel on specific model ARNs only
   → Can ONLY call specific Bedrock models
   → If leaked → attacker can only call those models (still bad, but contained)
```

**Practical Bedrock Example:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowBedrockInvokeSpecificModels",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:Converse"
      ],
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
      ]
    }
  ]
}
```

This policy allows ONLY calling the Claude 3.5 Sonnet model. Nothing else.

---

### IAM Roles vs. IAM Users

| | **IAM User** | **IAM Role** |
|---|---|---|
| **What is it?** | A permanent identity for a person | A temporary identity for a service/application |
| **Credentials** | Long-term Access Key + Secret Key | Temporary credentials (auto-rotated) |
| **Used by** | Human developers (local development) | Lambda functions, EC2 instances, ECS containers |
| **Best for** | `aws configure` on your laptop | Production applications on AWS compute |
| **Credential rotation** | Manual (you rotate when needed) | Automatic (AWS handles it) |
| **If leaked** | Must manually delete and recreate keys | Auto-expire (much safer) |

**Why IAM Roles are better in production:**

When your code runs in a Lambda function or on an EC2 instance, you can **attach an IAM Role** to that compute resource. AWS automatically provides temporary credentials that rotate frequently. Your code never needs to store any keys — it just calls boto3, which asks the compute environment for its role credentials.

```python
# In a Lambda function with the correct IAM Role attached:
# You don't need to configure ANYTHING — boto3 finds the role automatically
import boto3
client = boto3.client("bedrock-runtime", region_name="us-east-1")
# ↑ Works perfectly because Lambda's execution role provides credentials
```

---

### Why Production Systems Never Use Root Credentials

The **root user** is the original account you created when you signed up for AWS. It has unlimited, unconstrained power:
- Cannot be restricted by IAM policies
- Can do ANYTHING — delete all resources, close the account, override all security
- AWS explicitly recommends never using it for day-to-day tasks

**Best practices:**
1. Enable **MFA (Multi-Factor Authentication)** on root immediately
2. Generate root access keys? **Never.** Delete them if they exist.
3. Create a non-root IAM user for all development work
4. In production, use IAM Roles exclusively — no IAM user access keys

```
Security Hierarchy:
┌─────────────────────────────────────────────────────────────────┐
│  ROOT USER                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  For emergency only (e.g., locked out of account)       │   │
│  │  Enable MFA. Never create access keys. Lock away.       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  IAM Admin User (for setting up other users/roles)              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  IAM Developer User (your daily driver — via aws config) │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  IAM Roles (for Lambda, EC2, ECS — production systems)          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  No long-term keys. Auto-rotating temp credentials.      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference — Senior Engineer Tips Summary

> **Credential Safety:** Never commit `.env` files or `~/.aws/credentials` content to version control. Add both to `.gitignore` immediately. Use `git-secrets` or `truffleHog` to scan for accidentally committed secrets.

> **Region First:** Before writing a single line of code, confirm your target region supports the model you want. Check the Bedrock console → Model access → enable models in your region.

> **Token Budgeting:** Design your system prompts to be as short as effective. Long system prompts are a "tax" on every API call. 100 tokens saved = significant money at scale.

> **Start Small:** When debugging a new integration, send the simplest possible prompt ("Say 'OK'") first. Verify the plumbing works before sending complex prompts. This saves time and money.

> **Use the Converse API:** Unless you have a specific reason to use InvokeModel (access to model-specific features), use Converse. It's forward-compatible, cleaner, and model-agnostic.

> **Log Everything (At First):** During development, log the full request and response. In production, log token counts and latencies. You can't debug what you can't see.

> **Retry with Backoff:** Never retry immediately. Always wait, and wait longer each retry. Implement a maximum retry limit. Log every retry with the error code.

> **IAM Roles in Production:** Never deploy code with hardcoded credentials or even IAM user access keys in production. Attach IAM Roles to your compute resources and let AWS handle credential management.

> **Test Costs Early:** Before launching any feature to users, estimate the per-call cost and multiply by expected volume. Set Budget Alarms before you go live. AI API costs scale fast.

> **Security is Day One:** The best time to implement least privilege, proper IAM, and secure credential management is before you write production code — not after a security incident.

---

*This guide was written for beginners with the goal of becoming production-ready AI/ML engineers on AWS. The concepts here form the foundation of virtually every GenAI application built on AWS today. Revisit it as you build real projects — you'll notice new things each time.*

---

**Happy Building! 🚀**

