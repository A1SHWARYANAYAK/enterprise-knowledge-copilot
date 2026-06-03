import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_answer(question, context):

    prompt = f"""
    You are a document question answering assistant.

    Answer completely using the provided context.

    If the question asks for a summary,
    provide a structured summary.

    If the question asks for details,
    provide all relevant details from the context.

    Use bullet points when helpful.

    Do not make up information.
    Only use the provided context.

    If multiple items are found, list ALL of them.

    Use bullet points when appropriate.

    If the answer is not found, reply:
    "I could not find that information in the document."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "num_predict": 1024
            }
        }
    )

    result = response.json()

    print("\n========== RAW LLM OUTPUT ==========")
    print(result)
    print("====================================\n")

    return result["response"]