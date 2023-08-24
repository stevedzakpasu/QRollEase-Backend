from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import get_current_active_superuser, get_current_active_staff
from app.core.deps import get_session
from app.crud.crud_course import course
from app.schemas.course import CourseUpdate, CourseRead, CourseCreate

router = APIRouter()

@router.get("/courses", response_model=List[CourseRead], dependencies=[Depends(get_current_active_superuser)])
def get_courses(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    courses = course.get_multiple(session=session, offset=offset, limit=limit)
    return courses



@router.post("/courses", response_model=CourseCreate, dependencies=[Depends(get_current_active_staff)])
def create_course(
    *,
    session: Session = Depends(get_session),
    course_in: CourseCreate,

    ):
    db_course= course.get_by_course_code(session=session, course_code=course_in.course_code)
    
    if db_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course with this course code already exists"
        )
    

    new_course = course.create(session=session, obj_in=course_in)
    return new_course




@router.get("/courses/{course_code}", response_model=CourseRead, dependencies=[Depends(get_current_active_superuser)])
def get_course(
    *,
    session: Session = Depends(get_session),
    course_code: str
    ):
    db_course = course.get_by_course_code(session=session, course_code=course_code)
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return db_course


@router.put("/courses", response_model=CourseRead, dependencies=[Depends(get_current_active_superuser)])
def update_course(
    *,
    session: Session = Depends(get_session),
    course_in: CourseUpdate,
    course_id: str
    ):
    updated_course = course.update(session=session, course_id=course_id, obj_in=course_in)
    if not updated_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return updated_course



@router.delete("/courses", dependencies=[Depends(get_current_active_superuser)])
def delete_course(
    *,
    session: Session = Depends(get_session),
    course_code: str
    ):
    deleted_course = course.remove(session=session, course_code=course_code)
    if not deleted_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return {"success": "Course deleted successfully"}