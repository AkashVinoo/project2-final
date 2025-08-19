import requests

# Hardcoded AI Pipe token and base URL
AIPIPE_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.yyhzLRnLWkmCpvPFx3GvZIT8Bb8fjxTBEZmLRbaMLx8"
BASE_URL = "https://aipipe.org/openai/v1"

HEADERS = {
    "Authorization": f"Bearer {AIPIPE_TOKEN}",
    "Content-Type": "application/json",
}

def call_openai_chat(prompt: str, model: str = "gpt-4o-mini"):
    """Send a chat prompt to AI Pipe (OpenAI proxy)."""
    url = f"{BASE_URL}/responses"
    payload = {"model": model, "input": prompt}
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()

    if "output" in data and len(data["output"]) > 0:
        text_parts = []
        for item in data["output"]:
            for content in item.get("content", []):
                if "text" in content:
                    text_parts.append(content["text"])
        return "\n".join(text_parts)
    return ""

def call_openai_embedding(texts, model: str = "text-embedding-3-small"):
    """Generate embeddings for given text(s)."""
    if isinstance(texts, str):
        texts = [texts]
    url = f"{BASE_URL}/embeddings"
    payload = {"model": model, "input": texts}
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()
    return [item["embedding"] for item in data["data"]]

