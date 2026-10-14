"""Calculate the average score of students using the functional approach."""

from operator import itemgetter


def average_score(scores):
    """Return the average mark of the given students.

    Args:
        scores: List of (student name, mark) tuples.

    Returns:
        The average mark, or 0 when the list is empty.
    """
    if not scores:
        return 0

    marks = list(map(itemgetter(1), scores))
    return sum(marks) / len(marks)


scores = [("Alice", 85), ("Bob", 92), ("Charlie", 78), ("David", 95)]
print(average_score(scores))
print(average_score([("Alice", 100)]))
print(average_score([]))
