import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Use AI Proxy token
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
if AIPROXY_TOKEN:
    openai.api_key = AIPROXY_TOKEN
    openai.base_url = "https://aiproxy.sanand.workers.dev/openai/"  # proxy endpoint

def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    """
    Calls the AI Proxy (which forwards to OpenAI) with the given prompt.
    Returns the text content of the first choice, or None on failure.
    """
    if not AIPROXY_TOKEN:
        return None
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0,
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Proxy call failed: {e}")
        return None