from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlmodel import Session
from app.api.deps import get_current_active_superuser, get_current_active_user
from app.core.deps import get_session
from app.core.security import generate_and_send_verification_code
from app.models.user import User
from app.crud.crud_user import user
from app.schemas.user import UserAdminUpdate, UserCreateReturn, UserRead, UserAdminCreate, UserCreate, UserUpdate


router = APIRouter()

@router.get("/users", response_model=List[UserRead], dependencies=[Depends(get_current_active_superuser)])
def get_users(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    users = user.get_multiple(session=session, offset=offset, limit=limit)
    return users


@router.post("/users", response_model=UserRead, dependencies=[Depends(get_current_active_superuser)])
def admin_create_user(
    *, 
    session: Session = Depends(get_session),
    user_in: UserAdminCreate
    ):
    db_user = user.get_by_email(session=session, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    new_user = user.create_by_admin(session=session, obj_in=user_in)
    return new_user



@router.get("/users/me", response_model=UserCreateReturn)
def get_user_me(
    *,
    user: User = Depends(get_current_active_user),
    ):
    return user


@router.post("/users/open", response_model=UserCreateReturn)
def create_user(
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
    new_user = user.create_by_user(session=session, obj_in=user_in)
    return new_user


@router.post("/users/forgot_password")
def forgot_password(
    *,
    session: Session = Depends(get_session),
    email : EmailStr
    ):
    db_user = user.get_by_email(session=session, email=email)
    if db_user:
        # generate and send verification code
        pass
 
    else:        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user found with this email address!"
        )

@router.post("/users/reset_password")
def reset_password(
    *,
    session: Session = Depends(get_session),
    code : str
    # maybe email, idk {-_-}
    # new password too
    ):


    # check if the user code matches the code entered
    # if it does ask for new password
    # else ask for correct code
    if True:
        pass
 
    else:        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user found with this email address!"
        )


@router.get("/users/{user_id}", response_model=UserRead, dependencies=[Depends(get_current_active_superuser)])
def get_user(
    *,
    session: Session = Depends(get_session),
    user_id: int
    ):
    db_user = user.get_by_id(session=session, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put("/users", response_model=UserRead, dependencies=[Depends(get_current_active_superuser)])
def admin_update_user(
    *,
    session: Session = Depends(get_session),
    user_in: UserAdminUpdate,
    user_id: int
    ):
    updated_user = user.update(session=session, id=user_id, obj_in=user_in)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


@router.patch("/users", response_model=UserCreateReturn, dependencies=[Depends(get_current_active_user)])
def update_user(
    *,
    session: Session = Depends(get_session),
    user_in: UserUpdate,
    user_id: int
    ):
    updated_user = user.update(session=session, id=user_id, obj_in=user_in)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


@router.delete("/users", dependencies=[Depends(get_current_active_superuser)])
def delete_user(
    *,
    session: Session = Depends(get_session),
    user_id: int
    ):
    deleted_user = user.remove(session=session, id=user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"success": "User deleted successfully"}