import streamlit as st
from llm_backend import generate_resume_content

st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="📄",
    layout="wide"
)

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1>🚀 AI Resume & Portfolio Builder</h1>", unsafe_allow_html=True)
st.write("Generate professional resumes using AI")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")
    role = st.text_input("Target Job Role")
    education = st.text_area("Education")
    skills = st.text_area("Skills (comma separated)")
    projects = st.text_area("Projects")
    experience = st.text_area("Experience")

    generate = st.button("✨ Generate Resume")

with col2:
    st.subheader("📄 AI Output")
    output = st.empty()

if generate:
    if not name or not skills:
        st.warning("Please fill required fields")
    else:
        with st.spinner("Generating resume..."):
            result = generate_resume_content(
                name, role, education, skills, projects, experience
            )
            output.text_area("Generated Resume", result, height=500)
