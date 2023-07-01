from sqlmodel import select
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import get_current_active_superuser, get_current_verified_staff, get_current_verified_user
from app.core.deps import get_session
from app.crud.crud_attendance import attendance
from app.crud.crud_student import student
from app.crud.crud_lecture import lecture
from app.models.attendance import Attendance
from app.models.lecture import Lecture
from app.models.student import Student
from app.models.user import User
from app.schemas.attendance import AttendanceUpdate, AttendanceRead, AttendanceCreate, IndividuelAttendanceRead

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



@router.post("/attendances", response_model=AttendanceCreate, dependencies=[Depends(get_current_verified_staff)])
def staff_create_attendance(
    *,
    session: Session = Depends(get_session),
    attendance_in: AttendanceCreate,

    ):
    
    student_in = student.get_by_student_id(session=session, student_id=attendance_in.student_id)

    if not student_in:
         raise HTTPException(status_code=400, detail="Student not found")
        
    lecture_in = lecture.get_by_id(session=session, id=attendance_in.lecture_id)    

    if not lecture_in :
        raise HTTPException(status_code=404, detail="Lecture not found")

    existing_attendance = attendance.get_by_student_and_lecture_id(session=session,student_id = attendance_in.student_id, lecture_id=
                                                                attendance_in.lecture_id
                                                                   )
    if existing_attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already recorded"
        )

    new_attendance = attendance.create(session=session, obj_in=attendance_in)
    return new_attendance


@router.post("/students-attendances", response_model=AttendanceCreate, dependencies=[Depends(get_current_verified_user)])
def student_create_attendance(
    *,
    session: Session = Depends(get_session),
    attendance_in: AttendanceCreate ,
    user: User = Depends(get_current_verified_user),
    

    ):

    student_in = session.exec(
        select(Student).where(Student.student_id == attendance_in.student_id)
        ).first()
    
    current_student = session.exec(
        select(Student).join(User).where(User.id == user.id)
        ).first()

    if current_student != student_in:
         raise HTTPException(status_code=400, detail="Student ID does not match yours")
        
    if not student_in:
        raise HTTPException(status_code=404, detail="Student not found")
    

    lecture = session.exec(
        select(Lecture).where(Lecture.id == attendance_in.lecture_id)
        ).first()
  
        
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    

    existing_attendance = attendance.get_by_student_and_lecture_id(session=session, student_id=attendance_in.student_id, lecture_id=attendance_in.lecture_id)
    
   
    if existing_attendance:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already recorded"
        )


    new_attendance = attendance.create(session=session, obj_in=attendance_in)
    return new_attendance




@router.get("/attendances/{lecture_id}", response_model=List[AttendanceRead], dependencies=[Depends(get_current_active_superuser)])
def get_attendance(
    *,
    session: Session = Depends(get_session),
    lecture_id:int
    ):

    db_attendance = session.exec((select(Attendance).where(Attendance.lecture_id== lecture_id))).all()
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found"
        )
    return db_attendance


@router.get("/attendances/{student_id}", response_model=List[AttendanceRead], dependencies=[Depends(get_current_active_superuser)])
def get_individual_attendance(
    *,
    session: Session = Depends(get_session),
    student_id: str
    ):



    attendances = session.exec(select(Attendance).where(Attendance.student_id == student_id)).all()
    

    if not attendances:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendances not found"
        )
    return attendances

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
    attendance_id: int
    ):
    deleted_attendance = attendance.remove(session=session, attendance_ld=attendance_id)
    if not deleted_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found"
        )
    return {"success": "Attendance deleted successfully"}