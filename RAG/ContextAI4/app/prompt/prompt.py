from typing import List
from app.model.model import ChatMessage

def build_prompt(messages: List[ChatMessage])-> str:
    prompt = ""
    for msg in messages:
        role = msg.role
        if role == "system":
            prompt += f"system: {msg.content}\n"
        elif role == "user":
            prompt += f"user: {msg.content}\n"
        elif role == "assistant":
            prompt += f"assistant{msg.content}\n"
    
    prompt += "Assistant:"  
    return prompt