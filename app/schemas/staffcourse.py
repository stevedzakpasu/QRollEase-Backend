from sqlmodel import SQLModel, Field



class StaffCourseBase(SQLModel):
    staff_id: int = Field(foreign_key="staff.staff_id", primary_key=True)
    course_code: int = Field(foreign_key="course.course_code", primary_key=True)

