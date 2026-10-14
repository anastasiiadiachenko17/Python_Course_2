"""Remove an item from a list."""


def remove_item(items, item):
    """Return a new list with the first matching item removed.

    Args:
        items: List to take the items from.
        item: Value to remove.

    Returns:
        A new list with all the original items except the removed one.

    Raises:
        ValueError: If the item is not in the list.
    """
    remaining_items = items.copy()
    remaining_items.remove(item)
    return remaining_items


food_stuff = ["Potato", "Tomato", "Mango", "Milk"]
print(remove_item(food_stuff, "Mango"))

numbers = [2, 3, 7, 9]
print(remove_item(numbers, 3))

print(food_stuff)
