import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_report(threats: list) -> str:
    threat_lines = "\n".join(
        [f"- {t['threat']} (confidence: {t['score']:.0%})" for t in threats]
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""You are a cloud security analyst writing an official report.

Threats detected:
{threat_lines}

Write a professional security report with these exact sections:
1. Executive Summary (2-3 sentences)
2. Threat Analysis (one short paragraph per threat)
3. Priority Actions (top 5 actions, numbered)
4. Conclusion (1-2 sentences)"""
        }]
    )
    report_text = response.choices[0].message.content

    os.makedirs("reports", exist_ok=True)
    filename = f"reports/security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("CLOUD SECURITY POSTURE REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(report_text)

    print(f"Report saved to {filename}")
    return report_text