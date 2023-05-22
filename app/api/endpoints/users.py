

from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.deps import get_session
from app.schemas.user import UserRead
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