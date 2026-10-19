"""Count the lines and the words in the Steve Jobs speech file."""

SPEECH_FILE = "steve_job_speech.txt"


def count_lines_and_words(text):
    """Return how many lines and words the given text contains.

    Args:
        text: Text to measure.

    Returns:
        A tuple with the number of lines and the number of words.

    Raises:
        TypeError: If the text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected a string, not {type(text).__name__}.")

    return len(text.splitlines()), len(text.split())


if __name__ == "__main__":
    try:
        with open(SPEECH_FILE, encoding="utf-8") as speech_file:
            speech = speech_file.read()
    except FileNotFoundError:
        print(f"There is no file at {SPEECH_FILE!r}.")
    else:
        lines, words = count_lines_and_words(speech)
        print(f"Lines: {lines}")
        print(f"Words: {words}")
