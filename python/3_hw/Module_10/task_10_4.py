"""Find the most populated countries in the countries data file."""

import json
import os

COUNTRIES_FILE = os.path.join(
    os.path.dirname(__file__), "data", "countries_data.json"
)
DEFAULT_COUNT = 10


def rank_by_population(countries):
    """Return the countries ordered from the most to the least populated.

    Countries with the same population are ordered alphabetically, so
    the result does not depend on their order in the file.

    Args:
        countries: List of countries, each a mapping with a "name" and
            a "population" key.

    Returns:
        A list of mappings with the country name and its population.

    Raises:
        TypeError: If a country is not a mapping or its population is
            not a whole number.
        KeyError: If a country has no name or no population key.
    """
    ranked = []

    for country in countries:
        if not isinstance(country, dict):
            raise TypeError(f"Expected a country mapping, not {country!r}.")

        for key in ("name", "population"):
            if key not in country:
                raise KeyError(f"A country has no {key!r} key.")

        population = country["population"]

        if not isinstance(population, int) or isinstance(population, bool):
            raise TypeError(f"Population must be whole, not {population!r}.")

        ranked.append({"country": country["name"], "population": population})

    ranked.sort(key=lambda entry: (-entry["population"], entry["country"]))

    return ranked


def most_populated_countries(filename=COUNTRIES_FILE, count=DEFAULT_COUNT):
    """Return the most populated countries of the ones in a file.

    Args:
        filename: Path to the JSON file with the countries. Relative
            paths are resolved against the current directory, so the
            default points next to this file instead.
        count: How many countries to return.

    Returns:
        A list of mappings with the country name and its population,
        from the most to the least populated. The list is empty when
        the file cannot be read.

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

    return rank_by_population(countries)[:count]


if __name__ == "__main__":
    for entry in most_populated_countries():
        print(f"{entry['population']:>13,} {entry['country']}")
