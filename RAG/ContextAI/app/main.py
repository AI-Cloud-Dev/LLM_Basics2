from fastapi import FastAPI
from app.routes.chat_routes import router as chat_router
from app.routes.upload_routes import router as upload_router

app = FastAPI()

app.include_router(chat_router, prefix = "/api")
app.include_router(upload_router, prefix= "/api")