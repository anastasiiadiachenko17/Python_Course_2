"""Tests for to_upper_case with temporary input and output files."""

from data_processing import to_upper_case

TEXT = "Hello, World!\nline 2: abc 123"


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
