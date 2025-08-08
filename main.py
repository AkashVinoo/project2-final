from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
import os
import tempfile
from app.utils import process_request

app = FastAPI(title="Data Analyst Agent")

@app.post("/api/")
async def analyze(
    questions: UploadFile = File(...),
    files: Optional[List[UploadFile]] = File(None)
):
    # read questions
    q_text = (await questions.read()).decode("utf-8")

    # save attachments to temp folder
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