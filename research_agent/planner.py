"""Deterministic, explainable business-scenario plans (not autonomous LLM planning)."""
from __future__ import annotations
from .models import PlanStep
from .scenarios import SCENARIOS, ensure_scenario

def make_plan(user_query: str, scenario: str = "healthcare") -> list[PlanStep]:
    ensure_scenario(scenario)
    return [PlanStep(key=key, title=title, query=f"{user_query} {hints}")
            for key, title, hints in SCENARIOS[scenario]["steps"]]
