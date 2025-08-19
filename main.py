from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from typing import Optional
from app.utils import process_request

app = FastAPI()

@app.post("/api/")
async def handle_request(
    questions: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    data: Optional[UploadFile] = File(None),
    prompt: Optional[str] = Form(None),
):
    try:
        result = await process_request(prompt, questions, image, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok"}
