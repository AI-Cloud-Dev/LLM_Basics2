from fastapi import APIRouter, HTTPException, Query
from app.model.model import ChatRequest, ChatResponse
from app.service.rag_service import get_rag_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, session_id: str = Query(...)):
    try:
        response_text = get_rag_response(
            session_id=session_id,
            question=request.message
        )

        return ChatResponse(response=response_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))