from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.skill_extractor import extract_skills

def match_job_description(resume_text, job_description, resume_skills=None):
    """Compare resume and job description using TF-IDF and cosine similarity."""
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        vectors = vectorizer.fit_transform([resume_text, job_description])
        similarity = float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100)
    except ValueError:
        similarity = 0.0

    job_skills = extract_skills(job_description)
    resume_skills = resume_skills if resume_skills is not None else extract_skills(resume_text)
    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    coverage = (len(matched) / len(job_skills) * 100) if job_skills else 0.0
    return {
        "similarity": round(similarity, 1),
        "job_skills": job_skills,
        "matching_skills": matched,
        "missing_skills": missing,
        "skill_coverage": round(coverage, 1)
    }
