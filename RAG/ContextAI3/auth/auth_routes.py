from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth.auth_service import create_user, verify_password, users_db
from app.auth.jwt_handler import create_access_token

router = APIRouter()

class UserRegister(BaseModel):
    email: str
    password: str
    
class UserLogin(BaseModel):
    email: str
    password: str



@router.post("/register")
def register(user: UserRegister):
    try:
        new_user  = create_user(user.email, user.password)
        return {"message": "User created", "user": new_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user: UserLogin):
    db_user = users_db.get(user.email)
    
    if not db_user:
        raise HTTPException(status_code=400, detail= "Invalid Credentials")
    
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    token = create_access_token({
        "user_id": db_user["user_id"],
        "email": db_user["email"]
    })
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }