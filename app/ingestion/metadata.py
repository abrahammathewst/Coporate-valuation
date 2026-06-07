from pathlib import Path


def extract_metadata(pdf_path: str) -> dict:

    filename = Path(pdf_path).stem

    parts = filename.split("_")

    ticker = parts[0]

    year = None
    document_type = None

    for part in parts:

        if part.isdigit():
            year = int(part)

    if "Annual" in parts and "Report" in parts:
        document_type = "annual_report"

    return {
        "ticker": ticker,
        "year": year,
        "document_type": document_type,
        "source_file": Path(pdf_path).name
    }