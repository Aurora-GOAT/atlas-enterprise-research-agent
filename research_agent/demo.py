"""Synthetic, explicitly fictional demonstration corpus."""
from __future__ import annotations
import json
from pathlib import Path
from .models import Document, EvaluationCase
from .scenarios import SCENARIOS, ensure_scenario

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def demo_documents(scenario: str = "healthcare") -> list[Document]:
    ensure_scenario(scenario)
    if scenario != "healthcare":
        return [Document(document_id=f"DEMO-{scenario}-{name}", title=title,
                         filename=f"{scenario}_{name}.md", source_type="synthetic-demo", text=text)
                for name, title, text in SCENARIOS[scenario]["documents"]]
    return [
        Document(document_id=f"DEMO-{name}", title=title, filename=f"{name}.md",
                 source_type="synthetic-demo", text=(EXAMPLES / f"{name}.md").read_text(encoding="utf-8"))
        for name, title in [
            ("company", "模拟公司概览"), ("market", "模拟市场与客户"),
            ("product", "模拟产品及临床证据"), ("competition", "模拟竞争格局"),
            ("finance", "模拟财务与商业模式"), ("risks", "模拟风险与里程碑")
        ]
    ]


def demo_cases(scenario: str = "healthcare") -> list[EvaluationCase]:
    ensure_scenario(scenario)
    if scenario != "healthcare":
        return [EvaluationCase(query=query, expected_documents=[f"DEMO-{scenario}-{name}"])
                for query, name in SCENARIOS[scenario]["cases"]]
    raw = json.loads((EXAMPLES / "evaluation_cases.json").read_text(encoding="utf-8"))
    return [EvaluationCase.model_validate(x) for x in raw]
