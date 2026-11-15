from llm import ask_json

RESUME_PROMPT = """Extract from this resume as JSON with exactly these keys:
{{"skills": [], "tools": [], "years_experience": 0,
  "job_titles": [], "education": [], "achievements": []}}
Only include what is explicitly stated. Do not guess.

RESUME:
{text}"""

JD_PROMPT = """Extract from this job description as JSON with exactly these keys:
{{"required_skills": [], "nice_to_have": [], "min_years_experience": 0,
  "job_title": "", "responsibilities": []}}

JOB DESCRIPTION:
{text}"""

def extract_resume(text):
    return ask_json(RESUME_PROMPT.format(text=text))

def extract_jd(text):
    return ask_json(JD_PROMPT.format(text=text))