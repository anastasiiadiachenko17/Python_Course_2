"""Tests for the Module 10 file, text, language and country tasks."""

import json
import os

import pytest

from task_10_1 import work_with_file
from task_10_2 import count_lines_and_words
from task_10_3 import DEFAULT_COUNT, count_languages, most_spoken_languages
from task_10_4 import most_populated_countries, rank_by_population

SPEECH_PATH = os.path.join(os.path.dirname(__file__), "steve_job_speech.txt")
COUNTRIES_PATH = os.path.join(
    os.path.dirname(__file__), "data", "countries_data.json"
)

COUNTRIES = [
    {"name": "Afghanistan", "languages": ["Pashto", "Uzbek"]},
    {"name": "Canada", "languages": ["English", "French"]},
    {"name": "Nigeria", "languages": ["English"]},
    {"name": "Belgium", "languages": ["Dutch", "French", "German"]},
]

POPULATED = [
    {"name": "Brazil", "population": 206135893},
    {"name": "China", "population": 1377422166},
    {"name": "Bouvet Island", "population": 0},
    {"name": "India", "population": 1295210000},
    {"name": "Heard Island", "population": 0},
]


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
    with pytest.raises(TypeError, match="Expected a string"):
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


def test_appended_content_keeps_the_previous_one(tmp_path, capsys):
    """Appending adds to the file instead of replacing it."""
    file_path = str(tmp_path / "notes.txt")
    work_with_file("write", file_path, "first\n")
    work_with_file("append", file_path, "second\n")
    capsys.readouterr()

    with open(file_path, encoding="utf-8") as written_file:
        assert written_file.read() == "first\nsecond\n"


def test_writing_replaces_the_previous_content(tmp_path, capsys):
    """Writing twice leaves only the content of the second call."""
    file_path = str(tmp_path / "notes.txt")
    work_with_file("write", file_path, "first\n")
    work_with_file("write", file_path, "second\n")
    capsys.readouterr()

    with open(file_path, encoding="utf-8") as written_file:
        assert written_file.read() == "second\n"


def test_appending_creates_a_missing_file(tmp_path, capsys):
    """Appending to a file that does not exist creates it."""
    file_path = str(tmp_path / "new.txt")
    work_with_file("append", file_path, "only\n")
    capsys.readouterr()

    with open(file_path, encoding="utf-8") as written_file:
        assert written_file.read() == "only\n"


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


def write_countries(tmp_path, countries):
    """Write the countries as a JSON file and return its path.

    Args:
        tmp_path: Directory to write the file into.
        countries: Value to store as the JSON content.

    Returns:
        The path of the written file as a string.
    """
    countries_path = tmp_path / "countries_data.json"
    countries_path.write_text(json.dumps(countries), encoding="utf-8")

    return str(countries_path)


def test_a_country_counts_once_for_each_language():
    """Every language of a country adds one to its count."""
    french_countries = [c for c in COUNTRIES if "French" in c["languages"]]

    assert count_languages(COUNTRIES)["French"] == len(french_countries)


def test_languages_are_ranked_by_the_number_of_countries(tmp_path):
    """The most spoken language comes first, with its count."""
    path = write_countries(tmp_path, COUNTRIES)

    assert most_spoken_languages(path, 1) == [(2, "English")]


def test_equal_counts_are_ordered_alphabetically(tmp_path):
    """Languages with the same count keep an alphabetical order."""
    path = write_countries(tmp_path, COUNTRIES)

    assert most_spoken_languages(path, 3) == [
        (2, "English"),
        (2, "French"),
        (1, "Dutch"),
    ]


def test_asking_for_more_languages_than_there_are(tmp_path):
    """A count above the number of languages returns them all."""
    path = write_countries(tmp_path, COUNTRIES)
    spoken = {lang for c in COUNTRIES for lang in c["languages"]}

    assert len(most_spoken_languages(path, 100)) == len(spoken)


def test_countries_without_languages_are_counted_as_none(tmp_path):
    """A country with an empty language list adds no language."""
    path = write_countries(tmp_path, [{"name": "Nowhere", "languages": []}])

    assert most_spoken_languages(path, 3) == []


@pytest.mark.parametrize("count", [0, -1, 2.5, "three", None, True])
def test_count_must_be_a_positive_whole_number(count):
    """A count that is not a positive whole number is rejected."""
    with pytest.raises(ValueError, match="positive whole number"):
        most_spoken_languages(COUNTRIES_PATH, count)


def test_country_without_languages_key_is_rejected():
    """A country that has no languages key raises KeyError."""
    with pytest.raises(KeyError, match="has no languages"):
        count_languages([{"name": "Nowhere"}])


def test_country_that_is_not_a_mapping_is_rejected():
    """A country that is not a mapping raises TypeError."""
    with pytest.raises(TypeError, match="Expected a country mapping"):
        count_languages(["Nowhere"])


