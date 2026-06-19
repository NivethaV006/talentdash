# TalentDash – AI Salary Data Engineering Pipeline

## Overview

TalentDash is an AI-powered salary data engineering pipeline that collects raw salary information, normalizes it using Google's Gemini LLM, validates every record using Pydantic, standardizes company names and job levels, detects duplicate entries, and stores clean salary data into a Neon PostgreSQL database. A Flask dashboard is provided to visualize the processed data and quality metrics.

---

# Important Note

### Why only 20 salary records?

The project intentionally processes **20 salary records** for demonstration purposes.

**Reason 1:** The objective of this assessment is to demonstrate the complete end-to-end data engineering pipeline (scraping → LLM normalization → validation → storage → deduplication) rather than building a large dataset.

**Reason 2:** A smaller dataset keeps the pipeline reproducible, reduces unnecessary Gemini API usage, and allows every stage of the pipeline to be easily verified during evaluation.

The pipeline is scalable and can process a much larger dataset by increasing the scraper configuration.

---

# Architecture

```
Raw Salary Data
        │
        ▼
Web Scraper
        │
        ▼
Gemini LLM Normalization
        │
        ▼
Pydantic Validation
        │
        ▼
Company Normalization
        │
        ▼
Level Mapping
        │
        ▼
Neon PostgreSQL Storage
        │
        ▼
Duplicate Detection
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

---

# Project Structure

```
talentdash/

├── scraper/
├── llm/
├── validation/
├── company_normalization/
├── level_mapping/
├── storage/
├── dashboard/

├── requirements.txt
├── .env.example
├── README.md
```

---

# Pipeline Stages

## A1 – Salary Scraper

* Scrapes salary information from AmbitionBox.
* Extracts company, role, salary, experience, and location.
* Stores raw records in JSON format.

---

## A2 – LLM Normalization

Uses Gemini to convert raw scraped information into a standardized JSON schema.

Normalized fields include:

* Company
* Role
* Salary
* Experience
* Currency
* Location

---

## A3 – Pydantic Validation

Every normalized record is validated against a predefined schema.

* Invalid records are rejected.
* Rejection reasons are logged.
* Valid records proceed to the next stage.

---

## A4 – Company Normalization

Maps company aliases to a single standardized company.

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

Maps job titles and experience into standardized levels using rule-based logic with Gemini LLM fallback for ambiguous cases.

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

Validated records are stored in Neon PostgreSQL.

The pipeline generates a quality report containing:

* Total records scraped
* Records passed LLM normalization
* Records passed validation
* Records rejected
* Records stored successfully
* Null rate per field

---

## A7 – Deduplication

Before inserting a salary record:

* Checks company
* Role
* Level
* Location
* Salary

Records submitted within **48 hours** having salary differences within **10%** are skipped.

A cleanup utility is also provided to identify duplicate records already stored in the database.

---

# Database

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

Create a `.env` file.

```
DATABASE_URL=your_neon_database_url
GEMINI_API_KEY=your_gemini_api_key
```

---

# Installation

Clone the repository

```
git clone https://github.com/NivethaV006/talentdash.git
```

Install dependencies

```
pip install -r requirements.txt
```

Install Playwright browser

```
playwright install
```

---

# Database Setup

Create database tables

```
python storage/create_table.py
```

---

# Running the Pipeline

Run the following modules in order:

```
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

```
cd dashboard

python app.py
```

Open

```
http://localhost:5000
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

```
{
  "company":"Google"
}
```

Reason

```
Missing required field: role
```

### Example 2

```
{
  "salary":"abc"
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

The most challenging part of the project was integrating multiple independent pipeline stages while maintaining consistent data flow across scraping, normalization, validation, storage, and deduplication. Careful coordination was required to ensure that each stage consumed and produced data in a compatible format.

---

# Hardest Decision

The hardest design decision was implementing **rule-based level mapping with Gemini LLM as a fallback** instead of using the LLM for every record.

This approach reduced API usage, improved execution speed, and ensured deterministic results for common job titles while still allowing ambiguous cases to be classified intelligently.

---

# Deployment Status

The application was successfully tested locally with Neon PostgreSQL and the Flask dashboard.

Deployment to Render was initiated, but package import restructuring is still required for production deployment. The complete pipeline, dashboard, and database integration function correctly in the local development environment.

---

# Future Improvements

* Schedule automatic scraping using cron jobs.
* Containerize the application using Docker.
* Expand support to additional salary sources.
* Improve company alias matching using semantic similarity.
* Deploy the complete application to a production cloud environment.

---

# Author

**Nivetha V**


TalentDash – AI Data Engineering Internship Project
