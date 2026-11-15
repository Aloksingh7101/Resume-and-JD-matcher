from llm import ask

PROMPT = """You are a career coach. Given the resume, job description, and scores:

RESUME:
{resume}

JOB DESCRIPTION:
{jd}

SCORES: {scores}

Give:
1. Top 3 strengths for this role
2. Top gaps, and how to address each honestly
3. 3-5 resume bullets rewritten to better fit this JD

Rules: NEVER invent experience, skills, or numbers the candidate does not have.
Only rephrase and re-emphasize what is already in the resume."""

def analyze(resume_text, jd_text, scores):
    return ask(PROMPT.format(resume=resume_text, jd=jd_text, scores=scores))