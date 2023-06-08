from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

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

class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int


class StudentUpdate(SQLModel):
    student_id : Optional[str] = None
    programme: Optional[str] = None


