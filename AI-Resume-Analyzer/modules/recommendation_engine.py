import re

def generate_recommendations(resume_text, skills, matching):
    text = resume_text.lower()
    tips = []
    if not skills:
        tips.append("Add a clearly labelled Skills section containing relevant skills you genuinely have.")
    if matching["missing_skills"]:
        tips.append("The job description mentions these skills that were not detected: " +
                    ", ".join(matching["missing_skills"][:10]) +
                    ". Add them only if you actually know them.")
    if "project" not in text:
        tips.append("Add academic or personal projects. Explain the problem, tools used, and your contribution.")
    if not re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", resume_text):
        tips.append("Include a professional email address in your contact section.")
    if not any(word in text for word in ["achieved", "improved", "increased", "reduced", "built", "created", "implemented"]):
        tips.append("Start project and experience bullet points with action verbs and include measurable outcomes when possible.")
    if len(resume_text.split()) < 180:
        tips.append("The extracted resume looks brief. Add relevant details about education, projects, skills, and experience without filler.")
    if not tips:
        tips.append("Good coverage. Tailor your summary and project bullet points to the exact role.")
    return tips
