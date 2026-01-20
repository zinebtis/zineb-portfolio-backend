from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from ollama import Client

from app.rag.prompt import build_prompt


DB_PATH = "data/chroma_cv_db"

embeddings = OllamaEmbeddings(model="mxbai-embed-large")
vector_store = Chroma(
    persist_directory=DB_PATH,
    embedding_function=embeddings,
    collection_name="zineb_cv",
)
ollama_client = Client()


def _format_source(metadata: dict) -> str:
    source_type = metadata.get("source_type", "cv").upper()
    title = metadata.get("title", "Curriculum Vitae")
    year = metadata.get("year", "n.d.")
    return f"{source_type} — {title} ({year})"


def ask_agent(question: str) -> dict[str, list[str] | str]:
    documents = vector_store.similarity_search(question, k=3)
    context = "\n\n".join(doc.page_content for doc in documents)
    sources = [_format_source(doc.metadata) for doc in documents]
    prompt = build_prompt(query=question, context=context)
    response = ollama_client.generate(model="llama3.2", prompt=prompt)
    answer = response.get("response", "").strip()
    return {"answer": answer, "sources": sources}
