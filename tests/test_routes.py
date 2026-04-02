"""Integration tests for Flask routes."""

import pytest

from bastion_cost.web import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestIndex:
    def test_landing_page_loads(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"home security" in resp.data.lower()

    def test_landing_has_provider_options(self, client):
        resp = client.get("/")
        assert b"frontpoint" in resp.data.lower()
        assert b"ring" in resp.data.lower()


class TestBuilder:
    def test_builder_with_valid_params(self, client):
        resp = client.get("/builder?provider=adt&tier=2&contract=36")
        assert resp.status_code == 200

    def test_builder_missing_provider_redirects(self, client):
        resp = client.get("/builder")
        assert resp.status_code == 302

    def test_builder_invalid_provider_redirects(self, client):
        resp = client.get("/builder?provider=fake&tier=0&contract=0")
        assert resp.status_code == 302

    def test_builder_invalid_tier_redirects(self, client):
        resp = client.get("/builder?provider=adt&tier=99&contract=36")
        assert resp.status_code == 302


class TestResults:
    def test_results_with_valid_params(self, client):
        resp = client.get("/results?provider=adt&tier=2&contract=36&door_window_sensor=6&motion_sensor=2&hub_base=1")
        assert resp.status_code == 200

    def test_results_missing_provider_redirects(self, client):
        resp = client.get("/results")
        assert resp.status_code == 302

    def test_results_shows_true_monthly(self, client):
        resp = client.get("/results?provider=vivint&tier=0&contract=42&door_window_sensor=4")
        assert resp.status_code == 200
        assert b"true monthly" in resp.data.lower() or b"True Monthly" in resp.data

    def test_results_with_zero_equipment(self, client):
        resp = client.get("/results?provider=ring&tier=2&contract=0")
        assert resp.status_code == 200


class TestAbout:
    def test_about_page_loads(self, client):
        resp = client.get("/about")
        assert resp.status_code == 200
        assert b"april 2026" in resp.data.lower()

    def test_about_has_report_link(self, client):
        resp = client.get("/about")
        assert b"issues/new" in resp.data
