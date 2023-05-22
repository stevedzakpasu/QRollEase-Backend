from typing import Optional
from sqlmodel import Session, col, select
from app.models.user import User
from app.schemas.user import UserUpdate, UserCreate
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, *, session: Session, email: str) -> User:
        return session.exec(select(User).where(col(User.email) == email)).first()
    

    def create_user(self, *, session: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,


        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    

user = CRUDUser(User)
