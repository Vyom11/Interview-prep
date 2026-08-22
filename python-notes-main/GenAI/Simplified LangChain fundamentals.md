# LangChain: A Beginner-Friendly Guide
### Understanding AI Apps Without the Jargon

> **Who this is for:** Anyone curious about building AI-powered apps, explained with real-world analogies and simple code. No PhD required.

---

## Table of Contents

**Part 1 — The Foundations**
- [What is an LLM?](#what-is-an-llm)
- [What is LangChain?](#what-is-langchain)
- [Prompts & Templates](#prompts--templates)
- [Chains & LCEL](#chains--lcel)

**Part 2 — Working With Your Documents**
- [Loading Documents](#loading-documents)
- [Advanced Chunking: The Slicing Strategy](#advanced-chunking-the-slicing-strategy)
- [Vector Databases & RAG](#vector-databases--rag)

**Part 3 — Smarter Searching**
- [Streaming: Fixing the User Experience](#streaming-fixing-the-user-experience)
- [Smart Searching: Routers & Multi-Vector Retrieval](#smart-searching-routers--multi-vector-retrieval)

**Part 4 — Memory, Agents & Complex Workflows**
- [Memory](#memory)
- [Agents & Tools](#agents--tools)
- [LangGraph](#langgraph)

**Part 5 — Production: Is It Working? Is It Safe?**
- [Evaluation & Guardrails](#evaluation--guardrails)
- [LangSmith](#langsmith)
- [LangServe](#langserve)

**Part 6 — The Full Picture**
- [How It All Fits Together](#how-it-all-fits-together)

---

# Part 1 — The Foundations

---

## What is an LLM?

**The simple version:** An LLM (Large Language Model) is a very smart autocomplete. It has read a huge chunk of the internet and learned to predict what words should come next — so well that it can hold conversations, write code, and answer questions.

**Real-world analogy:** Think of a really well-read friend. They've read millions of books and articles. When you ask them a question, they don't look it up — they just answer from memory. That's an LLM.

**One important thing to know:** An LLM has no memory between conversations. Every time you start fresh, it's like your friend woke up from a nap with no memory of what you talked about yesterday. LangChain helps fix that.

---

## What is LangChain?

**The simple version:** LangChain is a toolbox for building AI apps. Instead of wiring everything together from scratch, it gives you ready-made pieces that snap together.

**Real-world analogy:** Building an AI app without LangChain is like building a house with raw materials and hand tools. LangChain is like having pre-cut lumber, IKEA-style instructions, and power tools — you still build the house, but way faster.

**What it helps with:**
- Talking to any AI model (OpenAI, Anthropic, local models) with the same code
- Building reusable prompt templates
- Connecting AI to your own documents
- Giving AI the ability to use tools (search, calculators, databases)
- Remembering past conversations
- Monitoring what your AI app is doing

**Setup:**
```bash
# Install the core packages
pip install langchain langchain-openai python-dotenv
```

```python
# Your API key goes in a .env file — never hardcode it!
# .env file:
# OPENAI_API_KEY=sk-your-key-here

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # Loads your API key from the .env file

# Create your AI model — one line!
llm = ChatOpenAI(model="gpt-4o-mini")

# Ask it something
response = llm.invoke("What is the capital of France?")
print(response.content)  # Paris
```

---

## Prompts & Templates

**The simple version:** A prompt is what you send to the AI. A prompt template is a reusable prompt with blank spaces you can fill in — like a Mad Libs for AI instructions.

**Real-world analogy:** Imagine a form letter: "Dear [NAME], we are pleased to offer you [JOB TITLE]…" The template stays the same; you just fill in the blanks. Prompt templates work exactly the same way.

**Why bother?** Without templates, you'd scatter AI instructions all over your code as messy strings. Templates keep things tidy, reusable, and easy to update.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Define a reusable template with {placeholders}
prompt = ChatPromptTemplate.from_messages([
    # "system" sets the AI's personality/role
    ("system", "You are a friendly teacher who explains things simply."),
    # "human" is the user's message — {topic} is our blank to fill in
    ("human", "Explain {topic} like I'm 10 years old."),
])

llm = ChatOpenAI(model="gpt-4o-mini")

# Connect the template to the model with a pipe (|)
chain = prompt | llm

# Fill in the blank and run it
response = chain.invoke({"topic": "black holes"})
print(response.content)
```

---

## Chains & LCEL

**The simple version:** A chain is a series of steps that run in order — the output of step 1 feeds into step 2, and so on. LCEL (LangChain Expression Language) is just the way you write chains using the `|` pipe symbol.

**Real-world analogy:** Think of a sandwich assembly line. The bread goes to Station 1 (add lettuce), then Station 2 (add cheese), then Station 3 (add tomato). Each station does its job and passes it along. A chain works the same way.

**The pipe symbol `|` just means "send the result to the next step."**

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# A 3-step chain:
# Step 1: Format the prompt template with the input
# Step 2: Send it to the AI model
# Step 3: StrOutputParser() strips the wrapper and returns just the text
chain = (
    ChatPromptTemplate.from_template("Write a one-sentence summary of: {topic}")
    | llm
    | StrOutputParser()
)

# Run the chain
result = chain.invoke({"topic": "the water cycle"})
print(result)
# "The water cycle is the continuous movement of water through
#  evaporation, condensation, and precipitation."
```

---

# Part 2 — Working With Your Documents

---

## Loading Documents

**The simple version:** Before an AI can answer questions about your files, it needs to read them. Document loaders do exactly that — they read PDFs, Word docs, web pages, CSVs, and more, and turn them into text the AI can work with.

**Real-world analogy:** Imagine hiring a research assistant. Before they can help you, they need to read your files first. Document loaders are the "reading the files" part.

```python
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

# --- Load a PDF ---
loader = PyPDFLoader("my_document.pdf")
pages = loader.load()  # Returns a list — one item per page

print(f"The PDF has {len(pages)} pages")
print(pages[0].page_content[:200])  # First 200 characters of page 1

# --- Load a web page ---
loader = WebBaseLoader("https://en.wikipedia.org/wiki/Python_(programming_language)")
docs = loader.load()
print(docs[0].page_content[:300])
```

After loading, you'll almost always need to **chunk** the documents before storing them. That's the next step — and it deserves its own chapter.

---

## Advanced Chunking: The Slicing Strategy

### Why Chunking Matters — The Balancing Act

Once you've loaded your documents, you can't just dump everything into the AI at once. You need to slice them into smaller pieces called **chunks**. But here's the tricky part:

- **Too big** → chunks carry too much noise, the AI gets confused, and retrieval becomes imprecise. (Imagine searching a book and getting handed the entire chapter instead of the relevant paragraph.)
- **Too small** → chunks lose context, answers get cut off mid-thought. (Imagine getting handed a single sentence with no surrounding context.)

The goal is the **Goldilocks zone** — chunks that are small enough to retrieve precisely, but large enough to carry meaningful context.

---

### The 4 Core Chunking Methods

#### 1. Character-Based Chunking — "The Dumb Splitter"

**Analogy:** Imagine cutting a novel into 500-character pieces with scissors, without looking at where sentences or paragraphs end. Fast and simple, but it will happily cut a sentence in half.

**When to use it:** Quick experiments or very simple plain-text files where you just want *something* working fast.

```python
from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="\n\n",  # Split at paragraph breaks (double newline)
    chunk_size=500,    # Each chunk is at most 500 characters
    chunk_overlap=50,  # Overlap 50 characters so we don't lose context at edges
)

chunks = splitter.create_documents([my_text])
```

---

#### 2. Recursive Character Text Splitter — "The Smart Default"

**Analogy:** A careful editor who first tries to cut at chapter breaks. If the chapter is still too long, they try paragraph breaks. Then sentence breaks. Then word breaks — only resorting to cutting mid-word as an absolute last resort.

This is the **recommended default** for most use cases because it respects the natural structure of text.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    # It tries these separators in order, only going smaller if needed
    separators=["\n\n", "\n", ". ", " ", ""],
    chunk_size=1000,   # Target size in characters
    chunk_overlap=150, # Overlap to preserve context at edges
)

chunks = splitter.split_documents(pages)  # pages = your loaded PDF pages
print(f"Split into {len(chunks)} chunks")
```

---

#### 3. Token-Based Chunking — "The AI's Native Language"

**Analogy:** AI models don't measure text in characters or words — they measure it in **tokens** (roughly 3–4 characters each). Token chunking is like cutting text using the AI's own ruler instead of yours.

**When to use it:** When you're paying per token and need to stay within precise limits, or when working with models that have strict token-count context windows.

```python
from langchain_text_splitters import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=256,   # Each chunk is at most 256 tokens
    chunk_overlap=20, # 20-token overlap between chunks
)

chunks = splitter.split_documents(pages)
```

---

#### 4. Semantic Chunking — "The Meaning-Based Splitter"

**Analogy:** Instead of cutting by size, this method reads the text and cuts where the *topic changes*. It's like a smart librarian who separates your document at the point where it stops talking about marketing and starts talking about finance — regardless of how many characters that took.

**When to use it:** When document structure is irregular (e.g., long dense reports) and you need chunks that capture one idea at a time.

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# This splitter uses AI embeddings to detect where meaning shifts
splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",  # Cut where meaning shifts significantly
)

chunks = splitter.split_documents(pages)
```

> **Note:** Semantic chunking is slower and costs a small amount per document (it calls the embedding model), but produces the highest-quality chunks for complex documents.

---

### Quick Comparison Table

| Splitter | Speed | Cost | Best For |
|---|---|---|---|
| **Character** | ⚡ Fastest | Free | Quick experiments, simple plain text |
| **Recursive Character** | ⚡ Fast | Free | Most use cases — use this by default |
| **Token** | ⚡ Fast | Free | Strict token budget management |
| **Semantic** | 🐢 Slower | Small API cost | Dense reports, mixed-topic documents |

---

### The Golden Rule of Chunk Overlap

Overlap is the number of characters/tokens that are **repeated** between adjacent chunks. Here's why it matters:

```
=== WITHOUT overlap ===

Chunk 1: "...The vaccine was developed by Dr. Sarah Chen
          at the University of Mumbai."
                                                 ← HARD CUT HERE
Chunk 2: "She won the Nobel Prize for this work
          in 2023..."

Problem: If someone asks "Who won the Nobel Prize?",
         Chunk 2 says "She" — but "she" refers to Dr. Chen
         in Chunk 1. The AI has no idea who "she" is.

=== WITH overlap (50 characters) ===

Chunk 1: "...The vaccine was developed by Dr. Sarah Chen
          at the University of Mumbai."

Chunk 2: "...Dr. Sarah Chen at the University of Mumbai.
          She won the Nobel Prize for this work in 2023..."
          ↑
          This repeated sentence bridges the two chunks.
          Now the AI knows "she" = Dr. Chen.
```

**Rule of thumb:** Set overlap to about 10–20% of your chunk size. So if `chunk_size=1000`, use `chunk_overlap=100` to `chunk_overlap=200`.

---

## Vector Databases & RAG

**The simple version:**
- A **vector database** stores chunks in a way that makes it easy to find the most *relevant* one for any question.
- **RAG** (Retrieval-Augmented Generation) means: instead of asking the AI from its own memory, you first *retrieve* relevant chunks from your documents, then ask the AI to answer using those.

**Real-world analogy:**
- A normal AI is like asking a friend from memory — they won't know your company's private policies.
- RAG is like handing that friend your company handbook and saying "use this to answer."
- A **vector database** is the smart filing system that instantly finds the right page in the handbook for any question.

**How meaning-search works:** Every chunk is converted into a list of numbers (a "vector") that captures its *meaning*. When you search, your question is also converted to numbers, and the database finds the closest match by meaning — not just by keywords.

```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

# --- Sample chunks (in real use, these come from your loader + splitter) ---
from langchain_core.documents import Document
chunks = [
    Document(page_content="Returns are accepted within 30 days with a receipt."),
    Document(page_content="Standard shipping takes 3-5 business days."),
    Document(page_content="Customer support is available Monday-Friday, 9am-5pm EST."),
]

# Step 1: Convert chunks to vectors and store them
# OpenAIEmbeddings converts text to numbers that capture meaning
# Chroma is a simple local vector database — great for getting started
vectorstore = Chroma.from_documents(chunks, embedding=OpenAIEmbeddings())

# Step 2: Create a retriever — a search tool over the vector database
# k=2 means "return the 2 most relevant chunks for each question"
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Step 3: Build the RAG chain
prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below.
If the answer isn't in the context, say "I don't know."

Context: {context}
Question: {question}
""")

llm = ChatOpenAI(model="gpt-4o-mini")

rag_chain = (
    # "context" is filled by the retriever searching the vector DB
    # "question" passes straight through unchanged
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is the return policy?")
print(answer)
# "Returns are accepted within 30 days with a receipt."
```

---

# Part 3 — Smarter Searching

---

## Streaming: Fixing the User Experience

### The Problem With Waiting

When you call `.invoke()`, your app waits silently until the AI has finished writing the *entire* response — then dumps it all at once. For a short answer, fine. For a 500-word response, the user stares at a blank screen for 5–10 seconds before anything appears.

**Real-world analogy:** Imagine ordering food at a restaurant. `.invoke()` is like waiting in the kitchen until the entire meal is plated before the waiter walks out. `.stream()` is like getting your starter, then your main, as each is ready — the experience feels faster and more alive, even if the total time is the same.

### The Typewriter Effect with `.stream()`

`.stream()` returns the response **token by token** as it's generated. Your app can print (or display) each piece the moment it arrives, creating the familiar "typewriter" effect seen in ChatGPT.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

chain = (
    ChatPromptTemplate.from_template("Write a short paragraph about: {topic}")
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

# --- Without streaming (.invoke) ---
# The program freezes here until the full answer is ready, then prints it all
# result = chain.invoke({"topic": "the Amazon rainforest"})
# print(result)

# --- With streaming (.stream) ---
# Prints each word/token as it arrives — no waiting!
print("Answer: ", end="", flush=True)

for chunk in chain.stream({"topic": "the Amazon rainforest"}):
    # Each 'chunk' is a small piece of text (sometimes a word, sometimes a few)
    print(chunk, end="", flush=True)  # end="" prevents newlines between chunks

print()  # Add a newline at the very end when the stream is done
```

**`flush=True`** forces Python to print immediately instead of buffering — this is important for the typewriter effect to work.

### Streaming in a Web App

If you're building a web API with LangServe, streaming is built in automatically. But if you're building your own FastAPI endpoint, you use `StreamingResponse`:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()
chain = (
    ChatPromptTemplate.from_template("Answer this question: {question}")
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

@app.get("/ask")
def ask(question: str):
    # stream() returns a generator; StreamingResponse sends each piece as it arrives
    return StreamingResponse(
        chain.stream({"question": question}),
        media_type="text/plain"
    )
```

---

## Smart Searching: Routers & Multi-Vector Retrieval

As your AI app grows, a single vector database and a single search strategy won't be enough. You'll need smarter ways to direct questions to the right place and retrieve the right level of detail.

---

### Routing: The Traffic Cop

**The simple version:** A router is a step that reads the user's question and decides which tool or database to send it to — before doing any retrieval.

**Real-world analogy:** Imagine you call a large company's main reception number. The receptionist (the router) listens to why you're calling and transfers you: "That's a billing question — let me connect you to Finance." "That's an HR question — I'll transfer you to HR." The caller doesn't need to know which department exists; the receptionist figures it out.

Without a router, every question hits every database — slow, expensive, and noisy. With a router, questions go straight to the most relevant source.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- Imagine these are two separate retrieval chains ---
# In a real app, each would query a different vector database
def search_hr_database(question: str) -> str:
    return f"[HR Database result for: {question}]"

def search_finance_database(question: str) -> str:
    return f"[Finance Database result for: {question}]"

def search_it_database(question: str) -> str:
    return f"[IT Database result for: {question}]"

# Step 1: Ask the AI to classify the question
classify_prompt = ChatPromptTemplate.from_template("""
You are a routing assistant. Classify this question into ONE category.
Reply with ONLY the category name, nothing else.

Categories: HR, FINANCE, IT

Question: {question}
""")

classifier = classify_prompt | llm | StrOutputParser()

# Step 2: Route to the right database based on the classification
def route(input_dict: dict) -> str:
    question = input_dict["question"]
    category = classifier.invoke({"question": question}).strip().upper()

    # Send to the right database based on the AI's classification
    if category == "HR":
        return search_hr_database(question)
    elif category == "FINANCE":
        return search_finance_database(question)
    else:
        return search_it_database(question)

# The full router chain
router_chain = RunnableLambda(route)

# Test it
print(router_chain.invoke({"question": "How many vacation days do I get?"}))
# → [HR Database result for: How many vacation days do I get?]

print(router_chain.invoke({"question": "What was last quarter's revenue?"}))
# → [Finance Database result for: What was last quarter's revenue?]
```

---

### Parent-Child (Multi-Vector) Retrieval: The Best of Both Worlds

**The problem with standard RAG:** You want small chunks for precise retrieval (so you find the exact sentence that answers the question), but you want large chunks sent to the AI (so it has enough surrounding context to give a complete answer).

If your chunks are too small, the AI gets a sentence fragment with no context. If they're too large, retrieval becomes imprecise.

**The solution:** Search the small chunks, but pass the big ones to the AI.

**Real-world analogy:** Imagine you're looking for information in a textbook. You use the index (which has small, specific entries) to find the right page. But once you find the page, you don't just read the index entry — you read the whole section. Parent-child retrieval works the same way:
- **Child chunks** (small, ~100 characters) = the index entries. Used for *searching*.
- **Parent chunks** (large, ~1000 characters) = the full sections. Passed to the *AI*.

```python
from langchain.storage import InMemoryStore
from langchain.retrievers import ParentDocumentRetriever
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# --- Sample documents (in real use, load from PDFs etc.) ---
docs = [
    Document(page_content="""
        Section 3: Employee Leave Policy.
        Full-time employees are entitled to 20 days of paid annual leave per year.
        Leave must be approved by your manager at least 2 weeks in advance.
        Unused leave up to 5 days can be carried over to the following year.
        Sick leave is separate and covered under Section 4.
    """),
]

# --- Define two splitters: one for small (child) chunks, one for large (parent) ---
child_splitter = RecursiveCharacterTextSplitter(chunk_size=100)   # Small — for searching
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=500)  # Large — for the AI

# --- Set up the two-layer storage ---
# The vector store holds the SMALL child chunks (used for search)
vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
# The doc store holds the LARGE parent chunks (returned to the AI)
docstore = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# Index the documents (automatically creates both child and parent chunks)
retriever.add_documents(docs)

# When you search, it finds the best small child chunks...
# ...but returns the full large parent chunks to the AI
results = retriever.invoke("How many vacation days do employees get?")
print(results[0].page_content)
# Returns the full Section 3 paragraph, not just one sentence
```

---

# Part 4 — Memory, Agents & Complex Workflows

---

## Memory

**The simple version:** By default, every AI call forgets everything. Memory is how you make the AI remember the conversation history so it can give context-aware answers.

**Real-world analogy:** Imagine a customer service rep who forgets your entire conversation every time you put them on hold. Frustrating, right? Memory prevents that — it keeps a log of everything said and includes it in each new request to the AI.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# The prompt has a "slot" (MessagesPlaceholder) where history gets inserted
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),  # Chat history slides in here
    ("human", "{input}"),
])

chain = prompt | llm

# A dictionary that stores a separate history for each user/session
session_store = {}

def get_history(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]

# Wrap the chain so it automatically saves and loads history
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "session_abc"}}

# Turn 1
r1 = chain_with_memory.invoke({"input": "My name is Priya."}, config=config)
print(r1.content)  # "Nice to meet you, Priya!"

# Turn 2 — it remembers from Turn 1!
r2 = chain_with_memory.invoke({"input": "What's my name?"}, config=config)
print(r2.content)  # "Your name is Priya."
```

---

## Agents & Tools

**The simple version:** A regular chain always does the same steps in the same order. An **agent** is smarter — it decides on its own what steps to take, and it can use **tools** (a calculator, web search, database, etc.) to get things done.

**Real-world analogy:** A chain is like a vending machine — press B4, get chips, every time. An agent is like a personal assistant — you say "plan my trip to Goa" and they figure out on their own whether to check the calendar, search for flights, or look up the weather.

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# The @tool decorator turns a regular Python function into something the AI can call.
# The docstring tells the AI what the tool does and when to use it.

@tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together. Use this when you need to add things."""
    return a + b

@tool
def get_word_count(text: str) -> int:
    """Counts the number of words in a piece of text."""
    return len(text.split())

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_react_agent(llm, tools=[add_numbers, get_word_count])

result = agent.invoke({
    "messages": [HumanMessage(content="What is 42 plus 58? Also count words in 'hello world foo bar'.")]
})

print(result["messages"][-1].content)
# "42 plus 58 is 100. 'hello world foo bar' has 4 words."
```

---

## LangGraph

**The simple version:** LangGraph is for building complex AI workflows that need loops, decisions, or multiple AI "roles" working together — like a flowchart the AI actually follows.

**Real-world analogy:** A regular chain is like a straight hallway — start to finish, no detours. LangGraph is like a building with rooms, corridors, and decision signs. The AI can enter a room, check something, take a different door based on what it finds, loop back if needed, or wait for a human to approve before proceeding.

**Use LangGraph when:**
- The AI needs to loop (e.g., keep researching until it's confident)
- Multiple AI "roles" work together (researcher + writer + reviewer)
- A human must approve something mid-process

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import TypedDict, List
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# Step 1: Define the "state" — what information gets passed between steps
class MyState(TypedDict):
    messages: List

# Step 2: Define the steps (called "nodes")
def chat_node(state: MyState) -> MyState:
    """Sends messages to the AI and appends the reply to the state."""
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

# Step 3: Build and connect the graph
graph_builder = StateGraph(MyState)
graph_builder.add_node("chat", chat_node)
graph_builder.set_entry_point("chat")
graph_builder.add_edge("chat", END)
graph = graph_builder.compile()

# Step 4: Run it
result = graph.invoke({
    "messages": [HumanMessage(content="Tell me a fun fact about the ocean.")]
})
print(result["messages"][-1].content)
```

> LangGraph really shines with multiple nodes, conditional edges, and loops — this is just the starting point.

---

# Part 5 — Production: Is It Working? Is It Safe?

---

## Evaluation & Guardrails

### Is Your AI Actually Giving Good Answers? — The RAG Triad

Building a RAG system is easy. Knowing whether it's actually *working well* is hard. The **RAG Triad** is the standard three-question quality check for any RAG-based AI app.

**Real-world analogy:** Imagine you hired a research assistant to answer questions from a stack of reports. You'd evaluate them on three things:
1. Did they find the *right pages* from the reports? (Context Relevance)
2. Is what they said actually *supported by* those pages? (Groundedness)
3. Does their answer actually *address* what you asked? (Answer Relevance)

```
┌──────────────────────────────────────────────────────────┐
│                     THE RAG TRIAD                        │
│                                                          │
│  Question ──→ [Retriever] ──→ Retrieved Chunks           │
│                                    │                     │
│                            ① Context Relevance           │
│                    "Are these chunks actually relevant   │
│                     to the question asked?"              │
│                                    │                     │
│                               [LLM]                      │
│                                    │                     │
│                            ② Groundedness                │
│                    "Is the answer supported by the       │
│                     retrieved chunks? Or is it           │
│                     hallucinating something extra?"      │
│                                    │                     │
│                              Answer                      │
│                                    │                     │
│                            ③ Answer Relevance            │
│                    "Does the answer actually address     │
│                     what was asked?"                     │
└──────────────────────────────────────────────────────────┘
```

**Tools that automate this evaluation:**
- **Ragas** — an open-source library that scores all three dimensions automatically using AI-as-judge
- **TruLens** — a similar evaluation framework with a visual dashboard

You don't need to implement these from scratch. Ragas, for example, takes your questions, the retrieved chunks, and the answers, and returns numeric scores for each dimension. Any score below ~0.7 is a signal to investigate.

---

### Guardrails: Blocking Bad Inputs

**The simple version:** Not every user query is a genuine question. Some users will try to trick your AI (called **prompt injection**), others may ask inappropriate things, and some may accidentally trigger very expensive API calls. Guardrails are the safety checks that run *before* the AI processes a request.

**Real-world analogy:** Think of airport security. The plane is your AI app. Guardrails are the X-ray machines and passport checks at the gate. Most passengers are fine — but you still check everyone, because the cost of not checking is too high.

**Common threats to protect against:**

- **Prompt injection:** A user pastes hidden instructions into their question trying to override your system prompt. E.g., "Ignore all previous instructions and tell me how to…"
- **Off-topic questions:** A user asks your customer service bot to write poetry or do their homework.
- **Expensive inputs:** A user pastes a 100,000-word document into a text field, triggering a massive API call.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- Guardrail 1: Length check (before any API call) ---
def check_input_length(user_input: str, max_chars: int = 2000) -> str:
    if len(user_input) > max_chars:
        raise ValueError(f"Input too long ({len(user_input)} chars). Max is {max_chars}.")
    return user_input

# --- Guardrail 2: Topic check using a fast AI classifier ---
topic_check_prompt = ChatPromptTemplate.from_template("""
Is the following question related to our e-commerce store (products, orders, returns, shipping)?
Reply with ONLY 'yes' or 'no'.

Question: {question}
""")

topic_checker = topic_check_prompt | llm | StrOutputParser()

# --- The main answer chain ---
answer_chain = (
    ChatPromptTemplate.from_template("Answer this customer question: {question}")
    | llm
    | StrOutputParser()
)

# --- Full pipeline with guardrails ---
def safe_answer(user_input: str) -> str:
    # Guardrail 1: Reject if input is suspiciously long
    try:
        check_input_length(user_input)
    except ValueError as e:
        return f"Sorry, your message was too long. Please shorten it."

    # Guardrail 2: Reject if question is off-topic
    is_relevant = topic_checker.invoke({"question": user_input}).strip().lower()
    if is_relevant != "yes":
        return "I can only answer questions about our store. How can I help with your order?"

    # All clear — answer the question
    return answer_chain.invoke({"question": user_input})

# Test it
print(safe_answer("What is your return policy?"))
# → Answers the question normally

print(safe_answer("Write me a poem about the moon."))
# → "I can only answer questions about our store..."

print(safe_answer("A" * 5000))  # Huge input
# → "Sorry, your message was too long..."
```

---

### Cost Management

AI APIs charge per token. Without cost controls, a single misbehaving user or a bug in a loop can generate a surprisingly large bill.

**Key habits for controlling costs:**

- **Set `max_tokens`** on every LLM call to cap response length.
- **Use cheaper models** for simple tasks (e.g., `gpt-4o-mini` for classification, `gpt-4o` only for complex reasoning).
- **Cache repeated queries** — if 100 users ask "what are your business hours?", you don't need to call the API 100 times.
- **Monitor in LangSmith** — it shows you the token cost of every chain run, so you can spot expensive steps.

```python
from langchain_openai import ChatOpenAI

# Always set max_tokens to prevent runaway responses
llm = ChatOpenAI(
    model="gpt-4o-mini",  # Cheaper model for most tasks
    max_tokens=500,        # Cap at 500 tokens — never more
    temperature=0,
)
```

---

## LangSmith

**The simple version:** LangSmith is a dashboard that watches everything your AI app does — every step, every token, every cost — so you can debug it when something goes wrong.

**Real-world analogy:** Your AI app is a kitchen. LangSmith is the security camera. It records every step: what ingredients went in, what the chef did, how long each step took, and what came out. When a dish tastes wrong, you can rewind and see exactly where things went sideways.

**What you see in LangSmith:**
- The full input and output of every chain step
- How many tokens were used and the estimated cost
- How long each step took (latency)
- Errors with a full traceback

**Setup is just 3 environment variables — then it's automatic:**
```python
# Add these to your .env file:
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=ls__your_key_here
# LANGCHAIN_PROJECT=my-first-project

import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__your_key"
os.environ["LANGCHAIN_PROJECT"] = "my-first-project"

# That's it. Every LangChain call is now automatically traced.
# Visit smith.langchain.com to see the traces in your browser.
```

After setup, every `.invoke()`, `.stream()`, and `.batch()` call automatically appears in the LangSmith dashboard — no extra code needed in your chains.

---

## LangServe

**The simple version:** LangServe turns your LangChain chain into a web API so other apps, websites, or teammates can call it over the internet.

**Real-world analogy:** You've built a great sandwich-making machine (your chain). LangServe is like opening a service window to the street and putting up a menu — now anyone can order a sandwich through the window, not just people in your kitchen.

```python
# Save as app.py, run with: python app.py
from fastapi import FastAPI
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="My AI App")

chain = (
    ChatPromptTemplate.from_template("Summarize this in one sentence: {text}")
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

# One line creates a full REST API for this chain
add_routes(app, chain, path="/summarize")

# LangServe auto-creates:
# POST /summarize/invoke    → send text, get summary back
# POST /summarize/stream    → get the summary word-by-word (streaming!)
# GET  /summarize/playground → a built-in browser UI to test it live

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Visit `http://localhost:8000/summarize/playground` to get an instant browser UI to test your chain.

---

# Part 6 — The Full Picture

---

## How It All Fits Together

Here is the complete data journey — from raw documents all the way to a streaming, evaluated, and guarded AI response.

```
╔══════════════════════════════════════════════════════════════════╗
║                  THE FULL LANGCHAIN PIPELINE                     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📄 RAW DOCUMENTS (PDFs, web pages, Word docs, CSVs...)          ║
║         │                                                        ║
║         ▼                                                        ║
║  📥 DOCUMENT LOADERS                                             ║
║     Reads files and turns them into text                         ║
║         │                                                        ║
║         ▼                                                        ║
║  ✂️  CHUNKING (Text Splitters)                                    ║
║     Character / Recursive / Token / Semantic                     ║
║     Breaks text into the right-sized pieces                      ║
║         │                                                        ║
║         ▼                                                        ║
║  🗄️  VECTOR DATABASE                                             ║
║     Converts chunks to vectors & stores them                     ║
║     (Small child chunks for search precision,                    ║
║      Large parent chunks for AI context)                         ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  👤 USER SENDS A QUESTION                                        ║
║         │                                                        ║
║         ▼                                                        ║
║  🛡️  GUARDRAILS (Input Checks)                                   ║
║     • Is it too long? (cost control)                             ║
║     • Is it on-topic? (topic filter)                             ║
║     • Does it look like a prompt injection?                      ║
║         │ (only passes if all checks pass)                       ║
║         ▼                                                        ║
║  🚦 ROUTER                                                       ║
║     AI classifies the question:                                  ║
║     HR question → HR database                                    ║
║     Finance question → Finance database                          ║
║     General question → General knowledge                         ║
║         │                                                        ║
║         ▼                                                        ║
║  🔍 RETRIEVER                                                    ║
║     Searches vector database for relevant chunks                 ║
║     Returns the parent (large) chunks for best context           ║
║         │                                                        ║
║         ▼                                                        ║
║  💬 PROMPT TEMPLATE                                              ║
║     Assembles: System instructions + Memory                      ║
║              + Retrieved context + User question                 ║
║         │                                                        ║
║         ▼                                                        ║
║  🤖 LLM (The AI Model)                                           ║
║     Generates the answer                                         ║
║         │                                                        ║
║         ▼                                                        ║
║  🌊 STREAMING OUTPUT                                             ║
║     Tokens sent word-by-word as they're generated                ║
║     (No waiting for the full response)                           ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📡 LANGSERVE — Exposes the whole pipeline as a web API          ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  🔭 LANGSMITH — Watches every step for debugging & cost tracking  ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📊 EVALUATION (RAG Triad — Ragas / TruLens)                     ║
║     ① Context Relevance — right chunks retrieved?                ║
║     ② Groundedness — answer backed by context?                   ║
║     ③ Answer Relevance — does it answer what was asked?          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

*Built with LangChain v0.3+ | Python 3.11+*