def test_languages_that_are_not_a_list_are_rejected():
    """Languages given as a plain string raise TypeError."""
    with pytest.raises(TypeError, match="must be a list"):
        count_languages([{"name": "Nowhere", "languages": "English"}])


def test_missing_countries_file_is_reported(tmp_path, capsys):
    """A countries file that does not exist is reported, not raised."""
    assert most_spoken_languages(str(tmp_path / "nope.json"), 3) == []
    assert "no file" in capsys.readouterr().out


def test_broken_countries_file_is_reported(tmp_path, capsys):
    """A countries file that is not valid JSON is reported."""
    broken_path = tmp_path / "countries_data.json"
    broken_path.write_text("{ broken", encoding="utf-8")

    assert most_spoken_languages(str(broken_path), 3) == []
    assert "not valid JSON" in capsys.readouterr().out


def test_the_real_data_file_gives_the_expected_top_languages():
    """The countries file ranks English, French and Arabic first."""
    assert most_spoken_languages(COUNTRIES_PATH, 3) == [
        (90, "English"),
        (45, "French"),
        (25, "Arabic"),
    ]


def test_the_real_data_file_gives_ten_languages():
    """The task asks for ten languages and the file has enough."""
    ten_languages = 10

    assert len(most_spoken_languages(COUNTRIES_PATH)) == ten_languages
    assert ten_languages == DEFAULT_COUNT


def test_countries_are_ranked_by_population(tmp_path):
    """The most populated country comes first with its population."""
    path = write_countries(tmp_path, POPULATED)

    assert most_populated_countries(path, 1) == [
        {"country": "China", "population": 1377422166},
    ]


def test_equal_populations_are_ordered_alphabetically():
    """Countries with the same population keep an alphabetical order."""
    ranked = rank_by_population(POPULATED)

    assert [entry["country"] for entry in ranked[-2:]] == [
        "Bouvet Island",
        "Heard Island",
    ]


def test_every_country_is_ranked():
    """Ranking keeps all the countries it is given."""
    assert len(rank_by_population(POPULATED)) == len(POPULATED)


def test_asking_for_more_countries_than_there_are(tmp_path):
    """A count above the number of countries returns them all."""
    path = write_countries(tmp_path, POPULATED)

    assert len(most_populated_countries(path, 100)) == len(POPULATED)


def test_no_countries_gives_no_ranking():
    """An empty list of countries produces an empty ranking."""
    assert rank_by_population([]) == []


@pytest.mark.parametrize("count", [0, -1, 1.5, "ten", None, True])
def test_country_count_must_be_a_positive_whole_number(count):
    """A count that is not a positive whole number is rejected."""
    with pytest.raises(ValueError, match="positive whole number"):
        most_populated_countries(COUNTRIES_PATH, count)


@pytest.mark.parametrize("key", ["name", "population"])
def test_country_without_a_required_key_is_rejected(key):
    """A country missing a needed key raises KeyError."""
    country = {"name": "Nowhere", "population": 1}
    del country[key]

    with pytest.raises(KeyError, match=f"no {key!r} key"):
        rank_by_population([country])


@pytest.mark.parametrize("population", ["5", 5.5, True, None])
def test_population_that_is_not_whole_is_rejected(population):
    """A population that is not a whole number raises TypeError."""
    with pytest.raises(TypeError, match="Population must be whole"):
        rank_by_population([{"name": "Nowhere", "population": population}])


def test_country_that_is_not_a_mapping_is_rejected_when_ranking():
    """A country that is not a mapping raises TypeError."""
    with pytest.raises(TypeError, match="Expected a country mapping"):
        rank_by_population(["Nowhere"])


def test_missing_countries_file_is_reported_when_ranking(tmp_path, capsys):
    """A countries file that does not exist is reported, not raised."""
    assert most_populated_countries(str(tmp_path / "nope.json"), 3) == []
    assert "no file" in capsys.readouterr().out


def test_broken_countries_file_is_reported_when_ranking(tmp_path, capsys):
    """A countries file that is not valid JSON is reported."""
    broken_path = tmp_path / "countries_data.json"
    broken_path.write_text("{ broken", encoding="utf-8")

    assert most_populated_countries(str(broken_path), 3) == []
    assert "not valid JSON" in capsys.readouterr().out


def test_the_real_data_file_gives_the_expected_top_countries():
    """The countries file ranks China, India and the USA first."""
    assert most_populated_countries(COUNTRIES_PATH, 3) == [
        {"country": "China", "population": 1377422166},
        {"country": "India", "population": 1295210000},
        {"country": "United States of America", "population": 323947000},
    ]


def test_the_real_data_file_gives_ten_countries():
    """The task asks for ten countries and the file has enough."""
    ten_countries = 10

    assert len(most_populated_countries(COUNTRIES_PATH)) == ten_countries
