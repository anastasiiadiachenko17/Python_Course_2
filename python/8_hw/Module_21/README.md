# Homework 21: Pytest, part 2

Six tasks, one folder each. Every task folder holds the code under test
and its tests, so each task can be run on its own.

```
Module_21/
├── requirements.txt     # pytest, pytest-rerunfailures
├── task_21_1/           # input_data fixture
├── task_21_2/           # temporary file fixtures, --keep-temp-files
├── task_21_3/           # all fixtures in tests/conftest.py
├── task_21_4/           # parametrized test
├── task_21_5/           # skip and xfail
└── task_21_6/           # flaky test, --reruns, --reruns-delay
```

## Setup

```bash
cd python/8_hw/Module_21
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the tests

Run each task from its own folder.

| Task | Command | Result |
| --- | --- | --- |
| 1 | `cd task_21_1 && pytest -v` | 1 passed |
| 2 | `cd task_21_2 && pytest -v` | 2 passed, temporary files deleted |
| 2 | `cd task_21_2 && pytest -v --keep-temp-files` | 2 passed, temporary files kept |
| 3 | `cd task_21_3 && pytest tests -v` | 3 passed |
| 3 | `cd task_21_3 && pytest tests --fixtures` | fixtures listed from `tests/conftest.py` |
| 4 | `cd task_21_4 && pytest tests -v` | 10 passed |
| 5 | `cd task_21_5 && pytest tests -v -rsx` | 9 passed, 1 skipped, 1 xfailed |
| 6 | `cd task_21_6 && pytest tests -v` | 1 failed about half of the time |
| 6 | `cd task_21_6 && pytest tests -v --reruns 3` | passes after a `RERUN` |
| 6 | `cd task_21_6 && pytest tests -v --reruns 3 --reruns-delay 2` | the same, with 2 seconds between reruns |

## Tasks

**Task 1.** The `input_data` fixture returns a config with a `server`
and a `database` section. `test_input_data_is_valid` checks the
sections, the keys of each section, and the type and range of every
value.

**Task 2.** `create_temp_file` creates a temporary file before the
test, yields it, and deletes it after the test. The `input_file` and
`output_file` fixtures use it, so a test gets two different files.
`to_upper_case` in `data_processing.py` writes the input text in upper
case into the output file. One test checks the result, the other
checks that the input file is unchanged. The `--keep-temp-files`
option, registered in `conftest.py`, turns the deletion off.

**Task 3.** All fixtures and the `--keep-temp-files` option are in
`tests/conftest.py`. The test files contain only tests.
`pythonpath = .` in `pytest.ini` lets the tests import the code from
the folder above.

**Task 4.** `test_to_upper_case_scenarios` runs the same check for
seven texts: lower, mixed and upper case, digits and signs, two lines,
Cyrillic and an empty string.

**Task 5.** The Cyrillic case is skipped with `pytest.param(...,
marks=pytest.mark.skip(reason=...))`, because the temporary file uses
the system encoding, which is not UTF-8 everywhere.
`test_to_upper_case_reads_from_start` is marked `xfail` for a known
issue: `to_upper_case` does not rewind the input file to the start.

**Task 6.** `test_to_upper_case_writes_upper_case_text` fails at random
half of the time. `--reruns` runs a failed test again, and
`--reruns-delay` waits between the runs. With `--reruns 3` all four
attempts fail only about once in 16 runs.

## Notes

- Tasks 3 to 6 are copies of the previous task with one change each,
  so every task stays as it was handed in.
- Running `pytest` from `Module_21` itself fails, because tasks 2 to 6
  each register `--keep-temp-files` and contain files with the same
  names. Run each task from its own folder.
- `venv/` is not in git. `requirements.txt` recreates it.
