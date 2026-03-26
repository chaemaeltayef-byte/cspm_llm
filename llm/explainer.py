import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_threat(threat_label: str, confidence_score: float) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""You are a cloud security expert.

A threat detection model flagged this:
- Threat: {threat_label}
- Confidence: {confidence_score:.0%}

In 3 sentences, explain what this threat means in simple terms for a cloud administrator."""
        }]
    )
    return response.choices[0].message.content