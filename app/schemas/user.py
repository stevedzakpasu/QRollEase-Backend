from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Column, String
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(
        index=True, sa_column=Column("email", String, unique=True))

