"""Tests for the Module 10 file and text counting tasks."""

import os

import pytest

from task_10_1 import work_with_file
from task_10_2 import count_lines_and_words

SPEECH_PATH = os.path.join(os.path.dirname(__file__), "steve_job_speech.txt")


def test_empty_text_has_nothing_to_count():
    """An empty text has no lines and no words."""
    assert count_lines_and_words("") == (0, 0)


def test_trailing_newline_does_not_add_a_line():
    """A newline at the end of the text does not start a new line."""
    assert count_lines_and_words("first\nsecond\n") == (2, 2)


def test_blank_line_inside_the_text_is_still_a_line():
    """An empty line between two lines is counted as a line."""
    assert count_lines_and_words("first\n\nthird") == (3, 2)


def test_repeated_whitespace_does_not_create_words():
    """Extra spaces and tabs do not produce empty words."""
    assert count_lines_and_words("  two \t words  ") == (1, 2)


def test_text_without_words_still_has_a_line():
    """A line of spaces counts as one line and no words."""
    assert count_lines_and_words("   ") == (1, 0)


def test_count_rejects_text_that_is_not_a_string():
    """A value that is not a string raises TypeError."""
    with pytest.raises(TypeError):
        count_lines_and_words(None)


def test_speech_file_has_the_expected_counts():
    """The speech file contains 22 lines and 2039 words."""
    with open(SPEECH_PATH, encoding="utf-8") as speech_file:
        speech = speech_file.read()

    assert count_lines_and_words(speech) == (22, 2039)


def test_written_content_can_be_read_back(tmp_path, capsys):
    """Reading a file prints the content that was written to it."""
    file_path = str(tmp_path / "notes.txt")
    work_with_file("write", file_path, "hello\n")
    work_with_file("read", file_path)

    assert "hello" in capsys.readouterr().out


def test_missing_file_is_reported(tmp_path, capsys):
    """Reading a file that does not exist is reported, not raised."""
    work_with_file("read", str(tmp_path / "nope.txt"))

    assert "no file" in capsys.readouterr().out


def test_unknown_operation_is_reported(capsys):
    """An unsupported operation is reported to the user."""
    work_with_file("delete", "any.txt")

    assert "Unknown operation" in capsys.readouterr().out


def test_writing_without_content_is_reported(tmp_path, capsys):
    """Writing with no content is reported instead of crashing."""
    work_with_file("write", str(tmp_path / "empty.txt"))

    assert "needs text content" in capsys.readouterr().out


def test_file_path_must_be_text(capsys):
    """A file path that is not a string is reported to the user."""
    work_with_file("read", None)

    assert "must be text" in capsys.readouterr().out
