# app/llm_client.py
from aipipe import AI

# 🔐 Your AI Pipe token
AIPIPE_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.yyhzLRnLWkmCpvPFx3GvZIT8Bb8fjxTBEZmLRbaMLx8"

# Initialize the AI client
ai_client = AI(api_key=AIPIPE_TOKEN)

def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    """
    Sends a prompt to AI Pipe and returns the assistant message text.
    Returns None on failure.
    """
    try:
        response = ai_client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[ERROR] AI Pipe call failed: {e}")
        return None
