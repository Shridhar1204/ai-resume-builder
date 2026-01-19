import os
import subprocess
from pathlib import Path
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from llm_backend import generate_resume_ai

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="📄",
    layout="wide"
)

# ---------------- SESSION ----------------
if "projects" not in st.session_state:
    st.session_state.projects = []
if "resume_ready" not in st.session_state:
    st.session_state.resume_ready = False

# ---------------- UI CSS ----------------
st.markdown("""
<style>
html, body { font-size:16px; }
.center-title { text-align:center; font-size:3rem; font-weight:700; }
.center-subtitle { text-align:center; font-size:1.3rem; color:#666; }
.stTabs [data-baseweb="tab"] { font-size:1.2rem; padding:1rem; }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='center-title'>AI Resume Builder</div>", unsafe_allow_html=True)
st.markdown("<div class='center-subtitle'>Generate a professional resume with pixel-perfect formatting</div>", unsafe_allow_html=True)

tabs = st.tabs(["📝 Build Resume", "📄 Preview & Download"])

# ================= BUILD TAB =================
with tabs[0]:
    st.subheader("Personal Information")
    name = st.text_input("Full Name *")
    role = st.text_input("Professional Title *")
    location = st.text_input("Location *")
    email = st.text_input("Email *")
    phone = st.text_input("Phone *")

    st.divider()
    summary = st.text_area("Summary (rough is fine)")
    skills = st.text_area("Skills (rough list is fine)")

    st.divider()
    st.subheader("Projects")

    if st.button("➕ Add Project"):
        st.session_state.projects.append({
            "title": "",
            "date": "",
            "bullets": ["", "", ""]
        })

    for i, p in enumerate(st.session_state.projects):
        with st.expander(f"Project {i+1}", expanded=True):
            p["title"] = st.text_input("Title", p["title"], key=f"t{i}")
            p["date"] = st.text_input("Date", p["date"], key=f"d{i}")
            for j in range(3):
                p["bullets"][j] = st.text_input(
                    f"Bullet {j+1}", p["bullets"][j], key=f"b{i}{j}"
                )
            if st.button("Remove", key=f"r{i}"):
                st.session_state.projects.pop(i)
                st.rerun()

    st.divider()
    education = st.text_area("Education")
    certificates = st.text_area("Certificates (optional)")

    generate = st.button("🚀 Generate Resume", type="primary")

# ================= GENERATE =================
if generate:
    raw_data = {
        "summary": summary,
        "skills": skills,
        "projects": st.session_state.projects,
        "education": education,
        "certificates": certificates
    }

    with st.spinner("AI is improving your resume..."):
        ai = generate_resume_ai(raw_data)

        skills_tex = " \\\\\n".join(ai["skills"])

        projects_tex = ""
        for p in ai["projects"]:
            projects_tex += f"""
\\textbf{{{p['title']}}} \\hfill {p['date']} \\\\
\\begin{{itemize}}
"""
            for b in p["bullets"]:
                projects_tex += f"\\item {b}\n"
            projects_tex += "\\end{itemize}\n"

        template = Path("resume_template.tex").read_text()
        tex = template.format(
            NAME=name,
            ROLE=role,
            LOCATION=location,
            EMAIL=email,
            PHONE=phone,
            LINKS="",
            SUMMARY=ai["summary"],
            SKILLS=skills_tex,
            PROJECTS=projects_tex,
            EDUCATION=ai["education"],
            CERTIFICATES=ai["certificates"]
        )

        Path("resume.tex").write_text(tex)
        subprocess.run(["pdflatex", "resume.tex"], stdout=subprocess.DEVNULL)

        st.session_state.resume_ready = True
        st.success("✅ Resume generated successfully!")

# ================= PREVIEW TAB =================
with tabs[1]:
    if not st.session_state.resume_ready:
        st.info("Generate a resume first")
    else:
        pdf_viewer("resume.pdf", width=800)
        with open("resume.pdf", "rb") as f:
            st.download_button("⬇ Download Resume", f, "Resume.pdf")
