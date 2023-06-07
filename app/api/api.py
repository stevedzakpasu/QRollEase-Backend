from fastapi import APIRouter
from app.api.endpoints import users, login, verification, student


api_router = APIRouter()


api_router.include_router(users.router, tags=["Users"])
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(verification.router, tags=["Verification"])
api_router.include_router(student.router, tags=["Students"])

