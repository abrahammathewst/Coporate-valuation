from app.ingestion.pipeline import ingest_pdf


def main():

    pdf_path = "./data/RIL-Integrated-Annual-Report-2025-26.pdf"

    chunks = ingest_pdf(pdf_path)

    print(f"\nFinal chunks stored: {len(chunks)}")


if __name__ == "__main__":
    main()