"""Local JSON workspace. Intended for single-user laptop MVP only."""
from __future__ import annotations
import json
import os
from pathlib import Path
from .models import Document, ResearchResult


class LocalStore:
    def __init__(self, directory: str | Path | None = None):
        self.root = Path(directory or os.environ.get("ERA_WORKSPACE", "./workspace"))
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "runs").mkdir(exist_ok=True)
        self.docs_file = self.root / "documents.json"

    def documents(self) -> list[Document]:
        if not self.docs_file.exists():
            return []
        return [Document.model_validate(x) for x in json.loads(self.docs_file.read_text(encoding="utf-8"))]

    def save_documents(self, docs: list[Document]):
        self.docs_file.write_text(json.dumps([d.model_dump() for d in docs], ensure_ascii=False, indent=2), encoding="utf-8")

    def add_document(self, doc: Document) -> None:
        docs = self.documents()
        if len(docs) >= 40:
            raise ValueError("Demo workspace limit: 40 documents")
        docs.append(doc)
        self.save_documents(docs)

    def save_result(self, result: ResearchResult) -> None:
        (self.root / "runs" / (result.run_id + ".json")).write_text(
            result.model_dump_json(indent=2), encoding="utf-8"
        )

    def load_result(self, run_id: str) -> ResearchResult | None:
        if not run_id.startswith("RUN-") or not run_id[4:].isalnum():
            return None
        path = self.root / "runs" / (run_id + ".json")
        return ResearchResult.model_validate_json(path.read_text(encoding="utf-8")) if path.exists() else None
