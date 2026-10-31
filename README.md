# AI Resume Analyzer

A beginner-friendly Flask college project that extracts text from PDF/DOCX resumes, identifies skills, compares a resume with a job description using TF-IDF and cosine similarity, calculates a transparent heuristic score, and generates improvement recommendations.

## Features
- PDF and DOCX resume upload (maximum 5 MB)
- Resume text extraction
- Dictionary-based skill extraction
- TF-IDF + cosine similarity job matching
- Matching and missing skill identification
- Transparent rule-based resume score
- Improvement recommendations
- SQLite analysis history
- Chart.js dashboard
- Downloadable PDF report

## Requirements
- Python 3.10 or newer
- VS Code (recommended)

## Setup on Windows

Open the project folder in VS Code, then run these commands in the terminal:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

If PowerShell blocks virtual-environment activation, use this for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Open the local address printed by Flask, usually `http://127.0.0.1:5000`.

## Project structure

```text
AI-Resume-Analyzer/
├── app.py
├── requirements.txt
├── README.md
├── database/
├── modules/
├── templates/
├── static/css/
├── uploads/
└── reports/
```

## How the analysis works
1. `resume_parser.py` extracts text from the uploaded file.
2. `skill_extractor.py` searches for terms in a small editable skill dictionary.
3. `job_matcher.py` vectorizes resume and job description text with TF-IDF and calculates cosine similarity.
4. `resume_scorer.py` calculates a transparent educational score using simple rules.
5. `recommendation_engine.py` creates suggestions from detected gaps.
6. `db.py` stores analysis summaries in SQLite.
7. `report_generator.py` creates a PDF report.

## Important limitations
- This is an educational project, not a real commercial ATS.
- The score is heuristic and should not be treated as an official hiring score.
- Skill extraction uses a fixed dictionary, so it may miss synonyms or skills not listed. Edit `SKILL_CATALOG` in `modules/skill_extractor.py` to expand it.
- Scanned/image-only PDFs may need OCR, which is not included in this basic version.
- Resume files are deleted from the uploads folder after analysis. Analysis summaries and the pasted job description remain in the local SQLite database.
- Chart.js and Google Fonts are loaded from CDNs, so those visual resources need internet access. The core analysis runs locally.

## Suggested viva topics
- Flask routes and request handling
- File uploads and validation
- PDF/DOCX text extraction
- Regular expressions
- TF-IDF vectorization
- Cosine similarity
- SQLite CRUD operations
- Rule-based scoring and recommendation logic
