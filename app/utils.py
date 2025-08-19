from .llm_client import call_openai_chat, call_openai_embedding
import pandas as pd
from typing import Optional
from fastapi import UploadFile

async def process_request(prompt: Optional[str], questions: Optional[UploadFile], image: Optional[UploadFile], data: Optional[UploadFile]):
    """Handles uploaded files + prompt and calls the LLM."""

    content_summary = []

    # Handle questions.txt
    if questions:
        q_text = (await questions.read()).decode("utf-8")
        content_summary.append(f"Questions:\n{q_text}")

    # Handle CSV file
    if data:
        df = pd.read_csv(data.file)
        summary = f"CSV with {df.shape[0]} rows and {df.shape[1]} columns. Columns: {', '.join(df.columns)}"
        content_summary.append(summary)

    # Handle image (we just note presence, not process actual pixels)
    if image:
        content_summary.append(f"Received image file: {image.filename}")

    # Combine prompt + summaries
    full_prompt = (prompt or "") + "\n\n" + "\n".join(content_summary)

    # Call AI Pipe (LLM + embeddings)
    chat_response = call_openai_chat(full_prompt)
    embeddings = call_openai_embedding(full_prompt)

    return {
        "response": chat_response,
        "embedding": embeddings,
        "summary": content_summary,
    }
