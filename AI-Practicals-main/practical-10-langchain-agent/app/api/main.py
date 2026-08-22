"""
FastAPI backend.
"""

from typing import Optional
from uuid import uuid4

from app.agent.agent import ask_agent
from app.rag.chain import ask_question
from fastapi import FastAPI
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI()


class QuestionRequest(BaseModel):
    """
    Request schema for the legacy RAG endpoint.
    """

    question: str


class AgentRequest(BaseModel):
    """
    Request schema for the LangChain agent endpoint.
    """

    question: str
    conversation_id: Optional[str] = None
    max_iterations: Optional[int] = 6


@app.post("/ask")
def ask(request: QuestionRequest):
    """
    Legacy RAG-only question endpoint.
    """

    answer = ask_question(request.question)
    return {"question": request.question, "answer": answer}


@app.post("/agent")
def agent(request: AgentRequest):
    """
    LangChain agent endpoint with conversation memory and max_iterations safety.
    """

    conversation_id = request.conversation_id or str(uuid4())
    answer = ask_agent(
        request.question,
        conversation_id=conversation_id,
        max_iterations=request.max_iterations or 6,
    )

    return {
        "question": request.question,
        "answer": answer,
        "conversation_id": conversation_id,
        "max_iterations": request.max_iterations or 6,
    }
