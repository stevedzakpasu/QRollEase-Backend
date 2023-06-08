from typing import Optional
from sqlmodel import Field

from app.schemas.lecture import LectureBase


class Lecture(LectureBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

