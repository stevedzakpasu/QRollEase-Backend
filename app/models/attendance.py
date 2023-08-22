from typing import Optional
from sqlmodel import Field

from app.schemas.attendance import AttendanceBase


class Attendance(AttendanceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

