import requests

# Your AI Proxy token (keep this secret)
AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.wqLRMdaf0un4yfEhgvVEo9pBt9ASGeJ64nObOLWTgv0"

# AI Proxy endpoint
AIPROXY_URL = "https://aiproxy.sanand.workers.dev/v1/chat/completions"

def call_ai_proxy(prompt: str, model: str = "gpt-4o-mini"):
    """
    Sends a prompt to the AI Proxy and returns the model's response.
    No OpenAI API key is required — only the proxy token.
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
        resp = requests.post(AIPROXY_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

        # Extract the model's reply
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[ERROR] AI Proxy call failed: {e}")
        return None
