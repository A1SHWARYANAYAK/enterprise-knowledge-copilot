from pathlib import Path

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
import time

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

templates = Jinja2Templates(
    directory="app/templates"
)


class QuestionRequest(BaseModel):
    question: str


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# --------------------------------------------------
# API Status
# --------------------------------------------------

@app.get("/api")
def api_root():

    return {
        "message": "Enterprise Knowledge Copilot Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    pages = extract_text_from_pdf(
        str(file_path)
    )

    all_chunks = []

    for page in pages:

        chunks = chunk_text(
            text=page["text"],
            page_number=page["page"]
        )

        all_chunks.extend(chunks)

    store_chunks(
        all_chunks,
        file.filename
    )
    # Delete uploaded PDF after indexing

    import os

    os.remove(file_path)

    return {
        "filename": file.filename,
        "pages": len(pages),
        "chunks": len(all_chunks),
        "stored_in_vector_db": True
    }


# --------------------------------------------------
# Search
# --------------------------------------------------

@app.get("/search")
def search(query: str):

    results = search_documents(
        query=query
    )

    return {
        "query": query,
        "results": results
    }


# --------------------------------------------------
# Ask Question (RAG)
# --------------------------------------------------

@app.post("/ask")
def ask(request: QuestionRequest):

    search_start = time.time()

    results = search_documents(
        query=request.question
    )
    
    print("\n========== RETRIEVED CHUNKS ==========")

    for idx, result in enumerate(results):

        print(f"\nChunk {idx + 1}")
        print(result["text"])

    print("\n======================================")

    print(
        f"Search took: {time.time() - search_start:.2f}s"
    )

    context = "\n\n".join(
        [item["text"] for item in results]
    )

    llm_start = time.time()

    answer = generate_answer(
        question=request.question,
        context=context
    )

    print(
        f"LLM took: {time.time() - llm_start:.2f}s"
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