import chromadb
from sentence_transformers import SentenceTransformer


client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_or_create_collection(
    name="documents"
)

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def store_chunks(chunks, filename):

    # --------------------------------------------------
    # Clear existing document from collection
    # --------------------------------------------------

    existing = collection.get()

    if existing["ids"]:

        collection.delete(
            ids=existing["ids"]
        )

    # --------------------------------------------------
    # Store new document
    # --------------------------------------------------

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        ids.append(
            f"{filename}_{chunk['page']}_{chunk['chunk_id']}"
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append(
            {
                "source": filename,
                "page": chunk["page"]
            }
        )

    embeddings = embedding_model.encode(
        documents
    ).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )