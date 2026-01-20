from pathlib import Path
import json
import os
import re

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from app.core.config import settings
from app.rag.chunker import chunk_text
from app.rag.loader import load_pdf_text


def write_chunks(path: Path, chunks: list[dict]) -> None:
    path.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")

def infer_section(text: str) -> str:
    compact = re.sub(r"\s+", "", text).lower()
    if "experience" in compact or "workexperience" in compact:
        return "experience"
    if "education" in compact or "degree" in compact or "gpa" in compact:
        return "education"
    if (
        "publications" in compact
        or "journalarticles" in compact
        or "conferencepapers" in compact
    ):
        return "publications"
    if "research" in compact or "researchstatement" in compact:
        return "research"
    if "honors" in compact or "achievements" in compact:
        return "honors"
    if "skills" in compact:
        return "skills"
    return "general"


def main() -> None:
    raw_path = Path(settings.data_dir) / "raw" / "cv.pdf"
    processed_dir = Path(settings.data_dir) / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    text = load_pdf_text(str(raw_path))
    (processed_dir / "cv.txt").write_text(text, encoding="utf-8")

    cv_chunks = chunk_text(text)
    cv_documents = []
    for chunk in cv_chunks:
        metadata = {
            "source_type": "cv",
            "section": infer_section(chunk.text),
            "title": "Curriculum Vitae",
            "year": 2025,
            "author": "Zineb Tissir",
            "institution": "Curriculum Vitae",
            "chunk_role": "summary",
        }
        cv_documents.append(Document(page_content=chunk.text, metadata=metadata))

    journal_chunks = [
        {
            "text": "Style-Aware and Uncertainty-Guided Approach to Semi-Supervised Domain Generalization in Medical Imaging. Key contributions include uncertainty-guided pseudo-labeling and style-aware augmentation.",
            "metadata": {
                "source_type": "journal",
                "section": "publications",
                "title": "Style-Aware and Uncertainty-Guided Approach to Semi-Supervised Domain Generalization in Medical Imaging",
                "venue": "Mathematics",
                "publisher": "MDPI",
                "year": 2025,
                "author": "Zineb Tissir",
                "chunk_role": "contribution",
            },
        }
    ]

    conference_chunks = [
        {
            "text": "A Comprehensive Data Imbalance Analysis for Covid-19 Classification Dataset. The study analyzes class imbalance and its impact on classification performance.",
            "metadata": {
                "source_type": "conference",
                "section": "publications",
                "title": "A Comprehensive Data Imbalance Analysis for Covid-19 Classification Dataset",
                "venue": "ICTC (IEEE)",
                "year": 2021,
                "author": "Zineb Tissir",
                "chunk_role": "abstract",
            },
        }
    ]

    thesis_chunks = [
        {
            "text": "Thesis: Multi-Style Ensemble Pseudo-Labeling for Semi-Supervised Domain Generalization. Focused on robust generalization under domain shifts.",
            "metadata": {
                "source_type": "thesis",
                "section": "education",
                "title": "Multi-Style Ensemble Pseudo-Labeling for Semi-Supervised Domain Generalization",
                "institution": "Gachon University",
                "year": 2023,
                "author": "Zineb Tissir",
                "chunk_role": "abstract",
            },
        }
    ]

    research_summary_chunks = [
        {
            "text": "Research focus on trustworthy AI systems under real-world domain shifts, especially in medical imaging. Emphasis on uncertainty-aware learning and robust generalization.",
            "metadata": {
                "source_type": "research_summary",
                "section": "research",
                "title": "Research Statement",
                "year": 2025,
                "author": "Zineb Tissir",
                "chunk_role": "overview",
            },
        }
    ]

    write_chunks(processed_dir / "journal_chunks.json", journal_chunks)
    write_chunks(processed_dir / "conference_chunks.json", conference_chunks)
    write_chunks(processed_dir / "thesis_chunks.json", thesis_chunks)
    write_chunks(processed_dir / "research_summary_chunks.json", research_summary_chunks)

    extra_documents = [
        Document(page_content=item["text"], metadata=item["metadata"])
        for item in journal_chunks
        + conference_chunks
        + thesis_chunks
        + research_summary_chunks
    ]

    os.environ["ANONYMIZED_TELEMETRY"] = "false"
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vector_store = Chroma(
        persist_directory="data/chroma_cv_db",
        embedding_function=embeddings,
        collection_name="zineb_cv",
    )

    vector_store.add_documents(cv_documents + extra_documents)
    vector_store.persist()

    print("✅ CV indexed successfully")
    print(f"📦 Number of chunks: {len(cv_documents) + len(extra_documents)}")


if __name__ == "__main__":
    main()
