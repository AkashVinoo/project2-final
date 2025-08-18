import os
import base64
from .llm_client import call_openai

def process_request(question_file, attachments=None):
    """
    Reads the question file, sends it to the LLM via AI Proxy,
    and returns a structured response.
    attachments: list of file paths for additional context
    """
    try:
        with open(question_file, "r", encoding="utf-8") as f:
            prompt = f.read()

        if attachments:
            prompt += "\n\nAttachments provided:\n"
            for file_path in attachments:
                if os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    size = os.path.getsize(file_path)
                    prompt += f"- {file_name} ({size} bytes)\n"

        answer = call_openai(prompt)

        if not answer:
            return {"error": "AI Proxy call failed or returned no content"}

        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}


def encode_file_to_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
