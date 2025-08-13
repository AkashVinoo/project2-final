# main.py
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from app.utils import process_request
from typing import List, Optional

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Data Analyst Agent API is running"}

@app.post("/api/")
async def analyze(
    question_file: UploadFile = File(...),
    attachments: Optional[List[UploadFile]] = File(None)
):
    try:
        # Save the uploaded question file to a temporary location
        with NamedTemporaryFile(delete=False, suffix=".txt") as tmp_q:
            tmp_q.write(await question_file.read())
            tmp_q_path = tmp_q.name

        # Save attachments (if any)
        attachment_paths = []
        if attachments:
            for file in attachments:
                with NamedTemporaryFile(delete=False) as tmp_a:
                    tmp_a.write(await file.read())
                    attachment_paths.append(tmp_a.name)

        # Process the request
        result = process_request(tmp_q_path, attachments=attachment_paths)

        # Clean up temp files
        try:
            os.remove(tmp_q_path)
            for p in attachment_paths:
                os.remove(p)
        except:
            pass

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
