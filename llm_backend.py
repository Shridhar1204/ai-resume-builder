import os
from dotenv import load_dotenv
from groq import Groq
from prompts import resume_prompt

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)

def generate_resume_content(name, role, education, skills, projects, experience):
    prompt = resume_prompt.format(
        name=name,
        role=role,
        education=education,
        skills=skills,
        projects=projects,
        experience=experience
    )

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ supported model
        messages=[
            {"role": "system", "content": "You are an expert resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1200
    )

    return completion.choices[0].message.content
