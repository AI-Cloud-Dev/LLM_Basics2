from fastapi import Request
from app.auth.jwt_handler import decode_token
from slowapi.util import get_remote_address
from app.auth.jwt_handler import decode_token
from slowapi import Limiter

def get_user_key(request: Request):
    auth = request.header.get("Authorization")
    
    if auth:
        token = auth.split(" ")[1]
        payload = decode_token(token)
        
        if payload:
            return payload.get("user_id")
    return get_remote_address(request)  #Fallback

limiter = Limiter(key_func= get_user_key)