# TalentDash – AI Salary Data Engineering Pipeline

## Overview

TalentDash is an end-to-end AI-powered salary data engineering pipeline that collects salary information from AmbitionBox, normalizes raw data using Google's Gemini LLM, validates every record with Pydantic, standardizes company names and job levels, detects duplicate records, stores clean data in a Neon PostgreSQL database, and visualizes processed information through a Flask dashboard.

The project demonstrates a complete ETL workflow suitable for modern AI Data Engineering applications.

---

# Live Deployment

**GitHub Repository**

https://github.com/NivethaV006/talentdash

**Live Dashboard (Render)**

https://talentdash-nwck.onrender.com/

---

# Important Note

## Why only 20 salary records?

The project intentionally processes **20 salary records** for demonstration purposes.

**Reason 1:** AmbitionBox uses pagination and anti-bot protection, making unrestricted automated scraping impractical for repeated execution.

**Reason 2:** Twenty records are sufficient to demonstrate every stage of the pipeline (scraping, normalization, validation, storage, deduplication, and reporting) while keeping Gemini API usage low and pipeline execution fast.

The architecture is fully scalable and can process much larger datasets by increasing the scraper configuration.

---

# Architecture

```
                   AmbitionBox
                        │
                        ▼
               Playwright Scraper
                        │
                        ▼
              Raw JSON Salary Records
                        │
                        ▼
         Gemini LLM Data Normalization
                        │
                        ▼
           Pydantic Schema Validation
                        │
                        ▼
        Company Name Normalization
                        │
                        ▼
      Standardized Level Mapping
                        │
                        ▼
        Duplicate Detection (48 hrs)
                        │
                        ▼
         Neon PostgreSQL Database
                        │
                        ▼
              Flask Dashboard
```

---

# Technologies Used

* Python
* Playwright
* BeautifulSoup
* Google Gemini API
* Pydantic
* PostgreSQL (Neon)
* Flask
* Bootstrap
* Git & GitHub
* Render

---

# Project Structure

```
talentdash/

│
├── scraper/
├── llm/
├── validation/
├── company_normalization/
├── level_mapping/
├── storage/
├── dashboard/
│
├── requirements.txt
├── .env.example
├── render.yaml
├── README.md
```

---

# Pipeline Stages

## A1 – Salary Scraper

* Scrapes salary information from AmbitionBox
* Extracts company, role, salary, experience and location
* Stores raw records as JSON

---

## A2 – LLM Normalization

Google Gemini converts raw salary information into a standardized JSON schema.

Normalized fields include:

* Company
* Role
* Location
* Currency
* Experience
* Salary
* Bonus
* Stock

---

## A3 – Pydantic Validation

Each normalized record is validated using Pydantic.

* Rejects malformed records
* Logs validation failures
* Allows only valid records into the pipeline

---

## A4 – Company Normalization

Maps multiple company aliases into one standardized company.

Example

```
Google India
GOOGLE
google

↓

company_slug = google
```

---

## A5 – Level Mapping

Maps job titles and years of experience into standardized engineering levels using rule-based logic with Gemini fallback.

Example

```
Software Engineer

↓

SDE-I

↓

SDE-II

↓

Senior SDE
```

---

## A6 – Storage & Quality Report

Stores validated records into Neon PostgreSQL.

Automatically generates:

* Total records scraped
* Records normalized
* Records validated
* Rejected records
* Successfully stored records
* Null rate per field

---

## A7 – Duplicate Detection

Before insertion, the pipeline checks:

* Company
* Role
* Level
* Location
* Salary

Records submitted within **48 hours** having salary differences within **10%** are treated as duplicates and skipped.

---

# Database Schema

## companies

* company_id
* company_name
* company_slug

## salary_records

* id
* company_id
* role
* level_standardized
* location
* currency
* experience_years
* base_salary
* bonus
* stock
* total_compensation
* source
* confidence_score
* submitted_at
* is_verified

---

# Environment Variables

Create a `.env` file in the project root.

```
DATABASE_URL=your_neon_database_url
GEMINI_API_KEY=your_gemini_api_key
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/NivethaV006/talentdash.git

cd talentdash
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Playwright browser (required only for running the scraper locally)

```bash
python -m playwright install chromium
```

---

# Database Setup

Create the database tables

```bash
python storage/create_table.py
```

---

# Running the Pipeline

Execute the pipeline modules in order:

```bash
python scraper/scraper.py

python llm/pipeline.py

python validation/validate_pipeline.py

python company_normalization/normalize_pipeline.py

python level_mapping/mapping_pipeline.py

python storage/store_pipeline.py

python storage/cleanup_pipeline.py
```

---

# Running the Dashboard

Local

```bash
cd dashboard

python app.py
```

Open

```
http://localhost:5000
```

Production

```
https://YOUR-RENDER-URL.onrender.com
```

---

# Sample Raw Record

```
Company : Tech Mahindra

Role : Software Engineer

Experience : 3.5 Years

Salary : ₹5.15 LPA

Location : India
```

---

# Sample Normalized Record

```json
{
    "company": "tech mahindra",
    "company_slug": "tech-mahindra",
    "role": "Software Engineer",
    "level_standardized": "SDE-II",
    "location": "India",
    "currency": "INR",
    "experience_years": 3.5,
    "base_salary": 515000,
    "bonus": 0,
    "stock": 0
}
```

---

# Sample Rejected Records

### Example 1

```json
{
    "company": "Google"
}
```

Reason

```
Missing required field: role
```

---

### Example 2

```json
{
    "salary": "abc"
}
```

Reason

```
base_salary must be an integer
```

---

# Sample Quality Report

```
Total Records Scraped          : 20
Passed LLM Normalization       : 20
Passed Pydantic Validation     : 20
Rejected Records               : 0
Stored Successfully            : 20
Duplicate Records              : 1

Null Rate Per Field

company                 0.00%
company_slug            0.00%
role                    0.00%
level_standardized      0.00%
location                0.00%
currency                0.00%
experience_years        0.00%
base_salary             0.00%
bonus                   0.00%
stock                   0.00%
```

---

# Challenges Faced

* Designing a modular ETL pipeline where every stage consumes and produces standardized JSON.
* Maintaining consistent data flow across scraping, LLM normalization, validation, storage, and reporting.
* Handling company alias normalization and duplicate salary detection while preserving data quality.

---

# Hardest Decision

The most important design decision was using **rule-based level mapping with Gemini LLM as a fallback** instead of using the LLM for every record.

This approach reduced API cost, improved execution speed, and produced deterministic results for common engineering roles while still handling ambiguous cases intelligently.

---

# Future Improvements

* Automate scraping using scheduled jobs.
* Dockerize the complete application.
* Support additional salary data sources.
* Improve company alias matching using semantic similarity.
* Add historical salary trend analysis.

---

# Author

**Nivetha V**

AI Data Engineering Internship Project
