from app.retrieval.retriever import search

from app.rag.prompt_builder import build_prompt

# from app.llm.gemini import generate_response
from app.llm.ollama import generate_response


def answer_question(
    query: str,
    ticker: str | None = None,
    year: int | None = None,
    document_type: str | None = None,
    k: int = 5
):

    results = search(
        query=query,
        limit=k,
        ticker=ticker,
        year=year,
        document_type=document_type
    )

    chunks = []

    for result in results:

        chunks.append(
            {
                "ticker": result.payload.get("ticker"),
                "year": result.payload.get("year"),
                "document_type": result.payload.get(
                    "document_type"
                ),
                "source_file": result.payload.get(
                    "source_file"
                ),

                "chunk_id": result.payload.get(
                    "chunk_id"
                ),
                "page": result.payload.get(
                    "page"
                ),
                "text": result.payload.get(
                    "text"
                )
            }
        )

    prompt = build_prompt(
        query=query,
        retrieved_chunks=chunks
    )

    answer = generate_response(
        prompt
    )

    return {
        "answer": answer,
        "sources": chunks
    }