import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from typing import List, Optional
from app.utils import process_request

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Data Analyst Agent API is running"}

@app.post("/api/")
async def analyze(
    question_file: UploadFile = File(...),
    attachments: Optional[List[UploadFile]] = File(None)
):
    """
    Receives one mandatory question file and zero or more attachments.
    """
    try:
        # Save question file
        with NamedTemporaryFile(delete=False, suffix=".txt") as tmp_q:
            tmp_q.write(await question_file.read())
            tmp_q_path = tmp_q.name

        # Save attachments
        attachment_paths = []
        if attachments:
            for f in attachments:
                with NamedTemporaryFile(delete=False) as tmp_a:
                    tmp_a.write(await f.read())
                    attachment_paths.append(tmp_a.name)

        # Process request
        result = process_request(tmp_q_path, attachments=attachment_paths)

        # Cleanup
        os.remove(tmp_q_path)
        for p in attachment_paths:
            os.remove(p)

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
