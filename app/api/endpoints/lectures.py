from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import get_current_active_staff, get_current_active_superuser, get_current_active_user, get_current_verified_staff
from app.core.deps import get_session
from app.crud.crud_lecture import lecture
from app.crud.crud_course import course
from app.schemas.lecture import LectureUpdate, StaffLectureRead,StudentLectureRead, LectureCreate

router = APIRouter()

@router.get("/lectures", response_model=List[StaffLectureRead], dependencies=[Depends(get_current_active_superuser)])
def get_lectures(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    lectures = lecture.get_multiple(session=session, offset=offset, limit=limit)
    return lectures

@router.get("/lectures/{course_code}", response_model=List[StudentLectureRead], dependencies=[Depends(get_current_active_user)])
def get_all_lectures(
    *,
    session: Session = Depends(get_session),
    course_code: str
    ):
    lectures = lecture.get_by_course_code(session=session, course_code=course_code)
    if not lectures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No lectures for this course"
        )
    return lectures

@router.get("/lectures/staff/{course_code}", response_model=List[StaffLectureRead], dependencies=[Depends(get_current_active_staff)])
def staff_get_all_lectures(
    *,
    session: Session = Depends(get_session),
    course_code: str
    ):
    lectures = lecture.get_by_course_code(session=session, course_code=course_code)
    if not lectures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No lectures for this course"
        )
    return lectures

@router.get("/lectures/id/{lecture_id}", response_model=StaffLectureRead, dependencies=[Depends(get_current_active_superuser)])
def get_lecture(
    *,
    session: Session = Depends(get_session),
    lecture_id: int
    ):
    db_lecture = lecture.get_by_id(session=session, id=lecture_id)
    if not db_lecture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecture not found"
        )
    return db_lecture
@router.post("/lectures", response_model=LectureCreate, dependencies=[Depends(get_current_verified_staff)])
def create_lecture(
    *,
    session: Session = Depends(get_session),
    lecture_in: LectureCreate,

    ):


    db_course = course.get_by_course_code(session=session, course_code=lecture_in.course_code)
    
 

    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The course code entered does not exist"
        )


    new_lecture = lecture.create(session=session, obj_in=lecture_in)
    return new_lecture








@router.put("/lectures", response_model=StaffLectureRead, dependencies=[Depends(get_current_active_staff)])
def update_lecture(
    *,
    session: Session = Depends(get_session),
    lecture_in: LectureUpdate,
    lecture_id: int
    ):
    updated_lecture = lecture.update(session=session, lecture_id=lecture_id, obj_in=lecture_in)
    if not updated_lecture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecture not found"
        )
    return updated_lecture



@router.delete("/lectures", dependencies=[Depends(get_current_active_superuser)])
def delete_lecture(
    *,
    session: Session = Depends(get_session),
    lecture_id: int
    ):
    deleted_lecture = lecture.remove(session=session, lecture_id=lecture_id)
    if not deleted_lecture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecture not found"
        )
    return {"success": "Lecture deleted successfully"}