from typing import Optional
from sqlmodel import Field

from app.schemas.staff import StaffBase


class Staff(StaffBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

