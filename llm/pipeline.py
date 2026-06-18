import json
import asyncio

from config import (
    RAW_INPUT_FILE,
    OUTPUT_FILE,
    BATCH_SIZE
)

from batch_processor import BatchProcessor


def load_raw_records():

    with open(
        RAW_INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_normalized_records(records):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )


async def main():

    print("\n========================================")
    print(" TalentDash - LLM Normalization Pipeline ")
    print("========================================\n")

    from utils import (
    load_json,
    save_json
    )

    raw_records = load_json(
        RAW_INPUT_FILE
    )

    total_input = len(raw_records)

    print(f"Input Records : {total_input}")

    processor = BatchProcessor()

    normalized_records = await processor.process(
        raw_records
    )

    save_json(
    normalized_records,
    OUTPUT_FILE
    )

    total_batches = (
        total_input + BATCH_SIZE - 1
    ) // BATCH_SIZE

    print("\n============= SUMMARY =============")

    print(
        f"Input Records          : {total_input}"
    )

    print(
        f"Batch Size             : {BATCH_SIZE}"
    )

    print(
        f"Total Batches          : {total_batches}"
    )

    print(
        f"Normalized Records     : {len(normalized_records)}"
    )

    print(
        f"Malformed Records      : {processor.malformed_count}"
    )

    print(
        f"Output File            : {OUTPUT_FILE}"
    )

    print("===================================\n")


if __name__ == "__main__":

    asyncio.run(
        main()
    )