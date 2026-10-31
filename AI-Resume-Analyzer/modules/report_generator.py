from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(item, output_path):
    styles = getSampleStyleSheet()
    title = ParagraphStyle("ReportTitle", parent=styles["Title"], textColor=colors.HexColor("#243b70"))
    story = [
        Paragraph("AI Resume Analyzer - Analysis Report", title),
        Spacer(1, 12),
        Paragraph(f"<b>Resume:</b> {item['filename']}", styles["BodyText"]),
        Paragraph(f"<b>Resume score:</b> {item['score']}/100", styles["BodyText"]),
        Paragraph(f"<b>Job description similarity:</b> {item['match_score']}%", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("<b>Detected skills</b>", styles["Heading2"]),
        Paragraph(", ".join(item["skills"]) or "No known skills detected.", styles["BodyText"]),
        Spacer(1, 8),
        Paragraph("<b>Missing job skills</b>", styles["Heading2"]),
        Paragraph(", ".join(item["missing_skills"]) or "No missing skills detected from the built-in skill list.", styles["BodyText"]),
        Spacer(1, 8),
        Paragraph("<b>Recommendations</b>", styles["Heading2"]),
        ListFlowable([ListItem(Paragraph(x, styles["BodyText"])) for x in item["recommendations"]], bulletType="bullet"),
        Spacer(1, 12),
        Paragraph("Note: This is an educational, rule-based estimate and is not an official ATS evaluation.", styles["Italic"])
    ]
    SimpleDocTemplate(output_path, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42).build(story)
