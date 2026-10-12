"""Actual retrieval metrics on a labeled mini benchmark.

No invented outcomes: every score comes from the current repository/test corpus.
"""
from __future__ import annotations
from .models import Document, EvaluationCase, EvaluationResult
from .retrieval import LocalRetriever


def evaluate(documents: list[Document], cases: list[EvaluationCase]) -> EvaluationResult:
    engine = LocalRetriever(documents)
    details = []
    count = 0
    hit_sum = 0.0
    rr_sum = 0.0
    for c in cases:
        if not c.expected_documents:
            continue
        candidates = engine.search(c.query, k=3)
        ranked_ids = [r.document_id for r in candidates]
        expected = set(c.expected_documents)
        first = next((rank for rank, did in enumerate(ranked_ids, 1) if did in expected), None)
        hit = first is not None
        hit_sum += float(hit)
        rr_sum += 1 / first if first else 0
        count += 1
        details.append({"query": c.query, "expected_documents": c.expected_documents,
                        "retrieved": ranked_ids, "hit_at_3": hit,
                        "reciprocal_rank": round(1 / first, 3) if first else 0})
    return EvaluationResult(
        cases=len(cases), evaluated=count,
        hit_at_3=round(hit_sum / count, 3) if count else 0,
        mean_reciprocal_rank=round(rr_sum / count, 3) if count else 0,
        individual_results=details,
        notes="Metrics reflect source retrieval against labeled synthetic test cases, not factual correctness, end-to-end task success, or user satisfaction.",
    )
