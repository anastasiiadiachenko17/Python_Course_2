"""Generator that picks the log records of one level."""

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")
RECORD_PARTS = 4


def filter_log(lines, level):
    """Yield the records of one level, reading the lines one by one.

    Every valid line looks like "<date> <time> <LEVEL> <message>".
    Blank lines and lines with fewer than four parts are skipped.

    The level is checked when the iteration starts, because the body
    of a generator runs only on the first next().

    Args:
        lines: Any iterable of strings, e.g. a list or an open file.
        level: Level to keep: DEBUG, INFO, WARNING or ERROR.

    Yields:
        A (timestamp, message) tuple for every matching line, where
        timestamp is "<date> <time>" and message has no trailing
        newline.

    Raises:
        ValueError: If level is not one of LEVELS.
    """
    if level not in LEVELS:
        raise ValueError(f"level must be one of {LEVELS}, got {level!r}")

    for line in lines:
        parts = line.rstrip().split(maxsplit=RECORD_PARTS - 1)
        if len(parts) < RECORD_PARTS:
            continue

        date, time, line_level, message = parts
        if line_level == level:
            yield f"{date} {time}", message
