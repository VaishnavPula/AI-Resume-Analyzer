import os
import pdfplumber
from docx import Document

def extract_resume_text(file_path):
    """Extract text from a PDF or DOCX resume."""
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    if extension == ".docx":
        doc = Document(file_path)
        parts = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text for cell in row.cells))
        return "\n".join(parts)
    raise ValueError("Unsupported file type.")
