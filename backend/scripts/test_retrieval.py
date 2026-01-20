from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

print("🚀 Starting retrieval test...")

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db = Chroma(
    persist_directory="data/chroma_cv_db",
    embedding_function=embeddings,
    collection_name="zineb_cv",
)

retriever = db.as_retriever(search_kwargs={"k": 3})

query = "What are Zineb's research areas?"
docs = retriever.invoke(query)

print(f"📄 Retrieved documents count: {len(docs)}")

for i, doc in enumerate(docs, 1):
    print(f"\n--- Document {i} ---")
    print(doc.page_content[:400])
