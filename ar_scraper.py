from playwright.sync_api import sync_playwright
from pathlib import Path
import requests
import pandas as pd

YEAR = "2025"

df = pd.read_csv("./data/ind_nifty500list.csv")

output_dir = Path("./data/annual_report")
output_dir.mkdir(parents=True, exist_ok=True)

failures = []

for _, row in df.iterrows():

    COMPANY = row["ISIN Code"]      # Search value
    SYMBOL = row["Symbol"]          # Filename

    browser = None

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)

            page = browser.new_page()

            page.goto(
                "https://www.bseindia.com/corporates/historicalannualreport"
            )

            page.wait_for_timeout(3000)

            # Search company using ISIN
            box = page.locator("main #scripsearchtxtbx")

            box.fill(COMPANY)

            page.wait_for_timeout(3000)

            # Select autocomplete result
            try:
                page.get_by_text(COMPANY).first.click()
            except:
                page.keyboard.press("ArrowDown")
                page.keyboard.press("Enter")

            page.wait_for_timeout(1000)

            # Submit
            page.get_by_role(
                "button",
                name="Submit"
            ).click()

            page.wait_for_selector(
                "table",
                timeout=15000
            )

            rows = page.locator("table tbody tr")

            pdf_url = None

            for i in range(rows.count()):

                report_row = rows.nth(i)

                row_year = (
                    report_row.locator("td")
                    .nth(0)
                    .inner_text()
                    .strip()
                )

                print(
                    f"{SYMBOL} -> YEAR {row_year}"
                )

                if row_year == YEAR:

                    icon = report_row.locator(
                        "i[aria-label='Download pdf']"
                    )

                    print(
                        f"{SYMBOL} -> Found PDF"
                    )

                    icon.click(force=True)

                    page.wait_for_timeout(5000)

                    pdf_url = page.context.pages[-1].url

                    print(
                        f"{SYMBOL} -> {pdf_url}"
                    )

                    break

            if not pdf_url:

                print(
                    f"SKIPPED: {SYMBOL} "
                    f"(No report for {YEAR})"
                )

                failures.append(
                    (
                        SYMBOL,
                        "No report found"
                    )
                )

                continue

            cookies = {
                c["name"]: c["value"]
                for c in page.context.cookies()
            }

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Referer": (
                    "https://www.bseindia.com/"
                )
            }

            print(
                f"{SYMBOL} -> Downloading..."
            )

            response = requests.get(
                pdf_url,
                headers=headers,
                cookies=cookies,
                timeout=120
            )

            if response.status_code != 200:

                print(
                    f"SKIPPED: {SYMBOL} "
                    f"(HTTP {response.status_code})"
                )

                failures.append(
                    (
                        SYMBOL,
                        f"HTTP {response.status_code}"
                    )
                )

                continue

            filename = (
                output_dir /
                f"{SYMBOL}_{YEAR}_Annual_Report.pdf"
            )

            with open(filename, "wb") as f:
                f.write(response.content)

            print(
                f"SUCCESS: {filename.name}"
            )

    except Exception as e:

        print(
            f"FAILED: {SYMBOL}"
        )

        print(e)

        failures.append(
            (
                SYMBOL,
                str(e)
            )
        )

    finally:

        try:
            if browser:
                browser.close()
        except:
            pass

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(
    f"Total Companies: {len(df)}"
)

print(
    f"Failures: {len(failures)}"
)

if failures:

    failure_df = pd.DataFrame(
        failures,
        columns=["Symbol", "Reason"]
    )

    failure_file = (
        output_dir /
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