# app/llm_client.py
import requests
import json

# 🔐 Your AI Proxy token
AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.wqLRMdaf0un4yfEhgvVEo9pBt9ASGeJ64nObOLWTgv0"

# AI Proxy endpoint (OpenAI-compatible path)
AIPROXY_URL = "https://aiproxy.sanand.workers.dev/v1/chat/completions"


def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    """
    Send a prompt to the AI Proxy and return parsed JSON.
    If the model response is not valid JSON, return None.
    """
    try:
        headers = {
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json"
        }

        # Force JSON output
        system_message = {
            "role": "system",
            "content": (
                "You are a JSON-only API. "
                "Always respond with a strictly valid JSON object, "
                "no prose, no explanations, no markdown."
            )
        }

        user_message = {"role": "user", "content": prompt}

        payload = {
            "model": model,
            "messages": [system_message, user_message],
            "max_tokens": 800,
            "temperature": 0
        }

        resp = requests.post(AIPROXY_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        raw_text = data["choices"][0]["message"]["content"].strip()

        # Try parsing JSON
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            print("[ERROR] Model did not return valid JSON:")
            print(raw_text)
            return None

    except Exception as e:
        print(f"[ERROR] AI Proxy call failed: {e}")
        return None
