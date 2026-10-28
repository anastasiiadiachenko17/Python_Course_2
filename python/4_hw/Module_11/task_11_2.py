"""Keep only the even numbers with a list comprehension."""


def even_numbers(numbers):
    """Return the even numbers in the order they appear.

    Args:
        numbers: List or range of whole numbers.

    Returns:
        A new list with only the even numbers.

    Raises:
        TypeError: If numbers is not a list or a range.
    """
    if not isinstance(numbers, (list, range)):
        raise TypeError(
            f"Expected a list or range of numbers, not {numbers!r}."
        )

    return [number for number in numbers if number % 2 == 0]


if __name__ == "__main__":
    print(f"Even numbers in 1..10: {even_numbers(range(1, 11))}")
    print(f"Even numbers in a list: {even_numbers([-6, 15, 0, 22, 37, 48])}")

    try:
        even_numbers(None)
    except TypeError as error:
        print(f"Cannot filter: {error}")
