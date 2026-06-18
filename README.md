# TalentDash – AI/Data Engineering Pipeline

## Overview

TalentDash is an AI-powered salary data pipeline that extracts salary information from public sources, normalizes it using Gemini LLM, validates records, removes duplicates, and prepares structured data for storage.

Current Progress:

* ✅ Playwright-based salary scraper
* ✅ User-Agent rotation
* ✅ Rate limiting
* ✅ Retry mechanism
* ✅ Per-record exception handling
* ✅ Raw JSON generation
* ✅ Gemini LLM normalization
* ✅ Batch processing (10 records/batch)
* ✅ Prompt & response logging

Upcoming Modules:

* Pydantic Validation
* Company Name Normalization
* Level Mapping
* Deduplication
* Storage Layer
* Quality Report

---

## Project Structure

```text
scraper/
    output/
        raw_records.json

llm/
    output/
        normalized_records.json

    logs/

config.py
prompt.py
client.py
pipeline.py
```

---

## Pipeline

```text
Scraper
    ↓
Raw Records
    ↓
Gemini LLM
    ↓
Normalized Records
    ↓
Pydantic Validation
    ↓
Company Normalization
    ↓
Level Mapping
    ↓
Deduplication
    ↓
Storage
```

---

## How to Run

### Clone

```bash
git clone https://github.com/NivethaV006/talentdash.git
cd talentdash
```

### Install

```bash
pip install -r requirements.txt
```

### Configure

Create a `.env`

```env
GEMINI_API_KEY=YOUR_API_KEY
MODEL_NAME=gemini-2.5-flash
BATCH_SIZE=10
TEMPERATURE=0
```

### Run Scraper

```bash
cd scraper
python scraper.py
```

### Run LLM Pipeline

```bash
cd ../llm
python pipeline.py
```

---

# Design Decisions

### Modular Scraper

The scraper is responsible only for collecting raw salary data. Database interaction and duplicate detection are handled in later pipeline stages, keeping the scraper lightweight and independent.

### Location Handling

AmbitionBox displays aggregated salary data on the listing page, while location-specific salaries require additional interaction and authentication. To maintain scraper reliability and avoid unnecessary anti-bot triggers, the pipeline stores the default aggregated location as **India** while preserving company URLs for future location enrichment.

### Data Scope

Salary extraction is limited to the **Engineering – Software & QA** category before collecting Software Engineer and Data Analyst records. This avoids mixing similarly named roles from unrelated domains and improves dataset consistency.

---

## Current Output

* Raw salary records
* Normalized JSON records
* Prompt log
* LLM response log

---

## Future Improvements

* Pydantic validation
* Company alias mapping
* Rule-based level mapping
* Deduplication
* PostgreSQL integration
* API ingestion
* Automated quality report


### Design Decision 1 – Modular Scraper

The scraper focuses only on extracting raw salary data. Deduplication and database interaction are handled as separate pipeline stages to keep the scraper independent, maintainable, and resilient.

### Design Decision 2 – Location Handling

Location-specific salaries on AmbitionBox require additional interaction that is not consistently accessible through automation. Therefore, the scraper stores the aggregated salary location as **India** while preserving company URLs for future location enrichment.

### Design Decision 3 – Department Selection

Salary records are collected only from the **Engineering – Software & QA** category before filtering Software Engineer and Data Analyst roles. This prevents unrelated job categories from entering the dataset and improves normalization quality.
