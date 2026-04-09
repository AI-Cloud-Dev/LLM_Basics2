from fastapi import FastAPI
from app.routes.chat_routes import router

app = FastAPI()

app.include_router(router, prefix = "/api")