import os
from dotenv import load_dotenv
from groq import Groq
from prompts import resume_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_resume_content(name, role, education, skills, projects, experience):
    prompt = resume_prompt.format(
        name=name,
        role=role,
        education=education,
        skills=skills,
        projects=projects,
        experience=experience
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional resume writer. "
                    "Write clean, structured, ATS-friendly resumes. "
                    "Use bullet points and clear section headings."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=1200
    )

    return response.choices[0].message.content
