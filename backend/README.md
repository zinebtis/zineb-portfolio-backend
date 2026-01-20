# Backend RAG Chat Service

Minimal FastAPI backend for a CV-powered assistant ("answer as Zineb").

## Structure
- `app/main.py`: FastAPI entry point
- `app/api/chat.py`: `/chat` endpoint
- `app/core/config.py`: settings/env
- `app/core/security.py`: basic validation + rate limiting (in-memory)
- `app/rag/`: document loading, chunking, embeddings, vector store, retrieval, prompt
- `app/services/llm.py`: LLM client abstraction
- `app/schemas/chat.py`: request/response models
- `data/`: raw/processed/vectorstore
- `scripts/ingest_cv.py`: one-time ingestion

## Quick start
1. Create `.env` (see root `.env` file).
   - `OPENAI_API_KEY=your_api_key_here`
   - `MODEL_NAME=gpt-4o-mini`
2. Install dependencies:
   - `python -m venv .venv`
   - `pip install -r requirements.txt`
3. Ingest CV:
   - `python scripts/ingest_cv.py`
4. Run:
   - `uvicorn app.main:app --reload`

## Notes
- The example LLM client uses OpenAI-style API keys.
- The vector store uses FAISS locally.
