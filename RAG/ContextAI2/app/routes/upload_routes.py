from fastapi import APIRouter, UploadFile, File, HTTPException, Query
# from app.service.pdf_service import extract_text_from_pdf, extract_text_from_doc, extract_text_from_excel
from app.service.pdf_service import get_extractor
from io import BytesIO


from app.service.embedding_service import get_embedding
from app.service.chunking_service import chunk_text
from app.service.vector_store import add_embeddings




router = APIRouter()
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), session_id: str =  Query(...)):
    filename = file.filename
    
    # 1. Validate extension
    extractor = get_extractor(filename)
    
    if not extractor:
        raise HTTPException(status_code= 400, detail= "Unsupported file Type")
    
    # 2. Validate file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (Max 5MB)")
    
    try:
        # 3. Reset pointer after reading - Convert to file-like object
        file_obj = BytesIO(contents)
        
        # 4. Extract text
        text = extractor(file_obj)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail= "No readable contents gound")
        
        # 5. Chunking
        chunks = chunk_text(text)
        
        # 6. Embeddings
        embeddings = [get_embedding(chunk) for chunk in chunks]
        
        # 7. Store in Vector DB
        add_embeddings(session_id, embeddings, chunks)
        
        return {
            "filename": filename,
            "length": len(text),
            "preview": text[:500]            
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
































# async def upload_file(file: UploadFile = File(...)):
#     filename = file.filename   #.lower()
    
#     # reset pointer (important!)
#     file.file.seek(0)
#     try:
               
#         # if filename.endswith(".pdf"):
#         #     text = extract_text_from_pdf(file.file)
        
#         # elif filename.endswith(".docx"):
#         #     text = extract_text_from_doc(file.file)
#         # elif filename.endswith((".xls", ".xlsx")):
#         #     text = extract_text_from_excel(file.file)
#         # else:
#         #     return {"error": "Unsupported file type"}
        
        
#         extractor = get_extractor(filename)

#         if not extractor:
#             return {"error": "Unsupported file type"}

#         text = extractor(file.file)
        
#         return {
#             "filename": file.filename,
#             "length": len(text),
#             "preview": text[:500]
#         }
#     except Exception as e:
#         return {"error": str(e)}

