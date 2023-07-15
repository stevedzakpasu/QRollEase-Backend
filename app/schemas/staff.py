from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Relationship, SQLModel, Field, Column, String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.models.staffcourse import StaffCourse

if TYPE_CHECKING:
    from app.models.course import Course

class StaffBase(SQLModel):
    staff_id: str = Field(
        index=True, sa_column=Column("staff_id", String(), unique=True))
    department: str
    user_id: int = Field(foreign_key="user.id")
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    courses: List["Course"] = Relationship(back_populates="staffs", link_model=StaffCourse)

class StaffCreate(StaffBase):
     pass

class StaffRead(StaffBase):
     id: int

class StaffUpdate(SQLModel):
     staff_id: Optional[str] = None
     department: Optional[str] = None