from pathlib import Path

from pypdf import PdfReader


def load_pdf_text(pdf_path: str) -> str:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"Missing PDF: {pdf_path}")
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)
