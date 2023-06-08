from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import get_current_active_superuser, get_current_active_user
from app.core.deps import get_session
from app.crud.crud_student import student
from app.schemas.student import StudentUpdate, StudentRead, StudentCreate
from app.models.user import User

router = APIRouter()

@router.get("/students", response_model=List[StudentRead], dependencies=[Depends(get_current_active_superuser)])
def get_students(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    students = student.get_multiple(session=session, offset=offset, limit=limit)
    return students



@router.post("/students", response_model=StudentRead, dependencies=[Depends(get_current_active_user)])
def create_student(
    *,
    session: Session = Depends(get_session),
    student_in: StudentCreate,
    user: User = Depends(get_current_active_user)

    ):
    db_student = student.get_by_student_id(session=session, student_id=student_in.student_id)
    
    if db_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this index number already exists"
        )
    
    db_student = student.get_by_user_id(session=session, user_id=user.id)
    
    if db_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this user id already exists"
        )
    student_in.user_id = user.id
    new_student = student.create(session=session, obj_in=student_in)
    return new_student




@router.get("/students/{student_id}", response_model=StudentRead, dependencies=[Depends(get_current_active_superuser)])
def get_student(
    *,
    session: Session = Depends(get_session),
    student_id: str
    ):
    db_student = student.get_by_id(session=session, student_id=student_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_student


@router.put("/students", response_model=StudentRead, dependencies=[Depends(get_current_active_superuser)])
def update_student(
    *,
    session: Session = Depends(get_session),
    student_in: StudentUpdate,
    student_id: str
    ):
    updated_student = student.update(session=session, student_id=student_id, obj_in=student_in)
    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return updated_student



@router.delete("/students", dependencies=[Depends(get_current_active_superuser)])
def delete_student(
    *,
    session: Session = Depends(get_session),
    student_id: str
    ):
    deleted_student = student.remove(session=session, student_id=student_id)
    if not deleted_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return {"success": "Student deleted successfully"}