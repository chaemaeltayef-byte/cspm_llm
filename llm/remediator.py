import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_remediation(threat_label: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""You are a cloud security expert.

Threat detected: {threat_label}

Give exactly 3 numbered remediation steps a cloud admin should take immediately.
Be specific and actionable. No introduction, just the 3 steps."""
        }]
    )
    return response.choices[0].message.content