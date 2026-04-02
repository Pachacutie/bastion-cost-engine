"""ETF (Early Termination Fee) calculation engine.

Implements per-provider ETF formulas, timeline generation, and optimal exit detection.
"""

from __future__ import annotations

from bastion_cost.data.providers import MONITORING
from bastion_cost.engine.calculator import true_monthly_cost


def etf_at_month(
    provider: str,
    tier_index: int,
    contract_months: int,
    month: int,
    equipment_total: float | None = None,
) -> float:
    """Calculate ETF owed if canceling at a specific month."""
    if contract_months == 0:
        if provider == "cove" and equipment_total and equipment_total > 0:
            return float(equipment_total)
        return 0.0

    remaining = max(0, contract_months - month)
    if remaining == 0:
        return 0.0

    monthly = MONITORING[provider]["tiers"][tier_index]["monthly"]

    if provider == "frontpoint":
        return remaining * monthly * 0.80

    if provider == "adt":
        return remaining * monthly * 0.75

    if provider == "vivint":
        equip = equipment_total or 0
        balance = equip * remaining / contract_months
        penalty = 300 if month <= 12 else 150
        return balance + penalty

    if provider == "cove":
        return float(equipment_total) if equipment_total else 0.0

    return 0.0


def etf_timeline(
    provider: str,
    tier_index: int,
    contract_months: int,
    equipment_total: float | None = None,
) -> list[tuple[int, float]]:
    """Generate ETF amounts at 6-month intervals through the contract."""
    if contract_months == 0:
        return []

    points = []
    for month in range(6, contract_months + 1, 6):
        amount = etf_at_month(provider, tier_index, contract_months, month, equipment_total)
        points.append((month, amount))

    if contract_months % 6 != 0:
        amount = etf_at_month(provider, tier_index, contract_months, contract_months, equipment_total)
        points.append((contract_months, amount))

    return points


def optimal_exit_month(
    provider: str,
    tier_index: int,
    contract_months: int,
    equipment_total: float | None = None,
) -> int | None:
    """Find the month where paying the ETF is cheaper than riding out the contract."""
    if contract_months == 0:
        return None

    monthly = true_monthly_cost(provider, tier_index, {})["total"]

    for month in range(1, contract_months + 1):
        etf = etf_at_month(provider, tier_index, contract_months, month, equipment_total)
        remaining_cost = (contract_months - month) * monthly
        if etf < remaining_cost:
            return month

    return None
