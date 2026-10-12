from research_agent.demo import demo_documents, demo_cases
from research_agent.engine import build_research
from research_agent.retrieval import LocalRetriever, chunk_text
from research_agent.evaluation import evaluate
from research_agent.ingest import extract_text, make_document
from research_agent.tools import cagr, market_revenue
import pytest


def test_demo_docs_are_synthetic():
    docs = demo_documents()
    assert len(docs) == 6
    assert all(d.source_type == "synthetic-demo" for d in docs)


def test_chunk_long():
    blocks = chunk_text("A" * 1300)
    assert len(blocks) > 2
    assert all(0 < len(b) <= 460 for b in blocks)


def test_retrieve_finance():
    found = LocalRetriever(demo_documents()).search("销售30台 单价45万元 收入1350万", k=3)
    assert found
    assert "DEMO-finance" in [e.document_id for e in found]


def test_report_all_citations_grounded():
    result = build_research("请研究该企业市场、产品和风险", demo_documents())
    assert result.mode == "offline-evidence"
    assert len(result.steps) == 5
    assert len(result.evidence) > 0
    ids = [e.citation_id for e in result.evidence]
    assert len(ids) == len(set(ids))
    assert all(f"[{cid}]" in result.report_markdown for cid in ids)
    assert "来源索引" in result.report_markdown


def test_empty_documents_have_gaps_and_no_citations():
    result = build_research("分析未知公司风险和竞品", [])
    assert result.metrics["retrieved_chunks"] == 0
    assert result.metrics["step_coverage"] == 0
    assert result.gaps


def test_llm_mode_without_key_is_safe(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = build_research("分析神经调控商业模式", demo_documents(), use_llm=True)
    assert result.mode == "offline-evidence"
    assert "OPENAI_API_KEY" in result.llm_note


def test_demo_benchmark_runs():
    result = evaluate(demo_documents(), demo_cases())
    assert result.evaluated == 10
    assert 0 <= result.hit_at_3 <= 1
    assert 0 <= result.mean_reciprocal_rank <= 1


def test_file_upload_limit():
    with pytest.raises(ValueError):
        extract_text("evil.exe", b"this text should not be loaded")
    with pytest.raises(ValueError):
        extract_text("blank.txt", b"Hi")
    doc = make_document("example.txt", b"Enough sample research content to parse and index in test.")
    assert doc.source_type == "upload"


def test_tools():
    assert market_revenue(100, .2, 100) == 2000
    assert cagr(100, 121, 2) == pytest.approx(.1)
    with pytest.raises(ValueError):
        cagr(0, 10, 2)
