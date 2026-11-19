"""Command line options for the tests in this folder."""


def pytest_addoption(parser):
    """Add the --keep-temp-files option to the pytest command.

    Args:
        parser: The pytest parser for command line options.
    """
    parser.addoption(
        "--keep-temp-files",
        action="store_true",
        help="Do not delete the temporary files after each test.",
    )
