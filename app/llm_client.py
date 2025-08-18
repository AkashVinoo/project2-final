# app/llm_client.py
from aipipe import AIPipe

# 🔐 Your AI Pipe token
AIPI_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.yyhzLRnLWkmCpvPFx3GvZIT8Bb8fjxTBEZmLRbaMLx8"

# Initialize the client
client = AIPipe(api_key=AIPI_TOKEN)

def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    """
    Send a prompt to AI Pipe and return the assistant message text.
    Returns None on failure.
    """
    try:
        response = client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0
        )
        # response['choices'][0]['message']['content'] style may vary depending on aipipe
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"[ERROR] AI Pipe call failed: {e}")
        return None
