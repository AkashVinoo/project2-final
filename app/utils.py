from .llm_client import call_openai_chat, call_openai_embedding
import base64

def process_request(prompt: str, attachments: dict = None):
    """
    Process the request: send prompt to LLM, generate embeddings,
    and handle optional attachments.
    """
    chat_response = call_openai_chat(prompt)
    embeddings = call_openai_embedding(prompt)

    files_info = {}
    if attachments:
        for fname, content in attachments.items():
            files_info[fname] = base64.b64encode(content).decode("utf-8")

    return {
        "response": chat_response,
        "embedding": embeddings,
        "attachments": files_info,
    }
