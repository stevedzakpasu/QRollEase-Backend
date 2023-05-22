from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.core.deps import get_session
from app.core.security import create_access_token
from app.core.settings import settings
from app.schemas.token import Token
from app.crud.crud_user import user


router = APIRouter(prefix="/login")

@router.post("/access-token", response_model=Token)
def login_access_token(*, session: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = user.authenticate(session=session, email=form_data.username, password=form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    elif not user.is_active(user=db_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES_MOBILE)
    access_token = create_access_token(db_user.email, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

    


@router.post("/access-token/admin", response_model=Token)
def login_access_token_admin(*, session: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = user.authenticate(session=session, email=form_data.username, password=form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    elif not user.is_active(user=db_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    elif not user.is_superuser(user=db_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES_WEB)
    access_token = create_access_token(db_user.email, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.post("/access-token/staff", response_model=Token)
def login_access_token_staff(*, session: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = user.authenticate(session=session, email=form_data.username, password=form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    elif not user.is_active(user=db_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    elif not (user.is_superuser(user=db_user) or user.is_staff(user=db_user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES_WEB)
    access_token = create_access_token(db_user.email, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }