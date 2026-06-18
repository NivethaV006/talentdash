import json

from client import GeminiClient

from config import (
    BATCH_SIZE,
    MALFORMED_LOG
)


class BatchProcessor:

    def __init__(self):

        self.client = GeminiClient()

        self.batch_size = BATCH_SIZE

        self.malformed_count = 0


    def create_batches(self, records):

        for i in range(
            0,
            len(records),
            self.batch_size
        ):

            yield records[
                i:i+self.batch_size
            ]


    async def process(self, records):

        normalized_records = []

        batches = list(
            self.create_batches(records)
        )

        total_batches = len(batches)

        print(f"\nTotal Batches : {total_batches}")

        for batch_no, batch in enumerate(
            batches,
            start=1
        ):

            print(
                f"\nProcessing Batch {batch_no}/{total_batches}"
            )

            try:

                response = await self.client.normalize_batch(
                    batch
                )

                if response is None:
                    continue

                if not isinstance(
                    response,
                    list
                ):

                    print(
                        f"Batch {batch_no} returned invalid JSON."
                    )

                    continue

                for index, record in enumerate(response):

                    if isinstance(record, dict):

                        normalized_records.append(
                            record
                        )

                    else:

                        self.log_malformed_record(
                            batch_no,
                            index,
                            record
                        )

            except Exception as e:

                print(
                    f"Batch {batch_no} Failed : {e}"
                )

        return normalized_records


    def log_malformed_record(
        self,
        batch_no,
        index,
        record
    ):

        self.malformed_count += 1

        malformed = {

            "batch": batch_no,

            "record_index": index,

            "record": record

        }

        with open(
            MALFORMED_LOG,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(

                json.dumps(
                    malformed,
                    ensure_ascii=False
                )

                + "\n"

            )

        print(
            f"Malformed Record Logged (Batch {batch_no})"
        )