from fastapi import FastAPI
from app.core.settings import settings
from app.api.api import api_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)


    
app.include_router(api_router, prefix="/api")