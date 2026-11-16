"""Tests for the add function and the Calculator class."""

import pytest

from calculator import Calculator, add


@pytest.fixture
def calculator():
    """Give every test a new Calculator.

    Returns:
        A Calculator instance.
    """
    return Calculator()


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [(2, 3, 5), (-4, -6, -10), (-7, 7, 0), (0, 0, 0), (10**20, 1, 10**20 + 1)],
    ids=["positive", "negative", "opposite", "zeros", "huge"],
)
def test_add(first, second, expected):
    """The add function returns the sum for different whole numbers."""
    assert add(first, second) == expected


def test_add_floats():
    """Float sums are compared with approx because of rounding."""
    assert add(0.1, 0.2) == pytest.approx(0.3)


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [(2, 3, 5), (-2, -3, -5), (-2, 3, 1), (0, 9, 9), (2.5, 0.5, 3.0)],
    ids=["positive", "negative", "mixed signs", "zero", "floats"],
)
def test_calculator_add(calculator, first, second, expected):
    """The calculator adds positive, negative, zero and float numbers."""
    assert calculator.add(first, second) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [(9, 4, 5), (4, 9, -5), (-3, -3, 0), (0, 5, -5), (1.5, 0.5, 1.0)],
    ids=["positive", "negative result", "equal", "from zero", "floats"],
)
def test_calculator_subtract(calculator, first, second, expected):
    """The calculator subtracts, the result can be negative."""
    assert calculator.subtract(first, second) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [(3, 4, 12), (-3, 4, -12), (-3, -4, 12), (7, 0, 0), (0.5, 4, 2.0)],
    ids=["positive", "one negative", "two negatives", "by zero", "float"],
)
def test_calculator_multiply(calculator, first, second, expected):
    """The calculator multiplies, a zero factor gives zero."""
    assert calculator.multiply(first, second) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [(10, 2, 5.0), (7, 2, 3.5), (-9, 3, -3.0), (0, 5, 0.0), (1, 3, 1 / 3)],
    ids=["exact", "with remainder", "negative", "zero top", "endless"],
)
def test_calculator_divide(calculator, first, second, expected):
    """The calculator divides and always returns a float."""
    assert calculator.divide(first, second) == pytest.approx(expected)


@pytest.mark.parametrize("zero", [0, 0.0], ids=["int zero", "float zero"])
def test_divide_by_zero_raises_zero_division_error(calculator, zero):
    """Dividing by zero raises ZeroDivisionError, so the test passes."""
    with pytest.raises(ZeroDivisionError):
        calculator.divide(5, zero)
