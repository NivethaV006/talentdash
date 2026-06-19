import json
from pathlib import Path

from db import get_connection
from company_repository import get_or_create_company
from deduplicator import is_duplicate


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def write_log(filename, data):

    with open(
        LOG_DIR / filename,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(
                data,
                ensure_ascii=False
            )
            + "\n"
        )


def store_record(record):

    company_id = get_or_create_company(

        record["company"],

        record["company_slug"]

    )

    duplicate = is_duplicate(

        company_id,

        record["role"],

        record["level_standardized"],

        record["location"],

        record["base_salary"]

    )

    if duplicate:

        write_log(

            "duplicates.jsonl",

            record

        )

        return "DUPLICATE"

    total_compensation = (

        record["base_salary"]

        + record["bonus"]

        + record["stock"]

    )

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """
        INSERT INTO salary_records(

        company_id,

        role,

        level_standardized,

        location,

        currency,

        experience_years,

        base_salary,

        bonus,

        stock,

        total_compensation,

        source,

        confidence_score

        )

        VALUES(

        %s,%s,%s,%s,%s,%s,

        %s,%s,%s,%s,%s,%s

        )

        """,

        (

            company_id,

            record["role"],

            record["level_standardized"],

            record["location"],

            record["currency"],

            record["experience_years"],

            record["base_salary"],

            record["bonus"],

            record["stock"],

            total_compensation,

            record["source"],

            record["confidence_score"]

        )

    )

    conn.commit()

    cur.close()

    conn.close()

    write_log(

        "inserted_records.jsonl",

        record

    )

    return "INSERTED"