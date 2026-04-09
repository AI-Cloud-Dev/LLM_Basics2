from fastapi import APIRouter, HTTPException, Query
from app.model.model import ChatRequest, ChatResponse, ChatMessage
from app.service.service import get_llm_response
from app.memory.memory_store import memory_store

router = APIRouter()

SYSTEM_PROMPT = ChatMessage(
    role = "system",
    content= "You are a helpful assistant. Answer clearly."
)

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, session_id: str = Query(...)):
    try:
        # 1. Get Existing Memory
        if session_id not in memory_store:
            memory_store[session_id] = [SYSTEM_PROMPT]
        MAX_MESSAGES = 10
        
        messages = memory_store[session_id]
        
        if len(messages) > MAX_MESSAGES:
            messages = messages[-MAX_MESSAGES:]
            memory_store[session_id] = messages
        
        # 2. Add user message
        user_msg = ChatMessage(role="user", content= request.message)
        messages.append(user_msg)
        
        if len(request.message)>2000:
            raise HTTPException(status_code=400, detail = "Message is too Long")
        
        # 3. Call LLM
        response_text = get_llm_response(messages)
        
        # 4. Store assistant response
        assistant_msg = ChatMessage(role = "assistant", content = response_text)
        messages.append(assistant_msg)
        
        return ChatResponse(response=response_text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @router.post("/chat")