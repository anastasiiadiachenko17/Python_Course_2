"""Tests for reversing strings and checking palindromes."""

import pytest

from string_operations import is_palindrome, reverse_string


@pytest.mark.parametrize(
    ("text", "expected"),
    [("abc", "cba"), ("a", "a"), ("", ""), ("ab cd", "dc ba")],
    ids=["word", "one letter", "empty", "with space"],
)
def test_reverse_string(text, expected):
    """The string is written backwards, spaces included."""
    assert reverse_string(text) == expected


@pytest.mark.P0
@pytest.mark.palindrome
@pytest.mark.parametrize(
    "text",
    ["level", "abba", "racecar", "a", "", "12321"],
    ids=["odd length", "even length", "long", "one letter", "empty", "digits"],
)
def test_palindromes_are_recognised(text):
    """Strings that read the same backwards are palindromes."""
    assert is_palindrome(text)


@pytest.mark.P0
@pytest.mark.palindrome
@pytest.mark.parametrize(
    "text",
    ["hello", "ab", "abca", "Anna", "nurses run"],
    ids=["word", "two letters", "almost", "capital", "space"],
)
def test_other_strings_are_not_palindromes(text):
    """Other strings, also with a capital letter or a space, are not."""
    assert not is_palindrome(text)
