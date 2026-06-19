import json
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_quality_report(stats):

    total = stats["total"]

    report = {

        "total_records_scraped":
            total,

        "records_passed_llm":
            stats["llm"],

        "records_passed_validation":
            stats["validation"],

        "records_rejected":
        {
            "duplicates":
                stats["duplicates"],

            "failed_insertions":
                stats["failed"]
        },

        "records_stored_successfully":
            stats["stored"],

        "null_rate_per_field":
            stats["null_rate"]
    }

    with open(

        OUTPUT_DIR / "quality_report.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            report,

            f,

            indent=4

        )

    print()

    print("=" * 45)
    print("QUALITY REPORT")
    print("=" * 45)

    print(f"Total Records Scraped      : {total}")
    print(f"Passed LLM                : {stats['llm']}")
    print(f"Passed Validation         : {stats['validation']}")
    print(f"Stored Successfully       : {stats['stored']}")
    print(f"Duplicates Skipped        : {stats['duplicates']}")
    print(f"Failed Insertions         : {stats['failed']}")

    print()

    print("Null Rate")

    for k, v in stats["null_rate"].items():

        print(f"{k:25} {v:.2f}%")