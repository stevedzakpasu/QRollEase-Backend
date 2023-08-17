import secrets
from typing import Optional
from sqlmodel import Field

from app.schemas.lecture import LectureBase


class Lecture(LectureBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lecture_secret: str = Field(default=lambda: secrets.token_hex(16), primary_key=True)