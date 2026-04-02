"""Tests that provider data dicts are complete and internally consistent."""

from bastion_cost.data.providers import MONITORING, EQUIPMENT, HIDDEN_FEES

EXPECTED_PROVIDERS = {"frontpoint", "adt", "ring", "simplisafe", "vivint", "abode", "cove"}


def test_all_providers_in_monitoring():
    assert set(MONITORING.keys()) == EXPECTED_PROVIDERS


def test_all_providers_in_hidden_fees():
    assert set(HIDDEN_FEES.keys()) == EXPECTED_PROVIDERS


def test_every_device_has_all_providers():
    for device_key, device in EQUIPMENT.items():
        assert set(device["providers"].keys()) == EXPECTED_PROVIDERS, (
            f"{device_key} missing providers: {EXPECTED_PROVIDERS - set(device['providers'].keys())}"
        )


def test_every_tier_has_required_fields():
    for provider, data in MONITORING.items():
        assert len(data["tiers"]) >= 1, f"{provider} has no tiers"
        for tier in data["tiers"]:
            assert "name" in tier, f"{provider} tier missing 'name'"
            assert "monthly" in tier, f"{provider} tier missing 'monthly'"
            assert "features" in tier, f"{provider} tier missing 'features'"
            assert isinstance(tier["monthly"], (int, float)), f"{provider} tier monthly not numeric"


def test_every_device_has_required_fields():
    for device_key, device in EQUIPMENT.items():
        assert "category" in device, f"{device_key} missing 'category'"
        assert "generic_retail" in device, f"{device_key} missing 'generic_retail'"
        assert "generic_name" in device, f"{device_key} missing 'generic_name'"


def test_no_negative_prices():
    for device_key, device in EQUIPMENT.items():
        assert device["generic_retail"] >= 0, f"{device_key} generic_retail is negative"
        for provider, price in device["providers"].items():
            if price is not None:
                assert price >= 0, f"{device_key}/{provider} price is negative"


def test_contract_months_are_valid():
    for provider, data in MONITORING.items():
        assert isinstance(data["contract_months"], list), f"{provider} contract_months not a list"
        for m in data["contract_months"]:
            assert isinstance(m, int) and m >= 0, f"{provider} invalid contract month: {m}"


def test_hidden_fees_have_notes():
    for provider, fees in HIDDEN_FEES.items():
        assert "notes" in fees, f"{provider} hidden fees missing 'notes'"
