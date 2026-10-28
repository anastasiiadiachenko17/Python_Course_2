"""Flatten a list of lists with a list comprehension."""

NESTED = [[5, 4, 7], [8, 9, 6], [7, 2, 4]]


def flatten(rows):
    """Return all items of the inner lists as one list.

    The items keep their order: the first list, then the second,
    and so on.

    Args:
        rows: List of lists to flatten.

    Returns:
        A new list with every item of every inner list.

    Raises:
        TypeError: If rows is not a list.
    """
    if not isinstance(rows, list):
        raise TypeError(f"Expected a list of lists, not {rows!r}.")

    return [item for row in rows for item in row]


if __name__ == "__main__":
    print(f"Flattened: {flatten(NESTED)}")

    try:
        flatten(None)
    except TypeError as error:
        print(f"Cannot flatten: {error}")
