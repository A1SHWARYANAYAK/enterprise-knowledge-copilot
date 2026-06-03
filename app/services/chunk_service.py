def chunk_text(text: str, chunk_size: int = 500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunks.append(
            {
                "chunk_id": len(chunks) + 1,
                "text": text[i:i + chunk_size]
            }
        )

    return chunks