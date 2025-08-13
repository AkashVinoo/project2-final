from typing import List, Optional

@app.post("/api/")
async def analyze(
    question_file: UploadFile = File(...),
    attachments: Optional[List[UploadFile]] = File(None)
):
    try:
        # Save the uploaded question file
        with NamedTemporaryFile(delete=False, suffix=".txt") as tmp_q:
            tmp_q.write(await question_file.read())
            tmp_q_path = tmp_q.name

        # Save attachments
        attachment_paths = []
        if attachments:
            for file in attachments:
                with NamedTemporaryFile(delete=False) as tmp_a:
                    tmp_a.write(await file.read())
                    attachment_paths.append(tmp_a.name)

        # Process request
        result = process_request(tmp_q_path, attachments=attachment_paths)

        # Cleanup
        try:
            os.remove(tmp_q_path)
            for p in attachment_paths:
                os.remove(p)
        except:
            pass

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
