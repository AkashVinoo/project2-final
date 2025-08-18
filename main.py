# main.py
import os
from fastapi import FastAPI, Request
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
        tmp_q_path = None
        attachment_paths = []

        print("Received form fields:", list(form.keys()))

        for key, value in form.items():
            if hasattr(value, "filename"):  # only handle files
                print(f"Processing file: {value.filename}")

                file_bytes = await value.read()

                if value.filename.endswith(".txt") and tmp_q_path is None:
                    # Treat the first .txt as the questions.txt
                    with NamedTemporaryFile(delete=False, suffix=".txt") as tmp_q:
                        tmp_q.write(file_bytes)
                        tmp_q_path = tmp_q.name
                else:
                    # Other files -> attachments
                    ext = value.filename.split(".")[-1]
                    with NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp_a:
                        tmp_a.write(file_bytes)
                        attachment_paths.append(tmp_a.name)

        if not tmp_q_path:
            return JSONResponse(
                content={"error": "Missing required questions.txt"},
                status_code=422
            )

        # Call your pipeline
        result = process_request(tmp_q_path, attachments=attachment_paths)

        # Cleanup
        try:
            os.remove(tmp_q_path)
            for p in attachment_paths:
                os.remove(p)
        except Exception:
            pass

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
