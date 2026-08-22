# The Complete LangChain Engineering Handbook
### From Absolute Beginner to Production AI Engineer

> **A comprehensive, beginner-friendly guide to building production-grade AI applications with LangChain, LCEL, LangGraph, and modern AI engineering practices.**

---

> **Who This Is For:** Python developers who are comfortable with the language but new to LangChain and AI engineering. You'll learn by building real systems, not just reading theory.

> **How To Use This Book:** Read sequentially from Step 0 if you're truly starting fresh. Skip to Step 1 if you already understand LLMs. Use the Table of Contents to jump between reference sections when building.

---

## Table of Contents

- [Step 0: Foundational AI & LLM Concepts](#step-0-foundational-ai--llm-concepts)
  - [0.1 What is an LLM?](#01-what-is-an-llm)
  - [0.2 APIs & AI Providers](#02-apis--ai-providers)
  - [0.3 What Problems LangChain Solves](#03-what-problems-langchain-solves)
  - [0.4 Core AI Application Patterns](#04-core-ai-application-patterns)
- [Step 1: The Basics — Models, Prompts & Parsers](#step-1-the-basics--models-prompts--parsers)
  - [1.1 LLMs vs. Chat Models](#11-llms-vs-chat-models)
  - [1.2 Prompt Engineering in LangChain](#12-prompt-engineering-in-langchain)
  - [1.3 Few-Shot Prompting](#13-few-shot-prompting)
  - [1.4 Output Parsers](#14-output-parsers)
- [Step 2: LCEL — LangChain Expression Language](#step-2-lcel--langchain-expression-language)
  - [2.1 Pipe Syntax & Runnable Data Flow](#21-pipe-syntax--runnable-data-flow)
  - [2.2 Standard Runnable Methods](#22-standard-runnable-methods)
  - [2.3 Advanced Runnables](#23-advanced-runnables)
- [Step 3: Data Ingestion & Storage](#step-3-data-ingestion--storage)
  - [3.1 Document Loaders](#31-document-loaders)
  - [3.2 Chunking Strategies & Text Splitters](#32-chunking-strategies--text-splitters)
  - [3.3 Embeddings & Vector Stores](#33-embeddings--vector-stores)
  - [3.4 The Indexing API](#34-the-indexing-api)
- [Step 4: Advanced RAG](#step-4-advanced-rag)
  - [4.1 Basic RAG via LCEL](#41-basic-rag-via-lcel)
  - [4.2 Advanced Retrievers](#42-advanced-retrievers)
  - [4.3 RAG Optimization](#43-rag-optimization)
  - [4.4 Production RAG Architectures](#44-production-rag-architectures)
- [Step 5: Memory & Conversational State](#step-5-memory--conversational-state)
  - [5.1 Chat History](#51-chat-history)
  - [5.2 RunnableWithMessageHistory](#52-runnablewithmessagehistory)
  - [5.3 Context Window Management](#53-context-window-management)
- [Step 6: Agents, Tools & LangGraph](#step-6-agents-tools--langgraph)
  - [6.1 Tools & Function Calling](#61-tools--function-calling)
  - [6.2 Agent Architectures](#62-agent-architectures)
  - [6.3 LangGraph Deep Dive](#63-langgraph-deep-dive)
  - [6.4 Advanced Agent Systems](#64-advanced-agent-systems)
- [Step 7: Production & Evaluation](#step-7-production--evaluation)
  - [7.1 LangSmith — Tracing & Observability](#71-langsmith--tracing--observability)
  - [7.2 LangServe — APIs & Deployment](#72-langserve--apis--deployment)
  - [7.3 Production Engineering](#73-production-engineering)
- [Complete Learning Roadmap](#complete-learning-roadmap)

---

# Step 0: Foundational AI & LLM Concepts

> **Why this step matters:** Before writing a single line of LangChain code, you need a mental model of what's happening underneath. Many developers skip this and spend weeks confused about why their AI app behaves unexpectedly. Invest 30 minutes here — it will save you 30 hours later.

---

## 0.1 What is an LLM?

### The Big Picture

An **LLM (Large Language Model)** is a software system trained on massive amounts of text that can read text you give it and generate text in response.

That's it at a high level. But let's build a proper mental model.

**Analogy: The Ultimate Autocomplete**

You know how your phone's keyboard predicts the next word? An LLM is like that, but trained on virtually all of human-written text — books, articles, code, scientific papers, conversations — and operating at a scale that produces coherent, intelligent-seeming responses paragraph after paragraph.

When you type "The capital of France is...", your phone predicts "Paris". When you ask an LLM "Explain quantum entanglement to a 10-year-old", it generates a multi-paragraph explanation because it has learned, from billions of examples, what a good explanation looks like.

### Tokens: The Building Blocks

LLMs don't read words the way humans do. They read **tokens**.

A **token** is roughly 3-4 characters or about 0.75 words in English. Here's how tokenization works:

```
"Hello, world!"  →  ["Hello", ",", " world", "!"]  →  4 tokens

"LangChain is awesome"  →  ["Lang", "Chain", " is", " awesome"]  →  4 tokens

"supercalifragilistic"  →  ["super", "cal", "if", "rag", "il", "istic"]  →  6 tokens
```

> **Beginner Note:** Why does tokenization matter to you as a developer?
> 1. **Cost**: AI APIs charge per token. Longer prompts = higher cost.
> 2. **Limits**: Models have a maximum number of tokens they can process at once (the "context window").
> 3. **Behavior**: Rare words get split into many tokens, making them slightly harder for the model to reason about.

**Quick Token Math:**
- 1,000 tokens ≈ 750 words ≈ 1.5 pages of text
- GPT-4o has a 128,000 token context window ≈ ~300 pages of text
- Claude 3.5 Sonnet: 200,000 token context window ≈ ~500 pages

### Context Windows: The Model's Working Memory

```
┌─────────────────────────────────────────────────────┐
│                  CONTEXT WINDOW                     │
│                                                     │
│  ┌──────────────┐  ┌────────────┐  ┌─────────────┐ │
│  │System Prompt │  │Chat History│  │ Your Message│ │
│  │(Instructions)│  │(Past turns)│  │  (New Input)│ │
│  └──────────────┘  └────────────┘  └─────────────┘ │
│                                                     │
│  Everything the model "sees" in a single request   │
└─────────────────────────────────────────────────────┘
```

The context window is the model's **total working memory for one request**. Once you send a request, the model sees everything in that window simultaneously — there's no scrolling, no "reading back". It processes the entire context at once.

This has profound implications:
- **The model has NO memory between separate API calls.** Each call starts fresh unless you manually include past conversation.
- **Long conversations cost more** because you must re-send the entire history each time.
- **Very long documents** may not fit in a single context window.

### How Text Generation Works

When an LLM generates a response, it doesn't write the whole answer at once. It generates **one token at a time**, each time predicting the most likely next token given everything before it:

```
Prompt: "The moon is"
Step 1: Predict next token → "a" (probability 0.4) or "made" (0.3) or "our" (0.2)...
Chosen: "a"

Step 2: Predict next given "The moon is a" → "natural" (0.5) or "large" (0.3)...
Chosen: "natural"

Step 3: "The moon is a natural" → "satellite" (0.7)...
...and so on until a stop condition is reached
```

This is why LLMs can "hallucinate" — they're always picking statistically likely next tokens, not looking up verified facts.

### Temperature and Top-P: Controlling Randomness

These two parameters control how "creative" vs "deterministic" the model's output is.

**Temperature (0.0 to 2.0)**

```
Temperature = 0.0  →  Always picks the single most probable token
                       Output: Deterministic, repetitive, safe
                       Use for: Structured data extraction, factual Q&A

Temperature = 0.7  →  Mixes high-probability with some randomness
                       Output: Natural, coherent, slightly varied
                       Use for: Most chatbot and assistant tasks

Temperature = 1.5  →  High randomness, unexpected token choices
                       Output: Creative, surprising, sometimes incoherent
                       Use for: Creative writing, brainstorming

Temperature = 2.0  →  Very high randomness
                       Output: Often gibberish
                       Use for: Rarely useful
```

**Top-P (0.0 to 1.0) — Nucleus Sampling**

Instead of controlling randomness directly, top-p limits which tokens are even considered:

- `top_p = 0.1` → Only consider tokens that together account for the top 10% of probability mass (very focused)
- `top_p = 0.9` → Consider tokens accounting for top 90% of probability mass (more variety)
- `top_p = 1.0` → Consider all tokens

> **Mental Model:** Think of temperature as "how drunk is the model?" and top-p as "how many options does it consider?" In practice, tune temperature first. Only adjust top-p if you need finer control.

> **Best Practice for Production:** Use `temperature=0` for extraction/classification tasks where you want consistency. Use `temperature=0.7` for conversational AI. Never go above `1.0` in production.

### Transformer Architecture (Intuition Only)

You don't need to understand the math, but this mental model helps:

A Transformer is built on a mechanism called **self-attention**. When processing a sentence, every word "looks at" every other word to understand context.

```
"The bank by the river was steep"
      ↕   ↕   ↕     ↕    ↕
"bank" pays attention to "river" → understands it means riverbank, not financial bank
```

This is why modern LLMs understand context so well — they don't read left-to-right like old RNNs. They process relationships between all words simultaneously.

For you as an engineer: this means **the order and phrasing of your prompt matters a lot**. Words near each other and in clear relationships are processed more effectively.

---

## 0.2 APIs & AI Providers

### The Landscape

You interact with LLMs through **APIs** (Application Programming Interfaces). You send text in, text comes out. The heavy computation happens on the provider's servers.

| Provider | Models | Strengths | Pricing Model |
|----------|--------|-----------|---------------|
| **OpenAI** | GPT-4o, GPT-4o-mini, o1 | Best ecosystem, function calling, multimodal | Per token (input/output) |
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus | Long context, safety, nuanced reasoning | Per token |
| **Google** | Gemini 1.5 Pro/Flash | 1M token context, multimodal, fast | Per token |
| **Meta (via providers)** | Llama 3.1, Llama 3.2 | Open weights, self-hostable | Free (self-hosted) or per token |
| **Mistral** | Mistral Large, Mixtral | European, strong code, efficient | Per token |
| **Cohere** | Command R+ | RAG-optimized, enterprise | Per token |

### Hosted vs. Local Inference

**Hosted (Cloud API):**
```
Your App → HTTPS Request → Provider's GPU Cluster → Response
```
- ✅ No hardware needed
- ✅ Always-updated models
- ✅ Scales automatically
- ❌ Data leaves your infrastructure
- ❌ Ongoing cost per request
- ❌ Latency depends on network

**Local/Self-Hosted:**
```
Your App → Local Process → Your GPU/CPU → Response
```
- ✅ Data never leaves your machine
- ✅ No per-request cost (after hardware)
- ✅ Lower latency for local use
- ❌ Requires GPU hardware for good performance
- ❌ Smaller models than cloud offerings
- ❌ You manage updates and infrastructure

**Tools for Local Models:**
- **Ollama**: The easiest way to run models locally. One command to download and run Llama, Mistral, Gemma, etc.
- **LM Studio**: GUI for running local models
- **vLLM**: Production-grade local serving (for servers with GPUs)
- **llama.cpp**: Ultra-efficient CPU inference

```bash
# Run Llama 3 locally with Ollama
brew install ollama          # macOS
ollama pull llama3.1         # Download the model
ollama run llama3.1          # Run interactively
```

LangChain integrates with all of these through a unified interface — you write the same application code regardless of which provider you use. That's one of its core values.

---

## 0.3 What Problems LangChain Solves

### The Raw API Problem

Before understanding LangChain, understand the pain it eliminates.

**Scenario:** You want to build a chatbot that answers questions about your company's documentation.

Without LangChain, here's what you'd need to write:

```python
# WITHOUT LangChain — everything manually

import openai
import json

client = openai.OpenAI(api_key="sk-...")

# Problem 1: Prompt management — hardcoded strings everywhere
def build_prompt(user_question, doc_context, chat_history):
    messages = []
    
    # Manually building the system prompt
    messages.append({
        "role": "system", 
        "content": f"You are a helpful assistant. Use this context: {doc_context}"
    })
    
    # Manually injecting chat history
    for turn in chat_history:
        messages.append({"role": turn["role"], "content": turn["content"]})
    
    # Manually adding the new message
    messages.append({"role": "user", "content": user_question})
    return messages

# Problem 2: No memory management — manual history tracking
chat_history = []

# Problem 3: No retrieval system — manual document handling
def find_relevant_docs(question):
    # You'd need to implement vector search from scratch
    # Load embeddings, compute similarity, retrieve chunks...
    pass  # This is 100+ lines of code

# Problem 4: No output parsing — manual string handling
def parse_response(response):
    content = response.choices[0].message.content
    # If you want structured output, parse it yourself
    # If it fails, handle errors manually
    return content

# Problem 5: Error handling, retries, rate limits — all manual
def call_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
            )
            return parse_response(response)
        except openai.RateLimitError:
            time.sleep(2 ** attempt)
    raise Exception("Max retries exceeded")

# Problem 6: Switching providers means rewriting everything
# If you want to try Anthropic, you rewrite all the API calls
```

This works for a demo. It becomes a nightmare at scale:
- Prompts scattered across the codebase
- No standardized way to chain operations
- Manual memory management
- No streaming support without significant extra work
- Switching models requires major refactoring

### What LangChain Provides

LangChain is a framework that provides **standardized, composable building blocks** for AI applications.

```
┌─────────────────────────────────────────────────────────────────┐
│                    LANGCHAIN SOLVES:                            │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Unified   │  │   Prompt    │  │       Memory &          │ │
│  │ Model API   │  │ Management  │  │   Conversation State    │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Retrieval  │  │   Agents    │  │    Chain Composition    │ │
│  │  (RAG)      │  │  & Tools    │  │    (LCEL Pipelines)     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Document   │  │   Output    │  │    Observability        │ │
│  │  Loaders    │  │  Parsers    │  │    (LangSmith)          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Specific problems it solves:**

1. **Provider Abstraction**: Write once, run on OpenAI, Anthropic, Ollama, or any other provider by changing one line.

2. **Prompt Management**: Reusable, parameterized prompt templates with version control and composition.

3. **Chain Composition (LCEL)**: Connect components with a clean pipe (`|`) syntax instead of nested function calls.

4. **Retrieval**: Built-in document loading, chunking, embedding, and semantic search infrastructure.

5. **Memory**: Conversation history persistence and injection without manual management.

6. **Agents & Tools**: Framework for LLMs that can call functions, search the web, query databases, etc.

7. **Output Parsing**: Structured extraction from LLM outputs with validation and retry logic.

8. **Observability**: LangSmith integration for tracing every request, debugging failures, and evaluating quality.

---

## 0.4 Core AI Application Patterns

Before diving into code, understand the four major patterns that AI applications fall into. Every LangChain system you build will be a variation of one (or a combination) of these:

### Pattern 1: Chatbot / Conversational AI

```
User → Message → LLM + History → Response → User
         ↑                              ↓
         └──────── Store History ←──────┘
```

**What it is:** A system that maintains conversation context and responds naturally to user input.

**Examples:** Customer service bots, virtual assistants, tutoring systems.

**Key challenge:** Memory — keeping track of what was said previously.

### Pattern 2: RAG (Retrieval-Augmented Generation)

```
User Question → Retriever → Relevant Docs → LLM → Answer
                    ↑
              Vector Database
              (Your Knowledge Base)
```

**What it is:** The LLM answers questions using information retrieved from your own documents/database rather than only its training data.

**Examples:** Document Q&A, enterprise knowledge base, support systems.

**Key challenge:** Retrieval quality — finding the *right* documents quickly and accurately.

**Why RAG?** LLMs have training cutoffs and don't know your private data. RAG bridges this gap.

### Pattern 3: AI Agents

```
User Goal → LLM (Reasoning) → Choose Tool → Execute Tool → Result
                ↑                                              ↓
                └──────────── Observe & Decide Again ←────────┘
```

**What it is:** An LLM that can take *actions* — calling APIs, running code, searching the web — to accomplish a goal through multiple steps of reasoning.

**Examples:** Research agents, coding assistants, autonomous workflow automation.

**Key challenge:** Reliability — ensuring the agent doesn't take wrong actions or get stuck in loops.

### Pattern 4: Structured Extraction / Data Pipeline

```
Unstructured Text → LLM → Structured Data (JSON/Objects) → Database/API
```

**What it is:** Using an LLM to extract structured information from unstructured text.

**Examples:** Invoice processing, resume parsing, content classification, entity extraction.

**Key challenge:** Consistency — getting the same output format reliably at scale.

---

### Environment Setup

Before proceeding, let's set up your development environment.

```bash
# Create a virtual environment (highly recommended)
python -m venv langchain-env
source langchain-env/bin/activate  # Linux/Mac
# langchain-env\Scripts\activate   # Windows

# Core LangChain packages
pip install langchain
pip install langchain-core
pip install langchain-community
pip install langchain-openai
pip install langchain-anthropic

# Additional utilities we'll use throughout
pip install python-dotenv        # Environment variable management
pip install pydantic             # Data validation (used heavily by LangChain)
pip install tiktoken             # OpenAI tokenizer
pip install faiss-cpu            # Vector store (CPU version)
pip install chromadb             # Alternative vector store
pip install sentence-transformers # Local embedding models
pip install pypdf                # PDF loading
pip install bs4                  # Web scraping / HTML loading
pip install langsmith            # Observability (optional but recommended)
pip install langgraph            # Agent framework
```

```bash
# Create a .env file for API keys (NEVER commit this to git)
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
LANGCHAIN_API_KEY=ls__your-key-here   # LangSmith (optional)
LANGCHAIN_TRACING_V2=true             # Enable LangSmith tracing
LANGCHAIN_PROJECT=my-langchain-project
EOF
```

```python
# In all your Python files, load env vars first
from dotenv import load_dotenv
load_dotenv()  # Reads .env file into environment variables

import os
openai_key = os.getenv("OPENAI_API_KEY")
```

> **Security Warning:** Never hardcode API keys in code. Never commit `.env` files to git. Add `.env` to your `.gitignore`. API key exposure can result in unexpected bills of thousands of dollars.

---

# Step 1: The Basics — Models, Prompts & Parsers

## 1.1 LLMs vs. Chat Models

### Understanding the Distinction

LangChain draws a clear distinction between two model types that behave differently at the API level:

**Text LLMs (Completion Models)**
- Take a single string of text as input
- Return a single string of text
- Used for: text completion, older-style generation tasks
- Example: `text-davinci-003` (now deprecated by OpenAI)

**Chat Models**
- Take a *list of messages* as input (with roles: system, human, AI)
- Return a message object
- Used for: virtually everything in modern AI applications
- Example: `gpt-4o`, `claude-3-5-sonnet`, `gemini-1.5-pro`

> **Beginner Note:** In 2024+, you'll almost exclusively use Chat Models. The distinction exists for historical reasons. LangChain standardizes the interface so they're used similarly.

### Message Types

Chat models communicate through **messages**. Each message has:
1. A **role** — who is "speaking"
2. **Content** — what is being said

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

# SystemMessage: Instructions to the model (its "personality" and rules)
system = SystemMessage(content="You are a helpful Python tutor who explains concepts simply.")

# HumanMessage: What the user says
human = HumanMessage(content="What is a list comprehension?")

# AIMessage: What the model responded (used when building history)
ai = AIMessage(content="A list comprehension is a concise way to create lists...")

# ToolMessage: Result from a tool call (used in agents)
tool_result = ToolMessage(content="[1, 4, 9, 16, 25]", tool_call_id="call_abc123")
```

**Mental Model: The Chat Turn**

```
┌─────────────────────────────────────────────────────────┐
│  SYSTEM: You are a helpful Python tutor...              │  ← Set once, persists
├─────────────────────────────────────────────────────────┤
│  HUMAN:  What is a list comprehension?                  │  ← Turn 1
│  AI:     A list comprehension is...                     │
├─────────────────────────────────────────────────────────┤
│  HUMAN:  Can you show me an example with numbers?       │  ← Turn 2
│  AI:     Sure! Here's one: [x**2 for x in range(10)]   │
├─────────────────────────────────────────────────────────┤
│  HUMAN:  What does the ** operator do?                  │  ← Turn 3 (your query)
└─────────────────────────────────────────────────────────┘
         Everything above gets sent as context for Turn 3
```

### Integrating Chat Model Providers

LangChain uses a **unified interface** across all providers. The same method calls work regardless of which LLM you use.

```python
# ─────────────────────────────────────────
# OpenAI
# ─────────────────────────────────────────
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    max_tokens=1000,
)

# ─────────────────────────────────────────
# Anthropic Claude
# ─────────────────────────────────────────
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=1000,
)

# ─────────────────────────────────────────
# Ollama (Local Models)
# ─────────────────────────────────────────
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(
    model="llama3.1",
    temperature=0.7,
)

# ─────────────────────────────────────────
# The SAME interface regardless of provider
# ─────────────────────────────────────────
from langchain_core.messages import HumanMessage

response = llm.invoke([HumanMessage(content="What is 2 + 2?")])
print(response.content)        # "4" (or "2 + 2 equals 4")
print(response.response_metadata)  # Token usage, model info, etc.
```

> **Key Insight:** This is the primary value of LangChain's model layer. You can experiment with GPT-4o, switch to Claude for cost reasons, and test a local Llama model — all without changing your application logic.

### Direct Invocation Example

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

# Initialize the model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Single message
response = llm.invoke([HumanMessage(content="What is the capital of Japan?")])
print(response.content)  # Tokyo

# With a system message
messages = [
    SystemMessage(content="You are a geography expert. Answer only with the city name, nothing else."),
    HumanMessage(content="What is the capital of Japan?"),
]
response = llm.invoke(messages)
print(response.content)  # Tokyo
print(type(response))    # <class 'langchain_core.messages.ai.AIMessage'>

# Inspect token usage
print(response.response_metadata)
# {'token_usage': {'completion_tokens': 1, 'prompt_tokens': 32, ...}}
```

---

## 1.2 Prompt Engineering in LangChain

### Why Prompt Templates?

Hardcoding prompt strings creates maintenance nightmares:

```python
# BAD: Scattered string formatting
def analyze_sentiment(text, language):
    prompt = f"Analyze the sentiment of this {language} text: {text}"
    # Fragile, no validation, hard to test, hard to reuse
```

LangChain's **PromptTemplate** and **ChatPromptTemplate** solve this with:
- Named variables with validation
- Reusable, composable templates
- Easy testing and modification
- Separation of prompt logic from application logic

### PromptTemplate (for simple string templates)

```python
from langchain_core.prompts import PromptTemplate

# Define a reusable template with named variables
template = PromptTemplate(
    input_variables=["topic", "audience"],
    template="""Write a brief explanation of {topic} for a {audience} audience.
    
Keep it under 100 words and use simple language."""
)

# Format the template (produces a string)
formatted = template.format(topic="neural networks", audience="high school student")
print(formatted)
# Write a brief explanation of neural networks for a high school student audience.
# Keep it under 100 words and use simple language.

# Alternative: from_template is cleaner
template = PromptTemplate.from_template(
    "Write a brief explanation of {topic} for a {audience} audience."
)
```

### ChatPromptTemplate (for chat models — what you'll use most)

```python
from langchain_core.prompts import ChatPromptTemplate

# Define a chat prompt with multiple message roles
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert {domain} consultant. Respond in a {tone} tone."),
    ("human", "I need help with: {question}"),
])

# Invoke to get formatted messages
messages = prompt.format_messages(
    domain="software architecture",
    tone="professional but approachable",
    question="Should I use microservices or a monolith for my startup?"
)

print(messages)
# [SystemMessage(content='You are an expert software architecture consultant...'),
#  HumanMessage(content='I need help with: Should I use microservices...')]

# Use with a model
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# LCEL pipe syntax (preview — full explanation in Step 2)
chain = prompt | llm
response = chain.invoke({
    "domain": "software architecture",
    "tone": "professional but approachable",
    "question": "Should I use microservices or a monolith for my startup?"
})
print(response.content)
```

### MessagesPlaceholder: Injecting Chat History

This is critical for conversational AI. You need a way to inject a dynamic list of past messages into your prompt:

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# MessagesPlaceholder acts as a "slot" for a list of messages
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Be concise."),
    MessagesPlaceholder(variable_name="chat_history"),  # ← Slot for history
    ("human", "{user_input}"),
])

# Simulate a conversation
chat_history = [
    HumanMessage(content="My name is Alex."),
    AIMessage(content="Nice to meet you, Alex! How can I help you today?"),
]

# The history gets injected into the prompt
messages = prompt.format_messages(
    chat_history=chat_history,
    user_input="What's my name?"
)

# The model now has context about the name
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = prompt | llm
response = chain.invoke({
    "chat_history": chat_history,
    "user_input": "What's my name?"
})
print(response.content)  # "Your name is Alex."
```

### Multi-Turn Conversation Example

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Socratic tutor. Guide students to answers through questions, never give direct answers."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm

# Manage history manually (we'll automate this in Step 5)
history = []

def chat(user_input: str) -> str:
    response = chain.invoke({
        "history": history,
        "input": user_input,
    })
    
    # Update history with the new exchange
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response.content))
    
    return response.content

# Interactive conversation
print(chat("I don't understand recursion."))
print(chat("Okay, but how does a function call itself?"))
print(chat("What happens if there's no base case?"))
```

---

## 1.3 Few-Shot Prompting

### What is Few-Shot Prompting?

**Few-shot prompting** means including examples of the task you want the model to perform, directly in your prompt. This dramatically improves output quality and consistency for structured tasks.

**Mental Model:** It's like training a new employee. Instead of just describing the job, you show them 3-5 completed examples. "Here's what good looks like — now do the same for this new case."

```
Zero-shot: "Classify this review as positive or negative: 'The food was amazing!'"

Few-shot:  "Classify reviews as positive or negative. Examples:
           - 'Best burger I've ever had' → positive
           - 'Waited 45 minutes and food was cold' → negative
           - 'Service was okay, nothing special' → neutral
           
           Now classify: 'The food was amazing!'"
```

Few-shot almost always outperforms zero-shot for classification, extraction, and formatting tasks.

### FewShotChatMessagePromptTemplate

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

# Define your examples
examples = [
    {
        "input": "The customer is very angry about the delayed shipment.",
        "output": """{"sentiment": "negative", "category": "shipping", "urgency": "high", "action_required": true}"""
    },
    {
        "input": "I absolutely love this product, it changed my life!",
        "output": """{"sentiment": "positive", "category": "product", "urgency": "low", "action_required": false}"""
    },
    {
        "input": "My order hasn't arrived yet and it's been 2 weeks.",
        "output": """{"sentiment": "negative", "category": "shipping", "urgency": "high", "action_required": true}"""
    },
    {
        "input": "The website is a bit slow sometimes but overall it's fine.",
        "output": """{"sentiment": "neutral", "category": "website", "urgency": "low", "action_required": false}"""
    },
]

# Template for each example
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

# Build the few-shot prompt
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

# Wrap in a full prompt
final_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a customer support classifier. 
Analyze customer messages and output ONLY a JSON object with these fields:
- sentiment: "positive", "negative", or "neutral"
- category: "shipping", "product", "website", "billing", or "other"
- urgency: "high", "medium", or "low"
- action_required: true or false"""),
    few_shot_prompt,
    ("human", "{input}"),
])

# Use it
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = final_prompt | llm

result = chain.invoke({"input": "I was charged twice for my subscription this month!"})
print(result.content)
# {"sentiment": "negative", "category": "billing", "urgency": "high", "action_required": true}
```

### Dynamic Few-Shot with Example Selectors

When you have many examples, you don't want to include all of them (wasted tokens). Use an **Example Selector** to dynamically choose the most relevant examples:

```python
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Large example bank
example_bank = [
    {"input": "Package not delivered", "output": "shipping_issue"},
    {"input": "Wrong item received", "output": "fulfillment_issue"},
    {"input": "Billing error on statement", "output": "billing_issue"},
    {"input": "Can't log into account", "output": "account_issue"},
    {"input": "Product quality poor", "output": "quality_issue"},
    {"input": "Website is down", "output": "technical_issue"},
    {"input": "Need to return item", "output": "returns"},
    {"input": "Subscription cancelled but still charged", "output": "billing_issue"},
    {"input": "Item arrived damaged", "output": "quality_issue"},
    {"input": "Tracking number not working", "output": "shipping_issue"},
]

# Selector picks the k most similar examples to the current input
example_selector = SemanticSimilarityExampleSelector.from_examples(
    example_bank,
    OpenAIEmbeddings(),      # Use embeddings to measure similarity
    FAISS,                   # Vector store to search
    k=3,                     # Return 3 most similar examples
)

# Test the selector
selected = example_selector.select_examples({"input": "My payment was processed twice"})
print(selected)
# Will return the billing-related examples since they're most similar
```

---

## 1.4 Output Parsers

### The Problem with Raw LLM Output

LLMs return strings. Your application needs structured data:

```python
# LLM might return:
"The sentiment is positive and the confidence is 0.95"
# But you need:
{"sentiment": "positive", "confidence": 0.95}

# Or it might return (inconsistently):
"Sentiment: POSITIVE | Confidence: 95%"
# Same meaning, different format — breaks your parser
```

Output parsers solve this with validation, type checking, and retry logic.

### StrOutputParser

The simplest parser — just extracts the string content from an `AIMessage`:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate the following text to {language}."),
    ("human", "{text}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# Without parser: response is an AIMessage object
chain = prompt | llm
result = chain.invoke({"language": "French", "text": "Hello, how are you?"})
print(type(result))   # <class 'langchain_core.messages.ai.AIMessage'>
print(result.content) # "Bonjour, comment allez-vous?"

# With parser: response is a plain string
chain_with_parser = prompt | llm | parser
result = chain_with_parser.invoke({"language": "French", "text": "Hello, how are you?"})
print(type(result))   # <class 'str'>
print(result)         # "Bonjour, comment allez-vous?"
```

### PydanticOutputParser — Structured Extraction

This is where output parsing becomes truly powerful. Define a Pydantic model for your desired output structure:

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

# ─────────────────────────────────────────
# Step 1: Define your output schema
# ─────────────────────────────────────────
class JobPosting(BaseModel):
    """Structured representation of a job posting."""
    title: str = Field(description="The job title")
    company: str = Field(description="The company name")
    location: str = Field(description="Job location or 'Remote'")
    salary_min: Optional[int] = Field(description="Minimum salary in USD, null if not mentioned")
    salary_max: Optional[int] = Field(description="Maximum salary in USD, null if not mentioned")
    required_skills: List[str] = Field(description="List of required technical skills")
    experience_years: Optional[int] = Field(description="Years of experience required, null if not specified")
    is_remote: bool = Field(description="Whether remote work is allowed")

# ─────────────────────────────────────────
# Step 2: Create the parser
# ─────────────────────────────────────────
parser = PydanticOutputParser(pydantic_object=JobPosting)

# ─────────────────────────────────────────
# Step 3: Include format instructions in prompt
# ─────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at extracting structured information from job postings.
    
{format_instructions}"""),
    ("human", "Extract information from this job posting:\n\n{job_posting_text}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = prompt | llm | parser

# ─────────────────────────────────────────
# Step 4: Use it
# ─────────────────────────────────────────
sample_posting = """
Senior Python Developer at TechCorp Inc.
Location: San Francisco, CA (Hybrid)

We're looking for a Senior Python Developer with 5+ years of experience.
Salary: $140,000 - $180,000

Required skills:
- Python (advanced)
- FastAPI or Django
- PostgreSQL
- Docker and Kubernetes
- AWS experience a plus

Remote work available 3 days per week.
"""

result = chain.invoke({
    "format_instructions": parser.get_format_instructions(),
    "job_posting_text": sample_posting,
})

print(type(result))  # <class '__main__.JobPosting'>
print(result.title)  # "Senior Python Developer"
print(result.salary_min)  # 140000
print(result.required_skills)  # ['Python', 'FastAPI or Django', 'PostgreSQL', ...]
print(result.is_remote)  # True

# Access as dict
print(result.model_dump())
```

### JSON Output with `with_structured_output()`

For modern OpenAI models, there's an even cleaner approach:

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List

class MovieReview(BaseModel):
    title: str = Field(description="Movie title")
    year: int = Field(description="Release year")
    rating: float = Field(description="Rating out of 10")
    pros: List[str] = Field(description="What the reviewer liked")
    cons: List[str] = Field(description="What the reviewer disliked")
    recommended: bool = Field(description="Whether the reviewer recommends it")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# bind the schema directly to the model
structured_llm = llm.with_structured_output(MovieReview)

result = structured_llm.invoke(
    "Review the movie Inception (2010) as a film critic."
)

print(result.title)    # "Inception"
print(result.rating)   # 9.0 (or whatever it decides)
print(result.pros)     # ["Stunning visual effects", "Complex narrative", ...]
print(result.recommended)  # True
```

> **Best Practice:** Use `with_structured_output()` when working with OpenAI/Anthropic models that support it natively. It's more reliable than parsing free-form text because the model is constrained at the token-generation level.

### RetryOutputParser — Handling Failures Gracefully

Sometimes the model doesn't follow formatting instructions perfectly:

```python
from langchain.output_parsers import RetryOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class SentimentResult(BaseModel):
    sentiment: str = Field(description="One of: positive, negative, neutral")
    score: float = Field(description="Confidence score between 0 and 1")
    reason: str = Field(description="Brief reason for the classification")

base_parser = PydanticOutputParser(pydantic_object=SentimentResult)

# Wraps the base parser with retry logic
retry_parser = RetryOutputParser.from_llm(
    parser=base_parser,
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    max_retries=3,  # Try up to 3 times to get valid output
)

# The retry parser will re-prompt the model with the error if parsing fails
# This dramatically reduces runtime failures in production
```

> **Production Tip:** Always use structured output approaches (`with_structured_output` or Pydantic parsers) for any pipeline where you need consistent data. Raw string parsing breaks silently in production.

---

### ✅ Chapter 1 Summary

| Concept | What It Is | When To Use |
|---------|-----------|-------------|
| `ChatOpenAI` | Wrapper around OpenAI's chat API | Most production apps |
| `SystemMessage` | Instructions to the model | Always — define the AI's role |
| `HumanMessage` | User's message | Building conversation history |
| `ChatPromptTemplate` | Reusable parameterized prompt | All prompt definitions |
| `MessagesPlaceholder` | Slot for dynamic message history | Conversational apps |
| `FewShotChatMessagePromptTemplate` | Examples-in-prompt | Classification, extraction tasks |
| `PydanticOutputParser` | Parse to typed objects | Structured data extraction |
| `with_structured_output()` | Native structured output | OpenAI/Anthropic models |

---

### 🏗️ Project 1: Text Analysis Pipeline

Build a complete text analysis system that extracts structured information from news articles:

```python
"""
Project 1: News Article Analyzer
Extracts: title, topic, sentiment, key entities, summary, credibility score
"""
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

class ArticleAnalysis(BaseModel):
    title: str = Field(description="Article headline")
    main_topic: str = Field(description="Primary topic in one phrase")
    sentiment: str = Field(description="Overall tone: positive, negative, or neutral")
    sentiment_score: float = Field(description="Sentiment confidence 0.0-1.0")
    key_entities: List[str] = Field(description="People, organizations, places mentioned")
    summary: str = Field(description="2-3 sentence summary")
    is_opinion: bool = Field(description="True if this is opinion/editorial, False if news")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(ArticleAnalysis)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert media analyst. Analyze news articles precisely and objectively."),
    ("human", "Analyze this article:\n\n{article}"),
])

chain = prompt | llm

# Test with sample text
sample_article = """
Tech Giant Announces Layoffs Affecting 12,000 Employees

Silicon Valley — In a surprising move that sent shockwaves through the technology sector,
MegaTech Corp announced today that it would be laying off approximately 12,000 workers,
representing about 6% of its global workforce. CEO John Smith cited "economic headwinds"
and "the need to refocus on core business priorities" as the primary drivers.

The announcement comes amid broader industry turbulence, with several major companies
having already reduced their headcount this year. Shares of MegaTech rose 3% following
the announcement, a reaction that critics argue prioritizes shareholder returns over
employee welfare.
"""

result = chain.invoke({"article": sample_article})
print(f"Topic: {result.main_topic}")
print(f"Sentiment: {result.sentiment} ({result.sentiment_score:.0%} confidence)")
print(f"Entities: {', '.join(result.key_entities)}")
print(f"Is opinion piece: {result.is_opinion}")
print(f"\nSummary: {result.summary}")
```

**Exercise:** Extend this to analyze a list of articles and generate a daily briefing report sorted by topic.

---

# Step 2: LCEL — LangChain Expression Language

## 2.1 Pipe Syntax & Runnable Data Flow

### What is LCEL?

LCEL (LangChain Expression Language) is the modern way to compose LangChain components into pipelines. It uses Python's **pipe operator** (`|`) to connect components.

**Before LCEL (old way):**
```python
# Old approach: verbose, harder to read
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run({"input": "..."})
# Problems: hard to compose, no streaming, limited customization
```

**With LCEL (modern way):**
```python
# Modern approach: composable, readable, powerful
chain = prompt | llm | parser
result = chain.invoke({"input": "..."})
```

### The Runnable Interface

**Every component in LangChain implements the `Runnable` interface.** This is the core abstraction that makes LCEL work.

```
┌─────────────────────────────────────────────────────────────────┐
│                    RUNNABLE INTERFACE                           │
│                                                                 │
│  Any component that has:                                        │
│  • invoke(input)  → synchronous execution                       │
│  • ainvoke(input) → async execution                             │
│  • stream(input)  → streaming output                            │
│  • batch(inputs)  → parallel batch processing                   │
│                                                                 │
│  ChatPromptTemplate  → Runnable ✓                               │
│  ChatOpenAI          → Runnable ✓                               │
│  StrOutputParser     → Runnable ✓                               │
│  Your custom lambda  → Runnable ✓ (via RunnableLambda)          │
└─────────────────────────────────────────────────────────────────┘
```

When you use the pipe operator `|`, LangChain creates a `RunnableSequence` — a chain where the output of each step becomes the input of the next:

```
Input Dict → Prompt Template → Messages → LLM → AIMessage → Parser → String
            [formats prompt]           [generates]        [extracts text]
```

### Type Flow Through a Chain

Understanding what type flows between components prevents confusion:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    ("human", "{question}"),
])
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Data flow:
# {"question": "..."} → (prompt) → [SystemMessage, HumanMessage] → (llm) → AIMessage → (parser) → "string"

chain = prompt | llm | parser

# All of these work identically:
chain.invoke({"question": "What color is the sky?"})

# You can also invoke individual steps:
messages = prompt.invoke({"question": "What color is the sky?"})
print(messages)  # ChatPromptValue with messages list

ai_message = llm.invoke(messages)
print(ai_message)  # AIMessage(content="The sky is blue.")

text = parser.invoke(ai_message)
print(text)  # "The sky is blue."
```

### A Complete, Real-World LCEL Chain

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Code review chain
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior Python developer conducting a code review.
Provide feedback in this exact format:

## Issues Found
[List issues with severity: CRITICAL / WARNING / SUGGESTION]

## Positive Aspects
[List what's done well]

## Refactored Version
[Provide improved code if needed]"""),
    ("human", "Review this Python code:\n\n```python\n{code}\n```"),
])

llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
parser = StrOutputParser()

code_reviewer = prompt | llm | parser

# Use it
sample_code = """
def get_user_data(id):
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + str(id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result
"""

feedback = code_reviewer.invoke({"code": sample_code})
print(feedback)
```

---

## 2.2 Standard Runnable Methods

Every LCEL chain exposes these five methods:

### `invoke()` — Synchronous Single Input

```python
# Blocks until complete, returns single result
result = chain.invoke({"question": "What is Python?"})
print(result)  # String (if parser is StrOutputParser)
```

### `ainvoke()` — Asynchronous Single Input

```python
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
llm = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | llm | StrOutputParser()

async def main():
    # Non-blocking — other code can run while waiting
    result = await chain.ainvoke({"topic": "programming"})
    print(result)
    
    # Run multiple chains concurrently
    topics = ["cats", "mathematics", "coffee"]
    tasks = [chain.ainvoke({"topic": t}) for t in topics]
    results = await asyncio.gather(*tasks)
    for topic, joke in zip(topics, results):
        print(f"{topic}: {joke}\n")

asyncio.run(main())
```

### `stream()` — Token Streaming

Streaming lets you display output as it's generated, creating a much better UX:

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a storyteller."),
    ("human", "Tell me a short story about {topic}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)
chain = prompt | llm | StrOutputParser()

# Stream the response token by token
print("Story: ", end="", flush=True)
for chunk in chain.stream({"topic": "a robot learning to paint"}):
    print(chunk, end="", flush=True)
print()  # New line when done
```

### `astream()` — Async Streaming

```python
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

chain = (
    ChatPromptTemplate.from_template("Explain {concept} in 3 paragraphs.")
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

async def stream_response():
    async for chunk in chain.astream({"concept": "machine learning"}):
        print(chunk, end="", flush=True)
    print()

asyncio.run(stream_response())
```

### `batch()` — Process Multiple Inputs

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

chain = (
    ChatPromptTemplate.from_template("Translate '{text}' to {language}.")
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

# Process all inputs concurrently (much faster than sequential invoke)
inputs = [
    {"text": "Hello", "language": "Spanish"},
    {"text": "Hello", "language": "French"},
    {"text": "Hello", "language": "Japanese"},
    {"text": "Hello", "language": "German"},
    {"text": "Hello", "language": "Arabic"},
]

results = chain.batch(inputs, config={"max_concurrency": 5})
for inp, result in zip(inputs, results):
    print(f"{inp['language']}: {result}")

# Output:
# Spanish: Hola
# French: Bonjour
# Japanese: こんにちは
# German: Hallo
# Arabic: مرحبا
```

---

## 2.3 Advanced Runnables

### RunnablePassthrough — Pass Input Unchanged

Use this when you need to pass the original input alongside transformed data:

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Useful for combining original input with retrieved context in RAG
# The input dict passes through to be available later in the chain

# Example: Augment context while keeping original question
def get_context(input_dict):
    """Simulate document retrieval"""
    query = input_dict["question"]
    # In real RAG, this would search a vector store
    return f"[Context: Python was created by Guido van Rossum in 1991]"

from langchain_core.runnables import RunnableLambda

rag_chain = (
    {
        "context": RunnableLambda(get_context),  # Add retrieved context
        "question": RunnablePassthrough(),        # Keep original question
    }
    | ChatPromptTemplate.from_messages([
        ("system", "Answer using this context: {context}"),
        ("human", "{question}"),
    ])
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

# Works but let's see RunnableParallel for a cleaner version
```

### RunnableParallel — Execute Multiple Chains Simultaneously

```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Two separate analysis chains that run in parallel
pros_chain = (
    ChatPromptTemplate.from_template("List 3 pros of: {topic}")
    | llm
    | StrOutputParser()
)

cons_chain = (
    ChatPromptTemplate.from_template("List 3 cons of: {topic}")
    | llm
    | StrOutputParser()
)

# Run both chains at the same time (concurrent, not sequential)
parallel_chain = RunnableParallel(
    pros=pros_chain,
    cons=cons_chain,
    topic=RunnablePassthrough(),  # Pass original input through too
)

result = parallel_chain.invoke({"topic": "working from home"})
print("Topic:", result["topic"])
print("\nPros:", result["pros"])
print("\nCons:", result["cons"])
```

### RunnableLambda — Wrap Any Python Function

This is the escape hatch that lets you include arbitrary Python logic in your chains:

```python
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import re

load_dotenv()

# Any function can become a Runnable
def extract_keywords(text: str) -> dict:
    """Extract keywords using simple heuristics (not AI)"""
    words = text.lower().split()
    stopwords = {"the", "a", "an", "is", "are", "was", "were", "i", "you", "he", "she"}
    keywords = [w for w in words if w not in stopwords and len(w) > 3]
    return {"text": text, "keywords": keywords[:5]}

def format_for_analysis(data: dict) -> str:
    """Format the extracted data"""
    return f"Text: {data['text']}\nKey terms: {', '.join(data['keywords'])}"

# Build a chain that mixes Python logic and AI
analysis_chain = (
    RunnableLambda(extract_keywords)       # Pure Python preprocessing
    | RunnableLambda(format_for_analysis)  # More Python formatting
    | ChatPromptTemplate.from_template(
        "Analyze this text and its key terms:\n{text}\n\nProvide sentiment and main theme."
    )
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

# Note: ChatPromptTemplate expects a dict input, but we're passing a string
# Fix: adjust the format_for_analysis to return a proper dict
def format_for_prompt(data: dict) -> dict:
    return {"text": f"Text: {data['text']}\nKey terms: {', '.join(data['keywords'])}"}

analysis_chain = (
    RunnableLambda(extract_keywords)
    | RunnableLambda(format_for_prompt)
    | ChatPromptTemplate.from_template("Analyze this:\n{text}")
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

result = analysis_chain.invoke("The revolutionary new AI model has transformed how developers build software applications.")
print(result)
```

### RunnableBranch — Conditional Routing

Route to different chains based on input content:

```python
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define specialized chains for different topics
technical_chain = (
    ChatPromptTemplate.from_template(
        "Answer this technical question with code examples where relevant:\n{question}"
    )
    | llm
    | StrOutputParser()
)

business_chain = (
    ChatPromptTemplate.from_template(
        "Answer this business question with practical, actionable advice:\n{question}"
    )
    | llm
    | StrOutputParser()
)

general_chain = (
    ChatPromptTemplate.from_template("Answer this question helpfully:\n{question}")
    | llm
    | StrOutputParser()
)

# Router function — determines which branch to take
def is_technical(input_dict: dict) -> bool:
    technical_keywords = ["code", "function", "algorithm", "api", "database", "python", "error", "bug"]
    question = input_dict.get("question", "").lower()
    return any(kw in question for kw in technical_keywords)

def is_business(input_dict: dict) -> bool:
    business_keywords = ["revenue", "market", "customer", "sales", "strategy", "roi", "profit"]
    question = input_dict.get("question", "").lower()
    return any(kw in question for kw in business_keywords)

# Build the routing logic
branch = RunnableBranch(
    (is_technical, technical_chain),   # If technical → technical_chain
    (is_business, business_chain),     # If business → business_chain
    general_chain,                      # Default → general_chain
)

# Test with different questions
questions = [
    {"question": "How do I fix a Python IndexError?"},
    {"question": "How should I price my SaaS product for enterprise customers?"},
    {"question": "What's the weather like in Tokyo?"},
]

for q in questions:
    print(f"Q: {q['question']}")
    print(f"A: {branch.invoke(q)[:100]}...")
    print()
```

---

### ✅ Chapter 2 Summary

| Concept | Purpose |
|---------|---------|
| LCEL pipe (`\|`) | Compose components into a pipeline |
| `invoke()` | Sync single execution |
| `ainvoke()` | Async single execution |
| `stream()` | Token-by-token output |
| `batch()` | Parallel processing of multiple inputs |
| `RunnablePassthrough` | Pass input unchanged to output |
| `RunnableParallel` | Run multiple chains concurrently |
| `RunnableLambda` | Wrap any Python function as Runnable |
| `RunnableBranch` | Conditional routing between chains |

---

# Step 3: Data Ingestion & Storage

## 3.1 Document Loaders

### The Data Ingestion Problem

AI applications need to work with your data. But your data exists in dozens of different formats:

```
PDFs     →  Reports, contracts, research papers
CSVs     →  Spreadsheets, datasets, logs
Word     →  Documentation, policies
HTML     →  Web pages, wikis
Markdown →  READMEs, docs
Text     →  Logs, notes, articles
JSON     →  API responses, structured data
PowerPoint → Presentations
Databases → SQL tables
```

LangChain's **Document Loaders** provide a unified interface that reads any format and outputs a standard `Document` object.

**The `Document` Object:**
```python
from langchain_core.documents import Document

doc = Document(
    page_content="This is the text content of the document chunk.",
    metadata={
        "source": "annual_report_2024.pdf",
        "page": 3,
        "author": "Finance Team",
        "created_at": "2024-01-15",
    }
)

print(doc.page_content)  # The actual text
print(doc.metadata)      # Information ABOUT the text
```

Metadata is crucial — it lets you filter retrievals by source, date, author, etc.

### Text & File Loaders

```python
from langchain_community.document_loaders import (
    TextLoader,
    CSVLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    JSONLoader,
)

# ─────────────────────────────────────────
# Text file
# ─────────────────────────────────────────
loader = TextLoader("./my_document.txt", encoding="utf-8")
docs = loader.load()
print(f"Loaded {len(docs)} document(s)")
print(docs[0].page_content[:200])

# ─────────────────────────────────────────
# CSV file — each row becomes a Document
# ─────────────────────────────────────────
loader = CSVLoader(
    file_path="./customers.csv",
    csv_args={"delimiter": ","},
    metadata_columns=["customer_id", "signup_date"],  # These go to metadata
)
docs = loader.load()
# Each doc's page_content will be all column values
# Specified columns also appear in metadata for filtering

# ─────────────────────────────────────────
# PDF — each page becomes a Document
# ─────────────────────────────────────────
loader = PyPDFLoader("./research_paper.pdf")
docs = loader.load()
print(f"PDF has {len(docs)} pages")
for i, doc in enumerate(docs[:3]):
    print(f"Page {i+1}: {len(doc.page_content)} characters")
    print(f"Metadata: {doc.metadata}")  # Includes page number, source

# ─────────────────────────────────────────
# JSON with jq-style path selection
# ─────────────────────────────────────────
loader = JSONLoader(
    file_path="./articles.json",
    jq_schema=".articles[].content",     # Extract the 'content' field of each article
    metadata_func=lambda record, i: {    # Custom metadata function
        "title": record.get("title", ""),
        "author": record.get("author", ""),
    }
)
docs = loader.load()
```

### Web & URL Loaders

```python
from langchain_community.document_loaders import WebBaseLoader
import bs4

# ─────────────────────────────────────────
# Load a single web page
# ─────────────────────────────────────────
loader = WebBaseLoader("https://en.wikipedia.org/wiki/Python_(programming_language)")
docs = loader.load()
print(docs[0].page_content[:500])

# ─────────────────────────────────────────
# Load with specific HTML element extraction
# ─────────────────────────────────────────
loader = WebBaseLoader(
    web_paths=("https://docs.python.org/3/tutorial/",),
    bs_kwargs={
        "parse_only": bs4.SoupStrainer(
            class_=("body", "section")  # Only extract content from these CSS classes
        )
    },
)
docs = loader.load()

# ─────────────────────────────────────────
# Load multiple URLs
# ─────────────────────────────────────────
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]
loader = WebBaseLoader(urls)
docs = loader.load()  # One document per URL
```

### Directory Loaders

```python
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader

# ─────────────────────────────────────────
# Load all .txt files in a directory
# ─────────────────────────────────────────
loader = DirectoryLoader(
    path="./docs",           # Directory to scan
    glob="**/*.txt",         # Pattern to match (recursive)
    loader_cls=TextLoader,   # Which loader to use per file
    show_progress=True,      # Progress bar
    use_multithreading=True, # Parallel loading (faster)
    max_concurrency=8,       # Thread pool size
)
docs = loader.load()
print(f"Loaded {len(docs)} text files")

# ─────────────────────────────────────────
# Load all PDFs in a directory
# ─────────────────────────────────────────
loader = DirectoryLoader(
    path="./reports",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
    use_multithreading=True,
)
docs = loader.load()
```

---

## 3.2 Chunking Strategies & Text Splitters

### Why Chunk at All?

You just loaded a 300-page PDF. Should you embed it as one giant document?

**Problems with giant documents:**
1. **Context window limits:** Models can't process unlimited text. A 300-page PDF is ~150,000 tokens — too big for many models.
2. **Retrieval precision:** If the document is one chunk, every question retrieves the entire 300 pages. The answer you need is on page 47, but you get everything.
3. **Embedding quality:** Embedding 150,000 tokens into one vector loses specificity. The vector becomes an average of everything.

**The solution: Chunk into smaller, semantically coherent pieces.**

```
300-page PDF
    ↓ Chunk
[Chunk 1: pages 1-2] [Chunk 2: pages 2-3] [Chunk 3: pages 3-4] ...
    ↓ Embed
[Vector 1] [Vector 2] [Vector 3] ...
    ↓ Query: "What was Q3 revenue?"
    ↓ Find most similar vectors
[Chunk 47: Contains Q3 revenue discussion] ← Retrieved
```

### CharacterTextSplitter

Splits by a character (default: `\n\n`):

```python
from langchain_text_splitters import CharacterTextSplitter

text = """Introduction
Welcome to this guide on Python programming.

Chapter 1: Variables
Variables store data values. Python has no command for declaring a variable.

Chapter 2: Data Types
Python has various built-in data types including integers, floats, and strings."""

splitter = CharacterTextSplitter(
    separator="\n\n",   # Split on double newlines (paragraph breaks)
    chunk_size=200,      # Maximum characters per chunk
    chunk_overlap=20,    # Characters to overlap between adjacent chunks
    length_function=len, # How to measure chunk length
)

chunks = splitter.create_documents([text])
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} ({len(chunk.page_content)} chars):")
    print(chunk.page_content[:100])
    print("---")
```

### RecursiveCharacterTextSplitter (Recommended Default)

This is the **most commonly used splitter** and should be your default choice. It tries multiple separators in order, falling back to smaller splits only when necessary:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    # Tries these separators in order until chunk is small enough:
    separators=[
        "\n\n",    # Paragraph breaks (most preferred — preserve structure)
        "\n",      # Line breaks
        ". ",      # Sentence boundaries
        ", ",      # Clause boundaries
        " ",       # Word boundaries
        "",        # Character-level (last resort)
    ],
    chunk_size=1000,     # Target chunk size in characters
    chunk_overlap=200,   # Overlap to maintain context across boundaries
    length_function=len,
    is_separator_regex=False,
)

# Split a long document
with open("my_long_document.txt", "r") as f:
    text = f.read()

chunks = splitter.create_documents(
    texts=[text],
    metadatas=[{"source": "my_long_document.txt"}]  # Metadata carries over
)

print(f"Split into {len(chunks)} chunks")
print(f"Avg chunk size: {sum(len(c.page_content) for c in chunks) / len(chunks):.0f} chars")
```

**Why overlap matters:**

```
Without overlap:
[...Python is great for data science.] [Machine learning is a subfield...]
                                       ↑ Context break: "data science" and "machine learning"
                                         might be connected but are now split

With overlap=100:
[...Python is great for data science.] [data science. Machine learning is a subfield...]
                                       ↑ The connection context is preserved in both chunks
```

### Token-Based Splitting

For models that charge by token, split by token count instead of character count:

```python
from langchain_text_splitters import TokenTextSplitter

# Split based on actual token count
splitter = TokenTextSplitter(
    chunk_size=256,    # Tokens per chunk
    chunk_overlap=20,  # Token overlap
    model_name="gpt-4o",  # Use this model's tokenizer
)

chunks = splitter.create_documents([long_text])
```

### Markdown & HTML Splitters

Structure-aware splitters that preserve semantic meaning:

```python
from langchain_text_splitters import MarkdownTextSplitter, HTMLHeaderTextSplitter

# ─────────────────────────────────────────
# Markdown: splits at heading boundaries
# ─────────────────────────────────────────
markdown_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)

markdown_text = """
# Introduction
Overview of the system architecture.

## Component A
Details about component A.

### Sub-component A1
Detailed technical specifications.

## Component B
Details about component B.
"""

chunks = markdown_splitter.create_documents([markdown_text])
# Chunks will respect heading hierarchy

# ─────────────────────────────────────────
# HTML: splits at header tags, adds them to metadata
# ─────────────────────────────────────────
html_splitter = HTMLHeaderTextSplitter(
    headers_to_split_on=[
        ("h1", "Header 1"),
        ("h2", "Header 2"),
        ("h3", "Header 3"),
    ]
)

html_text = "<h1>Guide</h1><p>Intro...</p><h2>Installation</h2><p>Steps...</p>"
chunks = html_splitter.split_text(html_text)
# Each chunk's metadata includes the parent headers:
# {'Header 1': 'Guide', 'Header 2': 'Installation'}
```

### Chunk Size Selection Guide

| Content Type | Recommended Chunk Size | Overlap |
|-------------|----------------------|---------|
| Short facts / Q&A | 256-512 tokens | 50 tokens |
| Narrative text / articles | 512-1024 tokens | 100-200 tokens |
| Technical docs / code | 512-1024 tokens | 100 tokens |
| Legal / contracts | 1024-2048 tokens | 200 tokens |
| Conversation logs | 256-512 tokens | 100 tokens |

> **Production Rule of Thumb:** Start with `chunk_size=1000, chunk_overlap=200` and tune from there based on retrieval quality.

---

## 3.3 Embeddings & Vector Stores

### What is an Embedding?

An **embedding** is a way to convert text into a list of numbers (a vector) that captures its semantic meaning.

**Mental Model:** Imagine a vast coordinate space with thousands of dimensions. Every sentence, paragraph, or document can be placed at a specific point in this space. Texts with similar meanings end up close together; unrelated texts end up far apart.

```
"The cat sat on the mat"     → [0.23, -0.45, 0.12, 0.89, ...]  (1536 numbers)
"A feline rested on a rug"   → [0.21, -0.43, 0.11, 0.87, ...]  (similar values!)
"The stock market crashed"   → [-0.67, 0.23, -0.44, 0.02, ...]  (very different)
```

When you query "Where did the cat go?", you embed the query into a vector and find the document vectors closest to it — that's semantic search.

### Embedding Models

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings, OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────
# OpenAI Embeddings (best quality, costs money)
# ─────────────────────────────────────────
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # 1536 dimensions, cheap
    # model="text-embedding-3-large" # 3072 dimensions, better quality
)

# Embed a single text
vector = embeddings.embed_query("What is machine learning?")
print(f"Vector dimension: {len(vector)}")   # 1536
print(f"First 5 values: {vector[:5]}")      # [-0.02, 0.04, -0.01, ...]

# Embed multiple documents (more efficient than one-by-one)
vectors = embeddings.embed_documents([
    "Machine learning is a type of AI.",
    "Python is a programming language.",
    "The sky is blue.",
])
print(f"Embedded {len(vectors)} documents")

# ─────────────────────────────────────────
# HuggingFace Embeddings (free, local, good quality)
# ─────────────────────────────────────────
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",  # 384 dims, fast
    # model_name="sentence-transformers/all-mpnet-base-v2" # 768 dims, better
    model_kwargs={"device": "cpu"},  # or "cuda" if you have GPU
    encode_kwargs={"normalize_embeddings": True},  # Normalize for cosine similarity
)
```

**Embedding Model Comparison:**

| Model | Dimensions | Speed | Quality | Cost |
|-------|-----------|-------|---------|------|
| `text-embedding-3-small` | 1536 | Fast | Excellent | ~$0.02/1M tokens |
| `text-embedding-3-large` | 3072 | Medium | Best | ~$0.13/1M tokens |
| `all-MiniLM-L6-v2` (HF) | 384 | Very Fast | Good | Free (local) |
| `all-mpnet-base-v2` (HF) | 768 | Fast | Very Good | Free (local) |
| `nomic-embed-text` (Ollama) | 768 | Medium | Good | Free (local) |

### FAISS — Local In-Memory Vector Store

FAISS (Facebook AI Similarity Search) is fast, runs locally, and is perfect for development and medium-scale production:

```python
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# ─────────────────────────────────────────
# Create from documents
# ─────────────────────────────────────────
documents = [
    Document(page_content="Python was created by Guido van Rossum.", 
             metadata={"source": "python_history.txt", "year": 1991}),
    Document(page_content="Python 3 was released in 2008.", 
             metadata={"source": "python_history.txt", "year": 2008}),
    Document(page_content="FastAPI is a modern web framework for Python.", 
             metadata={"source": "frameworks.txt"}),
    Document(page_content="Django is a full-stack Python web framework.", 
             metadata={"source": "frameworks.txt"}),
    Document(page_content="NumPy provides numerical computing for Python.", 
             metadata={"source": "libraries.txt"}),
]

# This will call the embedding API to embed all documents
vector_store = FAISS.from_documents(documents, embeddings)

# ─────────────────────────────────────────
# Similarity search
# ─────────────────────────────────────────
results = vector_store.similarity_search(
    query="Who invented Python?",
    k=2,  # Return top 2 most similar documents
)
for doc in results:
    print(f"Content: {doc.page_content}")
    print(f"Source: {doc.metadata['source']}")
    print()

# Search with scores (lower = more similar for L2; higher for cosine)
results_with_scores = vector_store.similarity_search_with_score(
    query="web frameworks for Python",
    k=3,
)
for doc, score in results_with_scores:
    print(f"Score: {score:.4f} | Content: {doc.page_content[:80]}")

# ─────────────────────────────────────────
# Save and load (persist to disk)
# ─────────────────────────────────────────
vector_store.save_local("./faiss_index")

# Later, reload without re-embedding
loaded_vs = FAISS.load_local(
    "./faiss_index", 
    embeddings,
    allow_dangerous_deserialization=True,  # Required flag for security awareness
)
```

### Chroma — Developer-Friendly Persistent Store

Chroma is great for development and moderate-scale production:

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# ─────────────────────────────────────────
# Create a persistent Chroma store
# ─────────────────────────────────────────
vector_store = Chroma(
    collection_name="my_documents",
    embedding_function=embeddings,
    persist_directory="./chroma_db",  # Automatically persists to disk
)

# ─────────────────────────────────────────
# Add documents from a PDF
# ─────────────────────────────────────────
loader = PyPDFLoader("./my_document.pdf")
raw_docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(raw_docs)

# Batch add (handles API rate limits automatically)
vector_store.add_documents(chunks)
print(f"Added {len(chunks)} chunks to Chroma")

# ─────────────────────────────────────────
# Search with metadata filtering
# ─────────────────────────────────────────
results = vector_store.similarity_search(
    query="quarterly revenue figures",
    k=5,
    filter={"page": 3},  # Only search page 3
)

# ─────────────────────────────────────────
# Get as a retriever (for use in chains)
# ─────────────────────────────────────────
retriever = vector_store.as_retriever(
    search_type="similarity",   # or "mmr" (Maximal Marginal Relevance)
    search_kwargs={
        "k": 5,
        "filter": {"source": "annual_report_2024.pdf"},
    }
)
```

### Pinecone — Production-Scale Vector Database

For production systems with millions of documents:

```bash
pip install pinecone-client langchain-pinecone
```

```python
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create an index (one-time setup)
index_name = "my-rag-index"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Must match embedding dimension
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Use with LangChain
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = PineconeVectorStore(
    index=pc.Index(index_name),
    embedding=embeddings,
    text_key="text",      # Field name for the document text
    namespace="default",  # Namespace for multi-tenancy
)

# All standard LangChain vector store operations work
vector_store.add_documents(documents)
results = vector_store.similarity_search("your query", k=5)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
```

**Vector Database Comparison:**

| Database | Best For | Hosting | Scale | Special Features |
|----------|---------|---------|-------|-----------------|
| FAISS | Development, prototyping | Local | <10M vectors | Extremely fast |
| Chroma | Development, small prod | Local/Docker | <1M vectors | Easy setup |
| Pinecone | Production SaaS | Cloud (managed) | Billions | Serverless, filtering |
| Qdrant | Production | Self/Cloud | Billions | Advanced filtering |
| Weaviate | Enterprise | Self/Cloud | Billions | GraphQL, multimodal |
| pgvector | Existing PostgreSQL users | Self | Millions | SQL integration |

---

## 3.4 The Indexing API

### The Problem: Duplicate Embeddings

Every time you run your ingestion pipeline, you risk embedding the same documents multiple times:

```
First run: Embed all 10,000 docs → Stored in vector DB ✓
Add 50 new docs, re-run pipeline:
  - Re-embeds all 10,000 existing docs (expensive!)
  - Plus the 50 new ones
  - Creates duplicates in vector DB
  - Search results now have duplicate chunks
```

The **Indexing API** with `RecordManager` solves this by tracking what's been indexed.

```python
from dotenv import load_dotenv
from langchain.indexes import SQLRecordManager, index
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Chroma(
    collection_name="indexed_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_indexed",
)

# RecordManager tracks which documents have been indexed
record_manager = SQLRecordManager(
    namespace="chroma/indexed_docs",
    db_url="sqlite:///record_manager_cache.sql",
)
record_manager.create_schema()  # Initialize the tracking table

# ─────────────────────────────────────────
# First indexing run
# ─────────────────────────────────────────
docs_v1 = [
    Document(page_content="Python was created in 1991.", metadata={"source": "python.txt"}),
    Document(page_content="Python is widely used for data science.", metadata={"source": "python.txt"}),
    Document(page_content="FastAPI is built on Starlette.", metadata={"source": "fastapi.txt"}),
]

result = index(
    docs_v1,
    record_manager,
    vector_store,
    cleanup="incremental",  # Only add new, delete removed
    source_id_key="source",  # Use 'source' metadata to identify documents
)
print(result)
# {'num_added': 3, 'num_updated': 0, 'num_skipped': 0, 'num_deleted': 0}

# ─────────────────────────────────────────
# Second run — same documents
# ─────────────────────────────────────────
result = index(docs_v1, record_manager, vector_store, cleanup="incremental", source_id_key="source")
print(result)
# {'num_added': 0, 'num_updated': 0, 'num_skipped': 3, 'num_deleted': 0}
# ← All 3 skipped because they haven't changed! No API calls made.

# ─────────────────────────────────────────
# Third run — add new doc, modify existing
# ─────────────────────────────────────────
docs_v2 = [
    Document(page_content="Python was created in 1991 by Guido van Rossum.", 
             metadata={"source": "python.txt"}),        # ← Modified
    Document(page_content="Python is widely used for data science.", 
             metadata={"source": "python.txt"}),        # ← Same
    Document(page_content="FastAPI is built on Starlette.", 
             metadata={"source": "fastapi.txt"}),       # ← Same
    Document(page_content="Pydantic handles data validation.", 
             metadata={"source": "pydantic.txt"}),      # ← New
]

result = index(docs_v2, record_manager, vector_store, cleanup="incremental", source_id_key="source")
print(result)
# {'num_added': 2, 'num_updated': 0, 'num_skipped': 2, 'num_deleted': 1}
# ← Added 1 new + 1 modified (as new), deleted old version of modified, skipped 2 unchanged
```

> **Production Tip:** Always use the Indexing API in production. Without it, re-running your pipeline wastes money on re-embedding and pollutes your vector store with duplicates.

---

### 🏗️ Project 2: PDF Knowledge Base

Build a complete document ingestion system for a collection of PDFs:

```python
"""
Project 2: PDF Knowledge Base Builder
Loads a directory of PDFs, chunks them intelligently, embeds them,
and stores them with deduplication using the Indexing API.
"""
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.indexes import SQLRecordManager, index

load_dotenv()

def build_knowledge_base(pdf_dir: str, db_dir: str = "./knowledge_base"):
    """
    Build or update a knowledge base from a directory of PDFs.
    Uses the Indexing API to avoid duplicate embeddings.
    """
    print(f"📚 Loading PDFs from {pdf_dir}...")
    
    # Load all PDFs
    loader = DirectoryLoader(
        path=pdf_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
        use_multithreading=True,
    )
    raw_docs = loader.load()
    print(f"   Loaded {len(raw_docs)} pages from PDF files")
    
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", ", ", " ", ""],
    )
    chunks = splitter.split_documents(raw_docs)
    print(f"   Split into {len(chunks)} chunks")
    
    # Set up embedding model and vector store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma(
        collection_name="pdf_knowledge_base",
        embedding_function=embeddings,
        persist_directory=db_dir,
    )
    
    # Set up record manager for deduplication
    record_manager = SQLRecordManager(
        namespace="chroma/pdf_kb",
        db_url=f"sqlite:///{db_dir}/record_manager.sql",
    )
    record_manager.create_schema()
    
    # Index (smart: only embeds new/changed documents)
    print("   Indexing chunks...")
    result = index(
        chunks,
        record_manager,
        vector_store,
        cleanup="incremental",
        source_id_key="source",
    )
    
    print(f"\n✅ Indexing complete:")
    print(f"   Added:   {result['num_added']}")
    print(f"   Updated: {result['num_updated']}")
    print(f"   Skipped: {result['num_skipped']}")
    print(f"   Deleted: {result['num_deleted']}")
    
    return vector_store

def query_knowledge_base(query: str, vector_store, k: int = 5):
    """Search the knowledge base."""
    results = vector_store.similarity_search_with_score(query, k=k)
    print(f"\n🔍 Query: {query}")
    print(f"   Top {k} results:\n")
    for doc, score in results:
        print(f"   Score: {score:.4f}")
        print(f"   Source: {doc.metadata.get('source', 'Unknown')} (page {doc.metadata.get('page', '?')})")
        print(f"   Content: {doc.page_content[:200]}...")
        print()

if __name__ == "__main__":
    # Build/update the knowledge base
    vs = build_knowledge_base("./pdfs")
    
    # Test queries
    query_knowledge_base("What are the main conclusions?", vs)
    query_knowledge_base("What methodology was used?", vs)
```

---

# Step 4: Advanced RAG

## 4.1 Basic RAG via LCEL

### The RAG Pattern

RAG (Retrieval-Augmented Generation) is the most important pattern in production AI engineering. It solves the fundamental problem: **LLMs don't know your private data, but you can teach them in real-time.**

```
┌─────────────────────────────────────────────────────────────────┐
│                     RAG PIPELINE                                │
│                                                                 │
│  User Question                                                  │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                                │
│  │  Retriever  │ ← Searches your knowledge base                 │
│  └──────┬──────┘                                                │
│         │ Returns relevant chunks                               │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                    │
│  │  Prompt = System + Context + Question   │                    │
│  └──────────────────────┬──────────────────┘                    │
│                         │                                       │
│                         ▼                                       │
│                    ┌─────────┐                                  │
│                    │   LLM   │ ← Generates answer using context │
│                    └────┬────┘                                  │
│                         │                                       │
│                         ▼                                       │
│                      Answer                                     │
└─────────────────────────────────────────────────────────────────┘
```

### Building a Basic RAG Chain

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

load_dotenv()

# ─────────────────────────────────────────
# Step 1: Build knowledge base
# ─────────────────────────────────────────
docs = [
    Document(page_content="LangChain is a framework for building LLM applications. It was created by Harrison Chase and released in 2022.", metadata={"source": "langchain_intro.txt"}),
    Document(page_content="LCEL (LangChain Expression Language) allows you to compose chains using the pipe operator (|). It supports streaming, async, and batch processing.", metadata={"source": "lcel_guide.txt"}),
    Document(page_content="LangGraph is a framework for building stateful, multi-actor applications with LLMs. It's built on top of LangChain and enables cyclical workflows.", metadata={"source": "langgraph_intro.txt"}),
    Document(page_content="LangSmith is a platform for debugging, testing, evaluating, and monitoring LLM applications. It provides tracing and observability.", metadata={"source": "langsmith_guide.txt"}),
    Document(page_content="Vector stores save document embeddings and enable semantic search. Common options include FAISS, Chroma, and Pinecone.", metadata={"source": "vector_stores.txt"}),
    Document(page_content="RAG (Retrieval-Augmented Generation) combines retrieval from a knowledge base with LLM generation to answer questions about private data.", metadata={"source": "rag_guide.txt"}),
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_documents(docs, embeddings)

# ─────────────────────────────────────────
# Step 2: Set up retriever
# ─────────────────────────────────────────
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

# ─────────────────────────────────────────
# Step 3: Define the RAG prompt
# ─────────────────────────────────────────
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that answers questions about LangChain.
    
Use the following retrieved context to answer the question. 
If the context doesn't contain enough information to answer, say so.
Always cite which document your answer comes from.

Context:
{context}"""),
    ("human", "{question}"),
])

# ─────────────────────────────────────────
# Step 4: Format retrieved documents
# ─────────────────────────────────────────
def format_docs(docs):
    """Format a list of documents into a single string with source attribution."""
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
        for doc in docs
    )

# ─────────────────────────────────────────
# Step 5: Build the RAG chain
# ─────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

rag_chain = (
    {
        "context": retriever | format_docs,  # Retrieve docs, then format them
        "question": RunnablePassthrough(),   # Pass question through unchanged
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)

# ─────────────────────────────────────────
# Step 6: Use it!
# ─────────────────────────────────────────
questions = [
    "What is LangChain and who created it?",
    "How does LCEL work?",
    "What is RAG and why would I use it?",
    "What is LangSmith used for?",
]

for question in questions:
    print(f"Q: {question}")
    print(f"A: {rag_chain.invoke(question)}")
    print("-" * 80)
```

### RAG with Source Citations

```python
from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

class CitedAnswer(BaseModel):
    """Answer with citations."""
    answer: str = Field(description="The answer to the question")
    citations: List[str] = Field(description="List of source document names cited")
    confidence: float = Field(description="Confidence in the answer, 0.0 to 1.0")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(CitedAnswer)

cited_prompt = ChatPromptTemplate.from_messages([
    ("system", """Answer the question based ONLY on the provided context.
    
Context Documents:
{context}

Return your answer with the specific document sources you cited."""),
    ("human", "{question}"),
])

cited_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | cited_prompt
    | structured_llm
)

result = cited_chain.invoke("What does LangSmith provide?")
print(f"Answer: {result.answer}")
print(f"Citations: {result.citations}")
print(f"Confidence: {result.confidence:.0%}")
```

---

## 4.2 Advanced Retrievers

### MultiQueryRetriever — Overcome Query Limitations

A single query might not capture all relevant aspects of a question. The model might phrase it slightly differently than how documents are written. **MultiQueryRetriever** solves this by generating multiple variations of your query:

```
User Query: "How does memory work in LangChain?"
                    ↓
        LLM generates multiple queries:
        1. "LangChain conversation memory management"
        2. "Chat history persistence in LangChain"
        3. "RunnableWithMessageHistory implementation"
                    ↓
        Search all 3 queries independently
                    ↓
        Deduplicate and combine results
```

```python
from dotenv import load_dotenv
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import logging

load_dotenv()

# Enable logging to see the generated queries (useful for debugging)
logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

# Set up knowledge base
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_documents(docs, embeddings)
base_retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Wrap with MultiQueryRetriever
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm,
    # num_queries=3,  # Default: generates 3 queries
)

# When you invoke this, it:
# 1. Generates 3 variations of your query
# 2. Runs all 3 against the vector store
# 3. Returns deduplicated results
results = multi_query_retriever.invoke("How do I handle conversation history?")
for doc in results:
    print(f"- {doc.page_content[:100]}")
```

### ContextualCompressionRetriever — Filter Irrelevant Content

Retrieved chunks often contain information that's tangentially related but not directly relevant. This retriever compresses/filters the retrieved content:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor, EmbeddingsFilter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# ─────────────────────────────────────────
# Option 1: LLM-based extraction (higher quality, slower)
# ─────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever,
)

# Returns only the relevant portions of retrieved documents
results = compression_retriever.invoke("What is LCEL?")
for doc in results:
    print(f"Compressed content: {doc.page_content}")

# ─────────────────────────────────────────
# Option 2: Embeddings-based filter (faster, cheaper)
# ─────────────────────────────────────────
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
embeddings_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.76)

compression_retriever_fast = ContextualCompressionRetriever(
    base_compressor=embeddings_filter,
    base_retriever=base_retriever,
)
```

### ParentDocumentRetriever — Best of Both Worlds

**The Problem:** Small chunks give precise retrieval but lack context. Large chunks give context but imprecise retrieval.

**The Solution:** Index small chunks for retrieval, but return their parent (larger) chunks for generation.

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Two different splitters: one for parent docs, one for child chunks
parent_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,   # Larger parent chunks
    chunk_overlap=100,
)
child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,    # Smaller child chunks for precise retrieval
    chunk_overlap=50,
)

# Vector store holds the small child embeddings
child_vector_store = Chroma(
    collection_name="child_chunks",
    embedding_function=embeddings,
)

# Document store holds the full parent documents
parent_doc_store = InMemoryStore()  # Use Redis or SQL in production

retriever = ParentDocumentRetriever(
    vectorstore=child_vector_store,
    docstore=parent_doc_store,
    parent_splitter=parent_splitter,
    child_splitter=child_splitter,
)

# Add documents
documents = [Document(page_content="...", metadata={"source": "doc1.txt"})]
retriever.add_documents(documents)

# When you retrieve:
# 1. Query matches small child chunks (precise matching)
# 2. Parent chunks are returned (rich context)
results = retriever.invoke("your question")
```

### SelfQueryRetriever — Natural Language Metadata Filtering

Let the LLM convert natural language queries into structured metadata filters:

```python
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Documents with rich metadata
documents = [
    Document(page_content="Quarterly earnings report shows 15% growth",
             metadata={"source": "Q3_2024_report.pdf", "year": 2024, "quarter": 3, "department": "finance"}),
    Document(page_content="New hiring policy announced for remote workers",
             metadata={"source": "HR_policy_2024.pdf", "year": 2024, "quarter": 1, "department": "hr"}),
    Document(page_content="Product roadmap for 2025 includes AI features",
             metadata={"source": "roadmap_2025.pdf", "year": 2025, "quarter": 1, "department": "product"}),
    Document(page_content="Q2 2024 financial results and forecasts",
             metadata={"source": "Q2_2024_report.pdf", "year": 2024, "quarter": 2, "department": "finance"}),
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Chroma.from_documents(documents, embeddings)

# Describe the metadata fields to the LLM
metadata_field_info = [
    AttributeInfo(
        name="year",
        description="The year the document was created",
        type="integer",
    ),
    AttributeInfo(
        name="quarter",
        description="The fiscal quarter (1, 2, 3, or 4)",
        type="integer",
    ),
    AttributeInfo(
        name="department",
        description="The department that created the document",
        type="string",
    ),
]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

self_query_retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vector_store,
    document_contents="Business documents from various departments",
    metadata_field_info=metadata_field_info,
    verbose=True,  # See the generated filter
)

# The retriever parses natural language into metadata filters
results = self_query_retriever.invoke("Show me only finance department documents from 2024")
# Internally generates: filter = {"year": 2024, "department": "finance"}
for doc in results:
    print(f"{doc.metadata['source']}: {doc.page_content[:80]}")

results = self_query_retriever.invoke("What are the Q3 2024 results?")
# filter = {"year": 2024, "quarter": 3}
```

### EnsembleRetriever — Hybrid Search

Combine multiple retrieval methods for better coverage:

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

documents = [
    Document(page_content="Python is a high-level programming language known for readability."),
    Document(page_content="FastAPI is a modern Python web framework for building APIs."),
    Document(page_content="The pandas library provides data analysis tools for Python."),
    Document(page_content="scikit-learn is a machine learning library for Python."),
]

# BM25: Keyword-based retrieval (good for exact matches)
bm25_retriever = BM25Retriever.from_documents(documents, k=2)

# FAISS: Semantic/embedding-based retrieval (good for meaning)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
faiss_retriever = FAISS.from_documents(documents, embeddings).as_retriever(search_kwargs={"k": 2})

# Ensemble: Combines both with weighted scoring
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever],
    weights=[0.5, 0.5],  # Equal weight; adjust based on your use case
)

# Gets results from both and re-ranks using Reciprocal Rank Fusion
results = ensemble_retriever.invoke("Python web development")
for doc in results:
    print(doc.page_content)
```

> **When to use Hybrid Search:** BM25 catches exact keyword matches (e.g., specific function names, version numbers, technical terms). Semantic search catches conceptual matches (e.g., synonyms, paraphrasing). Combining both gives the best coverage. Use this as your default retriever in production.

---

## 4.3 RAG Optimization

### Retrieval Evaluation

Before optimizing, measure. Define metrics:

```python
"""
RAG Evaluation Framework
Measures: Retrieval Recall, Context Precision, Answer Faithfulness
"""
from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class RAGEvalResult(BaseModel):
    faithfulness_score: float = Field(description="0-1: Is the answer grounded in context?")
    context_relevance: float = Field(description="0-1: How relevant are the retrieved docs?")
    answer_relevance: float = Field(description="0-1: Does the answer address the question?")
    reasoning: str = Field(description="Brief explanation of the scores")

eval_llm = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(RAGEvalResult)

def evaluate_rag_response(
    question: str,
    context_docs: List[str],
    generated_answer: str,
) -> RAGEvalResult:
    """Evaluate a single RAG response."""
    context = "\n\n".join(context_docs)
    
    eval_prompt = f"""Evaluate this RAG (Retrieval-Augmented Generation) response:

QUESTION: {question}

RETRIEVED CONTEXT:
{context}

GENERATED ANSWER: {generated_answer}

Evaluate on three criteria, each scored 0.0 to 1.0:
1. Faithfulness: Is the answer factually grounded in the context? (1.0 = fully grounded)
2. Context Relevance: How relevant is the retrieved context to the question? (1.0 = perfectly relevant)
3. Answer Relevance: How well does the answer address the question? (1.0 = completely answers it)"""
    
    return eval_llm.invoke(eval_prompt)

# Example usage
question = "What is LCEL used for?"
context = ["LCEL (LangChain Expression Language) allows composing chains with the pipe operator."]
answer = "LCEL is used to compose LangChain components into pipelines using the pipe operator."

result = evaluate_rag_response(question, context, answer)
print(f"Faithfulness: {result.faithfulness_score:.0%}")
print(f"Context Relevance: {result.context_relevance:.0%}")
print(f"Answer Relevance: {result.answer_relevance:.0%}")
print(f"Reasoning: {result.reasoning}")
```

### Re-ranking with Cross-Encoders

Vector similarity is fast but imprecise. Cross-encoders re-rank by actually reading both the query and document together:

```bash
pip install sentence-transformers
```

```python
from sentence_transformers import CrossEncoder
from langchain_core.documents import Document
from typing import List

# Cross-encoder models for re-ranking
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_documents(query: str, documents: List[Document], top_k: int = 3) -> List[Document]:
    """
    Re-rank documents using a cross-encoder.
    
    Phase 1 (vector retrieval): Fast, imprecise, retrieves ~10 docs
    Phase 2 (cross-encoder): Slow, precise, re-ranks to top k
    """
    if not documents:
        return []
    
    # Score each document
    pairs = [(query, doc.page_content) for doc in documents]
    scores = reranker.predict(pairs)
    
    # Sort by score (higher = more relevant)
    ranked = sorted(
        zip(scores, documents),
        key=lambda x: x[0],
        reverse=True,
    )
    
    # Return top k
    return [doc for _, doc in ranked[:top_k]]

# Usage in RAG pipeline
def rag_with_reranking(query: str, retriever, top_k_initial=10, top_k_final=3):
    # Phase 1: Fast vector retrieval (get more than you need)
    initial_docs = retriever.invoke(query)
    
    # Phase 2: Precise re-ranking
    reranked_docs = rerank_documents(query, initial_docs, top_k=top_k_final)
    
    return reranked_docs
```

---

## 4.4 Production RAG Architectures

### Streaming RAG

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# Build RAG chain (same as before)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_documents(docs, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer based on this context:\n\n{context}"),
    ("human", "{question}"),
])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

# Stream the response
print("Answer: ", end="", flush=True)
for chunk in rag_chain.stream("What is LangGraph?"):
    print(chunk, end="", flush=True)
print()
```

### Architecture Diagram: Production RAG System

```
┌──────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION RAG ARCHITECTURE                       │
│                                                                      │
│  ┌─────────────┐     ┌─────────────────────────────────────────┐    │
│  │  INGESTION  │     │              QUERY PIPELINE              │    │
│  │   PIPELINE  │     │                                         │    │
│  │             │     │  User Query                             │    │
│  │ Raw Docs    │     │      │                                  │    │
│  │     │       │     │      ▼                                  │    │
│  │  Loaders    │     │  Query Expansion (MultiQuery)           │    │
│  │     │       │     │      │                                  │    │
│  │  Splitters  │     │      ▼                                  │    │
│  │     │       │     │  Hybrid Retrieval (BM25 + Vector)       │    │
│  │  Embeddings │     │      │                                  │    │
│  │     │       │     │      ▼                                  │    │
│  │  Vector DB  │◄────┤  Re-ranking (CrossEncoder)              │    │
│  │             │     │      │                                  │    │
│  └─────────────┘     │      ▼                                  │    │
│                      │  Compression/Filtering                  │    │
│  ┌─────────────┐     │      │                                  │    │
│  │ Record Mgr  │     │      ▼                                  │    │
│  │(No Dupes)   │     │  Context Assembly + Prompt              │    │
│  └─────────────┘     │      │                                  │    │
│                      │      ▼                                  │    │
│  ┌─────────────┐     │     LLM Generation (Streaming)          │    │
│  │ LangSmith   │◄────┤      │                                  │    │
│  │ (Tracing)   │     │      ▼                                  │    │
│  └─────────────┘     │  Cited Answer + Sources                 │    │
│                      └─────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

---

### 🏗️ Project 3: Enterprise RAG Assistant

```python
"""
Project 3: Enterprise RAG Assistant
Full-featured RAG with: hybrid search, re-ranking, streaming, citations
"""
from dotenv import load_dotenv
from typing import AsyncGenerator, List
from pydantic import BaseModel, Field
import asyncio

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

load_dotenv()

class RAGConfig:
    """Centralized configuration for the RAG system."""
    embedding_model = "text-embedding-3-small"
    llm_model = "gpt-4o"
    llm_temperature = 0
    retriever_k_vector = 8
    retriever_k_bm25 = 8
    retriever_k_final = 5
    bm25_weight = 0.4
    vector_weight = 0.6

class EnterpriseRAGAssistant:
    def __init__(self, documents: List[Document], config: RAGConfig = None):
        self.config = config or RAGConfig()
        self._setup(documents)
    
    def _setup(self, documents: List[Document]):
        """Initialize all components."""
        # Embeddings and vector store
        self.embeddings = OpenAIEmbeddings(model=self.config.embedding_model)
        self.vector_store = Chroma.from_documents(documents, self.embeddings)
        
        # Hybrid retriever
        vector_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": self.config.retriever_k_vector}
        )
        bm25_retriever = BM25Retriever.from_documents(
            documents, k=self.config.retriever_k_bm25
        )
        self.retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, vector_retriever],
            weights=[self.config.bm25_weight, self.config.vector_weight],
        )
        
        # LLM
        self.llm = ChatOpenAI(
            model=self.config.llm_model,
            temperature=self.config.llm_temperature,
            streaming=True,
        )
        
        # RAG prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert assistant with access to a knowledge base.

Answer the user's question based ONLY on the retrieved context below.
If the context is insufficient, clearly state what information is missing.

Always:
1. Base your answer strictly on the provided context
2. Cite specific sources using [source_name] format
3. Be concise but complete
4. Indicate confidence level at the end

Retrieved Context:
{context}"""),
            ("human", "{question}"),
        ])
        
        # Build chain
        def format_docs(docs):
            formatted = []
            for i, doc in enumerate(docs[:self.config.retriever_k_final]):
                source = doc.metadata.get('source', f'Document {i+1}')
                formatted.append(f"[{source}]\n{doc.page_content}")
            return "\n\n---\n\n".join(formatted)
        
        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def ask(self, question: str) -> str:
        """Synchronous query."""
        return self.chain.invoke(question)
    
    def ask_stream(self, question: str):
        """Stream the response token by token."""
        for chunk in self.chain.stream(question):
            yield chunk
    
    async def ask_async(self, question: str) -> str:
        """Async query for concurrent requests."""
        return await self.chain.ainvoke(question)
    
    def get_sources(self, question: str) -> List[Document]:
        """Get the source documents for a query."""
        return self.retriever.invoke(question)[:self.config.retriever_k_final]


# Usage
sample_docs = [
    Document(page_content="Q3 2024 revenue was $125M, up 23% YoY. Key drivers: enterprise growth (+45%) and international expansion (+18%).", metadata={"source": "Q3_2024_earnings.pdf"}),
    Document(page_content="The new product launch is scheduled for Q1 2025. Initial beta users report 95% satisfaction rate.", metadata={"source": "product_roadmap.pdf"}),
    Document(page_content="Employee headcount reached 2,300 globally. Engineering team grew by 30% with focus on AI capabilities.", metadata={"source": "hr_report_2024.pdf"}),
]

assistant = EnterpriseRAGAssistant(sample_docs)

# Streaming usage
print("Streaming response:")
for chunk in assistant.ask_stream("What was our Q3 performance?"):
    print(chunk, end="", flush=True)
print("\n")

# Async usage for high-throughput
async def batch_queries():
    questions = [
        "What drove revenue growth?",
        "When is the new product launching?",
        "How has the team grown?",
    ]
    tasks = [assistant.ask_async(q) for q in questions]
    answers = await asyncio.gather(*tasks)
    for q, a in zip(questions, answers):
        print(f"Q: {q}\nA: {a}\n")

asyncio.run(batch_queries())
```

---

# Step 5: Memory & Conversational State

## 5.1 Chat History

### The Statefulness Problem

Every API call to an LLM is stateless. The model has no memory of previous calls. For a chatbot to work, you must manually include conversation history in every request.

```
Request 1: [User: "My name is Alex"] → Response: "Hi Alex!"
Request 2: [User: "What's my name?"] → Response: "I don't know your name"  ❌

Correct:
Request 2: [User: "My name is Alex", AI: "Hi Alex!", User: "What's my name?"]
         → Response: "Your name is Alex"  ✓
```

LangChain provides storage backends for persisting this history.

### ChatMessageHistory

```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

# In-memory history (lost when process exits)
history = ChatMessageHistory()

# Add messages
history.add_user_message("My name is Sarah.")
history.add_ai_message("Nice to meet you, Sarah!")
history.add_user_message("I work in data science.")
history.add_ai_message("That's a fascinating field!")

print(history.messages)
# [HumanMessage(content='My name is Sarah.'), AIMessage(content='Nice to meet you, Sarah!'), ...]

# Clear history
history.clear()
```

### Redis-Backed Persistent History

```bash
pip install redis langchain-community
# Also need a running Redis instance:
# docker run -d -p 6379:6379 redis
```

```python
from langchain_community.chat_message_histories import RedisChatMessageHistory

# Messages persist in Redis across sessions
def get_session_history(session_id: str):
    return RedisChatMessageHistory(
        session_id=session_id,
        url="redis://localhost:6379",
        ttl=3600,  # Expire sessions after 1 hour
    )

# Each user/session gets their own history
user_history = get_session_history("user_123_session_456")
user_history.add_user_message("Hello!")
# This persists to Redis

# Later, in a different process:
same_history = get_session_history("user_123_session_456")
print(same_history.messages)  # Messages are still there
```

### PostgreSQL-Backed Persistent History

```bash
pip install psycopg2-binary langchain-community
```

```python
from langchain_community.chat_message_histories import PostgresChatMessageHistory

def get_session_history(session_id: str):
    return PostgresChatMessageHistory(
        connection_string="postgresql://user:password@localhost/langchain_db",
        session_id=session_id,
        table_name="chat_histories",  # Will be created if it doesn't exist
    )
```

---

## 5.2 RunnableWithMessageHistory

### Automatic History Management

Manually managing history is tedious. `RunnableWithMessageHistory` wraps any chain and handles history injection automatically:

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

# ─────────────────────────────────────────
# 1. Base chain (no memory awareness needed)
# ─────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Be concise and friendly."),
    MessagesPlaceholder(variable_name="history"),  # ← Where history goes
    ("human", "{input}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
chain = prompt | llm

# ─────────────────────────────────────────
# 2. History storage (one per session)
# ─────────────────────────────────────────
session_store = {}  # In production, use Redis or PostgreSQL

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]

# ─────────────────────────────────────────
# 3. Wrap chain with history management
# ─────────────────────────────────────────
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",     # Which key in input dict is the user message
    history_messages_key="history", # Which key in prompt is the history placeholder
)

# ─────────────────────────────────────────
# 4. Use it — session_id maintains context
# ─────────────────────────────────────────
config = {"configurable": {"session_id": "user_alice"}}

response1 = chain_with_history.invoke(
    {"input": "Hi! My name is Alice and I'm learning LangChain."},
    config=config,
)
print(f"Turn 1: {response1.content}")

response2 = chain_with_history.invoke(
    {"input": "What am I learning?"},
    config=config,
)
print(f"Turn 2: {response2.content}")  # Knows about LangChain from turn 1

# Different session — no memory of Alice
config2 = {"configurable": {"session_id": "user_bob"}}
response3 = chain_with_history.invoke(
    {"input": "What am I learning?"},
    config=config2,
)
print(f"Bob's session: {response3.content}")  # Doesn't know
```

---

## 5.3 Context Window Management

### The Token Limit Problem

As conversations grow, they hit the model's context window limit. A 128k-token model can handle ~96k tokens of history... but that's still a practical limit for long sessions.

### Strategies Comparison

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| **Window Buffer** | Keep only last N messages | Simple, predictable | Loses old context |
| **Token Window** | Keep messages within token budget | Respects limits exactly | Requires tokenizer |
| **Summary Memory** | Summarize old messages | Preserves key info | Summary can miss details |
| **Entity Memory** | Track key entities | Good for factual recall | Complex to implement |

### Token Window Memory

```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
import tiktoken

def trim_messages_to_token_limit(
    messages: list,
    max_tokens: int = 4000,
    model: str = "gpt-4o-mini",
) -> list:
    """
    Trim messages to fit within token limit.
    Always keeps the system message.
    Removes oldest human/AI messages first.
    """
    enc = tiktoken.encoding_for_model(model)
    
    def count_tokens(messages):
        total = 0
        for msg in messages:
            total += len(enc.encode(msg.content)) + 4  # 4 for message formatting
        return total
    
    # Always keep system messages
    system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
    other_msgs = [m for m in messages if not isinstance(m, SystemMessage)]
    
    # Trim from the beginning until we fit
    while count_tokens(system_msgs + other_msgs) > max_tokens and other_msgs:
        other_msgs = other_msgs[2:]  # Remove oldest exchange (human + AI)
    
    return system_msgs + other_msgs

# Use in a chain with trimming
from langchain_core.runnables import RunnableLambda

def trim_and_respond(input_dict: dict) -> dict:
    """Trim history before passing to model."""
    input_dict["history"] = trim_messages_to_token_limit(
        input_dict.get("history", []),
        max_tokens=3000,
    )
    return input_dict
```

### Summary Memory

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List

class SummaryMemory:
    """
    Maintains a rolling summary of the conversation
    plus recent messages that haven't been summarized yet.
    """
    def __init__(self, llm, max_recent_messages: int = 6):
        self.llm = llm
        self.max_recent_messages = max_recent_messages
        self.summary = ""
        self.recent_messages: List = []
    
    def add_exchange(self, human_message: str, ai_message: str):
        """Add a human/AI exchange to memory."""
        self.recent_messages.append(HumanMessage(content=human_message))
        self.recent_messages.append(AIMessage(content=ai_message))
        
        # If we have too many recent messages, summarize the oldest ones
        if len(self.recent_messages) > self.max_recent_messages:
            self._compress()
    
    def _compress(self):
        """Summarize oldest messages and update the running summary."""
        # Take the oldest half of recent messages
        to_summarize = self.recent_messages[:self.max_recent_messages // 2]
        self.recent_messages = self.recent_messages[self.max_recent_messages // 2:]
        
        # Summarize using the LLM
        summary_prompt = f"""Current conversation summary:
{self.summary if self.summary else "No prior summary"}

New messages to incorporate:
{chr(10).join(f'{type(m).__name__}: {m.content}' for m in to_summarize)}

Update the summary to include the key information from the new messages.
Keep it concise (2-4 sentences max)."""
        
        response = self.llm.invoke(summary_prompt)
        self.summary = response.content
    
    def get_context(self) -> List:
        """Get messages to inject into the next request."""
        messages = []
        if self.summary:
            messages.append(SystemMessage(
                content=f"Previous conversation summary: {self.summary}"
            ))
        messages.extend(self.recent_messages)
        return messages

# Usage
llm = ChatOpenAI(model="gpt-4o-mini")
memory = SummaryMemory(llm, max_recent_messages=6)

# Simulate a long conversation
exchanges = [
    ("I'm building a RAG system", "Great! What's your use case?"),
    ("It's for customer support at an e-commerce company", "What documents will you index?"),
    ("Product manuals and FAQ pages, about 500 PDFs", "I recommend starting with chunk_size=1000"),
    ("Should I use Chroma or Pinecone?", "Chroma for dev, Pinecone for production"),
    ("We expect 10k daily users", "Definitely use Pinecone then for scale"),
    ("What embedding model?", "OpenAI text-embedding-3-small is a good balance"),
    ("What about the retrieval strategy?", "Try ensemble retrieval with BM25 + semantic"),
]

for human, ai in exchanges:
    memory.add_exchange(human, ai)
    print(f"Memory has {len(memory.recent_messages)} recent msgs, summary: {memory.summary[:80]}...")
```

---

# Step 6: Agents, Tools & LangGraph

## 6.1 Tools & Function Calling

### What Are Tools?

An **agent** is an LLM that can take actions. The "actions" it can take are called **tools**.

**Mental Model:** Think of an agent as a person at a computer. They can:
- Search the web (`search` tool)
- Run Python code (`python_repl` tool)
- Look up a database (`sql_query` tool)
- Call an API (`http_request` tool)
- Read/write files (`file_system` tool)

The LLM decides *which* tool to use and *what arguments* to pass, based on the task.

```
┌──────────────────────────────────────────────────────────────┐
│                     AGENT LOOP                               │
│                                                              │
│  User: "What's the weather in Paris and convert 25°C to °F?" │
│         │                                                    │
│         ▼                                                    │
│  LLM thinks: "I need to:                                     │
│    1. Call get_weather(city='Paris')                         │
│    2. Call convert_temperature(25, 'C', 'F')"                │
│         │                                                    │
│         ▼                                                    │
│  Execute tool: get_weather('Paris')  →  "22°C, partly cloudy"│
│  Execute tool: convert_temp(25, C, F)  →  "77°F"            │
│         │                                                    │
│         ▼                                                    │
│  LLM synthesizes: "The weather in Paris is 22°C (71.6°F)..." │
└──────────────────────────────────────────────────────────────┘
```

### Creating Tools with `@tool`

```python
from langchain_core.tools import tool
from typing import Optional
import requests
import json

# ─────────────────────────────────────────
# Simple tool with the @tool decorator
# ─────────────────────────────────────────
@tool
def get_word_count(text: str) -> int:
    """Count the number of words in a text string.
    
    Args:
        text: The text to count words in.
    
    Returns:
        The number of words as an integer.
    """
    return len(text.split())

print(get_word_count.name)         # "get_word_count"
print(get_word_count.description)  # "Count the number of words..."
print(get_word_count.invoke({"text": "Hello world this is LangChain"}))  # 5

# ─────────────────────────────────────────
# Tool with type hints and documentation
# ─────────────────────────────────────────
@tool
def search_wikipedia(query: str, max_results: int = 3) -> str:
    """Search Wikipedia for information about a topic.
    
    Args:
        query: The search query to look up on Wikipedia.
        max_results: Maximum number of results to return (default: 3).
    
    Returns:
        A string with the search results summary.
    """
    try:
        import wikipedia
        results = wikipedia.search(query, results=max_results)
        summaries = []
        for title in results[:2]:
            try:
                summary = wikipedia.summary(title, sentences=3)
                summaries.append(f"**{title}**: {summary}")
            except Exception:
                continue
        return "\n\n".join(summaries) if summaries else "No results found."
    except ImportError:
        return "Wikipedia package not installed. Run: pip install wikipedia"

# ─────────────────────────────────────────
# Tool with Pydantic input validation
# ─────────────────────────────────────────
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression to evaluate, e.g. '2 + 2 * 3'")

def safe_calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    try:
        # Only allow safe math operations
        allowed_chars = set("0123456789+-*/()., ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic math operations allowed"
        result = eval(expression)  # In production, use a proper math parser
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

calculator = StructuredTool.from_function(
    func=safe_calculator,
    name="calculator",
    description="Calculate mathematical expressions. Input is a math expression string.",
    args_schema=CalculatorInput,
)
```

### Binding Tools to a Model

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()

@tool
def get_current_temperature(city: str) -> str:
    """Get the current temperature for a city. Returns temperature in Celsius."""
    # Mock implementation
    temperatures = {
        "London": "15°C, cloudy",
        "Tokyo": "22°C, sunny",
        "New York": "18°C, partly cloudy",
        "Paris": "17°C, overcast",
    }
    return temperatures.get(city, f"Weather data not available for {city}")

@tool
def convert_celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit.
    
    Args:
        celsius: Temperature in Celsius
    
    Returns:
        Temperature in Fahrenheit
    """
    return (celsius * 9/5) + 32

tools = [get_current_temperature, convert_celsius_to_fahrenheit]

# Bind tools to the model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# The model now knows about these tools and can call them
response = llm_with_tools.invoke([
    HumanMessage(content="What's the temperature in Tokyo and what is that in Fahrenheit?")
])

print(response.content)       # Might be empty if tool calls are made
print(response.tool_calls)    # List of tool calls the model wants to make
# [{'name': 'get_current_temperature', 'args': {'city': 'Tokyo'}, 'id': 'call_abc'},
#  {'name': 'convert_celsius_to_fahrenheit', 'args': {'celsius': 22}, 'id': 'call_def'}]
```

---

## 6.2 Agent Architectures

### The ReAct Pattern

ReAct (**Re**asoning + **Act**ing) is the dominant agent pattern. The model alternates between:
1. **Thought:** Reasoning about what to do
2. **Action:** Choosing and calling a tool
3. **Observation:** Reading the tool result
4. Repeat until done

```
Thought: I need to find the weather in Paris
Action: get_current_temperature(city="Paris")
Observation: 22°C, partly cloudy

Thought: Now I need to convert 22°C to Fahrenheit
Action: convert_celsius_to_fahrenheit(celsius=22)
Observation: 71.6

Thought: I have all the information needed
Answer: The weather in Paris is 22°C (71.6°F), partly cloudy.
```

### Tool-Calling Agent with LangGraph

The modern way to build agents is with LangGraph (covered in depth next section). Here's a preview of a simple agent:

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@tool
def get_word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())

tools = [add, multiply, get_word_count]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create a ReAct agent in one line
agent = create_react_agent(llm, tools)

# Run the agent
result = agent.invoke({
    "messages": [("human", "What is 15 * 7, and how many words are in 'the quick brown fox'?")]
})

for message in result["messages"]:
    print(f"{type(message).__name__}: {message.content}")
```

---

## 6.3 LangGraph Deep Dive

### Why LangGraph?

Basic LCEL chains are linear: A → B → C → done.

Real AI applications need **cycles** (do something, check if it's done, do more if not), **branches** (if X then do Y else do Z), and **state** (remember what happened across many steps).

LangGraph provides exactly this: a framework for building stateful, multi-step AI workflows as **graphs**.

```
Linear Chain (LCEL):
Input → Step1 → Step2 → Step3 → Output

LangGraph (Stateful Graph):
           ┌──────────────┐
           │              │  ← can loop back
Input → Step1 → Step2 → Step3 → [Decide] → Output
                  ↑         │
                  └─────────┘  ← conditional routing
```

### Core Concepts

**State:** A TypedDict that holds all the data the graph needs. Every node reads from and writes to this state.

**Nodes:** Python functions (or runnables) that take the state and return updates to it.

**Edges:** Connections between nodes. Can be:
- Regular: always go from A to B
- Conditional: go to different nodes based on a condition
- `START` → first node
- Any node → `END` → terminates

```python
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator

# ─────────────────────────────────────────
# 1. Define the State
# ─────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # Annotated[..., operator.add] means: when updating this field,
    # APPEND new messages to existing ones (not replace)

# ─────────────────────────────────────────
# 2. Define Nodes (functions that process state)
# ─────────────────────────────────────────
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def call_model(state: AgentState) -> dict:
    """Node: Call the LLM with the current messages."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}  # Returns AIMessage to append

def should_continue(state: AgentState) -> str:
    """Conditional edge: Determine next step based on state."""
    last_message = state["messages"][-1]
    # If the model wants to call tools, route to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "call_tools"
    # Otherwise, we're done
    return END

# ─────────────────────────────────────────
# 3. Build the Graph
# ─────────────────────────────────────────
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("model", call_model)

# Add edges
workflow.add_edge(START, "model")  # Start at the model node
workflow.add_conditional_edges(
    "model",           # From this node
    should_continue,   # Use this function to decide
    {
        "call_tools": "model",  # If tools needed, call model again (simplified)
        END: END,               # If done, end
    }
)

# Compile
graph = workflow.compile()

# Run
result = graph.invoke({
    "messages": [HumanMessage(content="What is 2 + 2?")]
})
print(result["messages"][-1].content)
```

### Full ReAct Agent with LangGraph

```python
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv
import operator

load_dotenv()

# ─────────────────────────────────────────
# Define tools
# ─────────────────────────────────────────
@tool
def search_web(query: str) -> str:
    """Search the web for current information.
    
    Args:
        query: The search query
    
    Returns:
        Search results as a string
    """
    # Mock web search — in production, use Tavily, SerpAPI, etc.
    mock_results = {
        "langchain": "LangChain is a framework for building LLM applications, released in 2022.",
        "python": "Python 3.12 is the latest stable version as of 2024.",
    }
    for key, value in mock_results.items():
        if key.lower() in query.lower():
            return value
    return f"Searched for: {query}. No specific results found in mock database."

@tool
def calculate(expression: str) -> str:
    """Perform a mathematical calculation.
    
    Args:
        expression: A mathematical expression like '2 + 2' or '15 * 7'
    
    Returns:
        The result of the calculation
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

tools = [search_web, calculate]

# ─────────────────────────────────────────
# Set up the LLM with tools
# ─────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# ─────────────────────────────────────────
# Define State
# ─────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# ─────────────────────────────────────────
# Define Nodes
# ─────────────────────────────────────────
def agent_node(state: AgentState) -> dict:
    """Main agent node: calls LLM with current state."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# ToolNode handles executing tools automatically
tool_node = ToolNode(tools)

# ─────────────────────────────────────────
# Define Routing Logic
# ─────────────────────────────────────────
def should_continue(state: AgentState) -> str:
    """Route to tool execution or end based on model output."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "call_tools"
    return "end"

# ─────────────────────────────────────────
# Build the Graph
# ─────────────────────────────────────────
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "call_tools": "tools",  # Go execute tools
        "end": END,             # We're done
    }
)
workflow.add_edge("tools", "agent")  # After tools, go back to agent

graph = workflow.compile()

# ─────────────────────────────────────────
# Visualize the graph (optional)
# ─────────────────────────────────────────
# print(graph.get_graph().draw_mermaid())

# ─────────────────────────────────────────
# Run it
# ─────────────────────────────────────────
def run_agent(question: str):
    print(f"\n🤔 Question: {question}")
    print("─" * 60)
    
    result = graph.invoke({
        "messages": [HumanMessage(content=question)]
    })
    
    # Print the reasoning trace
    for msg in result["messages"]:
        msg_type = type(msg).__name__
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"🔧 Agent wants to call: {[tc['name'] for tc in msg.tool_calls]}")
        elif hasattr(msg, "content") and msg.content:
            print(f"💬 {msg_type}: {msg.content}")
    
    return result["messages"][-1].content

run_agent("What is LangChain and calculate 15 * 23?")
run_agent("What is 100 / 4 + 50?")
```

### Checkpointing — Persistent Agent Memory

LangGraph can persist state between runs using **checkpointers**:

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, START
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
import operator
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def chat_node(state: AgentState) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

workflow = StateGraph(AgentState)
workflow.add_node("chat", chat_node)
workflow.add_edge(START, "chat")
workflow.add_edge("chat", END)

# Add a checkpointer for persistence
memory = MemorySaver()  # In production, use SqliteSaver or PostgresSaver
graph = workflow.compile(checkpointer=memory)

# Thread ID acts like a session ID — each thread has its own state
thread_config = {"configurable": {"thread_id": "conversation_abc_123"}}

# Turn 1
result = graph.invoke(
    {"messages": [HumanMessage(content="My favorite color is blue.")]},
    config=thread_config,
)
print(result["messages"][-1].content)

# Turn 2 — the graph REMEMBERS the previous state automatically
result = graph.invoke(
    {"messages": [HumanMessage(content="What's my favorite color?")]},
    config=thread_config,
)
print(result["messages"][-1].content)  # "Your favorite color is blue."
```

### Human-in-the-Loop

LangGraph supports pausing for human approval before taking actions:

```python
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
import operator
from dotenv import load_dotenv

load_dotenv()

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email. This is a potentially dangerous action requiring approval.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body
    
    Returns:
        Confirmation message
    """
    # In production, this would actually send an email
    return f"Email sent to {to} with subject '{subject}'"

@tool
def draft_email(to: str, subject: str, body: str) -> str:
    """Create an email draft for review.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body
    
    Returns:
        Draft preview
    """
    return f"DRAFT:\nTo: {to}\nSubject: {subject}\n\n{body}"

tools = [send_email, draft_email]
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def agent(state: State) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}

tool_node = ToolNode(tools)

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END

workflow = StateGraph(State)
workflow.add_node("agent", agent)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

memory = MemorySaver()
# interrupt_before=["tools"] pauses execution BEFORE the tools node
graph = workflow.compile(
    checkpointer=memory,
    interrupt_before=["tools"],  # ← Human approval required before tool execution
)

config = {"configurable": {"thread_id": "approval_flow_1"}}

# Step 1: Initial run — will pause before tools
result = graph.invoke(
    {"messages": [HumanMessage(content="Draft an email to boss@company.com about project delays")]},
    config=config,
)

# The graph is now PAUSED — check what tools it wants to call
current_state = graph.get_state(config)
last_msg = current_state.values["messages"][-1]

if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
    print("⚠️ Agent wants to call:")
    for tc in last_msg.tool_calls:
        print(f"  Tool: {tc['name']}")
        print(f"  Args: {tc['args']}")
    
    # Human decision
    approval = input("\nApprove? (yes/no): ")
    
    if approval.lower() == "yes":
        # Resume execution from where it paused
        result = graph.invoke(None, config=config)
        print("✅ Tools executed:", result["messages"][-1].content)
    else:
        # Modify the state to cancel the tool calls
        graph.update_state(
            config,
            {"messages": [AIMessage(content="Tool execution cancelled by user.")]},
        )
        print("❌ Action cancelled")
```

### LangGraph Mermaid Diagram

```mermaid
graph TD
    START([START]) --> agent[Agent Node\nLLM decides action]
    agent --> decision{Has tool calls?}
    decision -->|Yes| tools[Tools Node\nExecutes tools]
    decision -->|No| END([END])
    tools --> agent
    
    style START fill:#4CAF50,color:#fff
    style END fill:#f44336,color:#fff
    style agent fill:#2196F3,color:#fff
    style tools fill:#FF9800,color:#fff
    style decision fill:#9C27B0,color:#fff
```

---

## 6.4 Advanced Agent Systems

### Research Agent

```python
"""
Research Agent: Autonomously researches a topic using multiple tools
and produces a structured report.
"""
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
import operator

load_dotenv()

# ─────────────────────────────────────────
# Research Tools
# ─────────────────────────────────────────
@tool
def web_search(query: str) -> str:
    """Search the web for information.
    
    Args:
        query: Search query string
    
    Returns:
        Relevant search results
    """
    # In production: use Tavily, SerpAPI, or DuckDuckGo
    return f"[Mock results for '{query}'] Found 10 relevant results about this topic."

@tool
def read_article(url: str) -> str:
    """Read and extract content from a web article.
    
    Args:
        url: URL of the article to read
    
    Returns:
        Article text content
    """
    # In production: use WebBaseLoader or newspaper3k
    return f"[Mock article content from {url}] This article discusses key findings..."

@tool
def save_note(topic: str, content: str) -> str:
    """Save a research note for later synthesis.
    
    Args:
        topic: The topic this note is about
        content: The note content
    
    Returns:
        Confirmation
    """
    return f"Note saved under topic '{topic}': {content[:50]}..."

research_tools = [web_search, read_article, save_note]

# ─────────────────────────────────────────
# Agent State with research tracking
# ─────────────────────────────────────────
class ResearchState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    research_topic: str
    iteration_count: int
    max_iterations: int

# ─────────────────────────────────────────
# Nodes
# ─────────────────────────────────────────
research_llm = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(research_tools)

RESEARCH_SYSTEM_PROMPT = """You are an expert research assistant. Your job is to:
1. Search for information on the given topic
2. Read relevant articles
3. Save important notes
4. After gathering sufficient information (at least 3 searches), 
   write a comprehensive report

Current iteration: {iteration}/{max_iterations}
Topic: {topic}

When you have enough information, provide your final research report."""

def researcher(state: ResearchState) -> dict:
    """Main research agent."""
    from langchain_core.messages import SystemMessage
    
    system_msg = SystemMessage(content=RESEARCH_SYSTEM_PROMPT.format(
        iteration=state["iteration_count"],
        max_iterations=state["max_iterations"],
        topic=state["research_topic"],
    ))
    
    messages = [system_msg] + list(state["messages"])
    response = research_llm.invoke(messages)
    
    return {
        "messages": [response],
        "iteration_count": state["iteration_count"] + 1,
    }

tool_executor = ToolNode(research_tools)

def should_continue(state: ResearchState) -> str:
    last_msg = state["messages"][-1]
    
    # Force stop if max iterations reached
    if state["iteration_count"] >= state["max_iterations"]:
        return END
    
    # Continue if there are tool calls
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"
    
    # Stop if no tool calls (agent finished)
    return END

# ─────────────────────────────────────────
# Build Graph
# ─────────────────────────────────────────
research_graph = StateGraph(ResearchState)
research_graph.add_node("researcher", researcher)
research_graph.add_node("tools", tool_executor)
research_graph.add_edge(START, "researcher")
research_graph.add_conditional_edges(
    "researcher", should_continue, {"tools": "tools", END: END}
)
research_graph.add_edge("tools", "researcher")

compiled_research_agent = research_graph.compile()

def research(topic: str, max_iterations: int = 6) -> str:
    """Run the research agent on a topic."""
    print(f"🔬 Researching: {topic}")
    
    result = compiled_research_agent.invoke({
        "messages": [HumanMessage(content=f"Research this topic thoroughly: {topic}")],
        "research_topic": topic,
        "iteration_count": 0,
        "max_iterations": max_iterations,
    })
    
    return result["messages"][-1].content

# Run it
report = research("The impact of large language models on software engineering")
print(report)
```

---

### 🏗️ Project 4: SQL Analyst Agent

```python
"""
Project 4: SQL Analyst Agent
An agent that can query a database, analyze results, and explain findings.
"""
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

load_dotenv()

# Create a sample SQLite database for demonstration
import sqlite3
import os

def create_sample_db(db_path: str = "sample.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        city TEXT,
        signup_date TEXT
    );
    
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product TEXT,
        amount REAL,
        order_date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );
    
    INSERT OR IGNORE INTO customers VALUES
        (1, 'Alice Johnson', 'alice@example.com', 'New York', '2024-01-15'),
        (2, 'Bob Smith', 'bob@example.com', 'Los Angeles', '2024-02-20'),
        (3, 'Carol White', 'carol@example.com', 'Chicago', '2024-01-05'),
        (4, 'David Brown', 'david@example.com', 'New York', '2024-03-10');
    
    INSERT OR IGNORE INTO orders VALUES
        (1, 1, 'Laptop', 1299.99, '2024-03-01'),
        (2, 1, 'Mouse', 29.99, '2024-03-15'),
        (3, 2, 'Keyboard', 79.99, '2024-02-25'),
        (4, 3, 'Monitor', 399.99, '2024-03-20'),
        (5, 3, 'Webcam', 89.99, '2024-03-21'),
        (6, 4, 'Laptop', 1299.99, '2024-04-01'),
        (7, 2, 'Headphones', 149.99, '2024-04-05');
    """)
    conn.commit()
    conn.close()

create_sample_db()

# Connect LangChain to the database
db = SQLDatabase.from_uri("sqlite:///sample.db")

# Create SQL toolkit
llm = ChatOpenAI(model="gpt-4o", temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_tools = toolkit.get_tools()

# Create the SQL agent
sql_agent = create_react_agent(llm, sql_tools)

def ask_database(question: str) -> str:
    """Ask the SQL agent a question about the database."""
    print(f"\n📊 Question: {question}")
    print("─" * 60)
    
    result = sql_agent.invoke({
        "messages": [HumanMessage(content=question)]
    })
    
    # Show the reasoning trace
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"  🔧 SQL: {tc['args'].get('query', tc['args'])}")
    
    answer = result["messages"][-1].content
    print(f"\n📋 Answer: {answer}")
    return answer

# Run queries
ask_database("How many customers do we have in each city?")
ask_database("What is the total revenue from each customer?")
ask_database("Who is our highest-spending customer and what did they buy?")
ask_database("What's the average order value, and which products are most popular?")
```

---

# Step 7: Production & Evaluation

## 7.1 LangSmith — Tracing & Observability

### Why You Need Observability

In production, AI applications fail in surprising ways:
- The LLM generates incorrect output
- Retrieval returns irrelevant documents
- An agent gets stuck in a loop
- Prompts cost 3x more tokens than expected
- A specific user query always fails

Without tracing, you're debugging blind. **LangSmith** provides full observability into every LangChain execution.

### Setup

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__your_key"
os.environ["LANGCHAIN_PROJECT"] = "my-project-name"
# That's it — all LangChain operations are now automatically traced
```

Every call to `.invoke()`, `.stream()`, `.batch()` on any LangChain component is now traced. In the LangSmith UI, you'll see:

- The full input/output of every step
- Token usage per step
- Latency per step
- The full chain hierarchy (nested chains show as trees)
- Error details with full traceback

### Manual Tracing

```python
from langsmith import traceable
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# Decorate any function to add it to the trace tree
@traceable(name="sentiment_analysis")
def analyze_sentiment(text: str) -> dict:
    response = llm.invoke(f"Classify sentiment (positive/negative/neutral): {text}")
    return {"text": text, "sentiment": response.content}

@traceable(name="batch_analysis")
def analyze_batch(texts: list) -> list:
    return [analyze_sentiment(t) for t in texts]

# These calls are now fully traced in LangSmith
result = analyze_batch([
    "I love this product!",
    "Terrible experience, 1 star.",
    "It's okay, nothing special.",
])
```

### Evaluation with LangSmith

```python
from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_openai import ChatOpenAI

client = Client()

# ─────────────────────────────────────────
# Create a dataset for evaluation
# ─────────────────────────────────────────
dataset = client.create_dataset(
    dataset_name="rag_eval_dataset",
    description="QA pairs for evaluating our RAG system",
)

# Add examples (question + expected answer)
examples = [
    {"input": {"question": "What is LangChain?"}, 
     "output": {"answer": "LangChain is a framework for building LLM applications"}},
    {"input": {"question": "What does LCEL stand for?"}, 
     "output": {"answer": "LangChain Expression Language"}},
]

client.create_examples(
    inputs=[e["input"] for e in examples],
    outputs=[e["output"] for e in examples],
    dataset_id=dataset.id,
)

# ─────────────────────────────────────────
# Define evaluators
# ─────────────────────────────────────────
def correctness_evaluator(run, example) -> dict:
    """LLM-as-judge: Is the answer correct?"""
    eval_llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    expected = example.outputs.get("answer", "")
    actual = run.outputs.get("answer", "") if run.outputs else ""
    
    prompt = f"""Rate if this answer is correct (yes/no/partial):
Expected: {expected}
Actual: {actual}

Respond ONLY with: yes, no, or partial"""
    
    verdict = eval_llm.invoke(prompt).content.strip().lower()
    score = {"yes": 1.0, "partial": 0.5, "no": 0.0}.get(verdict, 0.0)
    
    return {"key": "correctness", "score": score, "comment": verdict}

# ─────────────────────────────────────────
# Run evaluation
# ─────────────────────────────────────────
def rag_pipeline(inputs: dict) -> dict:
    """The function being evaluated."""
    # Your actual RAG chain here
    question = inputs["question"]
    answer = rag_chain.invoke(question)  # Assumes rag_chain exists
    return {"answer": answer}

results = evaluate(
    rag_pipeline,
    data=dataset.name,
    evaluators=[correctness_evaluator],
    experiment_prefix="rag_v1",
)
print(f"Average correctness: {results.aggregate_feedback['correctness']:.0%}")
```

---

## 7.2 LangServe — APIs & Deployment

### Exposing Chains as REST APIs

LangServe wraps any LangChain runnable in a FastAPI server automatically:

```bash
pip install langserve fastapi uvicorn
```

```python
# app.py
from fastapi import FastAPI
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LangChain API",
    version="1.0",
    description="AI-powered text processing endpoints",
)

# ─────────────────────────────────────────
# Define your chains
# ─────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Chain 1: Text summarization
summarize_chain = (
    ChatPromptTemplate.from_template(
        "Summarize the following text in 2-3 sentences:\n\n{text}"
    )
    | llm
    | StrOutputParser()
)

# Chain 2: Translation
translate_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a professional translator."),
        ("human", "Translate the following text to {language}:\n\n{text}"),
    ])
    | llm
    | StrOutputParser()
)

# ─────────────────────────────────────────
# Add routes — creates all endpoints automatically
# ─────────────────────────────────────────
add_routes(app, summarize_chain, path="/summarize")
add_routes(app, translate_chain, path="/translate")

# LangServe automatically creates:
# POST /summarize/invoke          - single invocation
# POST /summarize/batch           - batch processing
# POST /summarize/stream          - streaming
# GET  /summarize/input_schema    - JSON schema for inputs
# GET  /summarize/output_schema   - JSON schema for outputs
# GET  /summarize/playground      - Interactive UI

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```bash
# Run the server
python app.py

# Test with curl
curl -X POST http://localhost:8000/summarize/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": {"text": "LangChain is a framework for developing applications powered by large language models..."}}'

# Streaming
curl -X POST http://localhost:8000/summarize/stream \
  -H "Content-Type: application/json" \
  -d '{"input": {"text": "Long text to summarize..."}}'
```

### FastAPI with WebSocket Streaming

```python
# websocket_server.py
from fastapi import FastAPI, WebSocket
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

chain = (
    ChatPromptTemplate.from_template("Answer this question thoroughly: {question}")
    | ChatOpenAI(model="gpt-4o-mini", temperature=0.7, streaming=True)
    | StrOutputParser()
)

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive question from client
            question = await websocket.receive_text()
            
            # Stream response back token by token
            async for chunk in chain.astream({"question": question}):
                await websocket.send_text(chunk)
            
            # Signal end of response
            await websocket.send_text("[DONE]")
    
    except Exception as e:
        await websocket.close(code=1000)
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```yaml
# docker-compose.yml
version: "3.8"

services:
  langchain-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
    restart: unless-stopped
    volumes:
      - ./chroma_db:/app/chroma_db  # Persist vector store

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

---

## 7.3 Production Engineering

### Recommended Project Structure

```
my-langchain-app/
├── .env                      # API keys (NEVER commit)
├── .env.example              # Template for other developers
├── .gitignore                # Include .env, __pycache__, *.db
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
│
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app entry point
│   ├── config.py             # Settings and configuration
│   │
│   ├── chains/               # LCEL chains
│   │   ├── __init__.py
│   │   ├── rag_chain.py
│   │   ├── summarize_chain.py
│   │   └── analysis_chain.py
│   │
│   ├── agents/               # LangGraph agents
│   │   ├── __init__.py
│   │   ├── research_agent.py
│   │   └── sql_agent.py
│   │
│   ├── tools/                # Custom tools
│   │   ├── __init__.py
│   │   ├── search_tools.py
│   │   └── database_tools.py
│   │
│   ├── retrieval/            # RAG components
│   │   ├── __init__.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   └── ingestion.py
│   │
│   ├── models/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── requests.py
│   │   └── responses.py
│   │
│   └── utils/                # Utilities
│       ├── __init__.py
│       ├── callbacks.py
│       └── rate_limiter.py
│
├── data/                     # Data files
│   ├── documents/
│   └── vector_stores/
│
└── tests/
    ├── __init__.py
    ├── test_chains.py
    ├── test_agents.py
    └── test_retrieval.py
```

### Rate Limiting and Cost Control

```python
# utils/rate_limiter.py
import time
import threading
from collections import deque
from functools import wraps
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

class TokenBudgetTracker(BaseCallbackHandler):
    """Track token usage and enforce budget limits."""
    
    def __init__(self, daily_token_budget: int = 1_000_000):
        self.daily_budget = daily_token_budget
        self.tokens_used_today = 0
        self.reset_time = time.time() + 86400  # Reset in 24 hours
        self._lock = threading.Lock()
    
    def on_llm_end(self, response: LLMResult, **kwargs):
        """Called after each LLM call."""
        with self._lock:
            # Check if we need to reset
            if time.time() > self.reset_time:
                self.tokens_used_today = 0
                self.reset_time = time.time() + 86400
            
            # Count tokens used
            for generation_list in response.generations:
                for generation in generation_list:
                    if hasattr(generation, "generation_info"):
                        usage = generation.generation_info.get("usage", {})
                        total = usage.get("total_tokens", 0)
                        self.tokens_used_today += total
            
            # Alert if approaching budget
            if self.tokens_used_today > self.daily_budget * 0.8:
                print(f"⚠️ WARNING: Used {self.tokens_used_today:,} / {self.daily_budget:,} tokens today")
            
            if self.tokens_used_today > self.daily_budget:
                raise Exception(f"Daily token budget exceeded: {self.tokens_used_today:,} tokens used")
    
    @property
    def usage_percent(self) -> float:
        return self.tokens_used_today / self.daily_budget

class RateLimiter:
    """Token bucket rate limiter for API calls."""
    
    def __init__(self, requests_per_minute: int = 60):
        self.rpm = requests_per_minute
        self.timestamps = deque()
        self._lock = threading.Lock()
    
    def wait_if_needed(self):
        """Block if rate limit would be exceeded."""
        with self._lock:
            now = time.time()
            
            # Remove timestamps older than 1 minute
            while self.timestamps and now - self.timestamps[0] > 60:
                self.timestamps.popleft()
            
            if len(self.timestamps) >= self.rpm:
                sleep_time = 60 - (now - self.timestamps[0])
                if sleep_time > 0:
                    print(f"Rate limit: waiting {sleep_time:.1f}s")
                    time.sleep(sleep_time)
            
            self.timestamps.append(time.time())

# Usage
from langchain_openai import ChatOpenAI

budget_tracker = TokenBudgetTracker(daily_token_budget=500_000)
rate_limiter = RateLimiter(requests_per_minute=60)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    callbacks=[budget_tracker],  # Attach the tracker
)
```

### Async Architecture for High Throughput

```python
# High-throughput async processing
import asyncio
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

chain = (
    ChatPromptTemplate.from_template("Classify sentiment: {text}")
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

async def process_batch_async(
    texts: List[str],
    batch_size: int = 20,
    semaphore_limit: int = 10,
) -> List[str]:
    """
    Process a large batch of texts asynchronously.
    
    batch_size: How many to process concurrently
    semaphore_limit: Max concurrent API calls (to avoid rate limits)
    """
    semaphore = asyncio.Semaphore(semaphore_limit)
    
    async def process_one(text: str) -> str:
        async with semaphore:
            return await chain.ainvoke({"text": text})
    
    # Process in batches
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_results = await asyncio.gather(*[process_one(t) for t in batch])
        results.extend(batch_results)
        print(f"Processed {min(i + batch_size, len(texts))}/{len(texts)}")
    
    return results

# Process 1000 texts efficiently
texts = [f"Sample text {i} with some content to analyze." for i in range(100)]
results = asyncio.run(process_batch_async(texts, batch_size=20, semaphore_limit=10))
print(f"Processed {len(results)} texts")
```

### Error Handling and Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from langchain_core.runnables import RunnableLambda
import openai

def with_retry(chain, max_attempts: int = 3):
    """Wrap a chain with exponential backoff retry logic."""
    
    @retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        retry=retry_if_exception_type((
            openai.RateLimitError,
            openai.APITimeoutError,
            openai.APIConnectionError,
        )),
        reraise=True,
    )
    def wrapped_invoke(inputs):
        return chain.invoke(inputs)
    
    return RunnableLambda(wrapped_invoke)

# Usage
resilient_chain = with_retry(your_chain, max_attempts=3)
result = resilient_chain.invoke({"question": "..."})
```

### Security Considerations

```python
# security.py
import re
from langchain_core.runnables import RunnableLambda

class PromptInjectionGuard:
    """
    Basic guard against prompt injection attacks.
    In production, use a proper security scanning service.
    """
    
    INJECTION_PATTERNS = [
        r"ignore (all )?previous instructions",
        r"disregard (your|the) (system |previous )?instructions",
        r"you are now (a )?.*?(without|ignore|disregard)",
        r"act as if you (have no|don't have) restrictions",
        r"jailbreak",
        r"DAN mode",
        r"pretend you are",
    ]
    
    def __init__(self):
        self.patterns = [re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS]
    
    def check(self, text: str) -> str:
        for pattern in self.patterns:
            if pattern.search(text):
                raise ValueError(f"Potential prompt injection detected in input: {text[:100]}")
        return text

def input_sanitizer(inputs: dict) -> dict:
    """Sanitize user inputs before they reach the LLM."""
    guard = PromptInjectionGuard()
    
    for key, value in inputs.items():
        if isinstance(value, str):
            # Check for injection
            guard.check(value)
            # Limit input length
            if len(value) > 10000:
                raise ValueError(f"Input '{key}' exceeds maximum length of 10,000 characters")
    
    return inputs

# Wrap your chain with security
from langchain_core.runnables import RunnableLambda

safe_chain = RunnableLambda(input_sanitizer) | your_chain
```

---

### Common Production Failures & How to Fix Them

| Failure | Cause | Fix |
|---------|-------|-----|
| Hallucinations in RAG | Retrieved docs don't contain the answer | Add "I don't know" training, evaluate retrieval quality |
| High latency | Large prompts, no caching | Implement semantic caching, reduce prompt size |
| Token budget exhaustion | Uncontrolled context growth | Use token windows, summarization memory |
| Inconsistent output format | Model ignores format instructions | Use `with_structured_output()`, add validation |
| Agent infinite loops | No iteration limit, unclear stop condition | Add `max_iterations`, clear termination criteria |
| Duplicate embeddings | No dedup in ingestion | Use Indexing API with RecordManager |
| Rate limit errors | Too many concurrent requests | Implement rate limiter, exponential backoff |
| Context window overflow | Chat history too long | Implement sliding window or summary memory |

---

# Complete Learning Roadmap

## Phase 1: Foundation (Weeks 1-2)

**Goal:** Build your first working RAG chatbot.

- [ ] Complete Step 0 (LLM fundamentals)
- [ ] Set up development environment
- [ ] Build a simple Q&A chain with LCEL
- [ ] Load a PDF and answer questions about it
- [ ] Add conversation memory
- [ ] Deploy with FastAPI

**Mini Project:** PDF chatbot that can answer questions about a document of your choice.

## Phase 2: Intermediate (Weeks 3-4)

**Goal:** Build production-quality RAG systems.

- [ ] Implement advanced retrievers (MultiQuery, Ensemble)
- [ ] Add metadata filtering and self-query
- [ ] Implement the Indexing API for deduplication
- [ ] Add streaming to your FastAPI endpoints
- [ ] Set up LangSmith for observability
- [ ] Evaluate retrieval quality with test queries

**Mini Project:** Enterprise knowledge base for a set of company documents, with metadata filtering and streaming API.

## Phase 3: Advanced (Weeks 5-6)

**Goal:** Build autonomous agents with LangGraph.

- [ ] Build your first LangGraph agent with custom tools
- [ ] Implement checkpointing for persistent memory
- [ ] Add human-in-the-loop for sensitive operations
- [ ] Build a multi-agent system (researcher + writer)
- [ ] Implement SQL querying agent

**Mini Project:** Research agent that autonomously gathers information and produces reports.

## Phase 4: Production (Weeks 7-8)

**Goal:** Deploy and operate AI systems at scale.

- [ ] Implement proper error handling and retries
- [ ] Add rate limiting and cost controls
- [ ] Write unit tests for chains and agents
- [ ] Set up Docker deployment
- [ ] Implement CI/CD pipeline
- [ ] Add monitoring and alerting

**Mini Project:** Fully production-deployed AI service with monitoring, tested CI/CD, and cost controls.

---

## What To Learn Next

After mastering LangChain, these skills will make you a complete AI engineer:

**Deeper AI Engineering:**
- **LangGraph Platform** — Managed hosting for LangGraph agents
- **Fine-tuning** — Customize models with your own data (OpenAI fine-tuning API)
- **Embeddings research** — Matryoshka embeddings, binary quantization
- **Advanced RAG patterns** — GraphRAG, HyDE, FLARE
- **Multi-modal RAG** — Images, audio, video in your knowledge bases

**Infrastructure:**
- **Kubernetes** for containerized AI service deployment
- **Celery + Redis** for async task queues
- **Apache Kafka** for high-throughput event streaming
- **MLflow** for experiment tracking
- **Prometheus + Grafana** for metrics and dashboards

**Complementary Frameworks:**
- **LlamaIndex** — Alternative RAG framework with different strengths
- **DSPy** — Programmatic prompt optimization
- **Guardrails AI** — Input/output validation for AI
- **Instructor** — Structured output library

---

## Senior-Level Project Ideas

1. **Multi-Tenant RAG Platform**
   - Separate knowledge bases per customer
   - Usage metering and billing
   - Role-based access control
   - Admin dashboard

2. **Autonomous Code Review System**
   - Agent that reviews PRs and leaves GitHub comments
   - Learns from accepted/rejected suggestions over time
   - Integrates with CI/CD

3. **AI-Powered Data Pipeline**
   - Ingests unstructured data (emails, PDFs, Slack)
   - Extracts structured data to a database
   - Generates daily briefings

4. **Customer Support AI with Escalation**
   - RAG for knowledge base Q&A
   - Sentiment detection for escalation
   - CRM integration
   - Human handoff with full context

5. **Research Assistant with Persistent Memory**
   - Remembers past research topics
   - Cross-references findings across sessions
   - Generates literature review drafts

---

## How To Prepare For AI Engineering Interviews

### Technical Topics to Master

**Concepts:**
- Explain RAG and when you'd use it vs. fine-tuning
- Walk through the tradeoffs between different embedding models
- Explain what a context window is and how it limits system design
- Describe how you'd evaluate a RAG system's quality

**System Design:**
- Design a document Q&A system for 10 million documents
- Design a conversational AI system that needs to remember across sessions
- Design a rate-limited, cost-controlled LLM API service
- Design a multi-tenant AI platform

**Coding:**
- Build a basic RAG chain from scratch
- Implement a custom tool for an agent
- Write a custom memory management strategy
- Build an evaluation pipeline

### Interview Tips

1. **Always talk about tradeoffs.** Every choice (chunk size, embedding model, retriever type) has tradeoffs. Interviewers want to see you think in tradeoffs.

2. **Know your failure modes.** What happens when retrieval fails? When the LLM hallucinates? When the context window overflows? Showing you've thought about failure cases demonstrates production readiness.

3. **Have real project experience.** Build the projects in this handbook. Being able to say "I built X and encountered Y problem, which I solved by Z" is far more valuable than theoretical knowledge.

4. **Understand the fundamentals.** You'll be asked how embeddings work, what a token is, why RAG is better than fine-tuning for private data. This handbook gives you the foundation.

5. **Show LangSmith knowledge.** Mentioning observability, evaluation, and testing pipelines immediately signals production experience.

---

## Open Source Contributions

Contributing to LangChain and related projects is a great way to learn deeply and build your reputation:

**LangChain repos to contribute to:**
- `langchain-ai/langchain` — Core framework
- `langchain-ai/langgraph` — Agent framework
- `langchain-ai/langsmith-sdk` — Observability SDK

**Good first contributions:**
- Documentation improvements and examples
- Bug fixes in community integrations
- New document loaders (there are always new sources to add)
- New retriever implementations
- Tutorial notebooks

**How to find good issues:**
- Filter by `good first issue` or `help wanted` labels
- Look for issues tagged with your area of interest (RAG, agents, memory)
- Check the `[Needs docs]` label — documentation is always valuable

---

## Final Notes

This handbook has walked you from "what is an LLM" to deploying production AI systems with monitoring, security, and scalability. The field moves fast — new models, new frameworks, new patterns emerge constantly. But the fundamentals you've learned here — understanding tokens and context windows, building RAG pipelines, composing chains with LCEL, building agents with LangGraph — these will remain relevant because they're rooted in the underlying mechanics of how these systems work.

The best way to continue learning is to **build things**. Take the projects in each chapter, extend them, break them, and figure out why they broke. That's how you develop the intuition that separates good AI engineers from great ones.

---

*Version: 1.0 | LangChain v0.3+ | Python 3.11+*

*Verify package versions with `pip show langchain langchain-core langgraph` and check the [LangChain migration guide](https://python.langchain.com/docs/versions/migrating_chains/) for breaking changes.*
