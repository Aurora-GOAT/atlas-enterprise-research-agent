# Atlas v0.2 — Cross-industry product validation notes

## Product hypothesis
An evidence-first workflow (plan → source retrieval → referenced report → human review) may reduce manual reformatting across several enterprise tasks. **This has not yet been validated with real users.** The purpose of v0.2 is to test *technical portability* outside healthcare, not assert customer demand.

## Implemented synthetic scenarios
| Mode | Synthetic organization | Task-specific five-step research outline | Supplemental deterministic tool |
|---|---|---|---|
| Consumer | LumenLeaf (fictional brand) | Audience, funnel, competitors, unit economics, experiments | Visits / orders conversion and spend-per-order |
| Procurement | Northstar Operations (fictional purchasing team) | Requirements, cost, delivery, quality, decision risks | Quoted landed-cost and hard-constraint comparison |
| Healthcare | NeuroBridge Medical (fictional) | Product, market, competition, risk, milestones | Market-revenue calculator |

Demo switch replaces only *synthetic-demo* documents; previously user-uploaded local documents persist. To prevent mixed corpora, users should clear or isolate uploaded documents before formal per-scenario evaluation. Evaluation endpoint itself operates on each scenario's independent fixture corpus.

## Product boundaries
- The planner uses scenario-specific **rule-defined steps**, not an autonomous LLM planner.
- TF-IDF is lexical retrieval, not embedding-vector semantic RAG.
- The calculator is triggered **manually**, not autonomously selected by the language model.
- No real suppliers, user interviews, customer data, deployment, telemetry, A/B experiments, or measured time saving.
- 10 synthetic healthcare cases + 6 consumer cases + 6 procurement cases are small evaluation samples. Retrieval precision must not be conflated with factual correctness.
- Healthcare, consumer and procurement descriptions and figures are explicitly invented.
- Do not upload confidential material to the public repo or an internet-facing service.

## How to demo (localhost only)
1. Choose **消费品牌**, click load synthetic demo data, ask the auto-filled question; examine trace and sources.
2. Use the consumer funnel calculator; observe that advertising spend divided by *all* orders is not labeled true acquisition CAC.
3. Switch to **企业采购**; load that demo dataset. Compare Alpha/Beta price and lead-time/defect constraints using the calculator.
4. Switch to **医疗科技** to show the original vertical still works.
5. For each scenario, open **质量评估**, run the labeled retrieval benchmark and explain what it does *not* measure.

## What needs real product discovery
Interview 3–5 actual workers with consent; create a blinded public-document task benchmark, measure citation support, task success, time and correction rates; compare with baseline manual research and general-purpose AI products. Only then claim real business value.
