def chunk_text(
    text: str,
    page_number: int,
    chunk_size: int = 1000
):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunks.append(
            {
                "chunk_id": len(chunks) + 1,
                "page": page_number,
                "text": text[i:i + chunk_size]
            }
        )

    return chunks