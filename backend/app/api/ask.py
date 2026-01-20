from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.rag_agent import ask_agent


router = APIRouter()


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)


@router.post("/ask")
def ask(request: AskRequest) -> dict[str, str | list[str]]:
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required.")
    result = ask_agent(question)
    return {"answer": result["answer"], "sources": result["sources"]}
