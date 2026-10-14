"""Keep only the even numbers of a list using the functional approach."""


def filter_even(numbers):
    """Return a new list with only the even numbers.

    Args:
        numbers: List of integers to filter.

    Returns:
        A new list with the even numbers, in their original order.
    """
    return list(filter(lambda number: number % 2 == 0, numbers))


print(filter_even([1, 2, 3, 4, 5, 6]))
print(filter_even([7, 9, 11]))
print(filter_even([-4, -3, 0]))
print(filter_even([]))
