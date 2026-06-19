import json
from pathlib import Path

from normalizer import normalize_company


INPUT_FILE = "../validation/output/validated_records.json"

OUTPUT_FILE = "output/normalized_companies.json"

LOG_FILE = "logs/normalization_log.json"


def load():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save(records):

    Path("output").mkdir(
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

    Path("logs").mkdir(
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

    print("TalentDash Company Normalization")

    print("=" * 45)

    records = load()

    logs = []

    for record in records:

        result = normalize_company(
            record["company"]
        )

        logs.append(result)

        record["company"] = result["normalized"]

        record["company_slug"] = result["slug"]

    save(records)

    save_log(logs)

    print()

    print(
        f"Input Records : {len(records)}"
    )

    print(
        f"Output File   : {OUTPUT_FILE}"
    )

    print(
        f"Log File      : {LOG_FILE}"
    )

    print()

    print("Normalization Completed Successfully.")


if __name__ == "__main__":

    main()