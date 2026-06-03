import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_answer(question, context):

    prompt = f"""
You are a helpful enterprise knowledge assistant.

Answer ONLY using the provided context.

If the answer is not found, say:
"I could not find that information in the documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen3:4b",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()

    return result["response"]