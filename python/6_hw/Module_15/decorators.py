"""Decorators that count calls, repeat calls and wrap text in tags."""

import functools


def count_calls(func):
    """Count how many times the decorated function is called.

    Args:
        func: Function to decorate.

    Returns:
        A wrapper that returns what func returns and keeps the number
        of calls in its calls attribute, starting at 0.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def repeat(times):
    """Build a decorator that calls the function several times in a row.

    Args:
        times: How many times to call the function, 0 or more.

    Returns:
        A decorator whose wrapper returns a list with the result of
        every call.

    Raises:
        TypeError: If times is not an int.
        ValueError: If times is negative.
    """
    if not isinstance(times, int):
        raise TypeError(f"times must be an int, got {times!r}")
    if times < 0:
        raise ValueError(f"times must not be negative, got {times}")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]

        return wrapper

    return decorator


def bold(func):
    """Wrap the result of the function in <b>...</b>.

    Args:
        func: Function to decorate.

    Returns:
        A wrapper that returns the result of func inside <b> tags.
    """

    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"

    return wrapper


def italic(func):
    """Wrap the result of the function in <i>...</i>.

    Args:
        func: Function to decorate.

    Returns:
        A wrapper that returns the result of func inside <i> tags.
    """

    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"

    return wrapper
