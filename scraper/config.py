BASE_URL = "https://www.ambitionbox.com/salaries"

TARGET_ROLES = [
    "Software Engineer",
    "Data Analyst"
]

MIN_DELAY = 1.5
MAX_DELAY = 4.0

MAX_RECORDS = 60

HEADLESS = False

NAVIGATION_TIMEOUT = 60000

MAX_RETRIES = 3

OUTPUT_FILE = "output/raw_records.json"

LOG_FILE = "logs/scraper.log"