import streamlit as st
from llm_backend import generate_resume_content
from pdf_generator import generate_resume_pdf
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="📄",
    layout="wide"
)

# ---------- SESSION STATE INIT ----------
if "resume_ready" not in st.session_state:
    st.session_state.resume_ready = False

# ---------- HEADER ----------
st.title("📄 AI Resume Builder")
st.write(
    "Create a **professional, ATS-friendly resume** using AI and download it as a PDF."
)

st.divider()

# ---------- TABS ----------
tab1, tab2 = st.tabs(["📝 Build Resume", "📄 Preview & Download"])

# ---------- TAB 1: INPUT ----------
with tab1:
    st.subheader("Candidate Details")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        role = st.text_input("Target Job Role")
        education = st.text_area("Education", height=120)

    with col2:
        skills = st.text_area("Skills (comma separated)", height=120)
        projects = st.text_area("Projects", height=120)
        experience = st.text_area("Experience", height=120)

    generate = st.button("🚀 Generate Professional Resume", type="primary")

# ---------- GENERATION LOGIC ----------
if generate:
    if not name or not skills:
        st.error("Please provide at least your name and skills.")
    else:
        with st.spinner("Generating resume using AI..."):
            resume_text = generate_resume_content(
                name, role, education, skills, projects, experience
            )

            generate_resume_pdf(
                "generated_resume.pdf",
                name,
                resume_text
            )

            # ✅ SET STATE
            st.session_state.resume_ready = True

        st.success("Resume generated successfully! Go to Preview & Download tab.")

        # ✅ FORCE RERUN SO TABS UPDATE
        st.rerun()

# ---------- TAB 2: OUTPUT ----------
with tab2:
    if not st.session_state.resume_ready:
        st.info("Generate a resume first to preview it here.")
    else:
        st.subheader("📄 Resume Preview")

        pdf_viewer("generated_resume.pdf", width=750)

        with open("generated_resume.pdf", "rb") as f:
            st.download_button(
                "⬇ Download Resume PDF",
                f,
                file_name="AI_Resume.pdf",
                mime="application/pdf",
                type="primary"
            )
