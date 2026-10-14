"""Sum an arbitrary number of numeric arguments."""


def add_all_nums(*args):
    """Return the sum of all the given numbers.

    Args:
        *args: Values to add up. Every value must be an int or a float.

    Returns:
        The sum of all the given values, or 0 when called without any.

    Raises:
        TypeError: If any of the values is not an int or a float.
    """
    for value in args:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{value!r} is not a number")

    return sum(args)


print(add_all_nums(1, 2, 3, 4))
print(add_all_nums(2.5, 2.5))
print(add_all_nums(-5, 10))
print(add_all_nums())

try:
    add_all_nums(1, "two", 3)
except TypeError as error:
    print(f"Error: {error}")
