from typing import Optional
from sqlmodel import Field

from app.schemas.user import UserBase


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
