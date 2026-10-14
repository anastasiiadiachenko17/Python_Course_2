"""Square every number in a list using the functional approach."""


def square_all(numbers):
    """Return a new list with the square of every number.

    Args:
        numbers: List of numbers to square.

    Returns:
        A new list with the square of each given number.
    """
    return list(map(lambda number: number**2, numbers))


print(square_all([1, 2, 3, 4, 5]))
print(square_all([-3, 0, 7]))
print(square_all([2.5]))
print(square_all([]))
