from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.utils import process_request

app = FastAPI()

class RequestBody(BaseModel):
    prompt: str

@app.post("/api/")
def handle_request(body: RequestBody):
    try:
        result = process_request(body.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok"}
