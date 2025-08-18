# app/llm_client.py
from aipipe import AI

# 🔐 Your AI Pipe token
AIPIPE_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.yyhzLRnLWkmCpvPFx3GvZIT8Bb8fjxTBEZmLRbaMLx8"

# Initialize AI Pipe client
ai = AI(api_key=AIPIPE_TOKEN, model="gpt-4o-mini")

def call_openai(prompt: str):
    """
    Send a prompt to AI Pipe and return the assistant message.
    Returns None if call fails.
    """
    try:
        response = ai.chat(prompt)
        return response
    except Exception as e:
        print(f"[ERROR] AI Pipe call failed: {e}")
        return None
