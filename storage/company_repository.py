from db import get_connection


def get_or_create_company(company_name, company_slug):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT company_id
        FROM companies
        WHERE company_slug=%s
        """,
        (company_slug,)
    )

    row = cur.fetchone()

    if row:

        company_id = row[0]

    else:

        cur.execute(
            """
            INSERT INTO companies(company_name, company_slug)
            VALUES(%s,%s)
            RETURNING company_id
            """,
            (
                company_name,
                company_slug
            )
        )

        company_id = cur.fetchone()[0]

        conn.commit()

    cur.close()
    conn.close()

    return company_id