"""Turn nested country and capital pairs into a list of dictionaries."""

COUNTRIES = [
    [("Finland", "Helsinki")],
    [("Sweden", "Stockholm")],
    [("Norway", "Oslo")],
]


def to_dictionaries(countries):
    """Return each country and its capital as a dictionary in upper case.

    Args:
        countries: List of lists of (country, capital) tuples.

    Returns:
        A new list of {"country": ..., "city": ...} dictionaries in
        the order of the input.

    Raises:
        TypeError: If countries is not a list.
    """
    if not isinstance(countries, list):
        raise TypeError(f"Expected a list of countries, not {countries!r}.")

    return [
        {"country": country.upper(), "city": capital.upper()}
        for group in countries
        for country, capital in group
    ]


if __name__ == "__main__":
    print(f"Dictionaries: {to_dictionaries(COUNTRIES)}")

    try:
        to_dictionaries(None)
    except TypeError as error:
        print(f"Cannot convert: {error}")
