from app.ingestion.pipeline import ingest_directory


def main():

    ingest_directory(
        directory_path="./data/annual_report",
        recreate=True
    )


if __name__ == "__main__":
    main()