"""Local TF-IDF retrieval with traceable citations; no remote vector DB.

Chinese text uses char n-grams; English text uses the same analyzer to support
mixed-language queries without external tokenizers/weights.
"""
from __future__ import annotations
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Document, Evidence


def chunk_text(text: str, max_chars: int = 460, overlap: int = 70) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    # Preserve paragraph boundaries where possible; split long paragraphs.
    out: list[str] = []
    for p in paragraphs:
        if len(p) <= max_chars:
            out.append(p)
        else:
            offset = 0
            while offset < len(p):
                part = p[offset:offset+max_chars]
                if part.strip():
                    out.append(part)
                if offset + max_chars >= len(p):
                    break
                offset += max_chars - overlap
    return out


class LocalRetriever:
    def __init__(self, documents: list[Document]):
        self.documents = documents
        self.items: list[tuple[Document, int, str]] = []
        for doc in documents:
            for n, chunk in enumerate(chunk_text(doc.text)):
                self.items.append((doc, n, chunk))
        self.vectorizer = None
        self.matrix = None
        if self.items:
            self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4), sublinear_tf=True)
            self.matrix = self.vectorizer.fit_transform([item[2] for item in self.items])

    def search(self, query: str, k: int = 3, min_score: float = 0.025) -> list[Evidence]:
        if self.matrix is None or not query.strip():
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).ravel()
        ranked = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
        result = []
        for i in ranked:
            if len(result) >= k:
                break
            if float(scores[i]) < min_score:
                break
            doc, chunk_id, chunk = self.items[i]
            result.append(Evidence(
                citation_id="", document_id=doc.document_id, document_title=doc.title,
                excerpt=chunk, score=round(float(scores[i]), 4), chunk_id=chunk_id,
            ))
        return result
