"""Sum an arbitrary number of numeric arguments."""


def add_all_nums(*args):
    """Return the sum of all the given numbers.

    Args:
        *args: Values to add up. Every value must be an int or a float.

    Returns:
        The sum of the values, or None if any value is not a number.
    """
    for value in args:
        if not isinstance(value, (int, float)):
            print(f"{value!r} is not a number")
            return None

    return sum(args)


print(add_all_nums(1, 2, 3, 4))
print(add_all_nums(2.5, 2.5))
print(add_all_nums(-5, 10))
print(add_all_nums())

# Prints its own message, so there is nothing to print here.
add_all_nums(1, "two", 3)
