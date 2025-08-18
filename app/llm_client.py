import requests

# 🔐 Your AI Proxy token
AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.wqLRMdaf0un4yfEhgvVEo9pBt9ASGeJ64nObOLWTgv0"

# AI Proxy endpoint (OpenAI-compatible path)
AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    """
    Send a prompt to the AI Proxy and return the assistant message text.
    Returns None on failure.
    """
    try:
        headers = {
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800,
            "temperature": 0
        }
        resp = requests.post(AIPROXY_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[ERROR] AI Proxy call failed: {e}")
        return None
