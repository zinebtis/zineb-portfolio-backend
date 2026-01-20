from fastapi import APIRouter, HTTPException

from app.core.security import enforce_rate_limit, sanitize_query
from app.rag.retriever import retrieve_context
from app.rag.prompt import build_prompt
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm import generate_completion


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    enforce_rate_limit(request.client_id)
    query = sanitize_query(request.query)
    if not query:
        raise HTTPException(status_code=400, detail="Query is required.")

    context = retrieve_context(query)
    prompt = build_prompt(query=query, context=context)
    answer = generate_completion(prompt)

    return ChatResponse(answer=answer, sources=context.sources)
