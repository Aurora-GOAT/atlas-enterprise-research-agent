"""Transparent planning: domain-aware subquestions rather than opaque fake agents."""
from __future__ import annotations
from .models import PlanStep

PLANS = [
    ("technology", "技术与产品", "技术 产品 研发 临床 疗效 创新 工艺 技术壁垒 产品管线"),
    ("market", "市场与客户", "市场规模 目标客户 患者 需求 销量 渠道 增长 用户"),
    ("competition", "竞争与商业模式", "竞争 对手 竞品 商业模式 定价 销售 收入 替代"),
    ("risk", "风险与合规", "风险 注册 法规 合规 隐私 专利 现金流 不确定性"),
    ("milestone", "行动计划与关键里程碑", "里程碑 计划 时间 试点 上线 监管 交付"),
]


def make_plan(user_query: str) -> list[PlanStep]:
    return [PlanStep(key=key, title=title, query=f"{user_query} {hints}") for key, title, hints in PLANS]
