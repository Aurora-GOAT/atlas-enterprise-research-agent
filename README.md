# Atlas — Enterprise Research Agent

[![Tests](https://img.shields.io/badge/tests-local%20pytest-blue)](#testing-and-metrics) ![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab) ![Stage](https://img.shields.io/badge/stage-local%20MVP-087c74) ![Data](https://img.shields.io/badge/demo-synthetic%20only-777)

> **Evidence-first enterprise research assistant** built as an end-to-end product-manager / engineering portfolio project. Users can import public documents, choose among three business workflows (consumer brand research, supplier procurement, medical technology), break a request into five scenario-specific steps, retrieve attributable evidence, generate a cited report, run deterministic business calculators, and evaluate retrieval against small labeled synthetic benchmarks. **Runs offline without an API key.**

**中文简介：** 面向企业研究人员的可追溯 AI Agent 原型：研究任务拆解 → 本地知识库检索 → 来源核验与缺口提示 → 报告生成 → 检索评估。支持中文/英文混合内容。

## ✨ Product walkthrough

1. Select **消费品牌 / 企业采购 / 医疗科技**, then click **加载合成演示资料** (replaces prior synthetic demo files, but retains manually uploaded local files).
2. Run the pre-filled research question for a fictional consumer brand, fictional procurement operation or fictional medical technology company.
3. Review five planned research dimensions, source-indexed extracts `[S1]`… and evidence gaps.
4. Export a Markdown report. Use scenario-specific tools for consumer funnel or supplier constraints; market revenue calculator remains available.
5. Open the **质量评估** tab to run each synthetic scenario's labeled Hit@3 / MRR retrieval benchmark.

![Product screenshot](docs/screenshot.webp)

## Run in 3 minutes

Prerequisites: **Python 3.11+**. From the repository root:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Open **http://127.0.0.1:8000** in a browser. This application binds to localhost by default.

### Optional LLM-assisted draft

The base app needs **no key**. For optional OpenAI-compatible text synthesis, configure environment variables outside Git:

```bash
# Linux / macOS (example; do not paste a real token in chat or commit it)
export OPENAI_API_KEY="<your-key>"
export OPENAI_MODEL="gpt-4.1-mini"
python run.py
```

Then enable **大模型辅助总结** in the UI. LLM synthesis receives only selected excerpts and is shown as a **separately labeled draft requiring human verification**. API errors fall back to offline evidence mode. User uploads are transmitted to the configured LLM endpoint **only when that option is enabled**; review data policies first. Do not enter secret API keys in the UI.

## Architecture

```mermaid
flowchart LR
    A[Research question] --> B[Planner: 5 business dimensions]
    B --> C[Local Retriever: TF-IDF char n-grams]
    D[PDF DOCX CSV TXT MD uploads] --> E[Local chunk index]
    E --> C
    C --> F[Evidence registry: source ID + excerpt]
    F --> G[Grounded report with missing-evidence flags]
    F --> H[Optional LLM draft; explicit uncertainty]
    G --> I[Markdown export and human review]
    H --> I
    J[Scenario assumptions] --> K[Deterministic math tool]
    L[Labeled synthetic benchmark] --> M[Hit@3 / MRR evaluation]
```

- **Backend:** FastAPI, Pydantic, scikit-learn, httpx; PDF/DOCX ingestion via PyMuPDF/python-docx.
- **Frontend:** dependency-free HTML/CSS/JavaScript, responsive desktop/mobile layouts.
- **Knowledge:** in-process TF-IDF index rebuilt on each run; locally persisted JSON documents and reports in `workspace/` (gitignored).
- **Orchestration:** transparent `planner → retriever → evidence registry → report`, not a claim of autonomous browsing/multi-agent reasoning.
- **Tools:** explicit scenario revenue calculator (`/api/tools/revenue`); supporting CAGR and cash-runway Python functions.
- **Evaluation:** 10 human-authored labels for fictional source retrieval. Metrics are actual executed results, **not** product-market-fit claims.

## API quick reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/documents` | List local sources |
| GET | `/api/scenarios` | List available business demo scenarios |
| POST | `/api/demo/load?scenario=consumer` | Load a synthetic scenario corpus (consumer / procurement / healthcare) |
| POST | `/api/documents/upload` | Upload PDF/DOCX/TXT/MD/CSV; 8 MB max |
| POST | `/api/research` | Run 5-step research workflow |
| GET | `/api/runs/{run_id}/download` | Export cited Markdown report |
| POST | `/api/tools/revenue` | Calculate scenario revenue from explicit input |
| POST | `/api/tools/funnel` | Calculate consumer conversion / ad spend per order |
| POST | `/api/tools/supplier-compare` | Compare supplier landed quote / hard constraints |
| POST | `/api/evaluate/demo?scenario=consumer` | Retrieval benchmark (10 healthcare / 6 consumer / 6 procurement synthetic cases) |
| GET | `/docs` | Interactive OpenAPI API docs |

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/demo/load
curl -s http://127.0.0.1:8000/api/research \
  -H 'Content-Type: application/json' \
  -d '{"query":"分析医疗器械商业化与投资风险","use_llm":false}'
```

## Testing and metrics

```bash
pip install -r requirements-dev.txt
pytest -q
```

This tests document parsing, retrieval, citation consistency, missing data behavior, safe LLM fallback, API end-to-end workflow, deterministic numerical tools, and benchmark operation.

Run the real 10-case benchmark from the web UI or API. Current local results are recorded in [`docs/evaluation.md`](docs/evaluation.md). These scores describe **retrieval of synthetic sources only**; they do **not** establish accuracy of real commercial claims, human time saved, customer adoption, or hallucination rate.

## Scope & limitations

**What works now:** local document ingestion, task planning, source-referenced search, markdown reporting, missing-evidence flags, optional evidence-conditioned LLM notes, scenario tool, benchmark, tests, interactive UI.

**Not implemented / not validated:** real-time web research, authentication, multi-tenant permissions, production observability, real-world document annotation ground truth, security auditing, user-interview validation, enterprise integration (Slack/Drive/CRM), autonomous browser actions, citation-level claim verification. PDFs must have a text layer; scanned documents are not OCRed.

**Important security notes:** treat every uploaded document as untrusted content; any LLM must ignore instructions embedded in sources. The MVP stores uploads in local plaintext JSON and is intended for **localhost use only**. **Do not deploy publicly** with uploads enabled without authentication, rate limiting, malware scanning, encrypted storage, upload isolation, and a privacy review. Never upload confidential employer/client files. Do not commit `.env` or `workspace/`.

## Portfolio framing

This is a **self-directed product + engineering portfolio prototype**, not professional PE investment experience or a deployed enterprise SaaS. It can demonstrate product scoping, user workflows, RAG-style retrieval, evidence controls, tool design, UX, measurable evaluation, and tests. Distinguish fictional datasets, your own product design, and real validation when discussing it in interviews. See [`docs/PRD.md`](docs/PRD.md), [`docs/architecture.md`](docs/architecture.md), and [`docs/interview-story.md`](docs/interview-story.md).

## License

MIT — see [LICENSE](LICENSE).

### Windows quick start (中文)

After installing Python 3.11+, double-click **`start_windows.bat`**. It creates a local virtual environment, installs the requirements, and opens the app on `http://127.0.0.1:8000`. See the [Chinese quick-start guide](docs/中文使用指南.md).


## Cross-industry v0.2 update (2026-10-13)

Added two independent fictional verticals beyond medical devices: **consumer brand competitive/growth research** and **enterprise purchasing supplier comparison**. Each has a distinct research plan and provenance-linked documents. The UI switches demo corpora, runs a matching small benchmark, and includes simple deterministic business calculators. Regression suite: **18 tests locally passed** during development (consult live GitHub Actions for current remote CI). All results describe synthetic fixtures, *not* validated user outcomes. **No autonomous tool selection, production deployment or genuine customer research is claimed.** See [scope and product validation plan](docs/cross-industry-v0.2.md).
