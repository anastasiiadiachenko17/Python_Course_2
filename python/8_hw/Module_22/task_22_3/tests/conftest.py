"""Fixtures, options and hooks shared by all tests in this folder."""

import logging
import os
import tempfile

import pytest

logger = logging.getLogger(__name__)

ARTIFACTS_DIR = "artifacts"
LOG_FILE_NAME = "pytest.log.txt"


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


@pytest.hookimpl(wrapper=True)
def pytest_runtest_protocol(item):
    """Save the log of every test into its own artefact folder.

    Args:
        item: The test that is about to run.

    Yields:
        Control back to pytest, which runs the test.

    Returns:
        The result pytest gives back after running the test.
    """
    folder = item.config.rootpath / ARTIFACTS_DIR / item.name
    folder.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(folder / LOG_FILE_NAME, mode="w")
    handler.setFormatter(
        logging.Formatter(
            item.config.getini("log_file_format"),
            item.config.getini("log_file_date_format"),
        )
    )
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    try:
        return (yield)
    finally:
        root_logger.removeHandler(handler)
        handler.close()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Log the start of the setup stage, before the fixtures run.

    Args:
        item: The test whose fixtures are being prepared.
    """
    logger.info("===SETUP=== %s", item.name)


def pytest_runtest_call(item):
    """Log the start of the call stage, when the test body runs.

    Args:
        item: The test that is being run.
    """
    logger.info("===CALL=== %s", item.name)


def pytest_runtest_teardown(item):
    """Log the start of the teardown stage, before fixtures clean up.

    Args:
        item: The test whose fixtures are being cleaned up.
    """
    logger.info("===TEARDOWN=== %s", item.name)


@pytest.fixture
def input_data():
    """Give every test the same config with two sections.

    Returns:
        A dict with a "server" and a "database" section.
    """
    return {
        "server": {"host": "localhost", "port": 8080, "debug": False},
        "database": {"name": "students", "user": "admin", "timeout": 30},
    }


def create_temp_file(request):
    """Create a temporary file, give it to the test, then delete it.

    Args:
        request: The pytest request, used to read the command line option.

    Yields:
        The temporary file, open for writing and reading.
    """
    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".txt", delete=False
    ) as file:
        logger.info("Created temporary file %s", file.name)
        yield file
    if request.config.getoption("--keep-temp-files"):
        logger.info("Kept temporary file %s", file.name)
    else:
        os.remove(file.name)
        logger.info("Deleted temporary file %s", file.name)


@pytest.fixture
def input_file(request):
    """Temporary file the test writes the input text into.

    Yields:
        The temporary input file.
    """
    yield from create_temp_file(request)


@pytest.fixture
def output_file(request):
    """Temporary file the function under test writes the result into.

    Yields:
        The temporary output file.
    """
    yield from create_temp_file(request)
