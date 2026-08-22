# TOPIC 9: AI Agents & Tool Calling

## 1. Executive Summary
- AI Agents: LLMs that can take actions (call tools/APIs) to accomplish multi-step goals
- Tool Calling: structured mechanism for LLMs to request function execution
- Solve: tasks requiring external data, computation, or multiple sequential decisions
- Problem it solves: LLMs alone are static; agents extend them with world access
- Key insight: agent = LLM + tools + loop (perceive → reason → act → observe)
- Where it fits: above RAG; the most powerful and complex GenAI pattern
- Engineering concern: agents are non-deterministic; testing and reliability are hard
- Production agents require: tool validation, loop detection, cost limits, observability

## 2. Mental Model
- **Analogy**: An agent is like an employee with a phone and computer. You give them a goal; they figure out which tools to use and execute the steps.
- **ReAct loop**: Reason → Act → Observe → Reason → ... → Final Answer
- **Tool calling**: LLM speaks JSON; app executes the function; app returns result to LLM

```
User Goal
    ↓
LLM: "I need to [reason]. I'll call [tool] with [args]."
    ↓
Tool Execution (code runs)
    ↓
Observation returned to LLM
    ↓
LLM: "Based on [observation], I'll now [reason]. Call [tool2]..."
    ↓
Repeat until: LLM says "Final Answer: ..."
```

## 3. Core Concepts

| Concept | Definition |
|---------|-----------|
| Tool | A function the agent can call (search, calculator, DB query, API call) |
| Tool Schema | JSON schema defining tool name, description, parameters | 
| Function Calling | OpenAI's structured tool invocation format |
| ReAct | Reason + Act pattern — most common agent pattern |
| Planning | Agent creates multi-step plan before executing |
| Observation | Result returned after tool execution |
| Agent Loop | Reason → Act → Observe cycle |
| Max Iterations | Safety limit on agent loop iterations |
| Tool Router | LLM selects which tool to use |
| Structured Output | Tool calls are structured JSON — parseable |

## 4. Engineering Deep Dive

### Tool Calling with OpenAI
```python
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": "Search the document database for relevant information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "top_k": {"type": "integer", "description": "Number of results", "default": 5}
            },
            "required": ["query"]
        }
    }
}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What are our Q3 revenue figures?"}],
    tools=tools,
    tool_choice="auto"
)

# Check if tool was called
if response.choices[0].finish_reason == "tool_calls":
    tool_call = response.choices[0].message.tool_calls[0]
    func_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    # Execute tool
    result = search_documents(**args)
    
    # Return result to LLM
    messages.append(response.choices[0].message)  # Assistant message with tool_calls
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(result)
    })
    
    # Continue conversation
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )
```

### Tool Calling with Bedrock (Converse API)
```python
tools = [{
    "toolSpec": {
        "name": "search_documents",
        "description": "Search documents",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    }
}]

response = bedrock.converse(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    messages=messages,
    toolConfig={"tools": tools}
)

# Handle tool use
for block in response['output']['message']['content']:
    if block['type'] == 'toolUse':
        tool_name = block['name']
        tool_input = block['input']
        tool_use_id = block['toolUseId']
        
        # Execute and return result
        result = execute_tool(tool_name, tool_input)
        messages.append({'role': 'assistant', 'content': response['output']['message']['content']})
        messages.append({'role': 'user', 'content': [{'toolResult': {'toolUseId': tool_use_id, 'content': [{'text': str(result)}]}}]})
```

