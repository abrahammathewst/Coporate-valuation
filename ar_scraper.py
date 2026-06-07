from pathlib import Path

import pandas as pd
import requests

from playwright.sync_api import sync_playwright


CSV_FILE = "./data/ind_company_list.csv"

OUTPUT_DIR = Path("./data/annual_report")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

failures = []


def clean_company_name(name: str):

    return (
        str(name)
        .upper()
        .replace(".", "")
        .replace("/", "_")
        .strip()
    )


def download_company_reports(
    page,
    isin: str,
    company_name: str
):

    try:

        page.goto(
            "https://www.bseindia.com/corporates/historicalannualreport"
        )

        page.wait_for_timeout(3000)

        search_box = page.locator(
            "main #scripsearchtxtbx"
        )

        search_box.fill(isin)

        page.wait_for_timeout(3000)

        try:

            page.get_by_text(
                isin
            ).first.click()

        except Exception:

            page.keyboard.press(
                "ArrowDown"
            )

            page.keyboard.press(
                "Enter"
            )

        page.wait_for_timeout(1000)

        page.get_by_role(
            "button",
            name="Submit"
        ).click()

        page.wait_for_selector(
            "table",
            timeout=15000
        )

        rows = page.locator(
            "table tbody tr"
        )

        print(
            f"\n{company_name}: "
            f"{rows.count()} reports found"
        )

        for i in range(rows.count()):

            try:

                report_row = rows.nth(i)

                year = (
                    report_row
                    .locator("td")
                    .nth(0)
                    .inner_text()
                    .strip()
                )

                filename = (
                    OUTPUT_DIR /
                    f"{company_name}_{year}_Annual_Report.pdf"
                )

                if filename.exists():

                    print(
                        f"SKIPPED: "
                        f"{filename.name}"
                    )

                    continue

                print(
                    f"{company_name} -> {year}"
                )

                pages_before = len(
                    page.context.pages
                )

                icon = report_row.locator(
                    "i[aria-label='Download pdf']"
                )

                icon.click(force=True)

                page.wait_for_timeout(
                    5000
                )

                pages_after = len(
                    page.context.pages
                )

                if pages_after <= pages_before:

                    print(
                        f"{company_name} {year}: "
                        f"No PDF page opened"
                    )

                    continue

                pdf_page = (
                    page.context.pages[-1]
                )

                pdf_url = pdf_page.url

                cookies = {
                    c["name"]: c["value"]
                    for c in page.context.cookies()
                }

                headers = {
                    "User-Agent":
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/120.0.0.0 "
                        "Safari/537.36",
                    "Referer":
                        "https://www.bseindia.com/"
                }

                response = requests.get(
                    pdf_url,
                    headers=headers,
                    cookies=cookies,
                    timeout=120
                )

                if response.status_code != 200:

                    print(
                        f"{company_name} {year}: "
                        f"HTTP {response.status_code}"
                    )

                    continue

                with open(
                    filename,
                    "wb"
                ) as f:

                    f.write(
                        response.content
                    )

                print(
                    f"DOWNLOADED: "
                    f"{filename.name}"
                )

                try:
                    pdf_page.close()
                except Exception:
                    pass

            except Exception as e:

                print(
                    f"FAILED: "
                    f"{company_name} {year}"
                )

                print(e)

    except Exception as e:

        failures.append(
            (
                company_name,
                str(e)
            )
        )

        print(
            f"FAILED COMPANY: "
            f"{company_name}"
        )

        print(e)


def main():

    df = pd.read_csv(
        CSV_FILE
    )

    # TEST MODE
    # df = df.head(3)

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        try:

            total = len(df)

            for idx, row in enumerate(
                df.iterrows(),
                start=1
            ):

                _, row = row

                isin = row["ISIN"]

                company_name = clean_company_name(
                    row["NAME"]
                )

                print(
                    "\n"
                    + "=" * 80
                )

                print(
                    f"[{idx}/{total}] "
                    f"{company_name}"
                )

                download_company_reports(
                    page=page,
                    isin=isin,
                    company_name=company_name
                )

        finally:

            browser.close()

    print(
        "\n"
        + "=" * 80
    )

    print(
        "DOWNLOAD COMPLETE"
    )

    print(
        "=" * 80
    )

    print(
        f"Failures: "
        f"{len(failures)}"
    )

    if failures:

        failure_df = pd.DataFrame(
            failures,
            columns=[
                "Company",
                "Reason"
            ]
        )

        failure_file = (
            OUTPUT_DIR /
            "download_failures.csv"
        )

        failure_df.to_csv(
            failure_file,
            index=False
        )

        print(
            f"Failure log saved to:"
        )

        print(
            failure_file.resolve()
        )


if __name__ == "__main__":
    main()