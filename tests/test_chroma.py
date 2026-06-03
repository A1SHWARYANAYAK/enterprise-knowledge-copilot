import chromadb

client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_or_create_collection(
    name="documents"
)

collection.add(
    ids=["1"],
    documents=["Aishwarya knows Python and Scala"]
)

results = collection.query(
    query_texts=["What programming languages does Aishwarya know?"],
    n_results=1
)

print(results)