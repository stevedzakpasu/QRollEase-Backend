from sqlmodel import SQLModel, Field, String, Column, ForeignKey



class StaffCourseBase(SQLModel):
    staff_id: str = Field(foreign_key="staff.staff_id", primary_key=True)
    course_code: str =  Field(
        sa_column=Column(String, ForeignKey("course.course_code", ondelete="CASCADE"))  # Set the foreign key behavior on the table metadata
    )

