import re

def clean_text(text):
    """Lowercase text and normalize punctuation/whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()
