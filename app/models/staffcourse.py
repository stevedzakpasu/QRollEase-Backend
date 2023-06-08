from typing import Optional
from sqlmodel import Field

from app.schemas.staffcourse import StaffCourseBase


class StaffCourse(StaffCourseBase, table=True):
    pass

