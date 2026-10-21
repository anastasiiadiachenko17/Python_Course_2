"""Small example module cleaned up with ruff."""

from collections import OrderedDict


def add(a, b):
    """Return the sum of two numbers.

    Args:
        a: First number to add.
        b: Second number to add.

    Returns:
        The sum of the two numbers.
    """
    return a + b


def check(x):
    """Return the value and report it when it is None.

    Args:
        x: Value to look at.

    Returns:
        The value that was given.
    """
    if x is None:
        print("none!")
    return x


totals = OrderedDict()
totals["sum"] = add(2, 3)
print(totals["sum"])
