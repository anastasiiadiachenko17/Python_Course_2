"""Log random sensor temperatures for three minutes."""

import logging
import random
import time

LOG_FILE = "sensor.log"
RUN_SECONDS = 180
READING_INTERVAL_SECONDS = 1
MIN_TEMPERATURE_C = -10
MAX_TEMPERATURE_C = 50
HIGH_TEMPERATURE_C = 35
CRITICAL_TEMPERATURE_C = 45
FREEZING_TEMPERATURE_C = 0

logger = logging.getLogger(__name__)


def setup_logging():
    """Send every message to the console and warnings to the log file."""
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def log_reading(temperature):
    """Log one temperature with the level that matches its value.

    Args:
        temperature: Temperature in degrees Celsius.
    """
    logger.debug("Temperature: %s", temperature)

    if temperature > CRITICAL_TEMPERATURE_C:
        logger.critical("Critical temperature: %s", temperature)
    elif temperature > HIGH_TEMPERATURE_C:
        logger.warning("High temperature: %s", temperature)
    elif temperature < FREEZING_TEMPERATURE_C:
        logger.error("Freezing temperature: %s", temperature)


def monitor_sensor(duration_seconds=RUN_SECONDS):
    """Read the sensor every second and log every value.

    Args:
        duration_seconds: How long to keep reading the sensor.

    Returns:
        The list of temperatures that were read.
    """
    logger.info("Sensor started for %s seconds.", duration_seconds)
    temperatures = []
    deadline = time.monotonic() + duration_seconds

    try:
        while time.monotonic() < deadline:
            temperature = random.randint(MIN_TEMPERATURE_C, MAX_TEMPERATURE_C)
            temperatures.append(temperature)
            log_reading(temperature)
            time.sleep(READING_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logger.exception("Stopped by the user.")

    logger.info("Sensor stopped.")

    if temperatures:
        logger.info(
            "Summary: count=%s, min=%s, max=%s",
            len(temperatures),
            min(temperatures),
            max(temperatures),
        )
    else:
        logger.info("Summary: no temperatures were read.")

    return temperatures


if __name__ == "__main__":
    setup_logging()
    monitor_sensor()
