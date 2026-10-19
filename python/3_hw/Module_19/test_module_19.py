"""Tests for the Module 19 log parsing task."""

import os
import re

import pytest

from task_19_1 import PATTERNS, format_values, report_log_values

LOG_PATH = os.path.join(os.path.dirname(__file__), "device.log")

EXPECTED = {
    "Timestamp of the ERROR line": "2026-05-02 10:15:07.800",
    "SSID": "Lab Guest 5G",
    "RSSI": "-67",
    "IP without the subnet mask": "10.20.30.41",
    "All DNS servers": "['8.8.8.8', '1.1.1.1']",
    "Width and height": "1280, 720",
    "FPS": "29.97",
    "Stream bitrate": "2500",
    "Frame drop percentage": "4.0",
    "HTTP error code": "503",
    "Domain from the URL": "api.example.com",
    "Firmware version": "2.14.0",
    "MAC address": "A4:5E:60:1B:2C:3D",
    "Uptime as days, hours, minutes": "3, 04, 12",
    "Reboot reason": "WATCHDOG",
}


def read_log():
    """Return the text of the device log that ships with the task."""
    with open(LOG_PATH, encoding="utf-8") as log_file:
        return log_file.read()


def find(title, log):
    """Return the formatted value that the named pattern finds.

    Args:
        title: Name of the pattern in PATTERNS.
        log: Text to search in.

    Returns:
        The formatted value as report_log_values would print it.
    """
    return format_values(re.findall(PATTERNS[title], log, re.M))


@pytest.mark.parametrize("title", list(PATTERNS))
def test_pattern_finds_the_expected_value(title):
    """Each pattern extracts exactly the value the task asks for."""
    assert find(title, read_log()) == EXPECTED[title]


def test_every_item_of_the_task_is_covered():
    """There is a pattern and an expectation for every log item."""
    assert sorted(PATTERNS) == sorted(EXPECTED)


def test_target_bitrate_is_not_reported():
    """The target bitrate is ignored in favour of the stream one."""
    log = "fps=29.97 br=2500kbps\ntarget br=3000kbps (max)\n"

    assert find("Stream bitrate", log) == "2500"


def test_device_address_is_not_reported_as_dns():
    """The address of the device is not counted as a DNS server."""
    log = "ip=10.20.30.41/24\ndns servers: 8.8.8.8, 1.1.1.1\n"

    assert find("All DNS servers", log) == "['8.8.8.8', '1.1.1.1']"


def test_timestamp_is_not_taken_from_a_mac_address():
    """A clock time is not mistaken for part of a MAC address."""
    log = "10:15:09.002 INFO mac=A4:5E:60:1B:2C:3D\n"

    assert find("MAC address", log) == "A4:5E:60:1B:2C:3D"


def test_firmware_version_drops_the_prefix_and_suffix():
    """The version number is reported without the v and the suffix."""
    log = "fw=v10.0.1-beta7\n"

    assert find("Firmware version", log) == "10.0.1"


def test_ip_is_reported_without_the_mask():
    """The subnet mask is not part of the reported address."""
    log = "ip=192.168.0.1/16\n"

    assert find("IP without the subnet mask", log) == "192.168.0.1"


def test_only_the_error_line_gives_a_timestamp():
    """Lines of other levels do not provide the error timestamp."""
    expected = "2027-01-01 00:00:02.000"
    log = f"2026-05-02 10:15:01.234 INFO ok\n{expected} ERROR x\n"

    assert find("Timestamp of the ERROR line", log) == expected


def test_missing_log_file_is_reported(tmp_path, capsys):
    """A log file that does not exist is reported, not raised."""
    report_log_values(str(tmp_path / "nope.log"))

    assert "no file" in capsys.readouterr().out


def test_empty_log_finds_nothing(tmp_path, capsys):
    """An empty log produces no values but does not crash."""
    empty_log = tmp_path / "empty.log"
    empty_log.write_text("", encoding="utf-8")

    report_log_values(str(empty_log))

    assert "[]" in capsys.readouterr().out


def test_several_groups_are_joined_by_commas():
    """A pattern with several groups is shown as comma separated."""
    assert format_values([("1280", "720")]) == "1280, 720"
