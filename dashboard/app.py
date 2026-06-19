from flask import Flask, render_template, redirect
import psycopg2
from dotenv import load_dotenv
import os
import subprocess
import sys

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def conn():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def home():

    con = conn()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM companies")
    companies = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM salary_records")
    salaries = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT role) FROM salary_records")
    roles = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM salary_records
        WHERE is_verified = FALSE
    """)
    duplicates = cur.fetchone()[0]

    cur.close()
    con.close()

    return render_template(
        "index.html",
        companies=companies,
        salaries=salaries,
        roles=roles,
        duplicates=duplicates
    )



@app.route("/companies")
def companies():

    con = conn()
    cur = con.cursor()

    cur.execute("""
        SELECT
            company_id,
            company_name,
            company_slug
        FROM companies
        ORDER BY company_name
    """)

    rows = cur.fetchall()

    cur.close()
    con.close()

    return render_template(
        "companies.html",
        companies=rows
    )

@app.route("/salaries")
def salaries():

    con = conn()
    cur = con.cursor()

    cur.execute("""
        SELECT

            c.company_name,
            s.role,
            s.level_standardized,
            s.location,
            s.base_salary,
            s.total_compensation

        FROM salary_records s

        JOIN companies c
        ON c.company_id = s.company_id

        ORDER BY s.base_salary DESC
    """)

    rows = cur.fetchall()

    cur.close()
    con.close()

    return render_template(
        "salaries.html",
        rows=rows
    )

@app.route("/report")
def report():

    con = conn()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM salary_records")
    stored = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM salary_records
        WHERE is_verified = FALSE
    """)
    duplicates = cur.fetchone()[0]

    cur.close()
    con.close()

    return render_template(
        "report.html",
        stored=stored,
        duplicates=duplicates
    )


if __name__ == "__main__":
    app.run(debug=True)