"""Tests for cross-provider comparison engine."""

import pytest

from bastion_cost.engine.comparison import compare_all


class TestCompareAll:
    def test_returns_all_providers_plus_diy(self, sample_equipment):
        results = compare_all(sample_equipment)
        slugs = [r["provider"] for r in results]
        assert "diy" in slugs
        for p in ("frontpoint", "adt", "ring", "simplisafe", "vivint", "abode", "cove"):
            assert p in slugs

    def test_sorted_by_three_year_total(self, sample_equipment):
        results = compare_all(sample_equipment)
        totals = [r["three_year_total"] for r in results]
        assert totals == sorted(totals)

    def test_diy_is_cheapest(self, sample_equipment):
        results = compare_all(sample_equipment)
        assert results[0]["provider"] == "diy"

    def test_each_result_has_required_fields(self, sample_equipment):
        results = compare_all(sample_equipment)
        for r in results:
            assert "provider" in r
            assert "display_name" in r
            assert "equipment_cost" in r
            assert "monthly" in r
            assert "three_year_total" in r
            assert "contract" in r
            assert "etf_description" in r

    def test_none_devices_handled(self):
        equipment = {"smart_lock": 1}
        results = compare_all(equipment)
        assert len(results) == 8

    def test_provider_with_no_available_devices(self):
        equipment = {"indoor_camera": 2}
        results = compare_all(equipment)
        fp = next(r for r in results if r["provider"] == "frontpoint")
        assert fp["equipment_cost"] == 0

    def test_empty_equipment(self):
        results = compare_all({})
        assert len(results) == 8
        for r in results:
            assert r["equipment_cost"] == 0

    def test_contract_display(self, sample_equipment):
        results = compare_all(sample_equipment)
        ring = next(r for r in results if r["provider"] == "ring")
        assert ring["contract"] == "None"
        adt = next(r for r in results if r["provider"] == "adt")
        assert "36" in adt["contract"]
