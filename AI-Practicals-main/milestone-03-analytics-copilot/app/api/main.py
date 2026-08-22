"""
FastAPI backend with routing agent.
"""

from app.agent.runner import run_agent
from app.rag.chain import ask_question
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="RAG + SQL Routing Agent")


class QuestionRequest(BaseModel):
    question: str


class ChatRequest(BaseModel):
    question: str
    session_id: str = Field(default="default", description="Conversation thread id")
    user_id: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(request: QuestionRequest):
    """Legacy RAG-only endpoint (Milestone 2)."""
    answer = ask_question(request.question)
    return {"question": request.question, "answer": answer}


@app.post("/chat")
def chat(request: ChatRequest):
    """
    Routing agent: classifies SQL vs RAG, uses conversation memory per session_id.
    """
    result = run_agent(
        question=request.question,
        session_id=request.session_id,
        user_id=request.user_id,
    )
    return {
        "question": request.question,
        "answer": result["answer"],
        "route": result["route"],
        "session_id": result["session_id"],
        "error": result.get("error"),
    }
