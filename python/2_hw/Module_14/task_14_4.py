"""Capitalize the first letter of every word using the functional approach."""


def capitalize_words(sentence):
    """Return the sentence with the first letter of each word capitalized.

    Args:
        sentence: Sentence whose words should be capitalized.

    Returns:
        A new sentence with every word starting with a capital letter.
    """
    return " ".join(map(str.capitalize, sentence.split()))


print(capitalize_words("hello world, how are you?"))
print(capitalize_words("python is fun"))
print(capitalize_words(""))
