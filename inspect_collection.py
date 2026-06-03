import chromadb

client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_collection(
    name="documents"
)

results = collection.get()

print("IDS:")
print(results["ids"])

print("\nMETADATAS:")
print(results["metadatas"])