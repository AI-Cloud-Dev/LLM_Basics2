from fastapi import APIRouter, HTTPException, Depends
from app.model.model import ChatRequest, ChatResponse
from app.service.rag_service import get_rag_response
from app.auth.dependencies import get_current_user

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest, 
    user_id: str = Depends(get_current_user)  # secure identity
    ):
    try:
        response_text = get_rag_response(
            user_id=user_id,
            question=request.message
        )

        return ChatResponse(response=response_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))