from fastapi import APIRouter, HTTPException, Query
from app.model.model import ChatRequest, ChatResponse, ChatMessage
from app.memory.memory_store import memory_store
from app.service.service import get_llm_response


# print(dir(app.model.model))
router= APIRouter()

SYSTEM_PROMPT  = ChatMessage(
    role= "system",
    content= "You area helpful AI Assistant"
)

MAX_MESSAGES = 10 #Memory Limit

@router.post("/chat", response_model = ChatResponse)
def chat_endpoint(request: ChatRequest, session_id: str = Query(...)):
    try:
        # 1. Fetch or init memory
        if session_id not in memory_store:
            memory_store[session_id]= [SYSTEM_PROMPT]
            
        messages = memory_store[session_id]
        
        # 2. Add user message
        user_msg = ChatMessage(role= "user", content = request.message)
        messages.append(user_msg)
        
        # 3. Trim Memory
        if len(messages) > MAX_MESSAGES:
            messages = messages[-MAX_MESSAGES:]
            memory_store[session_id] = messages
            
        # 4. Call LLM
        response_text = get_llm_response(messages)
        
        # 5. Store assistant message
        assistant_msg = ChatMessage(role="assistant", content= response_text)
        messages.append(assistant_msg)
        
        return ChatResponse(response=response_text)
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail= str(e))