def chunk_text(
    text: str,
    page_number: int,
    chunk_size: int = 1500,
    overlap: int = 150
):

    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(text), step):

        chunks.append(
            {
                "chunk_id": len(chunks) + 1,
                "page": page_number,
                "text": text[i:i + chunk_size]
            }
        )

    return chunks