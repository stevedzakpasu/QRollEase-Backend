from sqlmodel import SQLModel, Field



class StaffCourseBase(SQLModel):
    staff_id: str = Field(foreign_key="staff.staff_id", primary_key=True)
    course_code: str = Field(foreign_key="course.course_code", primary_key=True)

