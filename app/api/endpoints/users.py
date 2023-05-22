

from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import get_session
from app.schemas.user import UserCreate, UserRead
from app.crud.crud_user import user
router = APIRouter()

@router.get("/users", response_model=List[UserRead])
def get_users(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    users = user.get_multiple(session=session, offset=offset, limit=limit)
    return users



@router.post("/users", response_model=UserRead)
def admin_create_user(
    *, 
    session: Session = Depends(get_session),
    user_in: UserCreate
    ):
    db_user = user.get_by_email(session=session, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    new_user = user.create_user(session=session, obj_in=user_in)
    return new_user