from fastapi import FastAPI
from sqlmodel import SQLModel
from app.core.settings import settings
from app.api.api import api_router

app = FastAPI(title=settings.PROJECT_NAME)


    
app.include_router(api_router, prefix="/api")