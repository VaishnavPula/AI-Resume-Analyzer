import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resume_analyzer.db")

def get_connection():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with get_connection() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                score INTEGER NOT NULL,
                match_score REAL NOT NULL,
                skills TEXT NOT NULL,
                missing_skills TEXT NOT NULL,
                recommendations TEXT NOT NULL,
                job_description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_analysis(filename, score, match, skills, missing, recommendations, job_description):
    with get_connection() as con:
        cur = con.execute("""
            INSERT INTO analyses
            (filename, score, match_score, skills, missing_skills, recommendations, job_description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (filename, score, match, json.dumps(skills), json.dumps(missing),
              json.dumps(recommendations), job_description))
        return cur.lastrowid

def decode_row(row):
    if row is None:
        return None
    item = dict(row)
    for key in ("skills", "missing_skills", "recommendations"):
        item[key] = json.loads(item[key])
    return item

def get_recent_analyses(limit=20):
    with get_connection() as con:
        rows = con.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [decode_row(row) for row in rows]

def get_analysis(analysis_id):
    with get_connection() as con:
        row = con.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,)).fetchone()
    return decode_row(row)
