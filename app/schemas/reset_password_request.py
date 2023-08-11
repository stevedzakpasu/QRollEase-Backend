from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel


class ResetPasswordRequest(SQLModel):
    email: EmailStr
    code: str
    new_password: Optional[str]