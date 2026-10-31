from modules.text_preprocessing import clean_text

SKILL_CATALOG = [
    "python", "java", "c", "c++", "javascript", "typescript", "html", "css",
    "flask", "django", "react", "node.js", "sql", "mysql", "sqlite", "mongodb",
    "git", "github", "linux", "windows", "data structures", "algorithms",
    "machine learning", "deep learning", "artificial intelligence", "nlp",
    "natural language processing", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "matplotlib", "seaborn", "excel", "power bi",
    "tableau", "rest api", "api", "oop", "docker", "aws", "azure",
    "communication", "problem solving", "teamwork"
]

def extract_skills(text):
    normalized = clean_text(text)
    found = []
    for skill in SKILL_CATALOG:
        # Word boundaries reduce accidental matches (e.g. C inside "communication").
        import re
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            found.append(skill)
    return sorted(set(found))
