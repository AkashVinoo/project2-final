import os
import tempfile
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

from app.utils import process_request

app = FastAPI(title="Data Analyst Agent")

# --- Force JSON errors instead of HTML ---
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": str(exc.detail)})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=422, content={"error": exc.errors()})

@app.exception_handler(Exception)
async def all_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"error": str(exc)})

# --- API endpoint ---
@app.post("/api/")
async def analyze(
    questions: Optional[UploadFile] = File(None, alias="questions"),
    questions_txt: Optional[UploadFile] = File(None, alias="questions.txt"),
    files: Optional[List[UploadFile]] = File(None)
):
    # Pick whichever form field is provided
    q_file = questions or questions_txt
    if not q_file:
        return JSONResponse(status_code=400, content={"error": "Missing questions.txt or questions file"})

    try:
        q_text = (await q_file.read()).decode("utf-8").strip()
        if not q_text:
            return JSONResponse(status_code=400, content={"error": "Questions file is empty"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Invalid questions file: {e}"})

    # Save any extra uploaded files to a temp directory
    tmpdir = tempfile.mkdtemp(prefix="daa_")
    saved_files = {}
    if files:
        for f in files:
            try:
                path = os.path.join(tmpdir, f.filename)
                with open(path, "wb") as fh:
                    fh.write(await f.read())
                saved_files[f.filename] = path
            except Exception as e:
                return JSONResponse(status_code=400, content={"error": f"Error saving file {f.filename}: {e}"})

    # Process request
    try:
        result = process_request(q_text, saved_files, tmpdir)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Processing failed: {e}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)