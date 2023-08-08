from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.api.deps import get_current_active_staff, get_current_active_superuser, get_current_verified_staff
from app.core.deps import get_session
from app.crud.crud_staff import staff
from app.models.course import Course
from app.models.staff import Staff
from app.models.staffcourse import StaffCourse
from app.schemas.staff import StaffUpdate, StaffRead, StaffCreate
from app.models.user import User
from app.schemas.user import UserRead
from app.crud.crud_course import course
router = APIRouter()


@router.get("/staffs/me", response_model=StaffRead, dependencies=[Depends(get_current_verified_staff)])
def get_staff_me(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_active_staff)
):
    db_staff = staff.get_by_user_id(session=session, user_id=user.id)

    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    return db_staff

@router.get("/staffs", response_model=List[StaffRead], dependencies=[Depends(get_current_active_superuser)])
def get_staffs(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    staffs = staff.get_multiple(session=session, offset=offset, limit=limit)
    return staffs



@router.post("/staffs", response_model=StaffRead, dependencies=[Depends(get_current_active_staff)])
def create_staff(
    *,
    session: Session = Depends(get_session),
    staff_in: StaffCreate,
    user: User = Depends(get_current_verified_staff)

    ):
    db_staff= staff.get_by_staff_id(session=session, staff_id=staff_in.staff_id)
    
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



@router.post("/staffs/me/courses/add",  dependencies=[Depends(get_current_active_staff)])
async def add_course_to_staff(
    course_code: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_active_staff)
): 

    db_staff = staff.get_by_user_id(session=session, user_id=user.id)
    
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    db_course = course.get_by_course_code(session=session, course_code=course_code)


    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
      
    staff_link = StaffCourse(staff_id=db_staff.staff_id,course_code=db_course.course_code) 

    session.add(staff_link)
    session.commit()

    return {"message": "Course added successfully"}


@router.get("/staffs/{staff_id}", response_model=StaffRead, dependencies=[Depends(get_current_active_superuser)])
def get_staff(
    *,
    session: Session = Depends(get_session),
    staff_id: str
    ):
    db_staff = staff.get_by_id(session=session, staff_id=staff_id)
    if not db_staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )
    return db_staff


@router.get("/staff-personal-info/{staff_id}", response_model=UserRead, dependencies=[Depends(get_current_active_superuser)])
def get_student_info(staff_id: int, session: Session = Depends(get_session)):
    query = session.exec(
        select(User).join(Staff).where(Staff.staff_id == staff_id)
        )
    result = query.first()
        
    if not result:
        raise HTTPException(status_code=404, detail="Staff not found")
    return result

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



@router.get("/staffs/me/courses", response_model=List[Course], dependencies=[Depends(get_current_active_staff)])
def get_student_courses(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_active_staff)
):
    db_staff = staff.get_by_user_id(session=session, user_id=user.id)

    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    staff_courses = session.exec(
        select(Course)
        .join(StaffCourse, Course.course_code == StaffCourse.course_code)
        .where(StaffCourse.staff_id == db_staff.staff_id)
    ).all()

    return staff_courses

