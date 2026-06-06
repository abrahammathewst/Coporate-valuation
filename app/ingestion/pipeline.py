from app.ingestion.pdf_loader import load_pdf
from app.ingestion.semantic_chunker import create_semantic_chunks
from app.ingestion.cleaner import filter_chunks

from app.vectorstore.qdrant_store import (
    recreate_collection,
    upload_chunks
)


def ingest_pdf(pdf_path: str):
    """
    Complete ingestion pipeline:
    PDF -> Semantic Chunks -> Cleaning -> Qdrant
    """

    print("Loading PDF...")

    documents = load_pdf(pdf_path)

    print(f"Pages loaded: {len(documents)}")

    print("\nCreating semantic chunks...")

    chunks = create_semantic_chunks(documents)

    print(f"Chunks before cleaning: {len(chunks)}")

    chunks = filter_chunks(chunks)

    print(f"Chunks after cleaning: {len(chunks)}")

    print("\nRecreating Qdrant collection...")

    recreate_collection()

    print("\nUploading chunks to Qdrant...")

    upload_chunks(chunks)

    print("\nIngestion completed successfully.")

    return chunks