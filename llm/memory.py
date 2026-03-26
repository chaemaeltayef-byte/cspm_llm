import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MEMORY_FILE = "memory/session_memory.json"

def save_memory(chat_history: list):
    """At end of session, ask LLM to summarize and save it."""
    if not chat_history:
        return

    os.makedirs("memory", exist_ok=True)

    # Ask LLM to summarize the session
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""Summarize this cloud security session in 5 bullet points.
Focus on: threats discussed, decisions made, remediation steps suggested.
Keep it concise for future reference.

Session:
{json.dumps(chat_history, indent=2)}"""
            }
        ]
    )
    summary = response.choices[0].message.content

    # Load existing memory if any
    existing = []
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            existing = json.load(f)

    # Append new summary
    existing.append({
        "timestamp": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
        "summary": summary
    })

    # Keep only last 5 sessions
    existing = existing[-5:]

    with open(MEMORY_FILE, "w") as f:
        json.dump(existing, f, indent=2)

    print("Session memory saved.")


def load_memory() -> str:
    """Load past session summaries to inject into system prompt."""
    if not os.path.exists(MEMORY_FILE):
        return ""

    with open(MEMORY_FILE, "r") as f:
        sessions = json.load(f)

    if not sessions:
        return ""

    memory_text = "PREVIOUS SESSION MEMORY:\n"
    for s in sessions:
        memory_text += f"\n[{s['timestamp']}]\n{s['summary']}\n"

    return memory_text