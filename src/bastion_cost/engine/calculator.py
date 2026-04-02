"""Core cost calculation engine.

Computes true monthly cost, 3-year total cost of ownership,
equipment markup percentages, and DIY alternative totals.
"""

from __future__ import annotations

from bastion_cost.data.providers import MONITORING, EQUIPMENT, HIDDEN_FEES
from bastion_cost.data.diy import diy_equipment_cost, SELF_MONITORING_MONTHLY


def true_monthly_cost(
    provider: str,
    tier_index: int,
    equipment: dict[str, int],
    financed: bool = False,
) -> dict:
    """Calculate true monthly cost including hidden recurring fees.

    Returns dict with 'advertised', 'line_items' list, and 'total'.
    """
    tier = MONITORING[provider]["tiers"][tier_index]
    advertised = tier["monthly"]
    fees = HIDDEN_FEES[provider]
    line_items = []

    if fees.get("cellular_monthly", 0) > 0:
        line_items.append({
            "name": "Cellular maintenance fee",
            "amount": fees["cellular_monthly"],
            "mandatory": True,
            "disclosed": False,
        })

    if fees.get("premium_service_monthly", 0) > 0:
        line_items.append({
            "name": "Premium Service Plan",
            "amount": fees["premium_service_monthly"],
            "mandatory": False,
            "disclosed": False,
        })

    if fees.get("camera_addon_monthly", 0) > 0:
        num_cameras = sum(
            equipment.get(k, 0) for k in ("indoor_camera", "outdoor_camera", "video_doorbell")
        )
        extra_cameras = max(0, num_cameras - 1)
        if extra_cameras > 0:
            line_items.append({
                "name": "Additional camera fee",
                "amount": fees["camera_addon_monthly"] * extra_cameras,
                "mandatory": False,
                "disclosed": True,
            })

    if fees.get("guard_response_monthly", 0) > 0:
        line_items.append({
            "name": "Guard response fee",
            "amount": fees["guard_response_monthly"],
            "mandatory": False,
            "disclosed": False,
        })

    if fees.get("permit_processing", 0) > 0:
        line_items.append({
            "name": "Permit processing fee",
            "amount": fees["permit_processing"],
            "mandatory": False,
            "disclosed": False,
        })

    if fees.get("camera_standalone_monthly", 0) > 0:
        num_cameras = sum(
            equipment.get(k, 0) for k in ("indoor_camera", "outdoor_camera", "video_doorbell")
        )
        if num_cameras > 0:
            line_items.append({
                "name": "Camera cloud fee",
                "amount": fees["camera_standalone_monthly"] * num_cameras,
                "mandatory": False,
                "disclosed": True,
            })

    if fees.get("economy_surcharge_monthly", 0) > 0 and financed:
        line_items.append({
            "name": "Economy Plan surcharge",
            "amount": fees["economy_surcharge_monthly"],
            "mandatory": True,
            "disclosed": False,
        })

    total = advertised + sum(item["amount"] for item in line_items)
    return {"advertised": advertised, "line_items": line_items, "total": total}


def equipment_cost(provider: str, equipment: dict[str, int]) -> float:
    """Total equipment cost from a specific provider. Skips None (not sold) devices."""
    total = 0.0
    for device_key, qty in equipment.items():
        if qty > 0 and device_key in EQUIPMENT:
            price = EQUIPMENT[device_key]["providers"].get(provider)
            if price is not None:
                total += price * qty
    return total


def three_year_total(
    provider: str,
    tier_index: int,
    contract_months: int,
    equipment: dict[str, int],
    financed: bool = False,
) -> dict:
    """Calculate 3-year total cost of ownership."""
    equip_total = equipment_cost(provider, equipment)
    monthly = true_monthly_cost(provider, tier_index, equipment, financed=financed)
    monitoring_36mo = monthly["total"] * 36
    fees = HIDDEN_FEES[provider]

    one_time = fees.get("activation", 0) + fees.get("installation", 0)
    grand = equip_total + monitoring_36mo + one_time

    diy = diy_equipment_cost(equipment) + (SELF_MONITORING_MONTHLY * 36)

    return {
        "equipment_total": equip_total,
        "true_monthly": monthly["total"],
        "monthly_breakdown": monthly,
        "monitoring_36mo": monitoring_36mo,
        "one_time_fees": one_time,
        "grand_total": grand,
        "diy_total": diy,
        "premium_over_diy": grand - diy,
    }


def equipment_markup(equipment: dict[str, int], provider: str) -> dict:
    """Per-device markup comparison: provider price vs generic retail."""
    items = []
    provider_total = 0.0
    generic_total = 0.0

    for device_key, qty in equipment.items():
        if qty <= 0 or device_key not in EQUIPMENT:
            continue
        device = EQUIPMENT[device_key]
        price = device["providers"].get(provider)
        if price is None:
            continue
        generic = device["generic_retail"]
        pct = ((price - generic) / generic) * 100 if generic > 0 else 0
        p_line = price * qty
        g_line = generic * qty
        items.append({
            "device_key": device_key,
            "name": device["generic_name"],
            "category": device["category"],
            "qty": qty,
            "provider_price": price,
            "generic_price": generic,
            "provider_line_total": p_line,
            "generic_line_total": g_line,
            "markup_pct": pct,
            "color": markup_color(pct),
        })
        provider_total += p_line
        generic_total += g_line

    overall_pct = ((provider_total - generic_total) / generic_total) * 100 if generic_total > 0 else 0

    return {
        "items": items,
        "provider_total": provider_total,
        "generic_total": generic_total,
        "overall_markup_pct": overall_pct,
    }


def markup_color(pct: float) -> str:
    """Color bucket: green (<100%), yellow (100-300%), red (>300%)."""
    if pct > 300:
        return "red"
    if pct >= 100:
        return "yellow"
    return "green"


def diy_total(equipment: dict[str, int]) -> dict:
    """DIY alternative total: generic equipment + $0 self-monitoring."""
    equip = diy_equipment_cost(equipment)
    monitoring = SELF_MONITORING_MONTHLY * 36
    return {
        "equipment": equip,
        "monitoring_36mo": monitoring,
        "grand_total": equip + monitoring,
    }
