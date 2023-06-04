from typing import Any
from fastapi_mail import FastMail, MessageSchema, MessageType
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt
from sqlmodel import Session
from fastapi import HTTPException, status
from app.core.settings import settings

import random
import string

from app.models.user import User




password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(subject: Any, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else: 
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    verification_code = ''.join(random.choice(characters) for _ in range(length))
    return verification_code




async def generate_and_send_verification_code(session: Session, current_user: User):
        mail = FastMail(settings.CONF)

        verification_code = generate_verification_code()
        code_expiration_time = datetime.now() + timedelta(minutes=15)

        current_user.verification_code = verification_code
        current_user.code_expiration_time = code_expiration_time
        session.commit()

        message = MessageSchema(
            subject="Verification Code",
            recipients=[current_user.email],
            body=f"Your verification code is: {verification_code}",
            subtype=MessageType.html
        )
        try:
            await mail.send_message(message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send verification code via email"
            )
        

def check_is_staff(email):

    username, domain = email.split('@')

    if domain == 'ug.edu.gh' or domain == 'staff.ug.edu.gh':
        return True
    else:
        return False