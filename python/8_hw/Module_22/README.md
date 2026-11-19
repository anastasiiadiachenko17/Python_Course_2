# Homework 22: pytest.ini, log capturing, HTML reports

Three tasks, one folder each. Every task folder is a small project with
the code and tests of modules 20 and 21 together, so the markers of both
modules live in one `pytest.ini`.

```
Module_22/
├── requirements.txt     # pytest, pytest-rerunfailures, pytest-html
├── task_22_1/           # root pytest.ini: markers, logging, addopts
├── task_22_2/           # stage logging hooks, log files as artefacts
└── task_22_3/           # pytest-html report in the artefacts
```

Each task folder has the same layout:

```
task_22_X/
├── pytest.ini
├── calculator.py           # from module 20
├── string_operations.py    # from module 20
├── data_processing.py      # from module 21
└── tests/
    ├── conftest.py
    ├── test_math.py
    ├── test_string_operations.py
    ├── test_basic_fixture.py
    └── test_data_processing.py
```

## Setup

```bash
cd python/8_hw/Module_22
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the tests

Run each task from its own folder. The options come from `pytest.ini`,
so a plain `pytest` is enough.

| Task | Command | Result |
| --- | --- | --- |
| 1 | `cd task_22_1 && pytest` | 52 passed, 1 skipped, 1 xfailed, with live logs |
| 1 | `cd task_22_1 && pytest -m P0` | 27 passed, 27 deselected |
| 2 | `cd task_22_2 && pytest` | the same, plus `artifacts/` with log files |
| 3 | `cd task_22_3 && pytest` | the same, plus `artifacts/report.html` |
| 3 | `open artifacts/report.html` | opens the report in the browser |

The flaky test from module 21 sometimes needs a rerun, so the summary
can also show `1 rerun`.

## Tasks

**Task 1.** `pytest.ini` in the project root holds everything:

- `pythonpath` and `testpaths`;
- the `palindrome` and `P0` markers;
- live logging with `log_cli`, `log_cli_level`, `log_format` and
  `log_date_format`;
- default options in `addopts`: `-v -rsx --strict-markers --reruns 3
  --reruns-delay 1`.

With `--strict-markers`, a misspelt marker is an error, so every marker
has to be registered here. The temporary file fixtures in
`tests/conftest.py` log when a file is created and deleted.

**Task 2.** Three hooks in `tests/conftest.py` log `===SETUP===`,
`===CALL===` and `===TEARDOWN===` with the test name. The `log_file`
options in `pytest.ini` write the log of the whole run to
`artifacts/pytest.log.txt`. The `pytest_runtest_protocol` wrapper hook
also writes the log of each test to
`artifacts/<test name>/pytest.log.txt`.

**Task 3.** `--html=artifacts/report.html --self-contained-html` in
`addopts` adds a pytest-html report to the artefacts. The report is a
single file with the result and the log of every test.

## Notes

- `artifacts/` is created by the test run and is not in git.
- Run each task from its own folder. Running `pytest` from `Module_22`
  itself fails, because the three tasks contain files with the same
  names.
- `venv/` is not in git. `requirements.txt` recreates it.
