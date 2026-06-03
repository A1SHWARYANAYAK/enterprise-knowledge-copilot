import chromadb

client = chromadb.PersistentClient(
    path="data/chroma"
)

try:
    client.delete_collection("documents")
    print("Collection deleted")
except Exception as e:
    print(f"Error: {e}")