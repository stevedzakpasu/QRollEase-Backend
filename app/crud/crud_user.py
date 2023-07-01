from typing import Optional
from fastapi import HTTPException
from sqlmodel import Session, col, select
from app.core.security import get_hashed_password, verify_password
from app.models.user import User
from app.schemas.user import UserAdminCreate, UserUpdate
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserAdminCreate, UserUpdate]):


    def get_by_email(self, *, session: Session, email: str) -> User:
        return session.exec(select(User).where(col(User.email) == email)).first()
    
    def get_by_id(self, *, session: Session, id: int) -> User:
        return session.exec(select(User).where(col(User.id) == id)).first()

    
    def create_by_user(self, *, session: Session, obj_in: UserAdminCreate) -> User:
    

        db_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            hashed_password=get_hashed_password(obj_in.password),
    
        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def create_by_admin(self, *, session: Session, obj_in: UserAdminCreate) -> User:



        db_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            hashed_password=get_hashed_password(obj_in.password),
            is_superuser=obj_in.is_superuser,
            is_staff=obj_in.is_staff,
            is_active=obj_in.is_active,

        )
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj

    def update(self, *, session: Session, id: int, obj_in: UserUpdate) -> User:
        db_obj = session.exec(select(User).where(col(User.id) == id)).first()
        if db_obj: 
            obj_data = obj_in.dict(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(db_obj, key, value)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        return db_obj

    def remove(self, *, session: Session, id: int) -> User:
        db_obj = session.exec(select(User).where(col(User.id) == id)).first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(db_obj)
        session.commit()
            
        return db_obj
    
    def authenticate(self, *, session: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(session=session, email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None
        return user
    
    
    # TO CHANGE
    def verify(self, *, session: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(session=session, email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None
        return user

    def is_active(self, *, user: User) -> bool:
        return user.is_active

    def is_superuser(self, *, user: User) -> bool:
        return user.is_superuser

    def is_staff(self, *, user: User) -> bool:
        return user.is_staff  
    
    def is_verified(self, *, user: User) -> bool:
        return user.is_verified
    


user = CRUDUser(User)
