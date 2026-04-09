from fastapi import APIRouter, UploadFile, File
# from app.service.pdf_service import extract_text_from_pdf, extract_text_from_doc, extract_text_from_excel
from app.service.pdf_service import get_extractor
router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    
    # reset pointer (important!)
    file.file.seek(0)
    try:
              
        # if filename.endswith(".pdf"):
        #     text = extract_text_from_pdf(file.file)
        
        # elif filename.endswith(".docx"):
        #     text = extract_text_from_doc(file.file)
        # elif filename.endswith((".xls", ".xlsx")):
        #     text = extract_text_from_excel(file.file)
        # else:
        #     return {"error": "Unsupported file type"}
        extractor = get_extractor(filename)

        if not extractor:
            return {"error": "Unsupported file type"}

        text = extractor(file.file)
        
        return {
            "filename": file.filename,
            "length": len(text),
            "preview": text[:500]
        }
    except Exception as e:
        return {"error": str(e)}

