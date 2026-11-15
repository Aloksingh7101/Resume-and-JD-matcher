import numpy as np
from google.genai import types
from llm import client

EMBED_MODEL = "gemini-embedding-001"

def embed(texts, batch_size=50):
    vectors = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        result = client.models.embed_content(
            model=EMBED_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(output_dimensionality=768),
        )
        vectors.extend(e.values for e in result.embeddings)
    v = np.array(vectors)
    return v / np.linalg.norm(v, axis=1, keepdims=True)

def skill_overlap(resume_skills, jd_skills):
    r = {s.lower().strip() for s in resume_skills}
    j = [s.lower().strip() for s in jd_skills]
    matched = [s for s in j if s in r]
    missing = [s for s in j if s not in r]
    score = len(matched) / len(j) if j else 0
    return score, matched, missing

def semantic_score(resume_text, jd_items):
    chunks = [c.strip() for c in resume_text.split("\n") if len(c.strip()) > 20]
    if not chunks or not jd_items:
        return 0.0
    c_emb = embed(chunks)
    j_emb = embed(jd_items)
    sims = j_emb @ c_emb.T
    return float(np.clip(sims.max(axis=1), 0, 1).mean())

def experience_score(resume_years, min_years):
    if not min_years:
        return 1.0
    return min(resume_years / min_years, 1.0)

def final_score(resume_text, resume, jd):
    s1, matched, missing = skill_overlap(
        resume.get("skills", []) + resume.get("tools", []),
        jd.get("required_skills", []))
    s2 = semantic_score(
        resume_text,
        jd.get("required_skills", []) + jd.get("responsibilities", []))
    s3 = experience_score(
        resume.get("years_experience", 0), jd.get("min_years_experience", 0))
    total = 0.4 * s1 + 0.4 * s2 + 0.2 * s3
    return {
        "total": round(total * 100),
        "skill_overlap": round(s1 * 100),
        "semantic": round(s2 * 100),
        "experience": round(s3 * 100),
        "matched": matched,
        "missing": missing,
    }