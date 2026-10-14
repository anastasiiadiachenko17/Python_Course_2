"""Calculate rectangle areas and print a few examples."""


def calculate_rectangle_area(length, width):
    """Return the area of a rectangle.

    Args:
        length: Length of the rectangle.
        width: Width of the rectangle.

    Returns:
        The area of the rectangle, as length multiplied by width.
    """
    return length * width


print(calculate_rectangle_area(3, 4))
print(calculate_rectangle_area(5, 5))
print(calculate_rectangle_area(2.5, 4))
print(calculate_rectangle_area(10, 1))
print(calculate_rectangle_area(0, 7))
