from typing import List
from app.model.model import ChatMessage

def build_prompt(messages: List[ChatMessage]) -> str:
    prompt = ""
    
    for msg in messages:
        role = msg.role
        
        if role == "system":
            prompt += f"System: {msg.content}\n"
        elif role == "user":
            prompt += f"User: {msg.content}\n"
        elif role == "assistant":
            prompt += f"Assistant: {msg.content}\n"
    
    prompt += "Assistant:"  # important for completion
    
    return prompt