from app.retrieval.retriever import search

from app.rag.prompt_builder import build_prompt
# from app.llm.gemini import generate_response
from app.llm.ollama import generate_response


def answer_question(
    query: str,
    k: int = 5
):

    results = search(
        query=query,
        limit=k
    )

    chunks = []

    for result in results:

        chunks.append(
            {
                "chunk_id": result.payload.get("chunk_id"),
                "page": result.payload.get("page"),
                "text": result.payload.get("text")
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