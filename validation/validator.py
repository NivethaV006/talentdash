import json

from pydantic import ValidationError

from schema import SalaryRecord


def validate_record(record):
    """
    Validate a single record.
    """

    try:

        validated = SalaryRecord(**record)

        return validated.model_dump(), None

    except ValidationError as e:

        return None, e.errors()


def validate_all_records(records):

    validated_records = []

    rejected_records = []

    for record in records:

        validated, error = validate_record(record)

        if validated:

            validated_records.append(validated)

        else:

            rejected_records.append(
                {
                    "record": record,
                    "error": error
                }
            )

    return validated_records, rejected_records


def save_rejections(rejected_records, output_file):

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        for record in rejected_records:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
            )

            file.write("\n")