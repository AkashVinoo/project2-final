# llm_client.py

import sys
import openai
import os

# =========================================
# HARDCODED AI PROXY TOKEN
# =========================================
AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA5MzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.wqLRMdaf0un4yfEhgvVEo9pBt9ASGeJ64nObOLWTgv0"

# Optional: Direct OpenAI key (fallback)
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "").strip()

def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    """
    Try AI Proxy first. If it fails, fall back to direct OpenAI API.
    """
    # === Try via AI Proxy ===
    try:
        openai.api_key = AIPROXY_TOKEN
        openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"  # FIXED path
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0,
        )
        return resp.choices[0].message.content

    except Exception as proxy_error:
        print(f"[WARN] AI Proxy failed: {proxy_error}")

        # === Fallback to direct OpenAI API ===
        if not OPENAI_KEY:
            print("[ERROR] No OpenAI API key found for fallback.")
            return None

        try:
            openai.api_key = OPENAI_KEY
            openai.api_base = "https://api.openai.com/v1"
            resp = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0,
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"[ERROR] Direct OpenAI call failed: {e}")
            return None
