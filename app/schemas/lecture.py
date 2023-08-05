from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class LectureBase(SQLModel):
    course_code : str =Field(foreign_key="course.course_code")
    lecture_description: str
    lecture_location : str
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )

    
class LectureCreate(SQLModel):
    id: int
    course_code : str =Field(foreign_key="course.course_code")
    lecture_description: str
    lecture_location : str



class LectureRead(LectureCreate):
    course_code : str =Field(foreign_key="course.course_code")
    lecture_description: str
    lecture_location : str



class LectureUpdate(SQLModel): 
    course_code: Optional[str] = None
    lecture_description: Optional[str] = None
    lecture_location: Optional[str] = None


