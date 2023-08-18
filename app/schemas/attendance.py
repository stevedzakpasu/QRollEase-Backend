from typing import Optional
from sqlmodel import SQLModel, Field



class AttendanceBase(SQLModel):
    student_id: str = Field(foreign_key="student.student_id", primary_key=True)
    lecture_secret: str = Field(foreign_key="lecture.lecture_secret", primary_key=True)

class AttendanceCreate(AttendanceBase):
    pass


class AttendanceRead(AttendanceBase):
    pass

# class IndividualAttendanceRead(SQLModel):
#     lecture_id : int
    


class AttendanceUpdate(SQLModel):
    student_id: Optional[str] = None
    lecture_secret: Optional[str] = None