### LangChain Agent
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search documents. Use for factual questions."""
    return vector_search(query)

@tool
def calculator(expression: str) -> str:
    """Calculate math expressions."""
    return str(eval(expression))

agent = create_tool_calling_agent(llm, [search, calculator], prompt)
executor = AgentExecutor(agent=agent, tools=[search, calculator], max_iterations=10, verbose=True)
result = executor.invoke({"input": "What is 15% of our Q3 revenue of $2.3M?"})
```

### Agent Design Patterns

| Pattern | Description | Use Case |
|---------|-------------|---------|
| ReAct | Reason then act alternately | General purpose |
| Plan-and-Execute | Plan all steps first, then execute | Complex multi-step |
| MRKL | Mixture of expert tools with router | Specialized tools |
| Self-Ask | Agent asks itself sub-questions | Multi-hop reasoning |
| Reflexion | Agent reflects on failures and retries | High quality required |
| Tree of Thoughts | Explore multiple reasoning paths | Hard reasoning |

### Tool Design Best Practices
1. **Clear descriptions**: LLM decides which tool to use based on description
2. **Narrow scope**: Each tool does one thing well
3. **Validate inputs**: Tools should validate before executing
4. **Return structured output**: JSON is better than free text for LLM consumption
5. **Handle errors gracefully**: Return error description, not Python exception
6. **Log all calls**: Essential for debugging
7. **Rate limit**: Prevent agents from hammering APIs
8. **Idempotent writes**: Especially for side-effecting tools

## 5. Architecture Perspective

### When to Use Agents
- Task requires dynamic decisions about what to do next
- Multiple tools needed in flexible order
- Task unknown upfront — agent must discover approach

### When NOT to Use Agents
- Deterministic workflow with known steps → use LangGraph DAG
- Performance critical → agents add latency per loop iteration
- High-stakes without human oversight → dangerous non-determinism
- Simple RAG → overkill

### Agent vs Workflow

| Aspect | Agent | Workflow (LangGraph) |
|--------|-------|---------------------|
| Control flow | LLM decides | You decide (code) |
| Predictability | Low | High |
| Flexibility | High | Medium |
| Debugging | Hard | Easier |
| Latency | High | Lower |
| Cost | High (many LLM calls) | Controlled |

## 6. Failure Modes & Debugging

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Agent loop | No termination condition | Max iterations exceeded | Set max_iterations, add explicit "DONE" signal |
| Tool hallucination | LLM invents tool names | ToolNotFound error | Strict tool validation, structured tool spec |
| Wrong tool selection | Ambiguous tool descriptions | Wrong output | Clear, distinct tool descriptions |
| Cost explosion | Too many iterations | API spend alert | max_iterations + cost_limit |
| Incorrect tool args | LLM misformats JSON | Pydantic validation error | Retry with error message |
| Prompt injection via tools | Tool returns adversarial content | Unexpected behavior | Sanitize tool outputs |
| Cascading errors | Tool failure causes bad next step | Early loop termination | Error handling per tool, retry logic |

## 7. End-to-End Flow
```
User: "What was our top-selling product in Q3 and how does it compare to Q2?"

Agent Iteration 1:
Thought: I need Q3 sales data
Action: query_database(sql="SELECT product, revenue FROM sales WHERE quarter='Q3'")
Observation: [{"product": "Widget A", "revenue": 450000}, ...]

Agent Iteration 2:
Thought: Now I need Q2 data for comparison
Action: query_database(sql="SELECT product, revenue FROM sales WHERE quarter='Q2'")
Observation: [{"product": "Widget A", "revenue": 380000}, ...]

Agent Iteration 3:
Thought: I have both quarters' data, can calculate comparison
Action: calculator(expression="(450000 - 380000) / 380000 * 100")
Observation: "18.42"

Final:
Answer: Widget A was our top-selling product in Q3 with $450K revenue, up 18.4% from Q2's $380K.
```

## 8. Terminology Cheat Sheet

| Term | Meaning | Why It Matters |
|------|---------|---------------|
| Tool | Callable function with schema | Agent's capabilities |
| Function Calling | Structured LLM → function invocation | Reliable tool use |
| Finish Reason | `tool_calls` or `stop` | Know when to execute vs when done |
| Tool Use ID | Unique ID linking call to result | Required for message threading |
| Max Iterations | Safety limit on agent loop | Prevent infinite loops |
| ReAct | Reason + Act pattern | Standard agent pattern |
| Scratchpad | Internal agent reasoning trace | Debugging |
| Parallel Tool Calls | Multiple tools called in one step | Faster agents |

## 10. Interview Revision

### Senior Questions

**Q1: How do you prevent agent infinite loops in production?**
- **Answer**: max_iterations parameter (hard limit). Time budget (wall clock timeout). Cost limit (track API spend per session). Explicit termination tools ("I'm done" signals). Loop detection (detect repeated tool calls with same args).

**Q2: How do you make tool calling reliable for production?**
- **Answer**: Strong tool descriptions (LLM selects based on them). Pydantic models for input/output validation. Retry with error feedback on invalid calls. Idempotent writes. Input sanitization. Structured output with JSON mode.

**Q3: When would you choose agents over a deterministic workflow?**
- **Answer**: When the decision of WHICH step to take next cannot be hardcoded (e.g., research task where depth is unknown). When steps depend on intermediate results in unpredictable ways. When flexibility > reliability need.

## 12. One-Page Revision Sheet

### Must Know
- ReAct: Reason → Act → Observe loop
- Tool calling: LLM returns JSON, app executes, app returns result
- max_iterations: safety limit, always set it
- Tool description quality = tool selection quality

### Production Nuggets
- Log every tool call and result — essential for debugging
- Validate tool outputs before feeding back to LLM
- Cost per agent run can be 10-50× simple LLM call

### Common Traps
- Agents without max_iterations → infinite loop risk
- Poor tool descriptions → LLM picks wrong tool
- Not handling tool failures gracefully → cascade failures

---

# TOPIC 10: LangGraph Fundamentals

## 1. Executive Summary
- LangGraph: workflow engine for building stateful multi-step AI systems as directed graphs
- Solves: complex agent workflows where LangChain's linear chains are insufficient
- Provides: nodes (logic), edges (transitions), state (shared data), conditional routing
- Key insight: not every AI workflow is a chain — some need loops, branches, human oversight
- Where it fits: orchestration layer for complex agents and multi-agent systems
- Built on top of LangChain, uses LCEL components as nodes
- Production advantages: explicit state machine = testable, debuggable, observable
- Native support for persistence, interrupts, human-in-the-loop, streaming

## 2. Mental Model
- **Analogy**: A state machine where each node is an LLM call or tool execution, and edges are routing rules
- **Comparison**: LangChain = Unix pipes; LangGraph = Kubernetes workflows
- **Key mental model**: 
```
State = {messages: [...], context: "...", step: "retrieve"}
Graph: nodes transform state; edges route to next node based on state
```

```
                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           ↓
                    ┌─────────────┐
                    │  Retriever  │──────────→ [state.context updated]
                    └──────┬──────┘
                           ↓
              ┌────────────┴────────────┐
              ↓ (has context)           ↓ (no context found)
    ┌────────────────┐        ┌──────────────────┐
    │   Generator    │        │  Fallback Answer │
    └────────┬───────┘        └────────┬─────────┘
             ↓                         ↓
          ┌──────────────────────────────┐
          │            END               │
          └──────────────────────────────┘
```

## 3. Core Concepts

| Concept | Definition |
|---------|-----------|
| StateGraph | The graph class — nodes + edges + state schema |
| State | TypedDict or Pydantic model — shared across all nodes |
| Node | Python function that takes state, returns partial state update |
| Edge | Unconditional transition between nodes |
| Conditional Edge | Edge that routes based on state value (function returns next node name) |
| START / END | Special nodes marking graph entry/exit |
| Compile | Turn graph definition into executable Runnable |
| Interrupt | Pause graph execution for human review |
| Checkpointer | Persist state to resume later (SQLite, Redis, Postgres) |
| Subgraph | A LangGraph used as a node in another graph |
| Channel | How state fields are updated (Append vs Replace) |
| Annotation | Type hints for state with reducer functions |

## 4. Engineering Deep Dive

### Basic LangGraph
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import AnyMessage
import operator

# Define state
class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]  # Append mode
    context: str
    retrieved: bool

# Define nodes
def retrieve(state: AgentState) -> dict:
    query = state["messages"][-1].content
    docs = retriever.invoke(query)
    return {"context": format_docs(docs), "retrieved": True}

def generate(state: AgentState) -> dict:
    response = llm.invoke([
        SystemMessage("Use context: " + state["context"]),
        *state["messages"]
    ])
    return {"messages": [response]}

def should_retrieve(state: AgentState) -> str:
    if state.get("retrieved"):
        return "generate"
    return "retrieve"

# Build graph
graph = StateGraph(AgentState)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)

graph.add_edge(START, "retrieve")
graph.add_conditional_edges("retrieve", should_retrieve, {
    "generate": "generate",
    "retrieve": "retrieve"  # loop
})
graph.add_edge("generate", END)

app = graph.compile()
result = app.invoke({"messages": [HumanMessage("What is RAG?")], "retrieved": False})
```

### Human-in-the-Loop
```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string(":memory:")
app = graph.compile(checkpointer=checkpointer, interrupt_before=["write_to_db"])

config = {"configurable": {"thread_id": "session-123"}}

# Run until interrupt
result = app.invoke(inputs, config=config)
# ... show user what will be written ...

# User approves → continue
result = app.invoke(None, config=config)  # Resume from checkpoint
```

### Multi-Agent Pattern (Supervisor)
```python
# Supervisor decides which agent to call next
def supervisor(state):
    response = llm.invoke(messages + [SystemMessage(f"Pick next: {workers}")])
    return {"next": parse_next_worker(response)}

def route_to_worker(state):
    return state["next"]  # Returns worker name or "FINISH"

builder = StateGraph(OverallState)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", research_agent)
builder.add_node("writer", write_agent)

builder.add_conditional_edges("supervisor", route_to_worker, 
    {"researcher": "researcher", "writer": "writer", "FINISH": END})
builder.add_edge("researcher", "supervisor")  # Report back
builder.add_edge("writer", "supervisor")      # Report back
```

### State Reducers
```python
from typing import Annotated
import operator

# Default: REPLACE on update
class State(TypedDict):
    counter: int  # Last write wins

# Append mode for message lists
class State(TypedDict):
    messages: Annotated[list, operator.add]  # Append each update

# Custom reducer
def merge_dicts(a, b):
    return {**a, **b}

class State(TypedDict):
    metadata: Annotated[dict, merge_dicts]
```

### LangGraph Architecture Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| Simple RAG Graph | retrieve → generate | Basic RAG with control |
| Self-Correcting | generate → evaluate → [fix or end] | Quality-critical output |
| Multi-Agent Supervisor | supervisor → route → worker → supervisor | Multi-agent coordination |
| Parallel Subgraphs | Fork to multiple agents, join results | Independent parallel tasks |
| Human-in-the-loop | Interrupt for human approval | High-stakes actions |
| Corrective RAG | retrieve → grade → [re-retrieve or generate] | High accuracy RAG |

## 5. Architecture Perspective

### LangChain vs LangGraph

| Dimension | LangChain | LangGraph |
|-----------|-----------|-----------|
| Paradigm | Chains (linear/parallel) | Graphs (loops, branches) |
| State | Passed between steps implicitly | Explicit TypedDict — shared |
| Loops | Not supported natively | First-class (conditional edges) |
| Branching | RunnableBranch (limited) | Full conditional routing |
| Persistence | Manual | Built-in checkpointing |
| Human-in-loop | Not built-in | Native interrupt/resume |
| Debugging | LangSmith traces | State at each node + LangSmith |
| Best for | Simple pipelines | Complex agents, multi-agent |

## 6. Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Graph cycle | Conditional edge always loops | Infinite execution | Add iteration counter in state; max recursion limit |
| State corruption | Multiple nodes write same field | Unexpected state values | Use reducers; validate state schema |
| Node failure | Exception in node function | Graph terminates with error | try/except in nodes, error state |
| Checkpoint bloat | Large state stored in checkpoint | Slow resume | Trim state before checkpoint, compress |
| Non-determinism | LLM routing decisions vary | Different paths in prod | Add temperature=0 for routing decisions |

## 7. End-to-End Flow
```
User Input → AgentState initialization
    ↓
START node
    ↓
router_node (conditional: what does user want?)
    ↙              ↓               ↘
retrieve_node   calculate_node   answer_directly_node
    ↓                ↓                   ↓
[State updated with context/result/answer]
    ↓
generate_node (assemble final answer)
    ↓
quality_check_node (conditional: good enough?)
    ↙ (no)                ↘ (yes)
regenerate_node          END
    ↓
generate_node (loop)
```

## 8. Terminology Cheat Sheet

| Term | Meaning | Why It Matters |
|------|---------|---------------|
| StateGraph | Graph class with state schema | Core LangGraph class |
| Runnable | LCEL interface | Nodes are Runnables |
| Checkpointer | State persistence layer | Human-in-loop + resume |
| Thread ID | Unique conversation ID | Multi-session state isolation |
| Interrupt | Pause before/after node | Human oversight |
| Reducer | How state field is updated on conflict | operator.add for lists |
| Subgraph | Graph as node | Modularity |
| compile() | Convert graph to executable | Required step |

## 9. Comparison Tables

### LangGraph vs CrewAI vs AutoGen

| Aspect | LangGraph | CrewAI | AutoGen |
|--------|-----------|--------|---------|
| Paradigm | State machine graph | Role-based crew | Conversational agents |
| Control | Developer controls routing | Framework controls | Framework controls |
| Flexibility | Very high | Medium | Medium |
| Learning curve | High | Low | Medium |
| Production readiness | High | Medium | Medium |
| Human-in-loop | Native | Limited | Some |
| Multi-agent | Yes (supervisor pattern) | Yes (crew) | Yes (GroupChat) |
| State management | Explicit | Implicit | Memory |

## 10. Interview Revision

### Senior Questions

**Q1: When would you use LangGraph over a simple LangChain chain?**
- **Answer**: When workflow has conditional branches (e.g., "if retrieval fails, try web search"). When you need loops (iterative refinement). When you need state persistence (multi-turn, pause/resume). When building multi-agent systems. When you need human-in-the-loop.

**Q2: How does LangGraph handle persistence?**
- **Answer**: Checkpointers serialize state after each node. SQLite for dev, Redis or Postgres for production. Thread ID isolates per conversation. Resume from checkpoint by passing same thread_id. State is serialized as JSON.

**Q3: Design a self-correcting RAG pipeline in LangGraph.**
- **Answer**: Nodes: retrieve → grade_documents → [route: pass/fail] → generate or re-retrieve. `grade_documents` node uses LLM to score each chunk for relevance. If score < threshold for most chunks → re-retrieve with refined query. Max 3 iterations. This is the "Corrective RAG" (CRAG) pattern.

## 12. One-Page Revision Sheet

### Must Know
- StateGraph: nodes + edges + shared typed state
- Conditional edges: routing function returns next node name
- Checkpointer: persist state (thread_id = session ID)
- Interrupt: human-in-the-loop primitive

### Interview Nuggets
- "LangGraph is the right choice when you need loops, branches, or human-in-the-loop"
- State machine = testable, observable, debuggable
- supervisor pattern = standard multi-agent architecture

### Common Traps
- Forgetting to add `operator.add` reducer for message lists → state overwritten
- Creating unintended infinite loops (no termination condition)
- Not using thread_id → state shared across conversations

---

# TOPIC 11: LangSmith & LangFuse

## 1. Executive Summary
- LangSmith: Anthropic/LangChain's observability and evaluation platform for LLM apps
- LangFuse: open-source alternative — tracing, evaluation, prompt management
- Both solve: "what happened inside my LLM call?" — without observability, debugging is impossible
- LLM observability includes: traces, spans, token counts, latency, costs, scores
- Where it fits: cross-cutting concern — every LLM call should be traced
- Why engineers care: LLM apps fail in mysterious ways; tracing is how you debug and improve

## 2. Mental Model
- **Analogy**: LangSmith/LangFuse is to LLM apps what Datadog/New Relic is to microservices
- **Core concept**: Trace = tree of spans. Root span = user request. Child spans = each LLM call, retrieval, tool call.
- **LLM debugging workflow**: bad output → find trace → inspect prompt → identify issue → fix → eval

```
User Request
    └─── Trace (root span)
              ├── Retrieval Span (latency=120ms, retrieved=5 docs)
              ├── LLM Span (model=claude-3, tokens=1200, cost=$0.002, latency=800ms)
              │   ├── Input: [system, user, context messages]
              │   └── Output: "The answer is..."
              └── Score (faithfulness=0.85, user_feedback=thumbs_up)
```

## 3. Core Concepts

| Concept | LangSmith | LangFuse |
|---------|-----------|---------|
| Trace | Run → child runs tree | Trace → Observations tree |
| Span | Run (LLM/Chain/Tool/Retriever) | Span/Generation/Event |
| Feedback | Human feedback + automated evals | Scores |
| Dataset | Curated input/output pairs for eval | Dataset |
| Evaluation | Run eval on dataset | Evals with scoring |
| Prompt Management | Prompt Hub | Prompt Management |
| Cost tracking | Automatic token cost | Yes (configurable) |
| Hosting | Cloud (SaaS) | Self-hostable or SaaS |

## 4. Engineering Deep Dive

### LangSmith Setup
```python
import os
os.environ["LANGCHAIN_API_KEY"] = "ls_..."
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# All LangChain calls automatically traced
chain = prompt | model | parser
result = chain.invoke({"question": "..."})  # Auto-traced!
```

### Manual Tracing with LangSmith
```python
from langsmith import traceable

@traceable(name="retrieve_documents", run_type="retriever")
def retrieve(query: str) -> list:
    return vector_store.search(query)

@traceable(name="generate_answer", run_type="llm")
def generate(context: str, question: str) -> str:
    return llm.invoke(f"Context: {context}\nQuestion: {question}")
```

### LangFuse Setup
```python
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com"  # or self-hosted
)

@observe()
def rag_pipeline(question: str) -> str:
    langfuse_context.update_current_observation(
        input={"question": question}
    )
    docs = retrieve(question)
    answer = generate(docs, question)
    langfuse_context.update_current_observation(
        output={"answer": answer},
        usage={"total_tokens": 1200}
    )
    return answer
```

### Adding Feedback / Scores
```python
# LangSmith
client = langsmith.Client()
client.create_feedback(
    run_id="...",
    key="faithfulness",
    score=0.85,
    comment="Grounded in provided context"
)

# LangFuse
langfuse.score(
    trace_id="...",
    name="faithfulness",
    value=0.85
)
```

### Prompt Management (LangSmith Hub)
```python
from langchain import hub
prompt = hub.pull("my-org/rag-prompt:v2")  # Version-controlled prompt
chain = prompt | model | parser
```

### Production Sampling
```python
# Don't trace every request in production — cost and latency
import random

if random.random() < 0.05:  # 5% sampling
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
else:
    os.environ["LANGCHAIN_TRACING_V2"] = "false"
```

## 5. Architecture Perspective

### LangSmith vs LangFuse

| Aspect | LangSmith | LangFuse |
|--------|-----------|---------|
| Vendor | LangChain (proprietary SaaS) | Open-source (MIT license) |
| Self-hosting | No | Yes (Docker, Kubernetes) |
| LangChain integration | Native, automatic | Via callbacks |
| Cost | Paid tiers | Free self-hosted |
| Data sovereignty | Data leaves your infra | Self-hosted = yours |
| Features | Full platform | Full platform |
| Compliance | Depends on SaaS | Self-hosted = full control |

**Enterprise choice**: LangFuse self-hosted for data sovereignty.  
**Startup choice**: LangSmith Cloud for fastest integration.

## 6. Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Tracing overhead | Every LLM call sends trace async | Latency increase | Sample in production |
| PII leakage | Prompts contain user data | Security audit | Mask PII before tracing |
| Trace storage costs | High volume traces | Bill spike | Sampling + retention policies |
| Missing traces | Async calls not awaited | Gaps in trace data | Ensure proper async handling |

## 7. End-to-End Flow
```
User Request
    ↓
LangSmith/LangFuse: Start Trace (trace_id)
    ↓
RAG Pipeline (each step creates child span)
  ├── Retrieval span: query, results, latency
  ├── LLM span: prompt, output, tokens, cost, latency
  └── Parser span: output
    ↓
End Trace: aggregate stats
    ↓
Background: RAGAS evaluators run on trace
    ↓
Dashboard: metrics, alerts, drill-down
```

## 8. Terminology Cheat Sheet

| Term | Meaning |
|------|---------|
| Trace | Full request tree from start to end |
| Span | Single operation within a trace |
| Run Type | LLM, Chain, Tool, Retriever, Parser |
| Score | Numeric quality assessment of a trace/span |
| Dataset | Collection of (input, expected_output) pairs |
| Evaluator | Function that scores a run |
| Prompt Hub | Versioned prompt management |
| Thread | Grouped traces for multi-turn conversation |

## 9. Comparison Tables

### Observability Tools

| Tool | Type | Self-host | LLM Native | Evals | Best For |
|------|------|-----------|-----------|-------|---------|
| LangSmith | SaaS | No | Yes (LangChain) | Yes | LangChain apps |
| LangFuse | OSS+SaaS | Yes | Yes | Yes | Data sovereignty |
| Helicone | SaaS | Partial | OpenAI focus | Basic | OpenAI apps |
| Arize Phoenix | OSS | Yes | Yes | Yes | ML + LLM |
| Datadog LLM Obs | SaaS | No | Yes (generic) | Basic | Enterprise Datadog users |

## 10. Interview Revision

**Q1: What would you monitor in a production RAG system?**
- **Answer**: Token usage and cost per request. Latency (p50, p95, p99) per stage. Retrieval hit rate (did retrieval return results?). RAGAS faithfulness (sampled). User feedback scores. Error rate. Context utilization (did LLM use the context?). Via LangSmith/LangFuse + custom metrics in CloudWatch.

**Q2: How do you use LangSmith for prompt optimization?**
- **Answer**: Trace all prod calls → identify low-score runs → inspect prompts → create dataset of failure cases → run evals on prompt variants → compare scores → deploy winner.

## 12. One-Page Revision Sheet

### Must Know
- LangSmith: auto-trace all LangChain calls with env vars
- LangFuse: self-hostable alternative, full data control
- Trace = tree of spans; root = user request
- Sample in production (5-10%) to control cost

### Interview Nuggets
- "Without observability, you're flying blind" — always mention in system design
- LangFuse for compliance/data sovereignty; LangSmith for developer speed
- Use scores + feedback to build eval datasets from production

### Common Traps
- Enabling full tracing in production without sampling → latency + cost
- PII in prompts going to external tracing SaaS → compliance issue

---

# TOPIC 12: CrewAI

## 1. Executive Summary
- CrewAI: multi-agent framework where AI "crew members" with roles collaborate on tasks
- Solves: complex tasks that benefit from specialization and parallel work
- Abstractions: Agent (role + goal + tools), Task (description + output), Crew (team + process)
- Where it fits: orchestration layer for multi-agent workflows; higher-level than LangGraph
- Trade-off: easier to define than LangGraph, less flexible and less control
- Process types: Sequential (tasks in order) or Hierarchical (manager delegates)
- Built on top of LangChain agents internally

## 2. Mental Model
- **Analogy**: A consulting team — you have a researcher, an analyst, and a writer, each doing their specialized task and passing outputs to the next.
- **Core components**: Agent (who) + Task (what) + Crew (team + how)

```
Crew (Research Team)
├── Agent: Researcher (role="researcher", tools=[search, browse])
│   └── Task: "Research competitor landscape" → Output: research_report
├── Agent: Analyst (role="analyst", tools=[calculator, data_query])
│   └── Task: "Analyze findings" → Output: analysis
└── Agent: Writer (role="writer", tools=[])
    └── Task: "Write executive summary" → Output: final_report
Process: Sequential (researcher → analyst → writer)
```

## 3. Core Concepts

| Concept | Definition |
|---------|-----------|
| Agent | LLM + role + goal + backstory + tools + memory |
| Task | Description + expected_output + agent assignment + context |
| Crew | Collection of agents + tasks + process type |
| Process | Sequential or Hierarchical execution |
| Manager Agent | In Hierarchical process — delegates tasks |
| Kickoff | Start the crew execution |
| Context | Task can use output of previous tasks as context |
| Memory | Short-term, long-term, entity, contextual memory per agent |
| Tool | Same as LangChain tools — functions agents can call |

## 4. Engineering Deep Dive

### Basic CrewAI Setup
```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)
search_tool = SerperDevTool()

# Define Agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI",
    backstory="Expert at identifying emerging trends",
    verbose=True,
    llm=llm,
    tools=[search_tool]
)

writer = Agent(
    role="Tech Content Strategist",
    goal="Write compelling technical content",
    backstory="Expert at making complex tech accessible",
    verbose=True,
    llm=llm
)

# Define Tasks
research_task = Task(
    description="Research the latest developments in LLM agents. Focus on 2024 innovations.",
    expected_output="A detailed report with key findings and sources",
    agent=researcher
)

write_task = Task(
    description="Based on the research, write an executive summary for non-technical stakeholders.",
    expected_output="500-word executive summary",
    agent=writer,
    context=[research_task]  # Uses output of research_task
)

# Create and run Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
print(result.raw)
```

### Hierarchical Process
```python
manager = Agent(
    role="Project Manager",
    goal="Coordinate team to produce excellent report",
    llm=ChatOpenAI(model="gpt-4o")
)

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,
    manager_agent=manager  # Manager delegates tasks
)
```

### Custom Tools
```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="Search query")

class VectorSearchTool(BaseTool):
    name: str = "Vector Search"
    description: str = "Search company knowledge base for relevant information"
    args_schema: type[BaseModel] = SearchInput
    
    def _run(self, query: str) -> str:
        results = vector_store.search(query, k=5)
        return "\n".join([r.page_content for r in results])
```

## 5. Architecture Perspective

### CrewAI vs LangGraph

| Aspect | CrewAI | LangGraph |
|--------|--------|-----------|
| Abstraction level | High (roles, crew) | Low (nodes, edges, state) |
| Ease of use | Easy | Hard |
| Control | Low | Full |
| Flexibility | Medium | Maximum |
| Multi-agent | Native concept | Supervisor pattern |
| State management | Implicit | Explicit |
| Human-in-loop | Limited | Native |
| Production hardening | Less | More |
| Best for | Quick multi-agent prototypes | Production agent systems |

**Rule of thumb**: Use CrewAI to prototype multi-agent idea. Use LangGraph to productionize it.

## 6. Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| Agent doesn't use tool | Poor tool description | Manual review | Improve description; mention in role goal |
| Task context lost | Long output truncated | Short final output | Summarize intermediate outputs |
| Agent hallucination | No tool to verify claim | Manual review | Add verification tools |
| Crew never finishes | Agent stuck in loop | Timeout | max_iterations on agents |
| Cost explosion | Many agents × many tasks | API bill | Token limits per agent |

## 7. End-to-End Flow
```
crew.kickoff(inputs={"topic": "LLM Agents"})
    ↓
Task 1 (Researcher Agent):
  - Thinks: "I need to search for recent LLM agent papers"
  - Calls: search_tool("LLM agents 2024 arxiv")
  - Gets results, formulates report
  - Output: research_report.md
    ↓
Task 2 (Analyst Agent):
  - Receives context: research_report.md
  - Analyzes trends, key findings
  - Output: analysis.md
    ↓
Task 3 (Writer Agent):
  - Receives context: analysis.md
  - Writes executive summary
  - Output: executive_summary.md
    ↓
Final Result: executive_summary.md content
```

## 8. Terminology Cheat Sheet

| Term | Meaning |
|------|---------|
| Agent backstory | Persona/context for the agent | Shapes behavior |
| Sequential process | Tasks run in order | Simple, predictable |
| Hierarchical process | Manager delegates | More flexible |
| Task context | Previous task outputs fed to current task | Information flow |
| Crew kickoff | Start execution | Entry point |
| Verbose | Log agent thinking steps | Debugging |

## 12. One-Page Revision Sheet

### Must Know
- Agent: role + goal + backstory + tools
- Task: description + expected_output + agent + context
- Crew: agents + tasks + Process.sequential or .hierarchical
- context=[task1] in Task → passes task1 output to this task

### Interview Nuggets
- "CrewAI is great for prototyping; LangGraph for production control"
- Hierarchical process = manager agent pattern
- Backstory shapes agent persona and behavior

### Common Traps
- Not passing context between tasks → each agent starts from scratch
- Overly complex crews → better to simplify with LangGraph

---

# TOPIC 13: Docker Fundamentals

## 1. Executive Summary
- Docker: containerization platform for packaging apps with their dependencies
- Solves: "it works on my machine" — containers guarantee identical environments
- For GenAI: package LLM applications, RAG pipelines, and ML services consistently
- Components: Dockerfile (recipe), Image (built artifact), Container (running instance)
- Why engineers care: reproducible deployment, microservice architecture, CI/CD
- In GenAI stack: package FastAPI endpoints, Embedding services, processing jobs
- Docker Compose: multi-container local development (app + OpenSearch + Redis)
- Kubernetes: production container orchestration (beyond Docker)

## 2. Mental Model
- **Analogy**: Docker image = shipping container — standardized, portable, self-contained
- **Dockerfile → Image → Container** = Recipe → Cake → Eating the cake
- **Layered filesystem**: Each instruction adds a layer; layers are cached; optimize for cache efficiency

```
Dockerfile (recipe)
    ↓ docker build
Image (immutable artifact, stored in registry)
    ↓ docker run
Container (running process with isolated filesystem, network, resources)
```

## 3. Core Concepts

| Concept | Definition |
|---------|-----------|
| Dockerfile | Instructions to build an image |
| Image | Immutable layered filesystem snapshot |
| Container | Running instance of an image |
| Layer | Each Dockerfile instruction creates a cache layer |
| Registry | Image storage (DockerHub, ECR, GCR) |
| Volume | Persistent storage mounted into container |
| Network | Container communication mechanism |
| Docker Compose | Multi-container local orchestration |
| Multi-stage build | Separate build and runtime stages |
| .dockerignore | Files to exclude from build context |
| Base image | Starting point for your image |
| ECR | AWS Elastic Container Registry |
| ECS/EKS | AWS container orchestration |

## 4. Engineering Deep Dive

### Production Dockerfile for GenAI App
```dockerfile
# ---- Build Stage ----
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy only requirements first (cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.11-slim

WORKDIR /app

# Don't run as root
RUN useradd -m -u 1000 appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Security: non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

ENV PATH=/home/appuser/.local/bin:$PATH

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Docker Compose for Local RAG Stack
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENSEARCH_HOST=opensearch
    depends_on:
      - opensearch
      - redis
    volumes:
      - ./data:/app/data  # Dev: mount local data

  opensearch:
    image: opensearchproject/opensearch:2.11.0
    environment:
      - discovery.type=single-node
      - DISABLE_SECURITY_PLUGIN=true
      - OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m
    ports:
      - "9200:9200"
    volumes:
      - opensearch_data:/usr/share/opensearch/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  opensearch_data:
```

### Key Docker Commands
```bash
# Build
docker build -t my-rag-app:1.0.0 .
docker build --platform linux/amd64 -t my-rag-app:1.0.0 .  # For M1 Mac → AWS

# Run
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... my-rag-app:1.0.0

# Compose
docker-compose up -d        # Start all services
docker-compose logs -f app  # Follow logs
docker-compose down -v      # Stop + remove volumes

# Debug
docker exec -it <container_id> /bin/bash
docker logs <container_id> --tail 100 -f

# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <ecr_url>
docker tag my-rag-app:1.0.0 <ecr_url>/my-rag-app:1.0.0
docker push <ecr_url>/my-rag-app:1.0.0
```

### Layer Caching Strategy
```dockerfile
# WRONG: requirements change = rebuild everything
COPY . .
RUN pip install -r requirements.txt  # Long step, cache bust on any file change

# RIGHT: dependencies before code
COPY requirements.txt .
RUN pip install -r requirements.txt  # Cached unless requirements.txt changes
COPY . .                             # Only this and below re-run on code change
```

### Best Practices for GenAI Containers

| Practice | Why |
|----------|-----|
| Multi-stage builds | Smaller final image (no build tools) |
| Non-root user | Security |
| .dockerignore | Exclude `.git`, `__pycache__`, `*.pyc`, test files |
| Pin base image versions | `python:3.11-slim` not `python:latest` |
| Health checks | Container orchestration needs them |
| Use `--no-cache-dir` for pip | Smaller image |
| Environment variables for config | Avoid secrets in image |
| platform flag for cross-arch | M1 Mac → `linux/amd64` for AWS |

## 5. Architecture Perspective

### Container in GenAI Architecture
```
ECS Cluster (AWS):
  ├── RAG API Service (ECS Task: my-rag-app:1.0.0)
  │   └── Auto-scale: 2-20 tasks based on CPU/request count
  ├── Embedding Service (ECS Task: embed-service:1.2.0)
  │   └── GPU-enabled task definition
  └── Ingestion Worker (ECS Task: ingestor:1.0.0)
      └── SQS-triggered, scale to 0

Supporting:
  ├── ECR: Image registry
  ├── OpenSearch: Vector DB (not containerized — managed service)
  └── RDS: Metadata store
```

## 6. Failure Modes

| Failure | Root Cause | Detection | Mitigation |
|---------|-----------|-----------|------------|
| OOM killed | Container memory limit too low | `exit code 137` | Increase memory limit, optimize app |
| Port binding fails | Port already in use | Startup error | Check ports, use dynamic allocation |
| Secret in image | Hardcoded API key in Dockerfile | Security scan (trivy) | Use env vars or AWS Secrets Manager |
| Huge image size | No multi-stage, no .dockerignore | `docker images` shows GB | Multi-stage + .dockerignore |
| Platform mismatch | Built on ARM, deployed on x86 | `exec format error` | `--platform linux/amd64` |
| Container starts but unhealthy | App crash, wrong port | Health check failing | Check HEALTHCHECK + logs |

## 7. End-to-End Flow
```
Developer pushes code
    ↓
CI/CD (GitHub Actions):
  docker build --platform linux/amd64 -t my-app:${GIT_SHA} .
  docker push ECR/my-app:${GIT_SHA}
    ↓
ECS Deployment:
  Update Task Definition with new image tag
  ECS rolling update: new tasks → health check passes → old tasks stop
    ↓
Running container:
  ENV VARS from Secrets Manager / Parameter Store
  VPC networking to OpenSearch, RDS
  ALB distributes traffic
  CloudWatch logs from stdout
```

## 8. Terminology Cheat Sheet

| Term | Meaning | Why It Matters |
|------|---------|---------------|
| Base image | Starting image (python:3.11-slim) | Determines size and security surface |
| Layer cache | Unchanged layers reused | Speeds up builds |
| Multi-stage | Build in one stage, copy to minimal runtime | Smaller production images |
| .dockerignore | Exclude files from build context | Faster builds, smaller context |
| ECR | AWS Elastic Container Registry | Where images live |
| ECS Task Definition | Container spec for ECS | How containers run in AWS |
| ENTRYPOINT vs CMD | ENTRYPOINT: binary; CMD: default args | Overridability |
| exec format error | Architecture mismatch (ARM vs x86) | Common M1 Mac pitfall |

## 12. One-Page Revision Sheet

### Must Know
- Dockerfile → Image → Container
- Layer caching: copy requirements before code
- Multi-stage builds: smaller, more secure images
- Non-root user in production containers
- `--platform linux/amd64` for M1 Mac building for AWS

### Production Nuggets
- Never put secrets in Dockerfile → use env vars + Secrets Manager
- Pin base image versions: `python:3.11.7-slim` not `python:latest`
- Health checks are mandatory for ECS/Kubernetes

### Common Traps
- Huge images (forget .dockerignore, no multi-stage)
- Root user in production
- Secrets in image layers
- Platform mismatch (M1 Mac → AWS)

---
