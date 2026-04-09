import requests
from typing import List
from app.model.model import ChatMessage
from app.prompt.prompt import build_prompt

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_llm_response(messages: List[ChatMessage]) -> str:
    
    prompt = build_prompt(messages)
    
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60   # ✅ important
        )
        response.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ollama connection error: {str(e)}")
    
    data = response.json()
    print("RAW:", data)  # debug

    
    return data.get("response", "").strip()