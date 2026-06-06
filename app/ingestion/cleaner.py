def filter_chunks(chunks, min_chars=100):

    filtered_chunks = []

    for chunk in chunks:
        text = chunk.page_content.strip()

        if len(text) < min_chars:
            continue

        filtered_chunks.append(chunk)

    return filtered_chunks