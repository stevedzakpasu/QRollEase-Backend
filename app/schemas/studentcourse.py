from sqlmodel import SQLModel, Field



class StudentCourseBase(SQLModel):
    student_id: str = Field(foreign_key="student.student_id", primary_key=True)
    course_code: str = Field(foreign_key="course.course_code", primary_key=True)

