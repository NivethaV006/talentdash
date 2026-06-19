from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Drop old tables if they exist
cur.execute("""
DROP TABLE IF EXISTS salary_records;
DROP TABLE IF EXISTS companies;
""")

# Companies table
cur.execute("""
CREATE TABLE companies (

    company_id SERIAL PRIMARY KEY,

    company_name TEXT UNIQUE NOT NULL,

    company_slug TEXT UNIQUE NOT NULL

);
""")

# Salary records table
cur.execute("""
CREATE TABLE salary_records (

    id SERIAL PRIMARY KEY,

    company_id INTEGER NOT NULL,

    role TEXT NOT NULL,

    level_standardized TEXT NOT NULL,

    location TEXT NOT NULL,

    currency TEXT NOT NULL,

    experience_years REAL NOT NULL,

    base_salary BIGINT NOT NULL,

    bonus BIGINT DEFAULT 0,

    stock BIGINT DEFAULT 0,

    total_compensation BIGINT NOT NULL,

    source TEXT NOT NULL,

    confidence_score REAL NOT NULL,

    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    is_verified BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_company
        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
        ON DELETE CASCADE

);
""")

conn.commit()

cur.close()
conn.close()

print("=" * 45)
print("TalentDash Database Initialized")
print("=" * 45)
print("✓ companies table created")
print("✓ salary_records table created")