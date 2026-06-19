from db import get_connection


def is_duplicate(
    company_id,
    role,
    level,
    location,
    base_salary
):

    conn = get_connection()
    cur = conn.cursor()

    lower = int(base_salary * 0.90)
    upper = int(base_salary * 1.10)

    cur.execute(
        """
        SELECT id
        FROM salary_records

        WHERE company_id=%s
        AND role=%s
        AND level_standardized=%s
        AND location=%s

        AND base_salary BETWEEN %s AND %s

        AND submitted_at >= NOW() - INTERVAL '48 HOURS'
        """,
        (
            company_id,
            role,
            level,
            location,
            lower,
            upper
        )
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row is not None