"""Build a table of powers as a list of tuples with a list comprehension."""

LAST_NUMBER = 10
HIGHEST_POWER = 5


def powers_table():
    """Return a tuple of powers for every number from 0 to LAST_NUMBER.

    Each tuple starts with the number, followed by the number raised
    to the powers 0, 1, ... HIGHEST_POWER.

    Returns:
        A list of tuples, one per number.
    """
    return [
        (number, *(number**power for power in range(HIGHEST_POWER + 1)))
        for number in range(LAST_NUMBER + 1)
    ]


if __name__ == "__main__":
    for row in powers_table():
        print(row)
