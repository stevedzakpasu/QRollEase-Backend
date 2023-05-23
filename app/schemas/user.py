from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Column, String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class UserBase(SQLModel):
    index_number : int|None = Field(
        index=True, sa_column=Column("index_number", String, unique=True))
    first_name: str
    last_name: str
    email: EmailStr = Field(
        index=True, sa_column=Column("email", String, unique=True))
    programme: Optional[str]
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    verification_code: Optional[str] = None
    code_expiration_time: Optional[datetime] = None
    is_superuser: Optional[bool] = Field(default=False)
    is_staff: Optional[bool] = Field(default=False)
    is_active: Optional[bool] = Field(default=True)
    is_verified : Optional[bool] = Field(default=False)




class UserAdminCreate(UserBase):
    password: str


class UserCreate(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserCreateReturn(SQLModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr




class UserRead(UserBase):
    id: int


class UserAdminUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_superuser: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_active: Optional[bool] = None

class UserUpdate(SQLModel):

    programme :Optional[str] = None

