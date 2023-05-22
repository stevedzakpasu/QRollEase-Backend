from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Column, String



class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(
        index=True, sa_column=Column("email", String, unique=True))


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None