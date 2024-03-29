from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.api.deps import get_current_active_superuser, get_current_active_user, get_current_verified_user
from app.core.deps import get_session
from app.crud.crud_student import student
from app.crud.crud_course import course
from app.models.course import Course
from app.models.student import Student
from app.models.studentcourse import StudentCourse
from app.schemas.student import StudentUpdate, StudentRead, StudentCreate
from app.models.user import User
from app.schemas.user import UserRead


router = APIRouter()


@router.get("/students/me", response_model=StudentRead, dependencies=[Depends(get_current_verified_user)])
def get_student_me(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_active_user)
):
    db_student = student.get_by_user_id(session=session, user_id=user.id)

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    return db_student

@router.get("/students", response_model=List[StudentRead], dependencies=[Depends(get_current_active_superuser)])
def get_students(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
    ):
    students = student.get_multiple(session=session, offset=offset, limit=limit)
    return students



@router.get("/students/{student_id}", response_model=StudentRead, dependencies=[Depends(get_current_active_superuser)])
def get_student(
    *,
    session: Session = Depends(get_session),
    student_id: str
    ):
    db_student = student.get_by_student_id(session=session, student_id=student_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return db_student

@router.get("/student-personal-info/{student_id}", response_model=UserRead, dependencies=[Depends(get_current_active_superuser)])
def get_student_info(student_id: int, session: Session = Depends(get_session)):
    query = session.exec(
        select(User).join(Student).where(Student.student_id == student_id)
        )
    result = query.first()
        
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return result

@router.post("/students", response_model=StudentRead, dependencies=[Depends(get_current_verified_user)])
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



@router.post("/students/me/courses/add",  dependencies=[Depends(get_current_active_user)])
async def add_course_to_student(
    course_code: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_active_user)
):

    db_student = student.get_by_user_id(session=session, user_id=user.id)
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_course = course.get_by_course_code(session=session, course_code=course_code)


    if not db_course:
        raise HTTPException(status_code=404, detail="Student not found")
      
    student_link = StudentCourse(student_id=db_student.student_id,course_code=db_course.course_code) 

    session.add(student_link)
    session.commit()

    return {"message": "Course added successfully"}



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


@router.get("/students/me/courses", response_model=List[Course], dependencies=[Depends(get_current_active_user)])
def get_student_courses(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_active_user)
):
    db_student = student.get_by_user_id(session=session, user_id=user.id)

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_courses = session.exec(
        select(Course)
        .join(StudentCourse, Course.course_code == StudentCourse.course_code)
        .where(StudentCourse.student_id == db_student.student_id)
    ).all()

    return student_courses


