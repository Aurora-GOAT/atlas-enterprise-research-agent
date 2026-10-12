"""Public API models: small, typed, directly explainable."""
from __future__ import annotations
from pydantic import BaseModel, Field


class Document(BaseModel):
    document_id: str
    title: str
    text: str
    filename: str = ""
    source_type: str = "demo"


class Evidence(BaseModel):
    citation_id: str
    document_id: str
    document_title: str
    excerpt: str
    score: float
    chunk_id: int


class PlanStep(BaseModel):
    key: str
    title: str
    query: str
    status: str = "done"
    evidence_count: int = 0


class ResearchRequest(BaseModel):
    query: str = Field(min_length=4, max_length=600)
    use_llm: bool = False
    top_k: int = Field(default=3, ge=1, le=6)
    scenario: str = "healthcare"


class ResearchResult(BaseModel):
    run_id: str
    query: str
    mode: str
    steps: list[PlanStep]
    evidence: list[Evidence]
    report_markdown: str
    gaps: list[str]
    warnings: list[str]
    metrics: dict[str, float | int]
    llm_note: str | None = None


class EvaluationCase(BaseModel):
    query: str
    expected_documents: list[str] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    cases: int
    evaluated: int
    hit_at_3: float
    mean_reciprocal_rank: float
    individual_results: list[dict]
    notes: str
