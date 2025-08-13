# llm_client.py

import sys
import openai

# =========================================
# DIRECTLY HARDCODED AI PROXY TOKEN
# =========================================
# WARNING: Never commit real keys to public repos.
# =========================================
AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.wqLRMdaf0un4yfEhgvVEo9pBt9ASGeJ64nObOLWTgv0"

if not AIPROXY_TOKEN:
    sys.stderr.write(
        "[ERROR] Missing AI Proxy token.\n"
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
