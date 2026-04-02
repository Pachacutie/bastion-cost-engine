"""Tests for ETF calculation engine."""

import pytest

from bastion_cost.engine.etf import etf_at_month, etf_timeline, optimal_exit_month


class TestEtfAtMonth:
    def test_frontpoint_80pct_month_6(self):
        result = etf_at_month("frontpoint", 0, 36, 6)
        assert result == pytest.approx(30 * 34.99 * 0.80)

    def test_frontpoint_80pct_month_18(self):
        result = etf_at_month("frontpoint", 0, 36, 18)
        assert result == pytest.approx(18 * 34.99 * 0.80)

    def test_frontpoint_80pct_month_36(self):
        result = etf_at_month("frontpoint", 0, 36, 36)
        assert result == pytest.approx(0.0)

    def test_adt_75pct_month_12(self):
        result = etf_at_month("adt", 2, 36, 12)
        assert result == pytest.approx(24 * 39.99 * 0.75)

    def test_vivint_year1_penalty(self):
        result = etf_at_month("vivint", 0, 60, 6, equipment_total=2000)
        expected_balance = 2000 * (60 - 6) / 60
        assert result == pytest.approx(expected_balance + 300)

    def test_vivint_year2_penalty(self):
        result = etf_at_month("vivint", 0, 60, 18, equipment_total=2000)
        expected_balance = 2000 * (60 - 18) / 60
        assert result == pytest.approx(expected_balance + 150)

    def test_cove_financed(self):
        result = etf_at_month("cove", 0, 36, 12, equipment_total=500)
        assert result == pytest.approx(500)

    def test_cove_paid_upfront(self):
        result = etf_at_month("cove", 0, 0, 12, equipment_total=0)
        assert result == pytest.approx(0)

    def test_ring_no_etf(self):
        result = etf_at_month("ring", 2, 0, 6)
        assert result == 0

    def test_simplisafe_no_etf(self):
        result = etf_at_month("simplisafe", 2, 0, 12)
        assert result == 0

    def test_abode_no_etf(self):
        result = etf_at_month("abode", 2, 0, 6)
        assert result == 0


class TestEtfTimeline:
    def test_frontpoint_36mo_intervals(self):
        timeline = etf_timeline("frontpoint", 0, 36)
        months = [t[0] for t in timeline]
        assert 6 in months
        assert 36 in months
        amounts = [t[1] for t in timeline]
        assert amounts == sorted(amounts, reverse=True)

    def test_no_contract_empty_timeline(self):
        timeline = etf_timeline("ring", 2, 0)
        assert len(timeline) == 0 or all(t[1] == 0 for t in timeline)


class TestOptimalExitMonth:
    def test_no_contract_returns_none(self):
        assert optimal_exit_month("ring", 2, 0) is None

    def test_contract_provider_returns_month(self):
        result = optimal_exit_month("frontpoint", 0, 36)
        if result is not None:
            assert isinstance(result, int)
            assert 1 <= result <= 36
