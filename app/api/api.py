from fastapi import APIRouter
from app.api.endpoints import staffs, students, users, login, verification, courses, lectures


api_router = APIRouter()


api_router.include_router(users.router, tags=["Users"])
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(verification.router, tags=["Verification"])
api_router.include_router(students.router, tags=["Students"])
api_router.include_router(staffs.router, tags=["Staffs"])
api_router.include_router(courses.router, tags=["Courses"])
api_router.include_router(lectures.router, tags=["Lectures"])

