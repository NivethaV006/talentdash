import json
import re
from pathlib import Path

# ---------------------------------------
# Base Directory
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent

ALIAS_FILE = BASE_DIR / "aliases.json"

with open(ALIAS_FILE, "r", encoding="utf-8") as f:
    ALIASES = json.load(f)


LEGAL_SUFFIXES = [
    "private limited",
    "pvt ltd",
    "pvt. ltd.",
    "pvt",
    "limited",
    "ltd",
    "inc",
    "llc",
    ".com"
]


def slugify(text):

    return (
        text.lower()
        .replace("&", "and")
        .replace(" ", "-")
    )


def normalize_company(name):

    original = name

    company = name.lower().strip()

    company = company.replace("&", "and")

    company = re.sub(r"[.,]", "", company)

    company = re.sub(r"\s+", " ", company)

    for suffix in LEGAL_SUFFIXES:

        pattern = r"\b" + re.escape(suffix) + r"\b"

        company = re.sub(pattern, "", company)

    company = re.sub(r"\s+", " ", company).strip()

    company = ALIASES.get(
        company,
        company
    )

    return {
        "original": original,
        "normalized": company,
        "slug": slugify(company)
    }