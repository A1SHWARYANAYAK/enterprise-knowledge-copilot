from pathlib import Path

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

from pydantic import BaseModel

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.services.vector_service import store_chunks
from app.services.search_service import search_documents
from app.services.llm_service import generate_answer


app = FastAPI(
    title="Enterprise Knowledge Copilot",
    version="1.0.0"
)


UPLOAD_DIR = Path("data/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():

    return {
        "message": "Enterprise Knowledge Copilot Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Save uploaded file

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF

    pages = extract_text_from_pdf(
        str(file_path)
    )

    all_chunks = []

    # Chunk pages

    for page in pages:

        chunks = chunk_text(
            text=page["text"],
            page_number=page["page"]
        )

        all_chunks.extend(chunks)

    # Store chunks in ChromaDB

    store_chunks(
        all_chunks,
        file.filename
    )

    return {
        "filename": file.filename,
        "pages": len(pages),
        "chunks": len(all_chunks),
        "stored_in_vector_db": True
    }


@app.get("/search")
def search(query: str):

    results = search_documents(
        query=query
    )

    return {
        "query": query,
        "results": results
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    # Retrieve relevant chunks

    results = search_documents(
        query=request.question
    )

    # Build context

    context = "\n\n".join(
        [item["text"] for item in results]
    )

    # Generate answer using Qwen
   
    answer = generate_answer(
        question=request.question,
        context=context
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": [
            {
                "source": result["source"],
                "page": result["page"],
                "snippet": result["snippet"]
            }
            for result in results
        ]
    }