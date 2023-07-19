from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from jose import JWTError, jwt, ExpiredSignatureError
from sqlmodel import Session
from app.crud.crud_user import user
from app.core.settings import settings
from app.core.deps import get_session
from app.models.user import User
from app.schemas.token import TokenPayLoad

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/access-token")


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = TokenPayLoad(**payload)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token expired. Please log in again."
        )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    current_user = user.get_by_email(session=session, email=token_data.sub)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not user.is_active(user=current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

def get_current_verified_user(current_user: User = Depends(get_current_user)) -> User:
    if not user.is_verified(user=current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not verified")
    
    return current_user

def get_current_verified_staff(current_user: User = Depends(get_current_user)) -> User:
    if not user.is_verified(user=current_user) :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not verified")

    if not user.is_staff(user=user) and not  user.is_superuser(user=current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough privileges")

    

    return current_user

def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    if not user.is_superuser(user=current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough privileges")
    return current_user


def get_current_active_staff(current_user: User = Depends(get_current_user)) -> User:
    if not user.is_staff(user=current_user) and not user.is_superuser(user=current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough privileges")
    return current_user