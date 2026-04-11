from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import os


# ----------PDF--------------
def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() or ""
    
    return clean_text(text)

# ---------DOCUMENT----------
def extract_text_from_doc(file) -> str:
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return clean_text(text)

# ----------EXCEL--------------
def extract_text_from_excel(file) -> str:
    try:
        df = pd.read_excel(file)
        text= df.to_string(index=False)
        return clean_text(text)
    except Exception as e:
        return Exception(f"Excel parsing error: {str(e)}")
    
# ---------- CLEANER ----------
def clean_text(text: str) -> str:
    return text.strip().replace("\n\n", "\n")


# -------- DISPATCHER --------
EXTRACTORS = {
    ".pdf": extract_text_from_pdf,
    ".docx": extract_text_from_doc,
    ".xls": extract_text_from_excel,
    ".xlsx": extract_text_from_excel,
}


def get_extractor(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    return EXTRACTORS.get(ext)