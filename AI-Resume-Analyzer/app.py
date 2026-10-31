import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from modules.resume_parser import extract_resume_text
from modules.skill_extractor import extract_skills
from modules.job_matcher import match_job_description
from modules.resume_scorer import calculate_resume_score
from modules.recommendation_engine import generate_recommendations
from database.db import init_db, save_analysis, get_recent_analyses, get_analysis
from modules.report_generator import generate_pdf_report

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-before-deployment")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
init_db()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "GET":
        return render_template("upload.html")

    resume = request.files.get("resume")
    job_description = request.form.get("job_description", "").strip()
    if not resume or not resume.filename:
        flash("Please choose a resume file.", "error")
        return redirect(url_for("analyze"))
    if not allowed_file(resume.filename):
        flash("Only PDF and DOCX files are supported.", "error")
        return redirect(url_for("analyze"))
    if len(job_description) < 20:
        flash("Please enter a job description of at least 20 characters.", "error")
        return redirect(url_for("analyze"))

    original_name = secure_filename(resume.filename)
    unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{original_name}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)
    resume.save(file_path)

    try:
        resume_text = extract_resume_text(file_path)
        if len(resume_text.strip()) < 40:
            raise ValueError("Not enough readable text found. Try a text-based PDF or DOCX file.")

        skills = extract_skills(resume_text)
        matching = match_job_description(resume_text, job_description, skills)
        score = calculate_resume_score(resume_text, skills, matching)
        recommendations = generate_recommendations(resume_text, skills, matching)

        analysis_id = save_analysis(
            filename=original_name, score=score["overall"],
            match=matching["similarity"], skills=skills,
            missing=matching["missing_skills"],
            recommendations=recommendations, job_description=job_description
        )
        result = {
            "id": analysis_id, "filename": original_name,
            "score": score, "matching": matching, "skills": skills,
            "recommendations": recommendations,
            "resume_preview": resume_text[:1600]
        }
        return render_template("dashboard.html", result=result)
    except Exception as exc:
        flash(f"Analysis failed: {exc}", "error")
        return redirect(url_for("analyze"))
    finally:
        try:
            os.remove(file_path)
        except OSError:
            pass

@app.route("/history")
def history():
    return render_template("history.html", analyses=get_recent_analyses())

@app.route("/report/<int:analysis_id>")
def report(analysis_id):
    item = get_analysis(analysis_id)
    if not item:
        flash("Analysis not found.", "error")
        return redirect(url_for("history"))
    path = os.path.join(REPORT_FOLDER, f"analysis_{analysis_id}.pdf")
    generate_pdf_report(item, path)
    return send_file(path, as_attachment=True, download_name=f"resume_analysis_{analysis_id}.pdf")

@app.errorhandler(413)
def too_large(_error):
    flash("File is too large. Maximum size is 5 MB.", "error")
    return redirect(url_for("analyze"))

if __name__ == "__main__":
    app.run(debug=True)
