"""Regression tests for deliberately fictional cross-industry flows."""
import pytest
from fastapi.testclient import TestClient
from research_agent import api
from research_agent.demo import demo_documents, demo_cases
from research_agent.engine import build_research
from research_agent.evaluation import evaluate
from research_agent.planner import make_plan
from research_agent.scenarios import SCENARIOS
from research_agent.store import LocalStore
from research_agent.business_tools import funnel_metrics, compare_suppliers

@pytest.mark.parametrize("scenario", ["healthcare","consumer","procurement"])
def test_scenario_retrieval_and_planning(scenario):
    docs=demo_documents(scenario)
    assert len(docs)>=4 and all(d.source_type=="synthetic-demo" for d in docs)
    plan=make_plan("分析市场策略与执行风险",scenario)
    assert len(plan)==5 and len({p.key for p in plan})==5
    r=build_research("分析市场策略与执行风险",docs,scenario=scenario)
    assert r.metrics["steps"]==5 and r.evidence and "来源索引" in r.report_markdown
    e=evaluate(docs,demo_cases(scenario))
    assert e.evaluated>=6 and 0<=e.hit_at_3<=1 and 0<=e.mean_reciprocal_rank<=1

def test_plans_are_industry_specific():
    assert make_plan("任务","consumer")[0].title!=make_plan("任务","healthcare")[0].title
    assert make_plan("任务","procurement")[0].title!=make_plan("任务","consumer")[0].title

def test_scenario_api(tmp_path,monkeypatch):
    monkeypatch.setattr(api,"store",LocalStore(tmp_path))
    c=TestClient(api.app)
    assert len(c.get("/api/scenarios").json())==3
    assert c.post("/api/demo/load?scenario=consumer").json()["loaded"]==4
    assert c.post("/api/demo/load?scenario=procurement").json()["total"]==4
    docs=c.get("/api/documents").json()
    assert len(docs)==4 and all(d["document_id"].startswith("DEMO-procurement") for d in docs)
    res=c.post("/api/research",json={"query":"比较供货商交期和产品质量风险","scenario":"procurement"})
    assert res.status_code==200 and res.json()["steps"][0]["title"]=="需求与采购约束"
    assert c.post("/api/evaluate/demo?scenario=consumer").status_code==200
    assert c.post("/api/demo/load?scenario=unknown").status_code==400
    assert c.post("/api/research",json={"query":"测试任务","scenario":"unknown"}).status_code==400

def test_fixtures_identified_as_fictional():
    for scenario,definition in SCENARIOS.items():
        assert len(definition["steps"])==5
        if scenario!="healthcare":
            assert all("虚构" in d[2] or "模拟" in d[2] for d in definition["documents"])

def test_business_tools():
    f=funnel_metrics(100000,2100,42000)
    assert f["conversion_rate"]==.021 and f["cost_per_order"]==20
    with pytest.raises(ValueError): funnel_metrics(10,11,0)
    sample={"quantity":800,"max_days":30,"max_defect_rate":.01,
        "alpha":{"unit_price":680,"shipping":8000,"days":21,"defect_rate":.008},
        "beta":{"unit_price":630,"shipping":25000,"days":45,"defect_rate":.014}}
    r=compare_suppliers(**sample)
    assert r["suppliers"]["alpha"]["quoted_cost"]==552000
    assert r["suppliers"]["alpha"]["meets_constraints"]
    assert r["suppliers"]["beta"]["quoted_cost"]==529000
    assert r["suppliers"]["beta"]["risk_flags"]==["late_delivery","defect_threshold"]
    c=TestClient(api.app)
    assert c.post("/api/tools/funnel",json={"visits":100000,"orders":2100,"ad_spend":42000}).status_code==200
    assert c.post("/api/tools/supplier-compare",json=sample).json()["suppliers"]["alpha"]["meets_constraints"]
