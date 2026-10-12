from fastapi.testclient import TestClient
from research_agent import api
from research_agent.store import LocalStore


def test_workflow(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "store", LocalStore(tmp_path))
    client = TestClient(api.app)
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/api/documents").json() == []
    assert client.post("/api/demo/load").status_code == 200
    assert len(client.get("/api/documents").json()) == 6
    res = client.post("/api/research", json={"query":"分析设备技术市场和投资风险"})
    assert res.status_code == 200
    r = res.json()
    assert r["run_id"].startswith("RUN-")
    assert len(r["steps"]) == 5
    assert r["evidence"]
    assert client.get(f"/api/runs/{r['run_id']}/download").status_code == 200
    assert client.post("/api/evaluate/demo").status_code == 200
    assert client.get("/").status_code == 200
    scenario=client.post("/api/tools/revenue", json={"users":600,"adoption_rate":0.05,"unit_price":450000})
    assert scenario.status_code == 200 and scenario.json()["value"] == 13500000


def test_validations(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "store", LocalStore(tmp_path))
    client = TestClient(api.app)
    assert client.post("/api/research", json={"query":"hi"}).status_code == 422
    assert client.post("/api/documents/upload", files={"file":("bad.exe",b"bad content")}).status_code == 400
    assert client.get("/api/runs/../../etc/passwd/download").status_code in {404, 422}
