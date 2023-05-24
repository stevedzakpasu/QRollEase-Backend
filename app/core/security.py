from typing import Any
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt

from app.core.settings import settings

import random
import string




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




# def resend_verification_code(user: User, session: Session):
#     # Generate new verification code and expiration time
#     new_verification_code = generate_verification_code()
#     new_code_expiration_time = datetime.now() + timedelta(minutes=15)

#     # Update the user's verification code and expiration time in the database
#     user.verification_code = new_verification_code
#     user.code_expiration_time = new_code_expiration_time
#     session.commit()

#     # Send the new verification code via email
#     message = Message(
#         subject="New Verification Code",
#         recipients=[user.email],
#         body=f"Your new verification code is: {new_verification_code}"
#     )
#     try:
#         mail.send_message(message)
#     except Exception as e:
#         # Handle email sending errors appropriately
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to send verification code via email"
#         )