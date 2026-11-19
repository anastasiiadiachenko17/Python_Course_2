"""Tests for to_upper_case with temporary input and output files."""

import random

import pytest

from data_processing import to_upper_case

TEXT = "Hello, World!\nline 2: abc 123"
FAIL_CHANCE = 0.5


def test_to_upper_case_writes_upper_case_text(input_file, output_file):
    """The output file holds the input text in upper case.

    The test is made flaky on purpose: it fails at random half of the
    time, to show how --reruns runs it again.
    """
    input_file.write(TEXT)
    input_file.seek(0)

    to_upper_case(input_file, output_file)

    output_file.seek(0)
    assert output_file.read() == "HELLO, WORLD!\nLINE 2: ABC 123"
    assert random.random() >= FAIL_CHANCE, "Random failure (flaky test)"


def test_to_upper_case_keeps_input_unchanged(input_file, output_file):
    """The input file still holds the original text after processing."""
    input_file.write(TEXT)
    input_file.seek(0)

    to_upper_case(input_file, output_file)

    input_file.seek(0)
    assert input_file.read() == TEXT


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("hello", "HELLO"),
        ("Hello World", "HELLO WORLD"),
        ("ALREADY UPPER", "ALREADY UPPER"),
        ("abc 123, !?", "ABC 123, !?"),
        ("one\ntwo", "ONE\nTWO"),
        pytest.param(
            "привіт",
            "ПРИВІТ",
            marks=pytest.mark.skip(
                reason="Cyrillic needs UTF-8 files, not every system "
                "uses it by default"
            ),
        ),
        ("", ""),
    ],
    ids=[
        "lower",
        "mixed",
        "upper",
        "digits and signs",
        "two lines",
        "cyrillic",
        "empty",
    ],
)
def test_to_upper_case_scenarios(input_file, output_file, text, expected):
    """Different texts come out in upper case, other symbols stay."""
    input_file.write(text)
    input_file.seek(0)

    to_upper_case(input_file, output_file)

    output_file.seek(0)
    assert output_file.read() == expected


@pytest.mark.xfail(
    reason="Known issue: to_upper_case reads from the current position "
    "and does not rewind the input file to the start"
)
def test_to_upper_case_reads_from_start(input_file, output_file):
    """The whole text is processed even if the file was not rewound."""
    input_file.write(TEXT)

    to_upper_case(input_file, output_file)

    output_file.seek(0)
    assert output_file.read() == "HELLO, WORLD!\nLINE 2: ABC 123"
