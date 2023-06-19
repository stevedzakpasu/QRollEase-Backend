from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import get_current_active_superuser, get_current_active_user
from app.core.deps import get_session
from app.crud.crud_attendance import attendance
from app.schemas.attendance import AttendanceUpdate, AttendanceRead, AttendanceCreate

router = APIRouter()

@router.get("/attendances", response_model=List[AttendanceRead], dependencies=[Depends(get_current_active_superuser)])
def get_attendances(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    attendances = attendance.get_multiple(session=session, offset=offset, limit=limit)
    return attendances



@router.post("/attendances", response_model=AttendanceCreate, dependencies=[Depends(get_current_active_user)])
def create_attendance(
    *,
    session: Session = Depends(get_session),
    attendance_in: AttendanceCreate,

    ):


    new_attendance = attendance.create(session=session, obj_in=attendance_in)
    return new_attendance




@router.get("/attendances/{attendance_id}", response_model=AttendanceRead, dependencies=[Depends(get_current_active_superuser)])
def get_attendance(
    *,
    session: Session = Depends(get_session),
    attendance_id: str
    ):
    db_attendance = attendance.get_by_id(session=session, attendance_idr=attendance_id)
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found"
        )
    return db_attendance


@router.put("/attendances", response_model=AttendanceRead, dependencies=[Depends(get_current_active_superuser)])
def update_attendance(
    *,
    session: Session = Depends(get_session),
    attendance_in: AttendanceUpdate,
    attendance_id: str
    ):
    updated_attendance = attendance.update(session=session, attendance_id=attendance_id, obj_in=attendance_in)
    if not updated_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found"
        )
    return updated_attendance



@router.delete("/attendances", dependencies=[Depends(get_current_active_superuser)])
def delete_attendance(
    *,
    session: Session = Depends(get_session),
    attendance_id: str
    ):
    deleted_attendance = attendance.remove(session=session, attendance_id=attendance_id)
    if not deleted_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found"
        )
    return {"success": "Attendance deleted successfully"}