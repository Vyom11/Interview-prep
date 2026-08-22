"""
FastAPI backend.
"""

# Import FastAPI
# Import RAG chain
from app.rag.chain import ask_question
from fastapi import FastAPI

# Import BaseModel
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI()


class QuestionRequest(BaseModel):
    """
    Request schema.
    """

    question: str


@app.post("/ask")
def ask(request: QuestionRequest):
    """
    Ask endpoint.
    """

    # Generate answer
    answer = ask_question(request.question)

    return {"question": request.question, "answer": answer}
