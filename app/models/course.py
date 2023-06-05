from typing import Optional
from sqlmodel import Field

from app.schemas.course import CourseBase


class Course(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
