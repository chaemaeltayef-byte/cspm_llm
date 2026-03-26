import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DEFAULT_SYSTEM_PROMPT = """You are a Cloud Security Posture Management (CSPM) expert assistant.
You specialize in:
- Identifying cloud misconfigurations (AWS, Azure, GCP)
- CIS Benchmark violations
- IAM policy risks
- Exposed storage buckets, open ports, unencrypted data
- Compliance frameworks (SOC2, ISO 27001, NIST)

When analyzing issues, always:
1. Identify the severity (Critical / High / Medium / Low)
2. Explain the risk
3. Give a concrete remediation step
"""

# Start with the default prompt — gets replaced when threats are loaded
system_prompt = DEFAULT_SYSTEM_PROMPT


def set_context(threats: list):
    """Called when threats are detected — updates the system prompt with threat context."""
    global system_prompt

    if not threats:
        system_prompt = DEFAULT_SYSTEM_PROMPT
        return

    threat_summary = "\n".join(
        [f"- {t['threat']} (confidence: {t['score']:.0%})" for t in threats]
    )
    system_prompt = f"""You are a Cloud Security Posture Management (CSPM) expert assistant.
The following threats were detected in this session:
{threat_summary}

When answering:
1. Identify the severity (Critical / High / Medium / Low)
2. Explain the risk clearly
3. Give a concrete remediation step
Be concise and helpful."""


def ask_chatbot(user_question: str, history: list) -> str:
    """Send a question to the chatbot with full conversation history."""
    messages = [{"role": "system", "content": system_prompt}]

    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({"role": "user", "content": user_question})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return response.choices[0].message.content


def reset_chat():
    """Reset the system prompt back to default (call this when starting a new session)."""
    global system_prompt
    system_prompt = DEFAULT_SYSTEM_PROMPT