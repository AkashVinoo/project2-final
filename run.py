# run.py
import sys
import json
from app.llm_client import call_openai

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run.py '<prompt>'")
        sys.exit(1)

    prompt = sys.argv[1]
    result = call_openai(prompt)

    if result is None:
        print(json.dumps({"error": "no result"}))
        sys.exit(1)

    # Ensure it's always valid JSON for Promptfoo
    try:
        parsed = json.loads(result)
    except Exception:
        parsed = {"raw_output": result}

    print(json.dumps(parsed, ensure_ascii=False))
