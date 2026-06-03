from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

embedding = model.encode(
    "Aishwarya is an AI Engineer"
)

print(len(embedding))