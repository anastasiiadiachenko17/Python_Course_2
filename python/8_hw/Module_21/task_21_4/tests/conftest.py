"""Fixtures and command line options shared by all tests in this folder."""

import os
import tempfile

import pytest


def pytest_addoption(parser):
    """Add the --keep-temp-files option to the pytest command.

    Args:
        parser: The pytest parser for command line options.
    """
    parser.addoption(
        "--keep-temp-files",
        action="store_true",
        help="Do not delete the temporary files after each test.",
    )


@pytest.fixture
def input_data():
    """Give every test the same config with two sections.

    Returns:
        A dict with a "server" and a "database" section.
    """
    return {
        "server": {"host": "localhost", "port": 8080, "debug": False},
        "database": {"name": "students", "user": "admin", "timeout": 30},
    }


def create_temp_file(request):
    """Create a temporary file, give it to the test, then delete it.

    Args:
        request: The pytest request, used to read the command line option.

    Yields:
        The temporary file, open for writing and reading.
    """
    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".txt", delete=False
    ) as file:
        yield file
    if not request.config.getoption("--keep-temp-files"):
        os.remove(file.name)


@pytest.fixture
def input_file(request):
    """Temporary file the test writes the input text into.

    Yields:
        The temporary input file.
    """
    yield from create_temp_file(request)


@pytest.fixture
def output_file(request):
    """Temporary file the function under test writes the result into.

    Yields:
        The temporary output file.
    """
    yield from create_temp_file(request)
