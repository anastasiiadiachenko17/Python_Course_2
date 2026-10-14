"""Reverse a list using a loop instead of the built-in helpers."""


def reverse_list(items):
    """Return a new list with the items in reverse order.

    Args:
        items: List of items to reverse.

    Returns:
        A new list with the same items in reverse order.
    """
    reversed_items = []

    for item in items:
        reversed_items.insert(0, item)

    return reversed_items


print(reverse_list([1, 2, 3, 4, 5]))
print(reverse_list(["A", "B", "C"]))
print(reverse_list([42]))
print(reverse_list([]))
