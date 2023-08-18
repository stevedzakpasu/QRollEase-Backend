import secrets
from typing import Optional
from sqlmodel import Field, Column, String

from app.schemas.lecture import LectureBase


class Lecture(LectureBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lecture_secret : str = Field( default_factory=lambda: secrets.token_hex(16),
        index=True, sa_column=Column("lecture_secret", String, unique=True))