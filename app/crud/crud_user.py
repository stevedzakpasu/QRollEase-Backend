from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, col, select
from app.core.security import generate_verification_code, get_hashed_password, verify_password
from app.models.user import User
from app.schemas.user import UserAdminCreate, UserUpdate
from app.crud.base import CRUDBase
from fastapi_mail import FastMail, MessageSchema, MessageType
from app.core.settings import settings

class CRUDUser(CRUDBase[User, UserAdminCreate, UserUpdate]):


    def get_by_email(self, *, session: Session, email: str) -> User:
        return session.exec(select(User).where(col(User.email) == email)).first()
    
    def get_by_id(self, *, session: Session, id: int) -> User:
        return session.exec(select(User).where(col(User.id) == id)).first()

    
    async def create_by_user(self, *, session: Session, obj_in: UserAdminCreate) -> User:
        verification_code = generate_verification_code()
        code_expiration_time = datetime.now() + timedelta(minutes=15)
        mail = FastMail(settings.CONF)

        db_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            hashed_password=get_hashed_password(obj_in.password),
            verification_code=verification_code,
            code_expiration_time=code_expiration_time
        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        # Sending verification code via email
        message = MessageSchema(
        subject="Thanks for registering on our platform!",
        recipients=[obj_in.email],
        body=f"Your verification code is: {verification_code}",
        subtype=MessageType.html)

        await mail.send_message(message)
  

        return db_obj

    def create_by_admin(self, *, session: Session, obj_in: UserAdminCreate) -> User:

        verification_code = generate_verification_code()
        code_expiration_time = datetime.now() + timedelta(minutes=15)

        db_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            hashed_password=get_hashed_password(obj_in.password),
            is_superuser=obj_in.is_superuser,
            is_staff=obj_in.is_staff,
            is_active=obj_in.is_active,
            verification_code=verification_code,
            code_expiration_time=code_expiration_time
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

    

user = CRUDUser(User)
