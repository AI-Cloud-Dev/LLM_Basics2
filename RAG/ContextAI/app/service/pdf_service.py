from PyPDF2 import PdfReader
from docx import Document
import pandas as pd


# ----------PDF--------------
def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() or ""
    
    return text

# ---------DOCUMENT----------
def extract_text_from_doc(file) -> str:
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# ----------EXCEL--------------
def extract_text_from_excel(file) -> str:
    df = pd.read_excel(file)
    return df.to_string(index=False)



# -------- DISPATCHER --------
EXTRACTORS = {
    ".pdf": extract_text_from_pdf,
    ".docx": extract_text_from_doc,
    ".xls": extract_text_from_excel,
    ".xlsx": extract_text_from_excel,
}


def get_extractor(filename: str):
    for ext, func in EXTRACTORS.items():
        if filename.endswith(ext):
            return func
    return None