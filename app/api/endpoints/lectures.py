from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import get_current_active_staff, get_current_active_superuser, get_current_active_user, get_current_verified_staff
from app.core.deps import get_session
from app.crud.crud_lecture import lecture
from app.schemas.lecture import LectureUpdate, LectureRead, LectureCreate

router = APIRouter()

@router.get("/lectures", response_model=List[LectureRead], dependencies=[Depends(get_current_active_superuser)])
def get_lectures(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    lectures = lecture.get_multiple(session=session, offset=offset, limit=limit)
    return lectures

@router.get("/lectures/{course_code}", response_model=List[LectureRead], dependencies=[Depends(get_current_active_user)])
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

@router.get("/lectures/id/{lecture_id}", response_model=LectureRead, dependencies=[Depends(get_current_active_superuser)])
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
    db_lecture_description= lecture.get_by_lecture_description(session=session, lecture_description=lecture_in.lecture_description)
    db_lecture= lecture.get_by_course_code(session=session, course_code=lecture_in.course_code)

    
    if db_lecture and db_lecture_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lecture with this lecture description already exists"
        )
    

    new_lecture = lecture.create(session=session, obj_in=lecture_in)
    return new_lecture








@router.put("/lectures", response_model=LectureRead, dependencies=[Depends(get_current_active_superuser)])
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