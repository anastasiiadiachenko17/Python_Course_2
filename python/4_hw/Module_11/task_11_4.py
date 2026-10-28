"""Sort fruit and number pairs by the number with a lambda function."""

FRUITS = [("apple", 50), ("banana", 10), ("cherry", 30)]


def sort_by_number(pairs):
    """Return the pairs sorted by their number, from the smallest.

    Pairs with the same number keep their original order.

    Args:
        pairs: List of (name, number) tuples.

    Returns:
        A new sorted list, the original list stays as it was.

    Raises:
        TypeError: If pairs is not a list.
    """
    if not isinstance(pairs, list):
        raise TypeError(f"Expected a list of pairs, not {pairs!r}.")

    return sorted(pairs, key=lambda pair: pair[1])


if __name__ == "__main__":
    print(f"Sorted by number: {sort_by_number(FRUITS)}")

    try:
        sort_by_number(None)
    except TypeError as error:
        print(f"Cannot sort: {error}")
