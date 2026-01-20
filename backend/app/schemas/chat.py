from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
