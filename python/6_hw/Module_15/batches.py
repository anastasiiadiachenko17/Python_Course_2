"""Iterator that splits any iterable into batches of a given size."""


class Batches:
    """Iterate over the items in lists of at most size elements.

    The items are read lazily, one batch at a time, so a generator or
    an open file is never read in full.

    Attributes:
        size: Number of elements in one batch, the last one may be
            shorter.
    """

    def __init__(self, items, size):
        """Prepare to split the items into batches.

        Args:
            items: Any iterable: a list, a tuple, a string, a
                generator, ...
            size: Number of elements in one batch, at least 1.

        Raises:
            TypeError: If size is not an int.
            ValueError: If size is smaller than 1.
        """
        if not isinstance(size, int):
            raise TypeError(f"size must be an int, got {size!r}")
        if size < 1:
            raise ValueError(f"size must be at least 1, got {size}")

        self._items = iter(items)
        self.size = size

    def __iter__(self):
        """Return the iterator itself.

        Returns:
            This Batches object.
        """
        return self

    def __next__(self):
        """Return the next batch.

        Returns:
            A list with the next size elements, or fewer for the last
            batch.

        Raises:
            StopIteration: If there are no elements left.
        """
        batch = []
        for item in self._items:
            batch.append(item)
            if len(batch) == self.size:
                break

        if not batch:
            raise StopIteration

        return batch
