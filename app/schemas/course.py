from datetime import datetime
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field, Column, String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.models.staff import Staff
from app.models.staffcourse import StaffCourse
from app.models.student import Student
from app.models.studentcourse import StudentCourse

class CourseBase(SQLModel):
    course_code : str = Field(
        index=True, sa_column=Column("course_code", String, unique=True))
    course_title: str
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    staffs: List["Staff"] = Relationship(back_populates="courses", link_model=StaffCourse)
    students: List["Student"] = Relationship(back_populates="courses", link_model=StudentCourse)

class CourseCreate(SQLModel):
    course_code : str = Field(
        index=True, sa_column=Column("course_code", String, unique=True))
    course_title: str


class CourseRead(CourseBase):
    id: int


class CourseUpdate(SQLModel): 
    course_code: Optional[str] = None
    course_title: Optional[str] = None

