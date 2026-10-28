"""Flip the keys and values of a dictionary with a dict comprehension."""

LETTERS = {"a": 1, "b": 2, "c": 3}


def flip(dictionary):
    """Return a new dictionary with the keys and values swapped.

    Args:
        dictionary: Dictionary to flip, its values must be hashable
            and unique.

    Returns:
        A new dictionary that maps every value to its key.

    Raises:
        TypeError: If dictionary is not a dict.
        ValueError: If several keys share a value, so flipping would
            lose some of the keys.
    """
    if not isinstance(dictionary, dict):
        raise TypeError(f"Expected a dictionary, not {dictionary!r}.")

    if len(set(dictionary.values())) != len(dictionary):
        raise ValueError(f"Values must be unique to flip, not {dictionary!r}.")

    return {value: key for key, value in dictionary.items()}


if __name__ == "__main__":
    print(f"Flipped: {flip(LETTERS)}")

    try:
        flip({"x": 1, "y": 1})
    except ValueError as error:
        print(f"Cannot flip: {error}")
