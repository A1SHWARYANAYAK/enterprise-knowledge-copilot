import chromadb

client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_collection(
    name="documents"
)

collection.delete(
    ids=["1"]
)

print("Deleted test record")