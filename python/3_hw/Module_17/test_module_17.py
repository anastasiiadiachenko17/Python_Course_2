"""Tests for the Module 17 sensor logging task."""

import logging
import re

import pytest

import task_17_1
from task_17_1 import (
    MAX_TEMPERATURE_C,
    MIN_TEMPERATURE_C,
    log_reading,
    monitor_sensor,
)


@pytest.fixture
def log_file(tmp_path, monkeypatch):
    """Set up logging into a temporary file and undo it afterwards.

    Args:
        tmp_path: Directory to keep the log file in.
        monkeypatch: Fixture used to point the task at that file.

    Yields:
        The path of the log file that the handlers write to.
    """
    path = tmp_path / "sensor.log"
    monkeypatch.setattr(task_17_1, "LOG_FILE", str(path))
    kept_handlers = task_17_1.logger.handlers[:]
    kept_level = task_17_1.logger.level

    task_17_1.setup_logging()

    yield path

    for handler in task_17_1.logger.handlers:
        handler.close()

    task_17_1.logger.handlers = kept_handlers
    task_17_1.logger.setLevel(kept_level)


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


def test_exactly_the_high_threshold_is_not_a_warning(caplog):
    """A temperature of exactly 35 is not high enough to warn."""
    with caplog.at_level(logging.DEBUG):
        log_reading(35)

    assert [record.levelname for record in caplog.records] == ["DEBUG"]


def test_one_degree_above_the_threshold_is_a_warning(caplog):
    """A temperature of 36 is the lowest one that is high."""
    with caplog.at_level(logging.DEBUG):
        log_reading(36)

    assert "WARNING" in [record.levelname for record in caplog.records]


def test_one_degree_above_the_critical_threshold_is_critical(caplog):
    """A temperature of 46 is the lowest one that is critical."""
    with caplog.at_level(logging.DEBUG):
        log_reading(46)

    assert "CRITICAL" in [record.levelname for record in caplog.records]


def test_one_degree_below_zero_is_an_error(caplog):
    """A temperature of minus one is the highest freezing one."""
    with caplog.at_level(logging.DEBUG):
        log_reading(-1)

    assert "ERROR" in [record.levelname for record in caplog.records]


def test_only_warnings_and_above_reach_the_log_file(log_file):
    """The log file keeps warnings and above, never debug or info."""
    log_reading(20)
    log_reading(38)
    log_reading(48)

    written = log_file.read_text(encoding="utf-8")

    assert "High temperature: 38" in written
    assert "Critical temperature: 48" in written
    assert "DEBUG" not in written
    assert "INFO" not in written


def test_log_file_lines_show_the_time_and_the_level(log_file):
    """Every line of the log file starts with the time and the level."""
    log_reading(48)

    line = log_file.read_text(encoding="utf-8").splitlines()[0]
    expected = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \| CRITICAL \| .+"

    assert re.fullmatch(expected, line)


def test_keyboard_interrupt_is_logged_with_its_traceback(caplog, monkeypatch):
    """Ctrl+C is logged as an error that carries the traceback."""

    def interrupt(seconds):
        raise KeyboardInterrupt

    monkeypatch.setattr(task_17_1.time, "sleep", interrupt)

    with caplog.at_level(logging.DEBUG):
        monitor_sensor(duration_seconds=10)

    stopped = [
        record
        for record in caplog.records
        if "Stopped by the user" in record.getMessage()
    ]

    assert stopped
    assert stopped[0].levelname == "ERROR"
    assert stopped[0].exc_info is not None


def test_a_summary_is_still_logged_after_an_interrupt(caplog, monkeypatch):
    """A run stopped by Ctrl+C still reports what it managed to read."""

    def interrupt(seconds):
        raise KeyboardInterrupt

    monkeypatch.setattr(task_17_1.time, "sleep", interrupt)

    with caplog.at_level(logging.INFO):
        monitor_sensor(duration_seconds=10)

    assert "Sensor stopped." in caplog.text
    assert "Summary: count=" in caplog.text
