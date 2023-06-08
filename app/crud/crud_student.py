from fastapi import HTTPException
from sqlmodel import Session, col, select
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate, StudentUpdate
from app.crud.base import CRUDBase


class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):


    def get_by_student_id(self, *, session: Session, student_id: str) -> Student:
        return session.exec(select(Student).where(col(Student.student_id) == student_id)).first()
    
    def get_by_id(self, *, session: Session, id: int) -> Student:
        return session.exec(select(Student).where(col(Student.id) == id)).first()
    
    def get_by_user_id(self, *, session: Session, user_id: int) -> Student:
        return session.exec(select(Student).where(col(Student.user_id) == user_id)).first()


    
    def create(self, *, session: Session, obj_in: StudentCreate) -> Student:
    

        db_obj = Student(
            student_id= obj_in.student_id,
            programme= obj_in.programme,
            user_id= obj_in.user_id

        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj



    def update(self, *, session: Session, student_id: str, obj_in: StudentUpdate) -> Student:
        db_obj = session.exec(select(Student).where(col(Student.student_id) == student_id)).first()
        if db_obj: 
            obj_data = obj_in.dict(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(db_obj, key, value)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        return db_obj

    def remove(self, *, session: Session, student_id: str) -> Student:
        db_obj = session.exec(select(Student).where(col(Student.student_id) == student_id)).first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Student not found")
        session.delete(db_obj)
        session.commit()
            
        return db_obj

    



student = CRUDStudent(Student)
