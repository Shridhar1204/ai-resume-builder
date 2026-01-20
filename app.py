import streamlit as st
import subprocess
from pathlib import Path
from streamlit_pdf_viewer import pdf_viewer
from llm_backend import generate_resume_ai

# ================= CONFIG =================
st.set_page_config(page_title="AI Resume Builder Pro", page_icon="🚀", layout="wide")

# ================= SESSION STATE =================
for k in ["projects", "experience", "certificates"]:
    if k not in st.session_state:
        st.session_state[k] = []

if "resume_ready" not in st.session_state:
    st.session_state.resume_ready = False
if "ats_score" not in st.session_state:
    st.session_state.ats_score = 0

# ================= ADVANCED CSS =================
st.markdown("""
<style>
    /* Main Background and Fonts */
    .main { background-color: #f8f9fa; }
    .center-title { font-size: 3.8rem; font-weight: 800; text-align: center; color: #1E3A8A; margin-bottom: 0; }
    .center-sub { font-size: 1.4rem; text-align: center; color: #4B5563; margin-bottom: 3rem; font-style: italic; }

    /* Section Styling */
    .section-box {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        border-left: 5px solid #1E3A8A;
    }

    /* Input Styling */
    label p { font-size: 1.15rem !important; font-weight: 700 !important; color: #6B7280 !important; }
    input, textarea { border-radius: 8px !important; }

    /* Tab Styling */
    .stTabs [data-baseweb="tab"] { font-size: 1.4rem !important; font-weight: 700 !important; padding: 1rem 3rem !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; }
    
    /* Button Styling */
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 700;
        border: none;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #2563EB;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)



# ================= SIDEBAR =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/942/942748.png", width=100)
    st.title("Settings")
    st.info("💡 **Tip:** Use 2-3 bullet points for experience to keep the resume to one page.")
    if st.button("🗑️ Reset Form", use_container_width=True):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# ================= HEADER =================
st.markdown("<div class='center-title'>🚀 AI Resume Builder</div>", unsafe_allow_html=True)
st.markdown("<div class='center-sub'>Transform your experience into a pixel-perfect PDF</div>", unsafe_allow_html=True)

# ================= HELPERS =================
def latex_safe(t):
    if not t: return ""
    return (t.replace("—", "--").replace("–", "-")
             .replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
             .replace("#", r"\#").replace("_", r"\_")
             .replace("{", r"\{").replace("}", r"\}"))

# ================= MAIN TABS =================
tabs = st.tabs(["📝 Build Your Profile", "📄 Preview & Export"])
build_tab, preview_tab = tabs[0], tabs[1]

with build_tab:
    # --- STEP 1: PERSONAL ---
    st.subheader("👤 Step 1: Personal Information")
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name", placeholder="John Doe")
            role = st.text_input("Professional Title", placeholder="Software Engineer")
        with c2:
            email = st.text_input("Email Address", placeholder="john@example.com")
            phone = st.text_input("Phone Number", placeholder="+1 234 567 890")
        location = st.text_input("Location (City, Country)", placeholder="New York, USA")

    # --- STEP 2: LINKS ---
    st.subheader("🔗 Step 2: Digital Presence")
    l_cols = st.columns(3)
    with l_cols[0]: linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/...")
    with l_cols[1]: github = st.text_input("GitHub URL", placeholder="github.com/...")
    with l_cols[2]: portfolio = st.text_input("Portfolio URL", placeholder="portfolio.com")

    # --- STEP 3: CONTENT ---
    st.divider()
    st.subheader("✍️ Step 3: Professional Content")
    
    st.write("### **Summary**")
    summary = st.text_area("Summary", height=120, label_visibility="collapsed", placeholder="Brief overview of your career...")

    st.write("### **Key Skills**")
    skills = st.text_area("Skills", height=100, label_visibility="collapsed", placeholder="Python, AWS, Project Management, etc.")

    # --- STEP 4: EXPERIENCE ---
    st.divider()
    col_exp, col_btn = st.columns([3, 1])
    with col_exp: st.subheader("💼 Step 4: Work Experience")
    with col_btn: 
        if st.button("➕ Add Work", use_container_width=True):
            st.session_state.experience.append({"role": "", "company": "", "date": "", "bullets": ["", ""]})

    for i, e in enumerate(st.session_state.experience):
        with st.expander(f"Work Experience {i+1} — {e['company'] if e['company'] else 'New'}", expanded=True):
            ec1, ec2 = st.columns(2)
            with ec1: e["role"] = st.text_input("Role", key=f"er{i}")
            with ec2: e["company"] = st.text_input("Company", key=f"ec{i}")
            e["date"] = st.text_input("Duration (e.g., Jan 2020 - Present)", key=f"ed{i}")
            for j in range(2):
                e["bullets"][j] = st.text_input(f"Key Achievement {j+1}", key=f"eb{i}{j}")
    
    # --- STEP 5: PROJECTS ---
    st.divider()
    col_proj, col_pbtn = st.columns([3, 1])
    with col_proj:
       st.subheader("🚀 Step 5: Projects")
    with col_pbtn:
       if st.button("➕ Add Project", use_container_width=True):
        st.session_state.projects.append({
            "title": "", "date": "", "bullets": ["", "", ""]
        })

    for i, p in enumerate(st.session_state.projects):
        with st.expander(f"Project {i+1} — {p['title'] if p['title'] else 'New'}", expanded=True):
          pc1, pc2 = st.columns(2)
        with pc1:
            p["title"] = st.text_input("Project Title", key=f"pt{i}")
        with pc2:
            p["date"] = st.text_input("Project Date", key=f"pd{i}")
        for j in range(3):
            p["bullets"][j] = st.text_input(
                f"Project Highlight {j+1}", key=f"pb{i}{j}"
            )


    # --- STEP 6: EDUCATION ---
    st.divider()
    st.subheader("🎓 Step 6: Education")
    etabs = st.tabs(["🏫 University", "🏫 Schooling"])
    
    with etabs[0]:
        st.write("#### Undergraduate / Postgraduate")
        uc1, uc2 = st.columns(2)
        with uc1:
            ug_degree = st.text_input("Degree Name", key="ug_deg")
            ug_college = st.text_input("Institution", key="ug_col")
        with uc2:
            ug_duration = st.text_input("Duration (Years)", key="ug_dur")
            ug_gpa = st.text_input("GPA / Grade", key="ug_gpa")
        ug_location = st.text_input("Institution Location", key="ug_loc")

    with etabs[1]:
        st.warning("Enter details for Class X and XII")
        sc1, sc2 = st.columns(2)
        with sc1:
            st.write("**Senior Secondary (XII)**")
            ss_school = st.text_input("XII School Name", key="ss_s")
            ss_board = st.text_input("XII Board", key="ss_b")
            ss_pct = st.text_input("XII Percentage", key="ss_p")
            ss_year = st.text_input("XII Year", key="ss_y")
        with sc2:
            st.write("**Secondary (X)**")
            sec_school = st.text_input("X School Name", key="sec_s")
            sec_board = st.text_input("X Board", key="sec_b")
            sec_pct = st.text_input("X Percentage", key="sec_p")
            sec_year = st.text_input("X Year", key="sec_y")

    # --- STEP 7: CERTIFICATES ---
    st.divider()
    col_cert, col_cbtn = st.columns([3, 1])
    with col_cert: st.subheader("📜 Step 7: Certificates")
    with col_cbtn: 
        if st.button("➕ Add Certificate", use_container_width=True):
            st.session_state.certificates.append({"name": "", "link": ""})

    for i, c in enumerate(st.session_state.certificates):
        with st.expander(f"Certificate {i+1}"):
            c["name"] = st.text_input("Certification Name", key=f"cn{i}")
            c["link"] = st.text_input("Verification Link", key=f"cl{i}")

   # -------- GENERATE BUTTON --------
    st.divider()
    if st.button("🚀 Generate Resume", type="primary", use_container_width=True):
        with st.spinner("Generating with AI..."):
            education_data = {
                "undergraduate": {"degree": ug_degree, "college": ug_college, "location": ug_location, "duration": ug_duration, "gpa": ug_gpa},
                "senior_secondary": {"school": ss_school, "year": ss_year, "board": ss_board, "pct": ss_pct},
                "secondary": {"school": sec_school, "year": sec_year, "board": sec_board, "pct": sec_pct}
            }

            raw_data = {
                "summary": summary, "skills": skills, "experience": st.session_state.experience,
                "projects": st.session_state.projects, "education": education_data,
                "certificates": st.session_state.certificates
            }

            ai = generate_resume_ai(raw_data)

            # --- BUILD LaTeX EXPERIENCE ---
            exp_tex = ""
            for e in ai["experience"]:
                exp_tex += f"\\textbf{{{latex_safe(e['role'])}}} -- {latex_safe(e['company'])} \\hfill {latex_safe(e['date'])} \\\\\n\\begin{{itemize}}\n"
                for b in e["bullets"][:2]:
                    exp_tex += f"\\item {latex_safe(b)}\n"
                exp_tex += "\\end{itemize}\n"

            # --- BUILD LaTeX PROJECTS ---
            proj_tex = ""
            for p in ai["projects"]:
                proj_tex += f"\\textbf{{{latex_safe(p['title'])}}} \\hfill {latex_safe(p['date'])} \\\\\n\\begin{{itemize}}\n"
                for b in p["bullets"]:
                    proj_tex += f"\\item {latex_safe(b)}\n"
                proj_tex += "\\end{itemize}\n"

            # --- BUILD LaTeX EDUCATION ---
            edu_items = []
            if ug_degree:
                edu_items.append(f"\\textbf{{{latex_safe(ug_degree)}}} -- {latex_safe(ug_college)}, {latex_safe(ug_location)} \\hfill {latex_safe(ug_duration)} \\\\ GPA: {latex_safe(ug_gpa)}")
            if ss_school:
                edu_items.append(f"\\textbf{{Class XII ({latex_safe(ss_board)})}} -- {latex_safe(ss_school)} \\hfill {latex_safe(ss_year)} \\\\ Percentage: {latex_safe(ss_pct)}")
            if sec_school:
                edu_items.append(f"\\textbf{{Class X ({latex_safe(sec_board)})}} -- {latex_safe(sec_school)} \\hfill {latex_safe(sec_year)} \\\\ Percentage: {latex_safe(sec_pct)}")
            edu_tex = " \\\\\n\\vspace{4pt}\n".join(edu_items)

            # --- BUILD LaTeX CERTIFICATES ---
            cert_tex = ""
            for c in st.session_state.certificates:
                if c["name"]:
                    if c["link"]:
                        link = c["link"] if c["link"].startswith("http") else f"https://{c['link']}"
                        cert_tex += f"\\href{{{link}}}{{{latex_safe(c['name'])}}} \\\\\n"
                    else:
                        cert_tex += f"{latex_safe(c['name'])} \\\\\n"

            # --- BUILD LaTeX LINKS ---
            l_list = []
            if linkedin: l_list.append(f"\\href{{{linkedin}}}{{LinkedIn}}")
            if github: l_list.append(f"\\href{{{github}}}{{GitHub}}")
            if portfolio: l_list.append(f"\\href{{{portfolio}}}{{Portfolio}}")
            links_tex = " \\quad | \\quad ".join(l_list)

            # --- ATS SCORE ---
            st.session_state.ats_score = min(95, 45 + len(ai["skills"]) * 2 + len(st.session_state.experience) * 7)

            # --- COMPILE ---
            template = Path("resume_template.tex").read_text()
            tex = template.format(
                NAME=name, ROLE=role, LOCATION=location, EMAIL=email, PHONE=phone, LINKS=links_tex,
                SUMMARY=latex_safe(ai["summary"]), SKILLS=" \\\\\n".join([latex_safe(s) for s in ai["skills"]]),
                EXPERIENCE=exp_tex, PROJECTS=proj_tex, EDUCATION=edu_tex, CERTIFICATES=cert_tex
            )
            Path("resume.tex").write_text(tex)
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "resume.tex"], stdout=subprocess.DEVNULL)
            st.session_state.resume_ready = True
            st.success("✅ Resume Ready!")
            st.balloons()

# ================= PREVIEW TAB =================
with preview_tab:
    if st.session_state.resume_ready:
        st.success("### Your Professional Resume is Ready!")
        c_p1, c_p2 = st.columns([2, 1])
        with c_p1:
            pdf_viewer("resume.pdf", width=800)
        with c_p2:
            st.write("#### 📊 Analysis")
            st.metric("ATS Compatibility", f"{st.session_state.ats_score}%")
            st.write("---")
            with open("resume.pdf", "rb") as f:
                st.download_button("📥 Download PDF", f, file_name=f"Resume_{name}.pdf", use_container_width=True)
    else:
        st.info("👋 **Start by filling in your details in the 'Build Your Profile' tab!**")