from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import Optional, List
from app.utils import process_request

app = FastAPI()

@app.post("/api/")
async def handle_request(
    questions: UploadFile = File(..., description="Upload questions.txt"),
    files: Optional[List[UploadFile]] = None
):
    try:
        # Read main questions.txt content
        prompt = (await questions.read()).decode("utf-8")

        # Collect optional attachments
        attachments = {}
        if files:
            for f in files:
                attachments[f.filename] = await f.read()

        result = process_request(prompt, attachments)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok"}
