from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue
)

from app.embeddings.hf_embeddings import get_embedding_model
from app.vectorstore.qdrant_store import (
    get_qdrant_client,
    COLLECTION_NAME
)


def _deduplicate_results(
    results,
    max_results=5
):
    """
    Remove near-identical chunks.
    """

    seen_texts = set()
    unique_results = []

    for result in results:

        text = result.payload.get(
            "text",
            ""
        ).strip()

        fingerprint = text[:200]

        if fingerprint in seen_texts:
            continue

        seen_texts.add(fingerprint)
        unique_results.append(result)

        if len(unique_results) >= max_results:
            break

    return unique_results


def search(
    query: str,
    limit: int = 5,
    ticker: str | None = None,
    year: int | None = None,
    document_type: str | None = None
):

    model = get_embedding_model()

    query_vector = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    client = get_qdrant_client()

    conditions = []

    if ticker:

        conditions.append(
            FieldCondition(
                key="ticker",
                match=MatchValue(
                    value=ticker
                )
            )
        )

    if year:

        conditions.append(
            FieldCondition(
                key="year",
                match=MatchValue(
                    value=year
                )
            )
        )

    if document_type:

        conditions.append(
            FieldCondition(
                key="document_type",
                match=MatchValue(
                    value=document_type
                )
            )
        )

    query_filter = None

    if conditions:

        query_filter = Filter(
            must=conditions
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=query_filter,
        limit=limit * 3
    ).points

    results = _deduplicate_results(
        results,
        max_results=limit
    )

    return results