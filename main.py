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
    """
    Accepts all uploaded files, finds the first text file for the question,
    and treats the rest as attachments.
    """
    try:
        form = await request.form()
        all_files = [v for v in form.values() if isinstance(v, UploadFile)]

        if not all_files:
            return JSONResponse(content={"error": "No files received"}, status_code=422)

        tmp_q_path = None
        attachment_paths = []
        text_file_found = False

        for file in all_files:
            content = await file.read()
            if file.filename.endswith(".txt") and not text_file_found:
                with NamedTemporaryFile(delete=False, suffix=".txt") as tmp_q:
                    tmp_q.write(content)
                    tmp_q_path = tmp_q.name
                    text_file_found = True
            else:
                with NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_a:
                    tmp_a.write(content)
                    attachment_paths.append(tmp_a.name)

        if not tmp_q_path:
            return JSONResponse(content={"error": "Missing required text file"}, status_code=422)

        result = process_request(tmp_q_path, attachments=attachment_paths)

        try:
            os.remove(tmp_q_path)
            for p in attachment_paths:
                os.remove(p)
        except:
            pass

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
