# app/llm_client.py
from aipipe import AI  # Correct import

# 🔐 Your AI Pipe token
AIPIPE_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.yyhzLRnLWkmCpvPFx3GvZIT8Bb8fjxTBEZmLRbaMLx8"

# Instantiate AI client
client = AI(api_key=AIPIPE_TOKEN)

def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    """
    Send a prompt to AI Pipe and return the assistant message text.
    Returns None on failure.
    """
    try:
        response = client.chat(
            prompt,
            model=model,
            max_tokens=800,
            temperature=0
        )
        return response.get("content", None)
    except Exception as e:
        print(f"[ERROR] AI Pipe call failed: {e}")
        return None

