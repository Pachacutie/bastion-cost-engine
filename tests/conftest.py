"""Shared test fixtures for bastion-cost-engine."""

import pytest


@pytest.fixture
def sample_equipment():
    """Standard equipment profile for testing: 6 door/window, 2 motion, 1 hub."""
    return {
        "door_window_sensor": 6,
        "motion_sensor": 2,
        "hub_base": 1,
    }


@pytest.fixture
def full_equipment():
    """Larger equipment profile: 6 d/w, 2 motion, 1 glass break, 1 smoke, 2 indoor cam, 1 hub."""
    return {
        "door_window_sensor": 6,
        "motion_sensor": 2,
        "glass_break_sensor": 1,
        "smoke_sensor": 1,
        "indoor_camera": 2,
        "hub_base": 1,
    }
