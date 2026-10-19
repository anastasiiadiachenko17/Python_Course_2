"""Tests for the Module 17 sensor logging task."""

import logging

from task_17_1 import (
    MAX_TEMPERATURE_C,
    MIN_TEMPERATURE_C,
    log_reading,
    monitor_sensor,
)


def test_normal_temperature_is_only_logged_as_debug(caplog):
    """A temperature inside the safe range produces a single record."""
    with caplog.at_level(logging.DEBUG):
        log_reading(20)

    assert [record.levelname for record in caplog.records] == ["DEBUG"]


def test_high_temperature_is_a_warning(caplog):
    """A temperature above 35 is logged as a warning."""
    with caplog.at_level(logging.DEBUG):
        log_reading(38)

    assert "WARNING" in [record.levelname for record in caplog.records]


def test_freezing_temperature_is_an_error(caplog):
    """A temperature below zero is logged as an error."""
    with caplog.at_level(logging.DEBUG):
        log_reading(-5)

    assert "ERROR" in [record.levelname for record in caplog.records]


def test_critical_temperature_wins_over_warning(caplog):
    """A temperature above 45 is critical even though it is also high."""
    with caplog.at_level(logging.DEBUG):
        log_reading(48)

    levels = [record.levelname for record in caplog.records]
    assert "CRITICAL" in levels
    assert "WARNING" not in levels


def test_upper_boundary_is_still_a_warning(caplog):
    """A temperature of exactly 45 is high but not critical."""
    with caplog.at_level(logging.DEBUG):
        log_reading(45)

    assert "WARNING" in [record.levelname for record in caplog.records]


def test_zero_is_not_an_error(caplog):
    """A temperature of exactly zero is not below freezing."""
    with caplog.at_level(logging.DEBUG):
        log_reading(0)

    assert [record.levelname for record in caplog.records] == ["DEBUG"]


def test_run_without_time_reads_nothing(caplog):
    """A run with no time left reports that nothing was read."""
    with caplog.at_level(logging.INFO):
        temperatures = monitor_sensor(duration_seconds=0)

    assert temperatures == []
    assert "no temperatures were read" in caplog.text


def test_short_run_logs_a_summary(caplog):
    """A short run reads at least one value and logs a summary."""
    with caplog.at_level(logging.INFO):
        temperatures = monitor_sensor(duration_seconds=1)

    assert temperatures
    assert "Summary: count=" in caplog.text


def test_readings_stay_inside_the_sensor_range():
    """Every reading is within the range the sensor can produce."""
    temperatures = monitor_sensor(duration_seconds=1)

    assert all(
        MIN_TEMPERATURE_C <= value <= MAX_TEMPERATURE_C
        for value in temperatures
    )
