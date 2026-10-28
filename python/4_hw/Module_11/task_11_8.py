"""Keep only the negative numbers and zero with a list comprehension."""

NUMBERS = [-4, -3, -2, -1, 0, 2, 4, 6]


def non_positive(numbers):
    """Return the negative numbers and zeros in the order they appear.

    Args:
        numbers: List of numbers to filter.

    Returns:
        A new list with only the numbers that are zero or below.

    Raises:
        TypeError: If numbers is not a list.
    """
    if not isinstance(numbers, list):
        raise TypeError(f"Expected a list of numbers, not {numbers!r}.")

    return [number for number in numbers if number <= 0]


if __name__ == "__main__":
    print(f"Negative and zero: {non_positive(NUMBERS)}")

    try:
        non_positive(None)
    except TypeError as error:
        print(f"Cannot filter: {error}")
