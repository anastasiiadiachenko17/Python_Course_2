"""Copy a list of numbers with a list comprehension."""


def copy_list(numbers):
    """Return a new list with the same numbers in the same order.

    Args:
        numbers: List of numbers to copy.

    Returns:
        A new list, so changing it leaves the original untouched.

    Raises:
        TypeError: If numbers is not a list.
    """
    if not isinstance(numbers, list):
        raise TypeError(f"Expected a list of numbers, not {numbers!r}.")

    return [number for number in numbers]  # noqa: C416


if __name__ == "__main__":
    original = [17, -42, 8.25, 0, 1024]
    copy = copy_list(original)
    copy.append(99)

    print(f"Original: {original}")
    print(f"Copy:     {copy}")

    try:
        copy_list(None)
    except TypeError as error:
        print(f"Cannot copy: {error}")
