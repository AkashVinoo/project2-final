import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from app.utils import process_request
from typing import List

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

        print("Received files:")
        for file in all_files:
            print(f"Filename: {file.filename}")

        # Save uploaded files to temporary paths
        for file in all_files:
            suffix = f".{file.filename.split('.')[-1]}"
            with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(await file.read())
                if file.filename.endswith(".txt") and tmp_q_path is None:
                    tmp_q_path = tmp_file.name
                else:
                    attachment_paths.append(tmp_file.name)

        if not tmp_q_path:
            return JSONResponse(
                content={"error": "Missing required text file for analysis"}, status_code=422
            )

        # Process request
        result = process_request(tmp_q_path, attachments=attachment_paths)

        # Clean up temporary files
        try:
            os.remove(tmp_q_path)
            for p in attachment_paths:
                os.remove(p)
        except Exception:
            pass

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
