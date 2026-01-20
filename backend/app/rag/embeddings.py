import os

import httpx


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/embeddings")
OLLAMA_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "mxbai-embed-large")


def _embed_single(text: str) -> list[float]:
    response = httpx.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": text},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    embedding = data.get("embedding")
    if not embedding:
        raise RuntimeError("Ollama returned no embedding")
    return embedding


def embed_texts(texts: list[str]):
    if not texts:
        raise ValueError("No texts provided for embeddings")

    if os.getenv("DEBUG_EMBEDDINGS") == "1":
        print("Embedding texts preview:", texts[:2])

    embeddings = [_embed_single(text) for text in texts]
    return embeddings
