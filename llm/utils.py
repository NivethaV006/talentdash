import json
from pathlib import Path
from datetime import datetime


def load_json(file_path):
    """
    Load JSON file.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(records, file_path):
    """
    Save JSON file.
    """

    Path(file_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )


def append_jsonl(record, file_path):
    """
    Append one JSON object per line.
    """

    Path(file_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(
            json.dumps(
                record,
                ensure_ascii=False
            )
            + "\n"
        )


def log(message):
    """
    Print timestamped log.
    """

    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
    )


def create_batches(records, batch_size):
    """
    Yield batches.
    """

    for i in range(
        0,
        len(records),
        batch_size
    ):

        yield records[
            i:i + batch_size
        ]


def validate_batch_response(response):
    """
    Ensure Gemini returned a list of dictionaries.
    """

    if not isinstance(response, list):
        return False

    for record in response:

        if not isinstance(record, dict):
            return False

    return True