from dataclasses import dataclass

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


@dataclass
class RetrievalResult:
    context: str
    sources: list[str]


def _format_source(metadata: dict) -> str:
    source_type = metadata.get("source_type", "cv").upper()
    title = metadata.get("title", "Curriculum Vitae")
    year = metadata.get("year", "n.d.")
    return f"{source_type} — {title} ({year})"


def retrieve_context(query: str, top_k: int = 4) -> RetrievalResult:
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vector_store = Chroma(
        persist_directory="data/chroma_cv_db",
        embedding_function=embeddings,
        collection_name="zineb_cv",
    )
    documents = vector_store.similarity_search(query, k=top_k)
    context = "\n\n".join(doc.page_content for doc in documents)
    sources = [_format_source(doc.metadata) for doc in documents]
    return RetrievalResult(context=context, sources=sources)