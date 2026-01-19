import streamlit as st
import subprocess
from pathlib import Path
from streamlit_pdf_viewer import pdf_viewer
from llm_backend import generate_resume_ai

# ================= CONFIG =================
st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="wide")

# ================= SESSION STATE =================
for k in ["projects", "experience", "certificates"]:
    if k not in st.session_state:
        st.session_state[k] = []

if "resume_ready" not in st.session_state:
    st.session_state.resume_ready = False
if "ats_score" not in st.session_state:
    st.session_state.ats_score = 0
if "go_preview" not in st.session_state:
    st.session_state.go_preview = False

# ================= CSS =================
st.markdown("""
<style>
.center-title{font-size:3rem;font-weight:700;text-align:center}
.center-sub{font-size:1.3rem;text-align:center;color:#666;margin-bottom:2rem}
.stTabs [data-baseweb="tab"]{font-size:1.3rem;padding:1.1rem 2rem}
label{font-size:1.05rem;font-weight:600}
textarea,input{font-size:1.05rem}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='center-title'>AI Resume Builder</div>", unsafe_allow_html=True)
st.markdown("<div class='center-sub'>Generate a professional resume with pixel-perfect formatting</div>", unsafe_allow_html=True)

# ================= HELPERS =================
def latex_safe(t):
    if not t:
        return ""
    return (t.replace("—", "--").replace("–", "-")
             .replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
             .replace("#", r"\#").replace("_", r"\_")
             .replace("{", r"\{").replace("}", r"\}"))

# ================= TABS =================
tabs = st.tabs(["📝 Build Resume", "📄 Preview & Download"])
build_tab = tabs[0]
preview_tab = tabs[1]

# ================= BUILD TAB =================
with build_tab:

    # -------- PERSONAL --------
    st.subheader("Personal Information")
    name = st.text_input("Full Name", key="name")
    role = st.text_input("Professional Title", key="role")
    location = st.text_input("Location", key="loc_main")
    email = st.text_input("Email", key="email")
    phone = st.text_input("Phone", key="phone")

    # -------- LINKS --------
    st.subheader("Links (optional)")
    l1, l2, l3 = st.tabs(["LinkedIn", "GitHub", "Portfolio"])
    with l1:
        linkedin = st.text_input("LinkedIn URL", key="linkedin")
    with l2:
        github = st.text_input("GitHub URL", key="github")
    with l3:
        portfolio = st.text_input("Portfolio URL", key="portfolio")

    st.markdown("---")

    # -------- SUMMARY --------
    st.markdown("### **Professional Summary**")
    summary = st.text_area("Summary", key="summary", height=150, label_visibility="collapsed")

    # -------- SKILLS --------
    st.markdown("### **Technical Skills**")
    skills = st.text_area("Skills", key="skills", height=120, label_visibility="collapsed")

    # -------- EXPERIENCE --------
    st.divider()
    st.subheader("Experience")
    if st.button("➕ Add Experience", key="add_exp"):
        st.session_state.experience.append(
            {"role": "", "company": "", "date": "", "bullets": ["", ""]}  # ✅ ONLY 2 BULLETS
        )

    for i, e in enumerate(st.session_state.experience):
        with st.expander(f"Experience {i+1}", expanded=True):
            e["role"] = st.text_input("Role", e["role"], key=f"er{i}")
            e["company"] = st.text_input("Company", e["company"], key=f"ec{i}")
            e["date"] = st.text_input("Duration", e["date"], key=f"ed{i}")
            for j in range(2):  # ✅ ONLY 2 BULLETS
                e["bullets"][j] = st.text_input(f"Bullet {j+1}", e["bullets"][j], key=f"eb{i}{j}")

    # -------- PROJECTS --------
    st.divider()
    st.subheader("Projects")
    if st.button("➕ Add Project", key="add_proj"):
        st.session_state.projects.append(
            {"title": "", "date": "", "bullets": ["", "", ""]}
        )

    for i, p in enumerate(st.session_state.projects):
        with st.expander(f"Project {i+1}", expanded=True):
            p["title"] = st.text_input("Title", p["title"], key=f"pt{i}")
            p["date"] = st.text_input("Date", p["date"], key=f"pd{i}")
            for j in range(3):
                p["bullets"][j] = st.text_input(f"Bullet {j+1}", p["bullets"][j], key=f"pb{i}{j}")

    # -------- EDUCATION --------
    st.divider()
    st.subheader("Education")
    ug_tab, pg_tab, school_tab = st.tabs(["Undergraduate", "Postgraduate", "School"])

    with ug_tab:
        ug_degree = st.text_input("Degree", key="ug_deg")
        ug_college = st.text_input("College", key="ug_col")
        ug_location = st.text_input("Location", key="ug_loc")
        ug_duration = st.text_input("Duration", key="ug_dur")
        ug_gpa = st.text_input("GPA", key="ug_gpa")

    with pg_tab:
        pg_degree = st.text_input("PG Degree", key="pg_deg")
        pg_college = st.text_input("PG College", key="pg_col")
        pg_duration = st.text_input("PG Duration", key="pg_dur")
        pg_gpa = st.text_input("PG GPA", key="pg_gpa")

    with school_tab:
        st.write("#### Senior Secondary (Class XII)")
        ss_school = st.text_input("School Name", key="ss_school")
        col_ss1, col_ss2, col_ss3 = st.columns(3)
        with col_ss1: ss_board = st.text_input("Board (e.g. CBSE)", key="ss_board")
        with col_ss2: ss_year = st.text_input("Year", key="ss_year")
        with col_ss3: ss_pct = st.text_input("Percentage/CGPA", key="ss_pct")
        
        st.divider()
        
        st.write("#### Secondary (Class X)")
        sec_school = st.text_input("School Name ", key="sec_school")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1: sec_board = st.text_input("Board (e.g. ICSE)", key="sec_board")
        with col_s2: sec_year = st.text_input("Year ", key="sec_year")
        with col_s3: sec_pct = st.text_input("Percentage/CGPA ", key="sec_pct")

    # -------- CERTIFICATES --------
    st.divider()
    st.subheader("Certificates")
    if st.button("➕ Add Certificate", key="add_cert"):
        st.session_state.certificates.append({"name": "", "link": ""})

    for i, c in enumerate(st.session_state.certificates):
        with st.expander(f"Certificate {i+1}", expanded=True):
            c["name"] = st.text_input("Certificate Name", c["name"], key=f"cn{i}")
            c["link"] = st.text_input("Certificate Link", c["link"], key=f"cl{i}")

    # -------- GENERATE --------
    if st.button("🚀 Generate Resume", type="primary"):
        education = {
            "undergraduate": {
                "degree": ug_degree, "college": ug_college,
                "location": ug_location, "duration": ug_duration, "gpa": ug_gpa
            }
        }
        if pg_degree:
            education["postgraduate"] = {
                "degree": pg_degree, "college": pg_college,
                "duration": pg_duration, "gpa": pg_gpa
            }
        if ss_school:
            education["senior_secondary"] = {"school": ss_school, "year": ss_year}
        if sec_school:
            education["secondary"] = {"school": sec_school, "year": sec_year}

        raw_data = {
            "summary": summary,
            "skills": skills,
            "experience": st.session_state.experience,
            "projects": st.session_state.projects,
            "education": education,
            "certificates": st.session_state.certificates
        }

        ai = generate_resume_ai(raw_data)

        # ================= BUILD LaTeX =================
        experience_tex = ""
        for e in ai["experience"]:
            experience_tex += f"\\textbf{{{latex_safe(e['role'])}}} -- {latex_safe(e['company'])} \\hfill {latex_safe(e['date'])} \\\\\n\\begin{{itemize}}\n"
            for b in e["bullets"][:2]:  # ✅ FORCE 2 BULLETS
                experience_tex += f"\\item {latex_safe(b)}\n"
            experience_tex += "\\end{itemize}\n"

        projects_tex = ""
        for p in ai["projects"]:
            projects_tex += f"\\textbf{{{latex_safe(p['title'])}}} \\hfill {latex_safe(p['date'])} \\\\\n\\begin{{itemize}}\n"
            for b in p["bullets"]:
                projects_tex += f"\\item {latex_safe(b)}\n"
            projects_tex += "\\end{itemize}\n"

        # ================= BUILD EDUCATION LaTeX =================
        edu_items = []
        
        # Undergraduate
        if ug_degree:
            edu_items.append(f"\\textbf{{{latex_safe(ug_degree)}}} -- {latex_safe(ug_college)}, {latex_safe(ug_location)} \\hfill {latex_safe(ug_duration)} \\\\ GPA: {latex_safe(ug_gpa)}")
        
        # Postgraduate
        if pg_degree:
            edu_items.append(f"\\textbf{{{latex_safe(pg_degree)}}} -- {latex_safe(pg_college)} \\hfill {latex_safe(pg_duration)} \\\\ GPA: {latex_safe(pg_gpa)}")
            
        # Senior Secondary
        if ss_school:
            ss_line = f"\\textbf{{Class XII ({latex_safe(ss_board)})}} -- {latex_safe(ss_school)} \\hfill {latex_safe(ss_year)} \\\\ Percentage: {latex_safe(ss_pct)}"
            edu_items.append(ss_line)
            
        # Secondary
        if sec_school:
            sec_line = f"\\textbf{{Class X ({latex_safe(sec_board)})}} -- {latex_safe(sec_school)} \\hfill {latex_safe(sec_year)} \\\\ Percentage: {latex_safe(sec_pct)}"
            edu_items.append(sec_line)

        education_tex = " \\\\\n\\vspace{4pt}\n".join(edu_items)

# ================= BUILD CERTIFICATES LaTeX =================
        certificates_tex = ""
        for c in st.session_state.certificates:
            if c["name"]:
                # If there is a link, wrap the name in a clickable href
                if c["link"]:
                    # Ensure the link starts with http if not present
                    clean_link = c["link"] if c["link"].startswith("http") else f"https://{c['link']}"
                    certificates_tex += f"\\href{{{clean_link}}}{{{latex_safe(c['name'])}}} \\\\\n"
                else:
                    certificates_tex += f"{latex_safe(c['name'])} \\\\\n"

        links = []
        if linkedin: links.append(f"\\href{{{linkedin}}}{{LinkedIn}}")
        if github: links.append(f"\\href{{{github}}}{{GitHub}}")
        if portfolio: links.append(f"\\href{{{portfolio}}}{{Portfolio}}")
        links_tex = " \\quad | \\quad ".join(links)

        st.session_state.ats_score = min(
            95,
            40 + len(ai["skills"]) * 3 + len(st.session_state.experience) * 8 + len(st.session_state.projects) * 6
        )

        template = Path("resume_template.tex").read_text()
        tex = template.format(
            NAME=name,
            ROLE=role,
            LOCATION=location,
            EMAIL=email,
            PHONE=phone,
            LINKS=links_tex,
            SUMMARY=latex_safe(ai["summary"]),
            SKILLS=" \\\\\n".join([latex_safe(s) for s in ai["skills"]]),
            EXPERIENCE=experience_tex,
            PROJECTS=projects_tex,
            EDUCATION=education_tex,
            CERTIFICATES=certificates_tex
        )

        # ... (All your LaTeX build and subprocess code stays here) ...

        Path("resume.tex").write_text(tex)
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "resume.tex"], stdout=subprocess.DEVNULL)

        # ✅ Set state to True
        st.session_state.resume_ready = True
        
        # ✅ Show success message (Remove st.rerun() so this actually stays visible)
        st.success("✅ Resume generated successfully! Click the '📄 Preview & Download' tab above.")
        st.balloons()
# ================= PREVIEW TAB =================
with preview_tab:
    if st.session_state.resume_ready:
        st.subheader("ATS Score")
        st.progress(st.session_state.ats_score / 100)
        st.caption(f"{st.session_state.ats_score}% match for ATS systems")

        pdf_viewer("resume.pdf", width=800, key=str(Path("resume.pdf").stat().st_mtime))
        with open("resume.pdf", "rb") as f:
            st.download_button("⬇ Download Resume", f, "Resume.pdf")
    else:
        st.info("Generate resume first")
