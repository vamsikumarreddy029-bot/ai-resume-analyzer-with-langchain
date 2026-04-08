import streamlit as st
from pipeline import run_pipeline
import PyPDF2
import docx

st.set_page_config(page_title="AI Resume Optimizer", layout="wide")

st.title("🚀 AI Resume Optimizer (Multi-LLM)")

# -------- LLM SELECT --------
provider = st.selectbox("Select LLM", ["OpenAI", "Gemini", "Claude"])
api_key = st.text_input("Enter API Key", type="password")

# -------- INPUT --------
option = st.radio("Choose Input:", ["Paste Text", "Upload File"])
resume_text = ""

if option == "Paste Text":
    resume_text = st.text_area("Paste Resume", height=300)

else:
    file = st.file_uploader("Upload Resume", type=["txt", "pdf", "docx"])

    if file:
        ext = file.name.split(".")[-1]

        if ext == "txt":
            resume_text = file.read().decode("utf-8", errors="ignore")

        elif ext == "pdf":
            pdf = PyPDF2.PdfReader(file)
            for page in pdf.pages:
                resume_text += page.extract_text() or ""

        elif ext == "docx":
            doc = docx.Document(file)
            for p in doc.paragraphs:
                resume_text += p.text + "\n"

# -------- RUN --------
if st.button("Optimize Resume"):

    if not api_key:
        st.error("Enter API key")
    elif not resume_text.strip():
        st.error("Enter resume")
    else:
        with st.spinner("Processing..."):
            result = run_pipeline(resume_text, provider, api_key)

        if "error" in result:
            st.error(result["error"])

        else:
            ats = result.get("ats", {})

            st.subheader("📊 ATS Score")
            st.metric("Score", ats.get("ats_score", "N/A"))

            st.subheader("💡 Suggestions")
            for s in ats.get("suggestions", []):
                st.write("•", s)

            st.subheader("🧠 Classification")
            st.json(result.get("classification", {}))

            st.subheader("🚀 Enhanced Resume (Editable)")
            edited = st.text_area("", result["enhanced_resume"], height=300)

            st.download_button(
                "Download Resume",
                edited,
                "optimized_resume.txt"
            )