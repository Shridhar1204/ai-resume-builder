import subprocess
from pathlib import Path

def generate_resume_pdf_latex(data, output_pdf="resume.pdf"):
    template = Path("resume_template.tex").read_text()

    tex = template.format(
        NAME=data["name"],
        ROLE=data["role"],
        LOCATION=data["location"],
        EMAIL=data["email"],
        PHONE=data["phone"],
        LINKS=data["links"],
        SUMMARY=data["summary"],
        SKILLS=data["skills"],
        PROJECTS=data["projects"],
        EDUCATION=data["education"],
        CERTIFICATES=data["certificates"]
    )

    tex_file = Path("resume.tex")
    tex_file.write_text(tex)

    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_file.name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    Path("resume.pdf").rename(output_pdf)
