from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field, Column, String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.models.studentcourse import StudentCourse

if TYPE_CHECKING:
    from app.models.course import Course

class StudentBase(SQLModel):
    student_id : str = Field(
        index=True, sa_column=Column("student_id", String, unique=True))
    programme: str
    user_id: int = Field(foreign_key="user.id")
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    courses: List["Course"] = Relationship(back_populates="students", link_model=StudentCourse)


class StudentCreate(SQLModel):
    student_id : str = Field(
        index=True, sa_column=Column("student_id", String, unique=True))
    programme: str
    user_id: int = Field(foreign_key="user.id")


class StudentRead(StudentCreate):
    id: int


class StudentUpdate(SQLModel):
    student_id : Optional[str] = None
    programme: Optional[str] = None


