# Exercise 2: ruff on a messy file

`messy.py` was cleaned with [ruff](https://docs.astral.sh/ruff/) 0.17.0.
The rules come from `pyproject.toml` in this folder: `line-length = 120`,
`target-version = "py311"`, double quotes, and
`select = ["E", "W", "F", "I", "UP", "B", "C4", "N", "Q"]`.

## Violations found before the fix

`ruff check .` reported **12 violations across 9 rules**, and
`ruff format --check .` reported **1 file would be reformatted**.

| Rule | Count | What it meant here | How it was fixed |
| --- | --- | --- | --- |
| `E401` | 1 | `import os, sys` put two imports on one line | `ruff check --fix` split them, then both turned out to be unused and went away |
| `I001` | 1 | the import block was unsorted | `ruff check --fix` sorted it; only `OrderedDict` was left |
| `F401` | 3 | `os`, `sys` and `json` were imported but never used | `ruff check --fix` removed all three |
| `N802` | 1 | the function was named `Add`, not snake_case | renamed by hand to `add` (not auto-fixable, since the call site has to change too) |
| `F841` | 2 | `unused = 42` and `msg = "done"` were assigned and never read | removed by hand (the auto-fix exists but is marked unsafe) |
| `F541` | 1 | `f"done"` was an f-string with no placeholder | `ruff check --fix` dropped the `f` prefix; the line was then deleted with `F841` |
| `E711` | 1 | `x == None` compared to `None` with `==` | changed by hand to `x is None` (the auto-fix is marked unsafe) |
| `Q000` | 1 | `'none!'` used single quotes | `ruff check --fix` switched to double quotes |
| `W292` | 1 | the file had no newline at the end | `ruff check --fix` added it |

`ruff format` also fixed the spacing that no lint rule covers:
`def Add(a,b)` to `def add(a, b)`, `result=a+b` to `result = a + b`, and
`print( Add(2 ,3) )` to `print(add(2, 3))`.

## Order of the fixes

```bash
ruff check .                 # 12 violations recorded in the table above
ruff format --check --diff . # 1 file would be reformatted
ruff check --fix .           # 7 fixed automatically, 4 left
ruff format .                # 1 file reformatted
```

The four that were left are the ones the task warns about: `N802`, `F841`
twice and `E711`. Ruff does not fix them on its own, because renaming a
function or deleting an assignment can change what the code does. They
were fixed by hand. No rule is silenced anywhere in the code.

While removing `F841` the variable `d` also lost its purpose, so the
`OrderedDict` is now filled and printed instead of being left empty.

## Result

```bash
ruff check .          # All checks passed!
ruff format --check . # 2 files already formatted
```

Ruff 0.17 formats `pyproject.toml` as well, so `.` counts two files here.
The exercise expects `1 file already formatted`, which is what the only
Python file of the folder reports on its own:

```bash
ruff format --check messy.py # 1 file already formatted
```

## Pre-commit

`.pre-commit-config.yaml` lives in the repository root, because that is
the only place pre-commit reads it from. Both hooks are limited to this
folder with `files: ^python/3_hw/Module_17/17_ruff/` and point at the
`pyproject.toml` of this exercise.

The limit is deliberate. This exercise asks for `line-length = 120`,
while the course grading criteria ask for 79. Without the limit,
`ruff format` would join lines in the other modules back together and
push them past 79 characters, which would cost points there.

```bash
pre-commit install
pre-commit run --all-files
```

```
ruff (17_ruff)...........................................................Passed
ruff-format (17_ruff)....................................................Passed
```
