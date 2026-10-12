"""Deterministic calculators for synthetic consumer and procurement scenarios.

Outputs are calculations based on user input; they do not fact-check documents,
replace procurement approvals or autonomously choose a supplier.
"""
from __future__ import annotations

def funnel_metrics(visits: int, orders: int, ad_spend: float) -> dict:
    if visits <= 0 or not 0 <= orders <= visits or ad_spend < 0:
        raise ValueError("visits must be positive; 0 <= orders <= visits; spend >= 0")
    return {
        "conversion_rate": round(orders/visits, 5),
        "cost_per_order": round(ad_spend/orders, 2) if orders else None,
        "warning": "广告支出/全部订单不等于真正新增获客CAC；须核验订单归因与口径。",
    }

def compare_suppliers(quantity: int, max_days: int, max_defect_rate: float,
                      alpha: dict, beta: dict) -> dict:
    if quantity <= 0 or max_days < 1 or not 0 <= max_defect_rate <= 1:
        raise ValueError("invalid procurement constraints")
    answer = {}
    for name,item in [("alpha",alpha),("beta",beta)]:
        unit_price,shipping,days,defect_rate = (
            item[x] for x in ("unit_price","shipping","days","defect_rate"))
        if unit_price < 0 or shipping < 0 or days < 1 or not 0 <= defect_rate <= 1:
            raise ValueError("invalid supplier inputs")
        flags = []
        if days > max_days: flags.append("late_delivery")
        if defect_rate > max_defect_rate: flags.append("defect_threshold")
        answer[name] = {
            "quoted_cost": round(quantity*unit_price+shipping,2),
            "meets_constraints": len(flags)==0,
            "risk_flags":flags,
        }
    return {"suppliers":answer,
            "caveat":"只对输入报价、交期与历史缺陷率做规则校验；不替代真实尽调、合同评估或采购审批。"}
