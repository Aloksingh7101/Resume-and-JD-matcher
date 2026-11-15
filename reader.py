import pdfplumber
from docx import Document

def read_file(file) -> str:
    name = file.name.lower()
    if name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        if not text.strip():
            raise ValueError("No text found. This PDF may be a scanned image.")
        return text
    if name.endswith(".docx"):
        return "\n".join(p.text for p in Document(file).paragraphs)
    return file.read().decode("utf-8")