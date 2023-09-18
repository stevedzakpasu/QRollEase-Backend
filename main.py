from fastapi import FastAPI
from app.core.deps import create_superuser
from app.core.settings import settings
from app.api.api import api_router

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
def on_startup():
    create_superuser()

    
app.include_router(api_router, prefix="/api")