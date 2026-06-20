import json
from pathlib import Path

from storage import store_record
from quality_report import generate_quality_report

# ---------------------------------------
# Base Directory
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------
# Files
# ---------------------------------------

INPUT_FILE = BASE_DIR / "level_mapping" / "output" / "mapped_records.json"


def load():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def calculate_null_rate(records):

    result = {}

    total = len(records)

    for key in records[0]:

        nulls = sum(
            1
            for r in records
            if r.get(key) is None
        )

        result[key] = (nulls / total) * 100

    return result


def main():

    print()

    print("=" * 45)
    print("TalentDash Storage Pipeline")
    print("=" * 45)

    records = load()

    stats = {

        "total": len(records),

        "llm": len(records),

        "validation": len(records),

        "stored": 0,

        "duplicates": 0,

        "failed": 0,

        "null_rate": calculate_null_rate(records)

    }

    for record in records:

        try:

            status = store_record(record)

            if status == "INSERTED":

                stats["stored"] += 1

            elif status == "DUPLICATE":

                stats["duplicates"] += 1

        except Exception as e:

            print(e)

            stats["failed"] += 1

    generate_quality_report(stats)


if __name__ == "__main__":

    main()