from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


# In Memory user store (for learning)

users_db = {}

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(email: str, password: str):
    print("PASSWORD:", password)
    print("LENGTH:", len(password))
    if email in users_db:
        raise Exception("User already exists")
    
    hashed_password= hash_password(password)
    
    users_db[email] = {
        "email": email,
        "hashed_password": hashed_password,
        "user_id": str(len(users_db) + 1)
    }
    
    return users_db[email]