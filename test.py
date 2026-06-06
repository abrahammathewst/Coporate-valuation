from app.retrieval.retriever import search


def main():

    query = "What was EBITDA growth?"

    results = search(
        query=query,
        limit=5
    )

    print(f"\nQuery: {query}")
    print(f"Retrieved: {len(results)} chunks\n")

    for rank, result in enumerate(results, start=1):

        payload = result.payload

        chunk_id = payload.get("chunk_id")
        doc_id = payload.get("doc_id")
        page = payload.get("page")
        source = payload.get("source")

        print("=" * 100)

        print(f"Rank     : {rank}")
        print(f"Score    : {result.score:.4f}")
        print(f"Chunk ID : {chunk_id}")
        print(f"Doc ID   : {doc_id}")
        print(f"Page     : {page}")
        print(f"Source   : {source}")

        print("\nChunk:\n")

        print(payload.get("text", "")[:1000])

        print("\n")


if __name__ == "__main__":
    main()