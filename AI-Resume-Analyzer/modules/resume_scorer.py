import re

def calculate_resume_score(resume_text, skills, matching):
    """Transparent rule-based estimate; not an official ATS score."""
    text = resume_text.lower()
    categories = {
        "Skills": min(20, len(skills) * 2),
        "Projects": 15 if any(x in text for x in ["project", "developed", "built"]) else 5,
        "Education": 15 if any(x in text for x in ["education", "b.tech", "bachelor", "degree", "university", "college"]) else 0,
        "Experience": 15 if any(x in text for x in ["experience", "internship", "worked", "employment"]) else 5,
        "Contact details": 10 if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", resume_text) else 0,
        "Job relevance": round(25 * matching["skill_coverage"] / 100)
    }
    return {
        "overall": min(100, int(sum(categories.values()))),
        "categories": categories,
        "explanation": "A transparent estimate based on detected skills, common resume sections, contact details, and job-skill coverage."
    }
