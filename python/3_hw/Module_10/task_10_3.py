"""Find the most spoken languages in the countries data file."""

import json
import os
from collections import Counter

COUNTRIES_FILE = os.path.join(
    os.path.dirname(__file__), "data", "countries_data.json"
)
DEFAULT_COUNT = 10


def count_languages(countries):
    """Return how many countries speak each language.

    Args:
        countries: List of countries, each a mapping with a
            "languages" key holding a list of language names.

    Returns:
        A Counter of a language name to the number of countries
        that speak it.

    Raises:
        TypeError: If a country is not a mapping or its languages
            are not a list.
        KeyError: If a country has no languages key.
    """
    counted = Counter()

    for country in countries:
        if not isinstance(country, dict):
            raise TypeError(f"Expected a country mapping, not {country!r}.")

        if "languages" not in country:
            name = country.get("name")
            raise KeyError(f"Country {name!r} has no languages.")

        languages = country["languages"]

        if not isinstance(languages, list):
            raise TypeError(f"Languages must be a list, not {languages!r}.")

        counted.update(languages)

    return counted


def most_spoken_languages(filename=COUNTRIES_FILE, count=DEFAULT_COUNT):
    """Return the most spoken languages of the countries in a file.

    Languages spoken by the same number of countries are ordered
    alphabetically, so the result does not depend on the order of
    the countries in the file.

    Args:
        filename: Path to the JSON file with the countries. Relative
            paths are resolved against the current directory, so the
            default points next to this file instead.
        count: How many languages to return.

    Returns:
        A list of tuples with the number of countries and the
        language, from the most to the least spoken. The list is
        empty when the file cannot be read.

    Raises:
        ValueError: If count is not a positive whole number.
    """
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise ValueError(
            f"Count must be a positive whole number, not {count!r}."
        )

    try:
        with open(filename, encoding="utf-8") as countries_file:
            countries = json.load(countries_file)
    except FileNotFoundError:
        print(f"There is no file at {filename!r}.")
        return []
    except json.JSONDecodeError as error:
        print(f"{filename!r} is not valid JSON: {error}")
        return []

    counted = count_languages(countries)
    ranked = sorted(counted.items(), key=lambda item: (-item[1], item[0]))

    return [(spoken, language) for language, spoken in ranked[:count]]


if __name__ == "__main__":
    for spoken, language in most_spoken_languages():
        print(f"{spoken:3} {language}")
