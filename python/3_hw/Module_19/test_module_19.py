"""Tests for the Module 19 log parsing and file combining tasks."""

import json
import os
import re

import pytest
import yaml

from task_19_1 import PATTERNS, format_values, report_log_values
from task_19_2 import combine_devices, combine_files

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


DEVICES = {
    "knight-lamar": {"device_type": "cocoa", "lab_env": "lab11-env-1"},
    "jaws-sand": {"device_type": "jaws", "lab_env": "lab11-env-39"},
}

LAB_ENVS = {"lab11-env-1": {"wifi": "lab11-wifi-2", "chamber": 30}}


def write_inputs(tmp_path, devices, lab_envs):
    """Write both input files and return their paths.

    Args:
        tmp_path: Directory to write the files into.
        devices: Mapping to store as the YAML device file.
        lab_envs: Mapping to store as the JSON environment file.

    Returns:
        A tuple with the path of the YAML and of the JSON file.
    """
    devices_path = tmp_path / "devices.yaml"
    lab_envs_path = tmp_path / "lab_envs.json"
    devices_path.write_text(yaml.safe_dump(devices), encoding="utf-8")
    lab_envs_path.write_text(json.dumps(lab_envs), encoding="utf-8")

    return devices_path, lab_envs_path


def test_known_environment_is_filled_in():
    """A device gets the description of the environment it uses."""
    combined = combine_devices(DEVICES, LAB_ENVS)

    assert combined["knight-lamar"]["lab_env"] == LAB_ENVS["lab11-env-1"]


def test_unknown_environment_becomes_none():
    """A device with an undescribed environment gets None."""
    combined = combine_devices(DEVICES, LAB_ENVS)

    assert combined["jaws-sand"]["lab_env"] is None


def test_other_attributes_are_kept():
    """Attributes other than lab_env survive the combination."""
    combined = combine_devices(DEVICES, LAB_ENVS)

    assert combined["jaws-sand"]["device_type"] == "jaws"


def test_input_devices_are_not_changed():
    """The device mapping given to the function stays untouched."""
    combine_devices(DEVICES, LAB_ENVS)

    assert DEVICES["knight-lamar"]["lab_env"] == "lab11-env-1"


def test_device_without_attributes_is_rejected():
    """A device without a mapping of attributes raises TypeError."""
    with pytest.raises(TypeError, match="has no attributes"):
        combine_devices({"knight-lamar": None}, LAB_ENVS)


def test_device_without_lab_env_is_rejected():
    """A device without a lab_env attribute raises KeyError."""
    with pytest.raises(KeyError, match="has no lab_env attribute"):
        combine_devices({"knight-lamar": {"device_type": "x"}}, LAB_ENVS)


def test_no_devices_gives_no_result():
    """An empty device mapping produces an empty result."""
    assert combine_devices({}, LAB_ENVS) == {}


def test_combined_file_can_be_read_back(tmp_path, capsys):
    """The written YAML file parses back into the combined mapping."""
    devices_path, lab_envs_path = write_inputs(tmp_path, DEVICES, LAB_ENVS)
    combined_path = tmp_path / "combined.yaml"

    combine_files(str(devices_path), str(lab_envs_path), str(combined_path))
    capsys.readouterr()

    written = yaml.safe_load(combined_path.read_text(encoding="utf-8"))

    assert written == combine_devices(DEVICES, LAB_ENVS)


def test_missing_input_file_is_reported(tmp_path, capsys):
    """An input file that does not exist is reported, not raised."""
    _, lab_envs_path = write_inputs(tmp_path, DEVICES, LAB_ENVS)

    combine_files(
        str(tmp_path / "nope.yaml"),
        str(lab_envs_path),
        str(tmp_path / "combined.yaml"),
    )

    assert "missing" in capsys.readouterr().out


def test_broken_json_is_reported(tmp_path, capsys):
    """An unparsable environment file is reported, not raised."""
    devices_path, lab_envs_path = write_inputs(tmp_path, DEVICES, LAB_ENVS)
    lab_envs_path.write_text("{ broken", encoding="utf-8")

    combine_files(
        str(devices_path),
        str(lab_envs_path),
        str(tmp_path / "combined.yaml"),
    )

    assert "cannot be parsed" in capsys.readouterr().out


def test_empty_devices_file_gives_empty_result(tmp_path, capsys):
    """An empty device file produces an empty YAML mapping."""
    devices_path, lab_envs_path = write_inputs(tmp_path, DEVICES, LAB_ENVS)
    devices_path.write_text("", encoding="utf-8")
    combined_path = tmp_path / "combined.yaml"

    combine_files(str(devices_path), str(lab_envs_path), str(combined_path))
    capsys.readouterr()

    assert yaml.safe_load(combined_path.read_text(encoding="utf-8")) == {}
