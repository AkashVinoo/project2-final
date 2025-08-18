from .llm_client import call_openai_chat, call_openai_embedding

def process_request(prompt: str):
    chat_response = call_openai_chat(prompt)
    embeddings = call_openai_embedding(prompt)
    return {"response": chat_response, "embedding": embeddings}
