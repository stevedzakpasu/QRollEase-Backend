from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import get_current_active_superuser
from app.core.deps import get_session

from app.crud.crud_course import course
from app.schemas.course import CourseCreate, CourseRead, CourseUpdate


router = APIRouter()


@router.get("/courses", response_model=List[CourseRead], dependencies=[Depends(get_current_active_superuser)])
def get_courses(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    result = course.get_multiple(session=session, offset=offset, limit=limit)
    return result


@router.post("/courses", response_model=CourseRead, dependencies=[Depends(get_current_active_superuser)])
def create_course(
    *,
    session: Session = Depends(get_session),
    obj_in: CourseCreate
    ):
    result = course.create(session=session, obj_in=obj_in)
    return result


@router.get("/courses/{course_id}", response_model=CourseRead, dependencies=[Depends(get_current_active_superuser)])
def get_course(
    *,
    session: Session = Depends(get_session),
    course_id: int
    ):
    result = course.get_by_id(session=session, id=course_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No course found"
        )
    return result


@router.put("/courses", response_model=CourseRead, dependencies=[Depends(get_current_active_superuser)])
def update_course(
    *,
    session: Session = Depends(get_session),
    course_id: int,
    obj_in: CourseUpdate
    ):
    result = course.update(session=session, id=course_id, obj_in=obj_in)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No course found"
        )
    return result


@router.delete("/courses", dependencies=[Depends(get_current_active_superuser)])
def delete_course(
    *,
    session: Session = Depends(get_session),
    course_id: int
    ):
    result = course.remove(session=session, id=course_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No course found"
        )
    return {"success": "Course deleted successfully"}