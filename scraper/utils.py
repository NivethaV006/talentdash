import json
import logging
import random
import time
from pathlib import Path

from config import (
    LOG_FILE,
    MIN_DELAY,
    MAX_DELAY,
)


# Create directories
Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def random_delay():
    """
    Random sleep to mimic human behaviour.
    """
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    time.sleep(delay)


def log_info(message):
    """
    Log informational messages.
    """
    print(f"[INFO] {message}")
    logging.info(message)


def log_error(message):
    """
    Log error messages.
    """
    print(f"[ERROR] {message}")
    logging.error(message)


def save_json(records, output_file):
    """
    Save records as JSON.
    """

    output_path = Path(output_file)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            records,
            f,
            indent=4,
            ensure_ascii=False
        )

    log_info(
        f"Saved {len(records)} records to {output_path}"
    )


def load_json(file_path):
    """
    Load JSON file if it exists.
    """

    path = Path(file_path)

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def retry(func, retries=3):
    """
    Retry helper for unstable operations.
    """

    for attempt in range(retries):

        try:
            return func()

        except Exception as e:

            log_error(
                f"Retry {attempt + 1} failed : {e}"
            )

            if attempt == retries - 1:
                raise

            random_delay()