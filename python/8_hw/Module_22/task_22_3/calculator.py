"""A function that adds two numbers and a basic calculator class."""


def add(first, second):
    """Return the sum of two numbers.

    Args:
        first: First number.
        second: Second number.

    Returns:
        first + second.
    """
    return first + second


class Calculator:
    """A basic calculator that adds, subtracts, multiplies and divides."""

    def add(self, first, second):
        """Return the sum of two numbers.

        Args:
            first: First number.
            second: Second number.

        Returns:
            first + second.
        """
        return first + second

    def subtract(self, first, second):
        """Return the difference of two numbers.

        Args:
            first: Number to subtract from.
            second: Number to subtract.

        Returns:
            first - second.
        """
        return first - second

    def multiply(self, first, second):
        """Return the product of two numbers.

        Args:
            first: First number.
            second: Second number.

        Returns:
            first * second.
        """
        return first * second

    def divide(self, first, second):
        """Return the quotient of two numbers.

        Args:
            first: Number to divide.
            second: Number to divide by, must not be zero.

        Returns:
            first / second, always a float.

        Raises:
            ZeroDivisionError: If second is zero.
        """
        return first / second
