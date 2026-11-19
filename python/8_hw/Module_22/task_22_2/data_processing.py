"""Read text from one file and write it in upper case to another."""


def to_upper_case(input_file, output_file):
    """Write the text of input_file in upper case into output_file.

    Args:
        input_file: Open file to read from, positioned at the start.
        output_file: Open file to write the result to.
    """
    output_file.write(input_file.read().upper())
