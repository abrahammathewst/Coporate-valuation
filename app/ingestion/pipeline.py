from app.ingestion.pdf_loader import load_pdf
from app.ingestion.semantic_chunker import create_semantic_chunks
from app.ingestion.cleaner import filter_chunks
from app.ingestion.metadata import extract_metadata

from app.vectorstore.qdrant_store import (
    recreate_collection,
    upload_chunks
)


def ingest_pdf(
    pdf_path: str,
    recreate: bool = False
):
    """
    Complete ingestion pipeline

    PDF
        ↓
    Metadata Extraction
        ↓
    Semantic Chunking
        ↓
    Cleaning
        ↓
    Qdrant
    """

    metadata = extract_metadata(pdf_path)

    print("\nDocument Metadata:")
    print(metadata)

    print("\nLoading PDF...")

    documents = load_pdf(pdf_path)

    print(f"Pages loaded: {len(documents)}")

    print("\nCreating semantic chunks...")

    chunks = create_semantic_chunks(documents)

    print(f"Chunks before cleaning: {len(chunks)}")

    chunks = filter_chunks(chunks)

    print(f"Chunks after cleaning: {len(chunks)}")

    if recreate:

        print("\nRecreating Qdrant collection...")

        recreate_collection()

    print("\nUploading chunks to Qdrant...")

    upload_chunks(
        chunks=chunks,
        metadata=metadata
    )

    print("\nIngestion completed successfully.")

    return chunks


def ingest_directory(
    directory_path: str,
    recreate: bool = True
):
    """
    Bulk ingestion of all PDFs in a folder.
    """

    from pathlib import Path

    pdf_files = sorted(
        Path(directory_path).glob("*.pdf")
    )

    if not pdf_files:
        raise ValueError(
            f"No PDFs found in: {directory_path}"
        )

    print(
        f"\nFound {len(pdf_files)} PDF files"
    )

    if recreate:

        print(
            "\nRecreating collection once before bulk ingestion..."
        )

        recreate_collection()

    total_chunks = 0

    for idx, pdf_file in enumerate(
        pdf_files,
        start=1
    ):

        print(
            "\n" + "=" * 80
        )

        print(
            f"[{idx}/{len(pdf_files)}] "
            f"{pdf_file.name}"
        )

        chunks = ingest_pdf(
            pdf_path=str(pdf_file),
            recreate=False
        )

        total_chunks += len(chunks)

    print(
        "\n" + "=" * 80
    )

    print(
        f"\nBulk ingestion completed."
    )

    print(
        f"Total chunks uploaded: {total_chunks}"
    )