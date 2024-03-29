from typing import Optional
from sqlmodel import SQLModel, Field



class AttendanceBase(SQLModel):
    student_id: str = Field(foreign_key="student.student_id", )
    lecture_secret: str = Field(foreign_key="lecture.lecture_secret")
    lecture_id: int = Field(foreign_key="lecture.id")

class AttendanceCreate(AttendanceBase):
    pass


class StudentAttendanceRead(SQLModel):
    student_id: str 
    lecture_id: int


class StaffAttendanceRead(AttendanceBase):
    pass

class AttendanceUpdate(SQLModel):
    student_id: Optional[str] = None
    lecture_secret: Optional[str] = None
