"""Tests for the Module 11 lambda and comprehension tasks."""

import ast
import inspect

import pytest

from task_11_1 import copy_list


def test_the_copy_has_the_same_numbers_in_the_same_order():
    """The copy holds every number of the original in its place."""
    assert copy_list([17, -42, 8.25, 0, 1024]) == [17, -42, 8.25, 0, 1024]


def test_the_copy_is_a_new_list():
    """The copy is a different object, not the original itself."""
    numbers = [12, 45, 78]

    assert copy_list(numbers) is not numbers


def test_changing_the_copy_leaves_the_original_untouched():
    """Adding to the copy does not add to the original."""
    numbers = [12, 45, 78]

    copy_list(numbers).append(99)

    assert numbers == [12, 45, 78]


def test_an_empty_list_gives_a_new_empty_list():
    """Copying an empty list gives another empty list."""
    numbers = []

    copy = copy_list(numbers)

    assert copy == []
    assert copy is not numbers


def test_negative_and_float_numbers_are_copied():
    """Numbers of any sign and type are copied as they are."""
    assert copy_list([-273.15, 0, 9.81]) == [-273.15, 0, 9.81]


def test_a_one_number_list_and_duplicates_are_copied():
    """A single number and repeated numbers are copied as they are."""
    assert copy_list([7]) == [7]
    assert copy_list([13, 13, 13]) == [13, 13, 13]


@pytest.mark.parametrize("not_a_list", [None, (12, 45), "17", 42])
def test_something_that_is_not_a_list_is_rejected(not_a_list):
    """Only a list can be copied."""
    with pytest.raises(TypeError, match="Expected a list of numbers"):
        copy_list(not_a_list)


def test_the_copy_is_made_with_a_list_comprehension():
    """The task asks for a list comprehension, not list() or slicing."""
    tree = ast.parse(inspect.getsource(copy_list))
    returned = next(
        node.value for node in ast.walk(tree) if isinstance(node, ast.Return)
    )

    assert isinstance(returned, ast.ListComp)
