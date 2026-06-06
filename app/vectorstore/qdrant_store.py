from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from app.embeddings.hf_embeddings import get_embedding_model


COLLECTION_NAME = "corporate_reports"
VECTOR_SIZE = 1024


def get_qdrant_client():

    return QdrantClient(
        host="localhost",
        port=6333
    )


def create_collection():

    client = get_qdrant_client()

    existing_collections = [
        collection.name
        for collection in client.get_collections().collections
    ]

    if COLLECTION_NAME in existing_collections:
        print(f"Collection '{COLLECTION_NAME}' already exists")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

    print(f"Collection '{COLLECTION_NAME}' created")


def recreate_collection():

    client = get_qdrant_client()

    try:
        client.delete_collection(
            collection_name=COLLECTION_NAME
        )
        print(f"Deleted '{COLLECTION_NAME}'")
    except Exception:
        pass

    create_collection()


def upload_chunks(chunks):

    client = get_qdrant_client()

    model = get_embedding_model()

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    print(f"Generating embeddings for {len(texts)} chunks...")

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    points = []

    for idx, (chunk, vector) in enumerate(
        zip(chunks, embeddings),
        start=1
    ):

        payload = {
            "chunk_id": idx,
            "doc_id": "ril_annual_report_2025_26",
            "page": chunk.metadata.get("page"),
            "source": chunk.metadata.get("source"),
            "text": chunk.page_content
        }

        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=vector.tolist(),
                payload=payload
            )
        )

    print("Uploading to Qdrant...")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True
    )

    print(f"Uploaded {len(points)} chunks successfully")


def get_collection_info():

    client = get_qdrant_client()

    info = client.get_collection(
        collection_name=COLLECTION_NAME
    )

    return info