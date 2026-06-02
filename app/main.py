from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Knowledge Copilot",
    version="1.0.0"
)

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