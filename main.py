# main.py
import os
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from app.utils import process_request

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Data Analyst Agent API is running"}

@app.post("/api/")
async def analyze(request: Request):
    try:
        form = await request.form()
        files = [v for v in form.values() if isinstance(v, UploadFile)]

        if not files:
            return JSONResponse({"error": "No files uploaded"}, status_code=422)

        tmp_q_path = None
        attachment_paths = []

        for file in files:
            suffix = f".{file.filename.split('.')[-1]}"
            with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(await file.read())
                if file.filename.endswith(".txt") and tmp_q_path is None:
                    tmp_q_path = tmp_file.name
                else:
                    attachment_paths.append(tmp_file.name)

        if not tmp_q_path:
            return JSONResponse({"error": "Missing required text file"}, status_code=422)

        result = process_request(tmp_q_path, attachments=attachment_paths)

        # Clean up temp files
        try:
            os.remove(tmp_q_path)
            for p in attachment_paths:
                os.remove(p)
        except Exception:
            pass

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
