"""Synthetic, explicitly fictional demonstration corpus."""
from __future__ import annotations
import json
from pathlib import Path
from .models import Document, EvaluationCase

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def demo_documents() -> list[Document]:
    return [
        Document(document_id=f"DEMO-{name}", title=title, filename=f"{name}.md",
                 source_type="synthetic-demo", text=(EXAMPLES / f"{name}.md").read_text(encoding="utf-8"))
        for name, title in [
            ("company", "模拟公司概览"), ("market", "模拟市场与客户"),
            ("product", "模拟产品及临床证据"), ("competition", "模拟竞争格局"),
            ("finance", "模拟财务与商业模式"), ("risks", "模拟风险与里程碑")
        ]
    ]


def demo_cases() -> list[EvaluationCase]:
    raw = json.loads((EXAMPLES / "evaluation_cases.json").read_text(encoding="utf-8"))
    return [EvaluationCase.model_validate(x) for x in raw]
