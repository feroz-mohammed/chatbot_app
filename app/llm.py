
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _fallback_reply(messages: List[Dict[str, str]]) -> str:
    user_last = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    if "hello" in user_last.lower():
        return "Hi! How can I help you today? (Fallback reply)"
    return f"I heard you say: '{user_last}'. I'm a demo assistant without an LLM configured yet."

def _openai_reply(messages: List[Dict[str, str]]) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"(OpenAI error: {e})\n" + _fallback_reply(messages)

def generate_reply(messages: List[Dict[str, str]]) -> str:

    if not any(m.get("role") == "system" for m in messages):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    if OPENAI_API_KEY:
        return _openai_reply(messages)
    return _fallback_reply(messages)
