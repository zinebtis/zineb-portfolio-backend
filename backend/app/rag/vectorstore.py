from pathlib import Path

import faiss
import numpy as np


def build_faiss_index(vectors: np.ndarray | list[list[float]]) -> faiss.Index:
    array = np.array(vectors, dtype="float32")
    if array.ndim != 2 or array.size == 0:
        raise ValueError("Embeddings must be a non-empty 2D array.")
    dimension = array.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(array)
    return index


def save_index(index: faiss.Index, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, path)


def load_index(path: str) -> faiss.Index:
    return faiss.read_index(path)
