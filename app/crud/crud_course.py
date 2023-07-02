from fastapi import HTTPException
from sqlmodel import Session, col, select
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate, CourseUpdate
from app.crud.base import CRUDBase


class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):


    def get_by_course_code(self, *, session: Session, course_code: str) -> Course:
        return session.exec(select(Course).where(col(Course.course_code) == course_code)).first()
    
    def get_by_id(self, *, session: Session, id: int) -> Course:
        return session.exec(select(Course).where(col(Course.id) == id)).first()  

    def get_by_course_code(self, *, session: Session, course_code: str) -> Course:
        return session.exec(select(Course).where(col(Course.course_code) == course_code)).first()    
    
    
    def get_by_staff_id(self, *, session: Session, id: int) -> Course:
        return session.exec(select(Course).where(col(Course.id) == id)).all()
    

    


    
    def create(self, *, session: Session, obj_in: CourseCreate) -> Course:
    

        db_obj = Course(
            course_code= obj_in.course_code,
            course_title = obj_in.course_title

        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj



    def update(self, *, session: Session, course_code: str, obj_in: CourseUpdate) -> Course:
        db_obj = session.exec(select(Course).where(col(Course.course_code) == course_code)).first()
        if db_obj: 
            obj_data = obj_in.dict(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(db_obj, key, value)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        return db_obj

    def remove(self, *, session: Session, course_code: str) -> Course:
        db_obj = session.exec(select(Course).where(col(Course.course_code) == course_code)).first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Course not found")
        session.delete(db_obj)
        session.commit()
            
        return db_obj

    



course = CRUDCourse(Course)
