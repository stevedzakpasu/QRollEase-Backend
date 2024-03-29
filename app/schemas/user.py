from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Column, String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(
        index=True, sa_column=Column("email", String, unique=True)) 
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



class UserAdminCreate(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(
        index=True, sa_column=Column("email", String, unique=True)) 
    password: str
    is_superuser: Optional[bool] = Field(default=False)
    is_staff: Optional[bool] = Field(default=False)
    is_active: Optional[bool] = Field(default=True)
    is_verified : Optional[bool] = Field(default=False)


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
    is_superuser: bool
    is_staff: bool
    is_active: bool
    is_verified : bool


class UserRead(UserBase):
    id: int


class UserAdminUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None

class UserUpdate(SQLModel):
    pass

