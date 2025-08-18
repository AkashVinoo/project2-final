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
        form = await request.form()  # Accept all uploaded files
        tmp_q_path = None
        attachment_paths = []

        # Process all form items
        for key, file in form.items():
            if isinstance(file, UploadFile):
                content = await file.read()
                if file.filename.endswith(".txt") and tmp_q_path is None:
                    # First .txt file is the question file
                    with NamedTemporaryFile(delete=False, suffix=".txt") as tmp_q:
                        tmp_q.write(content)
                        tmp_q_path = tmp_q.name
                else:
                    # All other files are attachments
                    ext = file.filename.split(".")[-1] if "." in file.filename else "dat"
                    with NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp_a:
                        tmp_a.write(content)
                        attachment_paths.append(tmp_a.name)

        # Fallback: create empty question file if none provided
        if not tmp_q_path:
            with NamedTemporaryFile(delete=False, suffix=".txt") as tmp_q:
                tmp_q.write(b"No questions provided")
                tmp_q_path = tmp_q.name

        result = process_request(tmp_q_path, attachments=attachment_paths)

        # Cleanup temp files
        try:
            os.remove(tmp_q_path)
            for p in attachment_paths:
                os.remove(p)
        except:
            pass

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
