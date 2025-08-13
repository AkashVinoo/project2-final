import os
import sys
import openai
from dotenv import load_dotenv

load_dotenv()

# Load AI Proxy token from environment
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

if not AIPROXY_TOKEN:
    sys.stderr.write(
        "[ERROR] Missing AIPROXY_TOKEN environment variable.\n"
        "Please set it in your Render Environment Variables.\n"
    )
    sys.exit(1)

# Configure OpenAI to use AI Proxy
openai.api_key = AIPROXY_TOKEN
openai.api_base = "https://aiproxy.sanand.workers.dev/openai"

def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    """
    Calls the AI Proxy (which forwards to OpenAI) with the given prompt.
    Returns the text content of the first choice, or None on failure.
    """
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
