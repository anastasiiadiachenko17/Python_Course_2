"""Read, write and append to files with error handling."""

READ = "read"
FILE_MODES = {READ: "r", "write": "w", "append": "a"}


def work_with_file(operation, file_path, content=None):
    """Perform a read, write or append operation on a file.

    The content of the file is printed when reading it.

    Args:
        operation: One of "read", "write" or "append".
        file_path: Path to the file to work with, as a string.
        content: Text to write, required for "write" and "append".
    """
    mode = FILE_MODES.get(operation)

    if mode is None:
        print(f"Unknown operation {operation!r}, use one of"
              f" {', '.join(FILE_MODES)}.")
        return

    if not isinstance(file_path, str):
        print(f"The file path must be text, not"
              f" {type(file_path).__name__}.")
        return

    if operation != READ and not isinstance(content, str):
        print(f"The {operation!r} operation needs text content.")
        return

    try:
        with open(file_path, mode, encoding="utf-8") as opened_file:
            if operation == READ:
                print(opened_file.read())
            else:
                opened_file.write(content)
                print(f"Done: {operation} {file_path}.")
    except FileNotFoundError:
        print(f"There is no file at {file_path!r}.")
    except IsADirectoryError:
        print(f"{file_path!r} is a folder, not a file.")
    except PermissionError:
        print(f"No permission to open {file_path!r}.")
    except UnicodeDecodeError:
        print(f"{file_path!r} is not a readable text file.")
    except OSError as error:
        print(f"Could not {operation} {file_path!r}: {error}")


if __name__ == "__main__":
    work_with_file("write", "notes.txt", "First line.\n")
    work_with_file("append", "notes.txt", "Second line.\n")
    work_with_file("read", "notes.txt")

    work_with_file("read", "missing.txt")
    work_with_file("read", ".")
    work_with_file("write", "notes.txt")
    work_with_file("delete", "notes.txt")
