"""Multiply all numbers of a list with functools.reduce() and a lambda."""

from functools import reduce

NUMBERS = [1, 2, 3, 4, 5]


def multiply_all(numbers):
    """Return the product of all numbers in a list.

    Args:
        numbers: List of numbers to multiply.

    Returns:
        The product of the numbers, or 1 for an empty list, the same
        as math.prod().

    Raises:
        TypeError: If numbers is not a list.
    """
    if not isinstance(numbers, list):
        raise TypeError(f"Expected a list of numbers, not {numbers!r}.")

    return reduce(lambda product, number: product * number, numbers, 1)


if __name__ == "__main__":
    print(f"Product of {NUMBERS}: {multiply_all(NUMBERS)}")

    try:
        multiply_all(None)
    except TypeError as error:
        print(f"Cannot multiply: {error}")
