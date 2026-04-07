import streamlit as st
from pypdf import PdfReader
from groq import Groq
import os
import re

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Page config
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# Custom styling
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🚀 AI Resume Analyzer for GCC Jobs")
st.markdown("### Get hired in UAE 🇦🇪 | Saudi 🇸🇦 | Qatar 🇶🇦")
st.info("Upload your resume and get ATS score + job match insights instantly")

# File upload
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")

st.warning("⚠️ For best results, upload a well-structured resume")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    st.subheader("📄 Resume Preview")
    st.write(text[:1200])

    if st.button("🚀 Analyze Resume"):
        with st.spinner("🔍 Analyzing your resume for GCC market..."):

            prompt = f"""
You are an expert ATS system and GCC recruiter.
Analyze the resume and return output in EXACT format:
ATS Score: (number out of 100)
Job Match Score (GCC Market): (number out of 100)
Strengths:
- point
Missing Skills:
- point
Improvements:
- point
Best Job Roles (UAE, Saudi Arabia, Qatar):
- role
Keep it structured and professional.
Resume:
{text}
"""

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

        # Display Results
        st.markdown("## 📊 Analysis Result")

        # ATS Score
        score_match = re.search(r"ATS Score:\s*(\d+)", result)
        if score_match:
            score = int(score_match.group(1))
            st.progress(score)
            st.success(f"✅ ATS Score: {score}/100")

        # Job Match Score
        job_match = re.search(r"Job Match Score.*:\s*(\d+)", result)
        if job_match:
            jm_score = int(job_match.group(1))
            st.progress(jm_score)
            st.info(f"🎯 Job Match Score: {jm_score}/100")

        # Structured output
        st.markdown("### 📄 Detailed Feedback")
        sections = result.split("\n\n")
        for section in sections:
            st.markdown(section)

        # Download button
        st.download_button(
            label="📥 Download Analysis Report",
            data=result,
            file_name="resume_analysis.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.caption("Built by Faraz Mubeen Haider | AI Engineer | Open to GCC Opportunities")
