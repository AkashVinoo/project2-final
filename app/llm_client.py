import requests

# Your AI Proxy token (keep secret)
AIPROXY_TOKEN = "YOUR_PROXY_TOKEN_HERE"

AIPROXY_URL = "https://aiproxy.sanand.workers.dev/v1/chat/completions"

def call_openai(prompt: str, model: str = "gpt-4o-mini"):
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
