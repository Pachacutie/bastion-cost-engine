"""Cross-provider comparison engine.

Calculates cost for all providers + DIY given the same equipment profile.
"""

from __future__ import annotations

from bastion_cost.data.providers import MONITORING, HIDDEN_FEES, PROVIDER_NAMES
from bastion_cost.data.diy import diy_equipment_cost, SELF_MONITORING_MONTHLY
from bastion_cost.engine.calculator import equipment_cost, true_monthly_cost


def compare_all(equipment: dict[str, int]) -> list[dict]:
    """Compare all providers + DIY for the same equipment profile.

    Each provider uses its highest available tier (max features).
    Sorted by 3-year total ascending.
    """
    results = []

    for provider, data in MONITORING.items():
        tier_index = len(data["tiers"]) - 1
        tier = data["tiers"][tier_index]

        equip = equipment_cost(provider, equipment)
        monthly_result = true_monthly_cost(provider, tier_index, equipment)
        monthly = monthly_result["total"]
        monitoring_36 = monthly * 36

        fees = HIDDEN_FEES[provider]
        one_time = fees.get("activation", 0) + fees.get("installation", 0)
        total_3yr = equip + monitoring_36 + one_time

        contract_months = max(data["contract_months"])
        if contract_months == 0:
            contract_str = "None"
            etf_desc = "$0 — cancel anytime"
        else:
            contract_str = f"{contract_months} mo"
            etf_desc = data["etf_description"]

        results.append({
            "provider": provider,
            "display_name": PROVIDER_NAMES[provider],
            "tier": tier["name"],
            "equipment_cost": equip,
            "monthly": monthly,
            "three_year_total": total_3yr,
            "contract": contract_str,
            "etf_description": etf_desc,
        })

    diy_equip = diy_equipment_cost(equipment)
    diy_monitoring = SELF_MONITORING_MONTHLY * 36
    results.append({
        "provider": "diy",
        "display_name": "DIY (Self-Monitor)",
        "tier": "Self-monitor",
        "equipment_cost": diy_equip,
        "monthly": SELF_MONITORING_MONTHLY,
        "three_year_total": diy_equip + diy_monitoring,
        "contract": "None",
        "etf_description": "$0 — no contract",
    })

    results.sort(key=lambda r: r["three_year_total"])
    return results
