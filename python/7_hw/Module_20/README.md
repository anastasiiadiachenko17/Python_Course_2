# Homework 20: Pytest

Four tasks, one folder each. Every task folder holds the code under test
and its tests, so each task can be run on its own.

```
Module_20/
├── requirements.txt     # pytest
├── pytest.ini           # palindrome marker (used by task 2)
├── task_20_1/           # add(), Calculator, ZeroDivisionError
├── task_20_2/           # is_palindrome(), palindrome marker
├── task_20_3/           # tests/ folder, test_multiply, -k filter
└── task_20_4/           # P0 marker, run everything except P0
```

## Setup

```bash
cd python/7_hw/Module_20
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the tests

Run each task from its own folder.

| Task | Command | Result |
| --- | --- | --- |
| 1 | `cd task_20_1 && pytest -v` | 28 passed |
| 2 | `cd task_20_2 && pytest test_string_operations.py -v` | 15 passed |
| 2 | `cd task_20_2 && pytest -m palindrome -v` | 11 passed, 4 deselected |
| 3 | `cd task_20_3 && pytest tests -v` | 43 passed |
| 3 | `cd task_20_3 && pytest tests/test_math.py -k test_multiply -v` | 5 passed, 23 deselected |
| 4 | `cd task_20_4 && pytest tests -m "not P0" -v` | 16 passed, 27 deselected |

## Tasks

**Task 1.** `calculator.py` has an `add()` function and a `Calculator`
class with `add`, `subtract`, `multiply` and `divide`. `test_math.py`
checks each of them with `parametrize`, including zero, negative and
float numbers. Float results are compared with `pytest.approx`. Dividing
by `0` or `0.0` is checked to raise `ZeroDivisionError`.

**Task 2.** `string_operations.py` has `reverse_string()` and
`is_palindrome()`. The comparison is exact, so `"Anna"` and
`"nurses run"` are not palindromes. Palindrome tests carry the
`palindrome` marker, registered in `Module_20/pytest.ini`.

**Task 3.** The tests are in a `tests/` folder next to the code.
`pythonpath = .` in `task_20_3/pytest.ini` lets the tests import the
code from the folder above. The multiplication test is named
`test_multiply`, so `-k test_multiply` selects only that test.

**Task 4.** The `P0` marker is set on the addition tests, the
multiplication test, one positive palindrome test (`True` expected)
and one negative palindrome test (`False` expected).
`-m "not P0"` runs everything else.

## Notes

- Tasks 3 and 4 are copies of the earlier code with the new layout,
  so tasks 1 and 2 stay as they were handed in.
- Running `pytest` from `Module_20` itself fails with
  `import file mismatch`, because tasks 1, 3 and 4 contain files with
  the same names. Run each task from its own folder.
- `venv/` is not in git. `requirements.txt` recreates it.
