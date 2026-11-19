"""Tests for to_upper_case with temporary input and output files."""

import os
import tempfile

import pytest

from data_processing import to_upper_case

TEXT = "Hello, World!\nline 2: abc 123"


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


def test_to_upper_case_writes_upper_case_text(input_file, output_file):
    """The output file holds the input text in upper case."""
    input_file.write(TEXT)
    input_file.seek(0)

    to_upper_case(input_file, output_file)

    output_file.seek(0)
    assert output_file.read() == "HELLO, WORLD!\nLINE 2: ABC 123"


def test_to_upper_case_keeps_input_unchanged(input_file, output_file):
    """The input file still holds the original text after processing."""
    input_file.write(TEXT)
    input_file.seek(0)

    to_upper_case(input_file, output_file)

    input_file.seek(0)
    assert input_file.read() == TEXT
