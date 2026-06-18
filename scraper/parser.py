from playwright.sync_api import Locator

from utils import log_error


def parse_salary_card(row: Locator):

    try:

        company_link = row.locator("a").first.get_attribute("href")

        if company_link:
            company_link = "https://www.ambitionbox.com" + company_link

        return {

            "raw_company":
            row.locator(
                '[data-testid="salary_comparison_widget-company-name"]'
            ).inner_text().strip(),

            "raw_role":
            row.locator(
                '[data-testid="salary_comparison_widget-company-designation"]'
            ).inner_text().replace(" Salary", "").strip(),

            "raw_salary_text":
            row.locator(
                '[data-testid="salary_comparison_widget-salary-range"]'
            ).inner_text().strip(),

            # Default aggregated salary is treated as India-wide
            "raw_location": "India",

            "raw_experience":
            row.locator(
                '[data-testid="salary_comparison_widget-company-experience"]'
            ).inner_text().strip(),

            "company_url": company_link

        }

    except Exception as e:

        print(f"\nFAILED ROW\n{row.inner_html()}\n")
        print(e)

        log_error(str(e))

        return None