from fastapi import FastAPI
from app.routes.chat_routes import router as chat_router
from app.routes.upload_routes import router as upload_router
from app.auth.auth_routes import router as auth_router
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse


app = FastAPI()

limiter = Limiter(key_func = get_remote_address)

app.include_router(chat_router, prefix = "/api")
app.include_router(upload_router, prefix= "/api")
app.include_router(auth_router, prefix = "/auth")

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content = {"detail": "Too many requests. Please try again later"}
    )