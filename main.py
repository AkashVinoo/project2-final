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
    all_files: List[UploadFile] = File(...)
):
    try:
        tmp_q_path = None
        attachment_paths = []

        # Process all uploaded files and separate them based on their original name
        for file in all_files:
            with NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_file:
                tmp_file.write(await file.read())
                
                if file.filename == "questions.txt":
                    tmp_q_path = tmp_file.name
                else:
                    attachment_paths.append(tmp_file.name)

        if not tmp_q_path:
            return JSONResponse(content={"error": "Missing required 'questions.txt' file"}, status_code=422)

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
