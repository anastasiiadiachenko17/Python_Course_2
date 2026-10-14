"""Add an item to the end of a list."""


def add_item(items, item):
    """Return a new list with the item added at the end.

    Args:
        items: List whose items come first in the result.
        item: Value to add at the end.

    Returns:
        A new list with all the original items plus the new item.
    """
    return items + [item]


food_stuff = ["Potato", "Tomato", "Mango", "Milk"]
print(add_item(food_stuff, "Meat"))

numbers = [2, 3, 7, 9]
print(add_item(numbers, 5))

print(add_item([], "first"))
print(food_stuff)
