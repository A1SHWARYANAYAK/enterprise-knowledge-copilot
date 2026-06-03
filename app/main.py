from pathlib import Path

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text


app = FastAPI(
    title="Enterprise Knowledge Copilot",
    version="1.0.0"
)

UPLOAD_DIR = Path("data/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def root():
    return {
        "message": "Enterprise Knowledge Copilot Running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    pages = extract_text_from_pdf(str(file_path))

    total_chunks = 0
    total_characters = 0

    for page in pages:
        chunks = chunk_text(page["text"])

        total_chunks += len(chunks)
        total_characters += len(page["text"])

    return {
        "filename": file.filename,
        "pages": len(pages),
        "chunks": total_chunks,
        "characters": total_characters
    }