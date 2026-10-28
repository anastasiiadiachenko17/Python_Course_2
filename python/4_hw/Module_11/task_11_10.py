"""Flatten nested country and capital pairs with a list comprehension."""

COUNTRIES = [
    [("Finland", "Helsinki")],
    [("Sweden", "Stockholm")],
    [("Norway", "Oslo")],
]
CODE_LENGTH = 3


def flatten_countries(countries):
    """Return each country, its code and its capital in upper case.

    The code is the first letters of the country name.

    Args:
        countries: List of lists of (country, capital) tuples.

    Returns:
        A new list of [COUNTRY, CODE, CAPITAL] lists in the order of
        the input.

    Raises:
        TypeError: If countries is not a list.
    """
    if not isinstance(countries, list):
        raise TypeError(f"Expected a list of countries, not {countries!r}.")

    return [
        [country.upper(), country[:CODE_LENGTH].upper(), capital.upper()]
        for group in countries
        for country, capital in group
    ]


if __name__ == "__main__":
    print(f"Flattened: {flatten_countries(COUNTRIES)}")

    try:
        flatten_countries(None)
    except TypeError as error:
        print(f"Cannot flatten: {error}")
