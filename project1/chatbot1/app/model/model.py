from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(..., min_length=1)

class ChatRequest(BaseModel):
    message: str

class Usage(BaseModel):
    tokens: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    usage: Optional[Usage] = None