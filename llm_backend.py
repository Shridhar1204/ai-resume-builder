import os
import json
from dotenv import load_dotenv
from groq import Groq
from prompts import resume_prompt

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=GROQ_API_KEY)

def generate_resume_ai(raw_data: dict) -> dict:
    prompt = resume_prompt(raw_data)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You output ONLY raw JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1600
    )

    content = response.choices[0].message.content.strip()

    if not content:
        raise ValueError("AI returned empty response")

    # Safe JSON extraction
    try:
        start = content.find("{")
        end = content.rfind("}") + 1
        return json.loads(content[start:end])
    except Exception:
        raise ValueError(f"Invalid AI JSON output:\n{content}")
