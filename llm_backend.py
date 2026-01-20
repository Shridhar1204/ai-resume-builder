import os, json
from dotenv import load_dotenv
from groq import Groq
from prompts import resume_prompt

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_resume_ai(raw_data):
    prompt = resume_prompt(raw_data)

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=2000
    )

    text = res.choices[0].message.content
    start, end = text.find("{"), text.rfind("}") + 1
    return json.loads(text[start:end])