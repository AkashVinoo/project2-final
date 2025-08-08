import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    """
    Calls the OpenAI API with the given prompt.
    Returns the text content of the first choice, or None on failure.
    """
    if not OPENAI_API_KEY:
        return None
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0,
        )
        return resp.choices[0].message.content
    except Exception:
        return None