"""DIY alternative pricing for cost comparison.

Generic retail prices mirror EQUIPMENT['generic_retail'] values.
Self-monitoring is $0. Optional paid monitoring note included for transparency.
"""

from .providers import EQUIPMENT

SELF_MONITORING_MONTHLY = 0

PAID_MONITORING_NOTE = (
    "Optional: SuretyDIY ($10-15/mo) or Noonlight ($10/mo) "
    "for professional monitoring without a contract."
)


def diy_equipment_cost(equipment: dict[str, int]) -> float:
    """Total cost of equivalent generic/DIY equipment."""
    total = 0.0
    for device_key, qty in equipment.items():
        if qty > 0 and device_key in EQUIPMENT:
            total += EQUIPMENT[device_key]["generic_retail"] * qty
    return total
