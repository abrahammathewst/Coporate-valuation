def build_prompt(
    query: str,
    retrieved_chunks: list
) -> str:

    context_parts = []

    for chunk in retrieved_chunks:

        context_parts.append(
            f"""
Chunk ID: {chunk['chunk_id']}
Page: {chunk['page']}

{chunk['text']}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an expert financial analyst.

Answer the user's question using ONLY the provided context.

When citing facts, include the source in the form:

(Source: Chunk ID X, Page Y). Please don't list the sources at the end of the answer.

If the answer cannot be found in the context,
say:

"I could not find the answer in the retrieved documents."

Context:
{context}

Question:
{query}

Answer:
"""

    return prompt