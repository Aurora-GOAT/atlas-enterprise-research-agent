"""Local-only FastAPI server + static, dependency-light interface."""
from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from .demo import demo_documents, demo_cases
from .engine import build_research
from .evaluation import evaluate
from .ingest import make_document, MAX_BYTES
from .models import ResearchRequest
from .store import LocalStore
from .tools import market_revenue, cagr, cash_runway
from pydantic import BaseModel, Field

class ScenarioInput(BaseModel):
    users: float = Field(ge=0, le=1e12)
    adoption_rate: float = Field(ge=0, le=1)
    unit_price: float = Field(ge=0, le=1e12)



ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="Enterprise Research Agent", version="0.1.0",
              description="Offline-first, evidence-linked business research assistant")
store = LocalStore()
app.mount("/assets", StaticFiles(directory=ROOT / "web"), name="assets")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(ROOT / "web" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}


@app.get("/api/documents")
def documents():
    return [{"document_id": d.document_id, "title": d.title, "filename": d.filename,
             "source_type": d.source_type, "chars": len(d.text)} for d in store.documents()]


@app.post("/api/demo/load")
def load_demo():
    old = [d for d in store.documents() if d.source_type != "synthetic-demo"]
    docs = old + demo_documents()
    if len(docs) > 40:
        raise HTTPException(400, "Workspace document limit")
    store.save_documents(docs)
    return {"loaded": 6, "total": len(docs)}


@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        payload = await file.read(MAX_BYTES + 1)
        doc = make_document(file.filename or "unnamed.txt", payload)
        store.add_document(doc)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return {"document_id": doc.document_id, "title": doc.title, "chars": len(doc.text)}


@app.post("/api/research")
def research(request: ResearchRequest):
    result = build_research(request.query, store.documents(), request.top_k, request.use_llm)
    store.save_result(result)
    return result


@app.get("/api/runs/{run_id}/download")
def download_report(run_id: str):
    result = store.load_result(run_id)
    if result is None:
        raise HTTPException(404, "Report not found")
    return PlainTextResponse(result.report_markdown, media_type="text/markdown",
                             headers={"Content-Disposition": f'attachment; filename="{run_id}.md"'})


@app.post("/api/evaluate/demo")
def evaluate_demo():
    return evaluate(demo_documents(), demo_cases())


@app.post("/api/tools/revenue")
def revenue_tool(params: ScenarioInput):
    """Deterministic scenario calculation, separate from evidence-based research."""
    value = market_revenue(params.users, params.adoption_rate, params.unit_price)
    return {"formula": "users × adoption_rate × unit_price", "value": round(value, 2),
            "unit": "与输入价格相同的货币单位", "disclaimer": "仅计算用户输入的假设，不等于已核实市场规模或营业收入"}
