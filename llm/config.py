from pathlib import Path
import os

from dotenv import load_dotenv

# ---------------------------------------
# Load Environment Variables
# ---------------------------------------

load_dotenv()

# ---------------------------------------
# Input / Output Files
# ---------------------------------------

RAW_INPUT_FILE = Path("../scraper/output/raw_records.json")

OUTPUT_FILE = Path("output/normalized_records.json")

# ---------------------------------------
# Logging
# ---------------------------------------

LOG_DIR = Path("logs")

PROMPT_LOG = LOG_DIR / "first_prompt.txt"

RESPONSE_LOG = LOG_DIR / "first_response.txt"

MALFORMED_LOG = LOG_DIR / "malformed_records.jsonl"

# ---------------------------------------
# Output Directories
# ---------------------------------------

OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ---------------------------------------
# Gemini Configuration
# ---------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Please configure it in the .env file."
    )

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-2.5-flash"
)

TEMPERATURE = float(
    os.getenv(
        "TEMPERATURE",
        "0"
    )
)

BATCH_SIZE = int(
    os.getenv(
        "BATCH_SIZE",
        "10"
    )
)

# ---------------------------------------
# Retry Configuration
# ---------------------------------------

MAX_RETRIES = 3

RETRY_DELAY = 3

# ---------------------------------------
# Pipeline Metadata
# ---------------------------------------

PIPELINE_NAME = "TalentDash Salary Normalization"

PIPELINE_VERSION = "1.0.0"