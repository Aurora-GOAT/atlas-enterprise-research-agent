"""Small deterministic numeric tools used by product research."""
from __future__ import annotations


def cagr(first: float, last: float, years: int) -> float:
    if first <= 0 or last < 0 or years <= 0:
        raise ValueError("first must be positive, last nonnegative, years positive")
    return (last / first) ** (1 / years) - 1


def market_revenue(users: float, adoption_rate: float, price: float) -> float:
    if users < 0 or price < 0 or not 0 <= adoption_rate <= 1:
        raise ValueError("invalid revenue model assumptions")
    return users * adoption_rate * price


def cash_runway(cash: float, monthly_burn: float) -> float:
    if cash < 0 or monthly_burn <= 0:
        raise ValueError("cash must be nonnegative; burn must be positive")
    return cash / monthly_burn
