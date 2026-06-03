import chromadb

client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_collection(
    name="documents"
)


def search_documents(
    query: str,
    n_results: int = 7
):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    formatted_results = []

    for doc, meta in zip(documents, metadatas):

        if meta is None:
            continue

        formatted_results.append(
            {
                "source": meta["source"],
                "page": meta["page"],
                "text": doc
            }
        )

    return formatted_results