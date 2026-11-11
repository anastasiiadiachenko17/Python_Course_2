"""Show the iterator, the generator and the decorators of Module 15."""

import os

from batches import Batches
from decorators import bold, count_calls, italic, repeat
from log_filter import filter_log

LOG_FILE = os.path.join(os.path.dirname(__file__), "device_module15.log")
MISSING_LOG_FILE = "missing.log"
BATCH_SIZE = 3


@count_calls
def ping(host):
    """Ping a host."""
    return f"pong from {host}"


@repeat(times=3)
def greet_three_times(name):
    """Greet someone."""
    return f"Hello, {name}!"


@bold
@italic
def greet_bold_italic(name):
    """Greet someone in bold italic."""
    return f"Hello, {name}!"


@italic
@bold
def greet_italic_bold(name):
    """Greet someone in italic bold."""
    return f"Hello, {name}!"


def plain_greet(name):
    """Greet someone without any tags."""
    return f"Hello, {name}!"


def print_errors(filename):
    """Print the ERROR records of a log file.

    Args:
        filename: Path to the log file.
    """
    try:
        with open(filename, encoding="utf-8") as log_file:
            records = list(filter_log(log_file, "ERROR"))
    except FileNotFoundError as error:
        print(f"Cannot read the log: {error}")
        return

    for timestamp, message in records:
        print(f"{timestamp} {message}")


def main():
    """Run every task of the homework and print the results."""
    print(f"--- Task 1: Batches(range(1, 8), {BATCH_SIZE}) ---")
    for batch in Batches(range(1, 8), BATCH_SIZE):
        print(batch)
    try:
        Batches([1, 2, 3], 0)
    except ValueError as error:
        print(f"Invalid size: {error}")

    print("\n--- Task 2: ERROR records of device_module15.log ---")
    print_errors(LOG_FILE)
    print_errors(MISSING_LOG_FILE)

    print("\n--- Task 3: count_calls ---")
    print(f"ping.calls before: {ping.calls}")
    print(ping("cam-01"))
    print(ping(host="cam-02"))
    print(f"ping.calls after: {ping.calls}")
    print(f"name and docstring: {ping.__name__!r}, {ping.__doc__!r}")

    print("\n--- Task 4: repeat(times=3) ---")
    print(greet_three_times("Ann"))
    print(f"name: {greet_three_times.__name__!r}")

    print("\n--- Task 5: bold and italic ---")
    print(f"@bold @italic: {greet_bold_italic('Ann')}")
    print(f"@italic @bold: {greet_italic_bold('Ann')}")
    print(f"without @:     {bold(italic(plain_greet))('Ann')}")
    print(f"name without wraps: {greet_bold_italic.__name__!r}")


if __name__ == "__main__":
    main()
