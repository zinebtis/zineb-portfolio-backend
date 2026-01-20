from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[Chunk]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be larger than overlap.")
    chunks: list[Chunk] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(Chunk(text=chunk, source=f"offset:{start}"))
        start += chunk_size - overlap
    return chunks
