from playwright.sync_api import sync_playwright

from config import (
    BASE_URL,
    TARGET_ROLES,
    HEADLESS,
    OUTPUT_FILE
)

from parser import parse_salary_card
from user_agents import get_random_user_agent
from utils import (
    random_delay,
    log_error,
    log_info,
    save_json
)


def launch_browser():

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=HEADLESS
    )

    context = browser.new_context(
        user_agent=get_random_user_agent(),
        viewport={
            "width": 1400,
            "height": 900
        }
    )

    page = context.new_page()

    return playwright, browser, page


from playwright.sync_api import Error

def open_salary_page(page):

    for attempt in range(3):

        try:

            log_info(f"Opening AmbitionBox (Attempt {attempt+1})")

            page.goto(
                BASE_URL,
                wait_until="domcontentloaded",
                timeout=90000
            )

            page.wait_for_timeout(3000)

            random_delay()

            return

        except Error as e:

            print(f"Retry {attempt+1}: {e}")

            if attempt == 2:
                raise

            page.wait_for_timeout(5000)


def close_popup(page):

    try:

        page.locator(
            '[aria-label="Close"]'
        ).click(timeout=2000)

        page.wait_for_timeout(500)

        log_info("Popup Closed")

    except:

        pass


def select_role(page, role):

    log_info(f"Selecting {role}")

    close_popup(page)

    try:
        page.locator(
            f'button[aria-label="{role}"]'
        ).click()

    except:
        page.get_by_role(
            "button",
            name=role
        ).click()

    # Wait until salary rows are visible
    page.wait_for_selector(
        'tbody tr:has([data-testid="salary_comparison_widget-company-name"])',
        timeout=10000
    )

    random_delay()


def extract_current_page(page):

    records = []

    rows = page.locator(
        'tbody tr:has([data-testid="salary_comparison_widget-company-name"])'
    )

    total = rows.count()

    print(f"\nActual Salary Rows : {total}")

    for i in range(total):

        try:

            row = rows.nth(i)

            record = parse_salary_card(row)

            if record:

                records.append(record)

                log_info(
    f"{record['raw_company']} | {record['raw_role']}"
            )

        except Exception as e:

            log_error(f"Row {i}: {e}")

    return records


def scrape_role(page, role):
    """
    Scrape one role from salary listing.
    """

    select_role(page, role)

    records = extract_current_page(page)

    print(f"\n{role} -> {len(records)} records collected.")

    return records





def scrape_all_roles():

    playwright, browser, page = launch_browser()

    try:

        open_salary_page(page)

        all_records = []

        for role in TARGET_ROLES:

            print("\n==============================")
            print(f"Scraping : {role}")
            print("==============================")

            records = scrape_role(page, role)

            all_records.extend(records)

            # Save progress after every role
            save_json(
                all_records,
                OUTPUT_FILE
            )

            print(f"\n{role} -> {len(records)} records collected.")

        # Count unique companies
        companies = {
            r["raw_company"]
            for r in all_records
        }

        print("\n====================================")
        print(f"Software Roles Scraped : {len(TARGET_ROLES)}")
        print(f"Unique Companies       : {len(companies)}")
        print(f"Total Records          : {len(all_records)}")
        print(f"Saved To               : {OUTPUT_FILE}")
        print("====================================")

        log_info(f"Unique Companies : {len(companies)}")
        log_info(f"Total Records : {len(all_records)}")

        # Final save
        save_json(
            all_records,
            OUTPUT_FILE
        )

    finally:

        browser.close()

        playwright.stop()

if __name__ == "__main__":

    scrape_all_roles()