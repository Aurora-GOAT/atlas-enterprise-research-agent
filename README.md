# Atlas — Enterprise Research Agent

[![Tests](https://img.shields.io/badge/tests-local%20pytest-blue)](#testing-and-metrics) ![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab) ![Stage](https://img.shields.io/badge/stage-local%20MVP-087c74) ![Data](https://img.shields.io/badge/demo-synthetic%20only-777)

> **Evidence-first enterprise research assistant** built as an end-to-end product-manager / engineering portfolio project. Users can import public documents, break a broad research request into five analyzable tasks, retrieve attributable evidence, generate a cited report, model a revenue scenario, and evaluate retrieval quality against a labeled benchmark. **Runs offline without an API key.**

**中文简介：** 面向企业研究人员的可追溯 AI Agent 原型：研究任务拆解 → 本地知识库检索 → 来源核验与缺口提示 → 报告生成 → 检索评估。支持中文/英文混合内容。

## ✨ Product walkthrough

1. Click **加载合成演示资料** (load six explicitly fictional company documents).
2. Ask: `分析 NeuroBridge Medical 的技术、市场、竞品、财务与投资风险，列出尽调问题。`
3. Review five planned research dimensions, source-indexed extracts `[S1]`… and evidence gaps.
4. Export a Markdown report. Adjust a what-if revenue calculation using the deterministic tool.
5. Open the **质量评估** tab to run labeled Hit@3 / MRR retrieval benchmarks.

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
| POST | `/api/demo/load` | Load six synthetic documents |
| POST | `/api/documents/upload` | Upload PDF/DOCX/TXT/MD/CSV; 8 MB max |
| POST | `/api/research` | Run 5-step research workflow |
| GET | `/api/runs/{run_id}/download` | Export cited Markdown report |
| POST | `/api/tools/revenue` | Calculate scenario revenue from explicit input |
| POST | `/api/evaluate/demo` | Measure retrieval on 10 labeled cases |
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
