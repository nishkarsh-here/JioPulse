"""A small retrieval-augmented layer.

Knowledge documents under ``ai/knowledge`` are chunked and embedded once,
then the most relevant chunks are pulled back for a given question. The
index is cached for the life of the process so we only pay for embeddings
a single time.
"""
import os
import numpy as np
import streamlit as st

from src.ai.llm import embed, ai_is_configured

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge")


def _load_documents():
    docs = []
    if os.path.isdir(KNOWLEDGE_DIR):
        for fn in sorted(os.listdir(KNOWLEDGE_DIR)):
            if fn.endswith((".md", ".txt")):
                with open(os.path.join(KNOWLEDGE_DIR, fn), encoding="utf-8") as fh:
                    docs.append(fh.read())
    return docs


def _chunk(text, max_chars=600):
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if len(cur) + len(p) + 2 <= max_chars:
            cur = (cur + "\n\n" + p).strip()
        else:
            if cur:
                chunks.append(cur)
            cur = p
    if cur:
        chunks.append(cur)
    return chunks


@st.cache_resource(show_spinner=False)
def _build_index():
    chunks = []
    for text in _load_documents():
        chunks.extend(_chunk(text))
    if not chunks or not ai_is_configured():
        return {"chunks": chunks, "matrix": None}
    matrix = np.asarray(embed(chunks), dtype="float32")
    matrix /= (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-8)
    return {"chunks": chunks, "matrix": matrix}


def retrieve(query, k=4):
    """Return up to ``k`` (chunk, score) pairs most relevant to ``query``."""
    idx = _build_index()
    chunks, matrix = idx["chunks"], idx["matrix"]
    if matrix is None or not chunks:
        return []
    qv = np.asarray(embed([query])[0], dtype="float32")
    qv /= (np.linalg.norm(qv) + 1e-8)
    sims = matrix @ qv
    order = np.argsort(-sims)[:k]
    return [(chunks[i], float(sims[i])) for i in order]
