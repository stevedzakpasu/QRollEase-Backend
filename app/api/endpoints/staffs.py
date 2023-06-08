from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import get_current_active_superuser, get_current_active_user
from app.core.deps import get_session
from app.crud.crud_staff import staff
from app.schemas.staff import StaffUpdate, StaffRead, StaffCreate
from app.models.user import User

router = APIRouter()

@router.get("/staffs", response_model=List[StaffRead], dependencies=[Depends(get_current_active_superuser)])
def get_staffs(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    staffs = staff.get_multiple(session=session, offset=offset, limit=limit)
    return staffs



@router.post("/staffs", response_model=StaffRead, dependencies=[Depends(get_current_active_user)])
def create_staff(
    *,
    session: Session = Depends(get_session),
    staff_in: StaffCreate,
    user: User = Depends(get_current_active_user)

    ):
    db_staff= staff.get_by_staff_id(session=session, staff_in=staff_in.staff_id)
    
    if db_staff:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Staff with this staff id already exists"
        )
    
    db_staff = staff.get_by_user_id(session=session, user_id=user.id)
    
    if db_staff:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Staff with this user id already exists"
        )
    staff_in.user_id = user.id
    new_staff = staff.create(session=session, obj_in=staff_in)
    return new_staff




@router.get("/staffs/{staff_id}", response_model=StaffRead, dependencies=[Depends(get_current_active_superuser)])
def get_staff(
    *,
    session: Session = Depends(get_session),
    staff_id: str
    ):
    db_staff = staff.get_by_id(session=session, staff_idr=staff_id)
    if not db_staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )
    return db_staff


@router.put("/staffs", response_model=StaffRead, dependencies=[Depends(get_current_active_superuser)])
def update_staff(
    *,
    session: Session = Depends(get_session),
    staff_in: StaffUpdate,
    staff_id: str
    ):
    updated_staff = staff.update(session=session, staff_id=staff_id, obj_in=staff_in)
    if not updated_staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )
    return updated_staff



@router.delete("/staffs", dependencies=[Depends(get_current_active_superuser)])
def delete_staff(
    *,
    session: Session = Depends(get_session),
    staff_id: str
    ):
    deleted_staff = staff.remove(session=session, staff_id=staff_id)
    if not deleted_staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )
    return {"success": "Staff deleted successfully"}