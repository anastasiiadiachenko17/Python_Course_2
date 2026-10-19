"""Extract device values from the log file with regular expressions."""

import re

LOG_FILE = "device.log"

PATTERNS = {
    "Timestamp of the ERROR line": r"^(\S+ \S+) ERROR",
    "SSID": r'ssid="([^"]+)"',
    "RSSI": r"rssi=(-?\d+)",
    "IP without the subnet mask": r"ip=(\d{1,3}(?:\.\d{1,3}){3})",
    "All DNS servers": r"(?<=[:,] )(\d{1,3}(?:\.\d{1,3}){3})",
    "Width and height": r"res=(\d+)x(\d+)",
    "FPS": r"fps=(\d+\.\d+)",
    "Stream bitrate": r"(?<!target )br=(\d+)",
    "Frame drop percentage": r"\((\d+\.\d+)%\)",
    "HTTP error code": r"code=(\d+)",
    "Domain from the URL": r"https://([^/]+)",
    "Firmware version": r"fw=v(\d+\.\d+\.\d+)",
    "MAC address": r"((?:[0-9A-F]{2}:){5}[0-9A-F]{2})",
    "Uptime as days, hours, minutes": r"uptime=(\d+)d(\d+)h(\d+)m",
    "Reboot reason": r'reboot_reason="([^"]+)"',
}


def format_values(values):
    """Return the values found by one pattern as a readable string.

    Args:
        values: List of matches returned by re.findall.

    Returns:
        The value itself when the pattern matched once, its parts
        joined by commas when the pattern has several capture groups,
        and the whole list when the pattern matched more than once.
    """
    if len(values) != 1:
        return str(values)

    only_value = values[0]

    if isinstance(only_value, tuple):
        return ", ".join(only_value)

    return only_value


def report_log_values(file_path=LOG_FILE):
    """Print the value that every pattern finds in the log file.

    Args:
        file_path: Path to the log file to read.
    """
    try:
        with open(file_path, encoding="utf-8") as log_file:
            log = log_file.read()
    except FileNotFoundError:
        print(f"There is no file at {file_path!r}.")
        return

    for number, (title, pattern) in enumerate(PATTERNS.items(), start=1):
        values = re.findall(pattern, log, re.M)
        print(f"{number:>2}. {title}: {format_values(values)}")


if __name__ == "__main__":
    report_log_values()
