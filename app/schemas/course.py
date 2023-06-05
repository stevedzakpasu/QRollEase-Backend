from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Column, String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class CourseBase(SQLModel):
    code: str = Field(index=True, sa_column=Column("code", String, unique=True))
    name: str
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
    code: Optional[str] = None
    name: Optional[str] = None
