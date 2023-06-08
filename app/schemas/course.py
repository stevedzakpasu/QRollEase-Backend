from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class CourseBase(SQLModel):
    course_code : str = Field(
        index=True, sa_column=Column("course_code", String, unique=True))
    course_title: str
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )

class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: int


class CourseUpdate(SQLModel): 
    course_code: Optional[str] = None
    course_title: Optional[str] = None

