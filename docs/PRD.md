# Atlas — Product Requirements Document (PRD)

**Version**: 0.1.0 (portfolio MVP)  
**Product type**: Evidence-grounded Enterprise Research Agent  
**Project status**: runnable local prototype; no real customer validation completed

## 1. Problem and customer hypothesis

**Hypothesized users:** corporate development associates, business analysts, BD professionals and industry researchers who repeatedly read fragmented PDFs, internal briefs, spreadsheets and competitive intelligence.

**Jobs to be done:** "When I receive a vaguely defined company research request, I want to collect relevant existing evidence, organize it by investment/business questions, identify gaps, and draft a reviewable report without losing track of where numbers came from."

**Unvalidated pain-point hypotheses:** (H1) multi-source search is time-consuming, (H2) copying facts loses provenance, (H3) team members spend time checking claims and preparing reporting templates. These are hypotheses drawn from workflow modeling, **not user interviews**. Real interviews and time-motion measurements remain TODO.

## 2. User stories / acceptance criteria

| ID | User story | Acceptance criterion | MVP status |
|---|---|---|---|
| US-01 | As a researcher, I can upload common documents | TXT/MD/CSV/PDF/DOCX up to 8MB, informative errors | Implemented |
| US-02 | As a researcher, I can start from an ambiguous business question | Query becomes 5 visible research steps | Implemented |
| US-03 | As a reviewer, I can trace content to sources | Cited excerpt includes document title and internal source ID | Implemented |
| US-04 | As a reviewer, I am told when evidence is missing | Empty retrieval produces gap rather than invented analysis | Implemented |
| US-05 | As a PM, I can measure retrieval behavior | Benchmark runs labeled Hit@3 and MRR | Implemented |
| US-06 | As an analyst, I can calculate a what-if market revenue scenario | Calculator returns expected result with assumptions and disclaimer | Implemented |
| US-07 | As a researcher, I can export a draft | Export source-linked Markdown | Implemented |
| US-08 | As a reviewer, I can check contradictory sources automatically | Contradiction flags with cited evidence | Not yet implemented |
| US-09 | As an enterprise admin, I can enforce user permissions | RBAC, isolated storage, audit records | Not yet implemented |
| US-10 | As a PM, I can prove task time savings | Real measured baseline vs tool usage | Not yet validated |

## 3. Workflow and design choices

1. **Input**: explicit query, manual file upload or fictional demo corpus.
2. **Planner**: 5 transparent task templates: technology / market / competition / risk / milestones; prioritizes explainability over free-form agentic planning.
3. **Retrieval**: character n-gram TF-IDF cosine similarity over paragraph chunks; avoids an external embedding service and works offline with mixed Chinese/English.
4. **Evidence registry**: de-duplicates `(document_id, chunk_id)`, labels each retrieved excerpt `[S#]`, adds document and chunk trace.
5. **Grounded draft**: organizes direct extracts, displays absent source warnings; optional LLM writes a separately marked interpretative draft from retrieved excerpts only.
6. **Human in the loop**: researcher must check critical facts, source currency and conclusions; no one-click investment decision.
7. **Evaluation**: synthetic labeled gold documents (10 questions), Hit@3, MRR.

**Why not promise a multi-agent autonomous system?** The MVP is intentionally a bounded agent workflow. Autonomous crawling and unconstrained tool access increase privacy, prompt-injection and hallucination risks without a verified business need.

## 4. Product success metrics (definitions, not fabricated achievements)

- **Retrieval Hit@3:** fraction of benchmark questions where at least one expected source is among top-3 results.
- **MRR:** mean of `1 / rank(first expected document)` for evaluated cases; zero when not found.
- **Evidence coverage:** fraction of five task dimensions with ≥1 retrieved excerpt. This is **not factual accuracy**.
- **Claim citation validity (future):** fraction of human-reviewed factual claims correctly supported by cited spans.
- **Task success (future):** percent of real users who complete target reporting tasks without external rescue.
- **Time saved (future):** `(human baseline time - assisted task time) / human baseline time`, measured with comparable tasks and qualified participants.
- **Cost/latency (future):** API token cost and end-to-end task p50/p95 after deploying LLM features.

## 5. Design and technical tradeoffs

- Local document indexing is simple and private but does not scale to thousands of documents; future: local SQLite FTS + hybrid vector search, reranking and metadata filters.
- Character n-gram search avoids a bilingual tokenization dependency but can miss semantic paraphrases; evaluation may suggest hybrid embeddings.
- Citations are excerpts, not independently verified facts; reviewer trust still requires source checks.
- Global single-user workspace is not appropriate for production; future: auth/tenancy/ACL and auditable retention.
- LLM can add natural-language synthesis but must show uncertainty and preserve evidence boundaries.

## 6. Future product experiments

- Interview 5–8 actual analysts across different industries; record permissioned, anonymized workflow pain points.
- Conduct task-level usability testing, comparing baseline manual research to assisted tasks on the same public corpus.
- Build a held-out 30–50-question domain benchmark with labeled spans and contradiction cases.
- Test a dual retrieval model (TF-IDF + embeddings) and compare Hit@3/MRR, latency, and cost.
- Add typed tool calling with explicit human approval for external actions and source import.
- Build proper enterprise access control, audit trail, source retention policy, and safe redaction.

## 7. Non-goals

No automatic investment advice, no guarantee of company facts, no external live browsing, no automatic export to confidential systems, no claimed real-user adoption.
