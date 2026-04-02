"""Tests for core cost calculation engine."""

import pytest

from bastion_cost.engine.calculator import (
    true_monthly_cost,
    three_year_total,
    equipment_markup,
    equipment_cost,
    diy_total,
    markup_color,
)


class TestTrueMonthlyCost:
    def test_frontpoint_standard_no_hidden_fees(self):
        result = true_monthly_cost("frontpoint", 0, {})
        assert result["advertised"] == 34.99
        assert result["total"] == 34.99
        assert len(result["line_items"]) == 0

    def test_vivint_includes_cellular_and_premium(self):
        result = true_monthly_cost("vivint", 0, {})
        assert result["advertised"] == 24.99
        fees = {item["name"]: item["amount"] for item in result["line_items"]}
        assert fees["Cellular maintenance fee"] == 1.48
        assert fees["Premium Service Plan"] == 10.00
        assert result["total"] == pytest.approx(36.47)

    def test_vivint_camera_addon_with_cameras(self):
        result = true_monthly_cost("vivint", 0, {"indoor_camera": 2})
        fees = {item["name"]: item["amount"] for item in result["line_items"]}
        assert fees["Additional camera fee"] == 5.00

    def test_ring_no_hidden_fees(self):
        result = true_monthly_cost("ring", 2, {})
        assert result["advertised"] == 9.99
        assert result["total"] == 9.99

    def test_cove_economy_surcharge_when_financed(self, sample_equipment):
        result = true_monthly_cost("cove", 0, sample_equipment, financed=True)
        fees = {item["name"]: item["amount"] for item in result["line_items"]}
        assert fees["Economy Plan surcharge"] == 10.00

    def test_abode_camera_fees(self):
        result = true_monthly_cost("abode", 2, {"indoor_camera": 2})
        fees = {item["name"]: item["amount"] for item in result["line_items"]}
        assert "Camera cloud fee" in fees


class TestEquipmentCost:
    def test_basic_equipment(self, sample_equipment):
        cost = equipment_cost("frontpoint", sample_equipment)
        assert cost == pytest.approx(629.91)

    def test_none_device_excluded(self):
        cost = equipment_cost("frontpoint", {"indoor_camera": 2})
        assert cost == 0.0

    def test_zero_quantity_excluded(self):
        cost = equipment_cost("adt", {"door_window_sensor": 0})
        assert cost == 0.0


class TestThreeYearTotal:
    def test_adt_complete_36mo_dispatch_verification(self, full_equipment):
        result = three_year_total("adt", 2, 36, full_equipment)
        assert result["equipment_total"] == pytest.approx(958.98)
        assert result["one_time_fees"] > 0
        assert result["grand_total"] > 0

    def test_ring_no_contract_no_hidden_fees(self, sample_equipment):
        result = three_year_total("ring", 2, 0, sample_equipment)
        assert result["one_time_fees"] == 0

    def test_includes_diy_comparison(self, sample_equipment):
        result = three_year_total("adt", 2, 36, sample_equipment)
        assert "diy_total" in result
        assert result["diy_total"] < result["grand_total"]
        assert "premium_over_diy" in result


class TestEquipmentMarkup:
    def test_markup_percentage(self):
        result = equipment_markup({"door_window_sensor": 1}, "frontpoint")
        item = result["items"][0]
        assert item["provider_price"] == 34.99
        assert item["generic_price"] == 8
        assert item["markup_pct"] == pytest.approx(337.375)

    def test_none_device_excluded(self):
        result = equipment_markup({"indoor_camera": 1}, "frontpoint")
        assert len(result["items"]) == 0

    def test_totals(self, sample_equipment):
        result = equipment_markup(sample_equipment, "adt")
        assert result["provider_total"] > 0
        assert result["generic_total"] > 0
        assert result["overall_markup_pct"] > 0


class TestMarkupColor:
    def test_green_under_100(self):
        assert markup_color(50) == "green"

    def test_yellow_100_to_300(self):
        assert markup_color(150) == "yellow"
        assert markup_color(300) == "yellow"

    def test_red_over_300(self):
        assert markup_color(301) == "red"


class TestDiyTotal:
    def test_basic(self, sample_equipment):
        result = diy_total(sample_equipment)
        assert result["equipment"] == pytest.approx(148.0)
        assert result["monitoring_36mo"] == 0
        assert result["grand_total"] == pytest.approx(148.0)
