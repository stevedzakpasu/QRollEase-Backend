from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class LectureBase(SQLModel):
    course_code : str =Field(foreign_key="course.course_code")
    lecture_description: str
    lecture_location : str
    is_active : bool
    accuracy: float
    latitude: float
    longitude: float
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )


    
class StaffLectureRead(LectureBase):
    id: int
    lecture_secret: str


class StudentLectureRead(LectureBase):
    id: int

class LectureCreate(SQLModel):
    course_code : str =Field(foreign_key="course.course_code")
    lecture_description: str
    lecture_location : str
    is_active : bool
    accuracy: float
    latitude: float
    longitude:float


class LectureUpdate(SQLModel): 
    course_code: Optional[str] = None
    lecture_description: Optional[str] = None
    lecture_location: Optional[str] = None
    lecture_secret: Optional[str] = None
    is_active : Optional[bool] = None
    accuracy: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


