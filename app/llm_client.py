import requests

# Corrected AI Proxy endpoint
AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

# 🔑 Hardcoded token (for dev only, don’t commit to public repos)
AIPROXY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.wqLRMdaf0un4yfEhgvVEo9pBt9ASGeJ64nObOLWTgv0"


def call_llm(messages, model="gpt-4o-mini"):
    """
    Call the AI Proxy (OpenAI-compatible) API.
    :param messages: List of dicts like [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    :param model: Model name (default gpt-4o-mini)
    """
    headers = {
        "Authorization": f"Bearer {AIPROXY_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    response = requests.post(AIPROXY_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]
