"""Join nested first and last name pairs into full names."""

NAMES = [
    [("Asabeneh", "Yetayeh")],
    [("David", "Smith")],
    [("Donald", "Trump")],
    [("Bill", "Gates")],
]


def full_names(names):
    """Return each first and last name joined with a space.

    Args:
        names: List of lists of (first name, last name) tuples.

    Returns:
        A new list of full names in the order of the input.

    Raises:
        TypeError: If names is not a list.
    """
    if not isinstance(names, list):
        raise TypeError(f"Expected a list of names, not {names!r}.")

    return [f"{first} {last}" for group in names for first, last in group]


if __name__ == "__main__":
    print(f"Full names: {full_names(NAMES)}")

    try:
        full_names(None)
    except TypeError as error:
        print(f"Cannot join: {error}")
