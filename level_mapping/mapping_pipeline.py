import json
from pathlib import Path

from level_mapper import map_level

# ---------------------------------------
# Base Directory
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------
# Files
# ---------------------------------------

INPUT_FILE = BASE_DIR / "company_normalization" / "output" / "normalized_companies.json"

OUTPUT_FILE = BASE_DIR / "level_mapping" / "output" / "mapped_records.json"

LOG_FILE = BASE_DIR / "level_mapping" / "logs" / "mapping_log.json"


def load():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save(records):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            records,
            f,
            indent=4,
            ensure_ascii=False
        )


def save_log(logs):

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            logs,
            f,
            indent=4,
            ensure_ascii=False
        )


def main():

    print()

    print("=" * 45)

    print("TalentDash Level Mapping")

    print("=" * 45)

    records = load()

    logs = []

    for record in records:

        result = map_level(
            record["role"],
            record["experience_years"]
        )

        record["level_standardized"] = result["level"]

        record["confidence_score"] = result["confidence"]

        logs.append({

            "role": record["role"],

            "experience": record["experience_years"],

            "mapped_level": result["level"],

            "confidence": result["confidence"],

            "method": result["method"]
        })

    save(records)

    save_log(logs)

    print()

    print(f"Input Records : {len(records)}")

    print(f"Mapped Records: {len(records)}")

    print(f"Output File   : {OUTPUT_FILE}")

    print(f"Log File      : {LOG_FILE}")

    print()

    print("Level Mapping Completed.")


if __name__ == "__main__":

    main()