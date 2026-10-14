"""Calculate a factorial using the functional approach."""

import operator
from functools import reduce


def factorial(number):
    """Return the factorial of a non-negative integer.

    Args:
        number: Non-negative integer to compute the factorial of.

    Returns:
        The factorial of the number, and 1 for 0.
    """
    return reduce(operator.mul, range(1, number + 1), 1)


print(factorial(0))
print(factorial(1))
print(factorial(5))
print(factorial(10))
