from typing import Optional
from sqlmodel import Session, col, select
from app.models.user import User
from app.schemas.user import UserUpdate, UserCreate
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, *, session: Session, email: str) -> User:
        return session.exec(select(User).where(col(User.email) == email)).first()

    

user = CRUDUser(User)
