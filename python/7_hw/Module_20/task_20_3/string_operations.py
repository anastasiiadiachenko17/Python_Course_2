"""String operations: reverse a string and check for a palindrome."""


def reverse_string(text):
    """Return the string written backwards.

    Args:
        text: String to reverse.

    Returns:
        A new string with the characters in reverse order.
    """
    return text[::-1]


def is_palindrome(text):
    """Tell whether a string is equal to its reversed version.

    The check is exact: upper and lower case letters and spaces count,
    so "Anna" is not a palindrome but "anna" is.

    Args:
        text: String to check.

    Returns:
        True if the string reads the same backwards, False if not.
    """
    return text == reverse_string(text)
