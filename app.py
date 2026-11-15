import streamlit as st
from reader import read_file
from extractor import extract_resume, extract_jd
from matcher import final_score
from analysis import analyze

st.set_page_config(page_title="Resume & JD Matcher", layout="wide")
st.title("Smart Resume & JD Matcher")

col1, col2 = st.columns(2)
resume_file = col1.file_uploader("Upload resume", type=["pdf", "docx", "txt"])
jd_text = col2.text_area("Paste job description", height=250)

if st.button("Analyze"):
    if not resume_file or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        try:
            with st.spinner("Analyzing..."):
                resume_text = read_file(resume_file)
                resume = extract_resume(resume_text)
                jd = extract_jd(jd_text)
                scores = final_score(resume_text, resume, jd)
                report = analyze(resume_text, jd_text, scores)

            st.metric("Overall Match", f"{scores['total']}%")
            a, b, c = st.columns(3)
            a.metric("Skill overlap", f"{scores['skill_overlap']}%")
            b.metric("Semantic fit", f"{scores['semantic']}%")
            c.metric("Experience", f"{scores['experience']}%")

            t1, t2 = st.tabs(["Skills", "AI Suggestions"])
            with t1:
                st.success("Matched: " + (", ".join(scores["matched"]) or "none"))
                st.error("Missing: " + (", ".join(scores["missing"]) or "none"))
            with t2:
                st.markdown(report)
        except Exception as e:
            st.error(f"Something went wrong: {e}")