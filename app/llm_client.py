# app/llm_client.py
import os
import requests

# 🔐 Your Hugging Face token (sign up at https://huggingface.co/settings/tokens)
HF_TOKEN = os.environ.get("HF_TOKEN", "")  # You can also hardcode it for now

# Example: using a text-generation model
HF_MODEL = "gpt2"  # Lightweight free model; can switch to bigger models like 'tiiuae/falcon-7b-instruct'

API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

def call_openai(prompt: str, model: str = None):
    """
    Sends prompt to Hugging Face Inference API and returns text.
    """
    try:
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {"inputs": prompt, "options": {"wait_for_model": True}}

        resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        # Hugging Face returns list of dicts: [{'generated_text': "..."}]
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        else:
            return str(data)

    except Exception as e:
        print(f"[ERROR] Hugging Face API call failed: {e}")
        return None
