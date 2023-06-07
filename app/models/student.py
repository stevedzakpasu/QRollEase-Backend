from typing import Optional
from sqlmodel import Field

from app.schemas.student import StudentBase


class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

