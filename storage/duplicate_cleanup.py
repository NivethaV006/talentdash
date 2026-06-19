from db import get_connection


def deduplicate_existing_records():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

    SELECT
        id,
        company_id,
        role,
        level_standardized,
        location,
        base_salary,
        submitted_at

    FROM salary_records

    ORDER BY

        company_id,
        role,
        level_standardized,
        location,
        submitted_at DESC

    """)

    rows = cur.fetchall()

    latest = {}

    duplicates = 0

    for row in rows:

        record_id = row[0]
        company_id = row[1]
        role = row[2]
        level = row[3]
        location = row[4]
        salary = row[5]

        key = (
            company_id,
            role,
            level,
            location
        )

        if key not in latest:

            latest[key] = (record_id, salary)

            continue

        latest_salary = latest[key][1]

        difference = abs(salary - latest_salary) / latest_salary

        if difference <= 0.05:

            cur.execute(

                """
                UPDATE salary_records
                SET is_verified = FALSE
                WHERE id=%s
                """,

                (record_id,)

            )

            duplicates += 1

    conn.commit()

    cur.close()
    conn.close()

    return duplicates