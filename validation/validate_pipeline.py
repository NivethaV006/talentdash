import json
from pathlib import Path

from validator import (
    validate_all_records,
    save_rejections
)

# ---------------------------------------
# Base Directory
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------
# Files
# ---------------------------------------

INPUT_FILE = BASE_DIR / "llm" / "output" / "normalized_records.json"

VALIDATED_OUTPUT = BASE_DIR / "validation" / "output" / "validated_records.json"

REJECTION_OUTPUT = BASE_DIR / "validation" / "logs" / "rejections.jsonl"


def load_records():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_validated(records):

    VALIDATED_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        VALIDATED_OUTPUT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():

    print()

    print("=" * 40)

    print(" TalentDash - Pydantic Validation ")

    print("=" * 40)

    records = load_records()

    print()

    print(
        f"Input Records : {len(records)}"
    )

    validated_records, rejected_records = validate_all_records(
        records
    )

    save_validated(
        validated_records
    )

    save_rejections(
        rejected_records,
        REJECTION_OUTPUT
    )

    print()

    print("========== VALIDATION SUMMARY ==========")

    print(
        f"Input Records        : {len(records)}"
    )

    print(
        f"Validated Records    : {len(validated_records)}"
    )

    print(
        f"Rejected Records     : {len(rejected_records)}"
    )

    print(
        f"Validated File       : {VALIDATED_OUTPUT}"
    )

    print(
        f"Rejection Log        : {REJECTION_OUTPUT}"
    )

    print("=" * 40)


if __name__ == "__main__":

    main()