from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
import os
import tempfile
from app.utils import process_request

app = FastAPI(title="Data Analyst Agent")

@app.post("/api/")
async def analyze(
    request: Request,
    questions: Optional[UploadFile] = File(None, alias="questions"),
    questions_txt: Optional[UploadFile] = File(None, alias="questions.txt"),
    files: Optional[List[UploadFile]] = File(None)
):
    # Use whichever is provided
    q_file = questions or questions_txt
    if not q_file:
        raise HTTPException(status_code=400, detail="Missing questions.txt or questions file")
    
    q_text = (await q_file.read()).decode("utf-8")

    # Save attachments to temp folder
    tmpdir = tempfile.mkdtemp(prefix="daa_")
    saved_files = {}
    if files:
        for f in files:
            path = os.path.join(tmpdir, f.filename)
            with open(path, "wb") as fh:
                content = await f.read()
                fh.write(content)
            saved_files[f.filename] = path

    try:
        result = process_request(q_text, saved_files, tmpdir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content=result)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)