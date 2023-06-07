from fastapi import HTTPException
from sqlmodel import Session, col, select
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate, StudentUpdate
from app.crud.base import CRUDBase


class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):


    def get_by_index_number(self, *, session: Session, index_number: str) -> Student:
        return session.exec(select(Student).where(col(Student.index_number) == index_number)).first()
    
    def get_by_id(self, *, session: Session, id: int) -> Student:
        return session.exec(select(Student).where(col(Student.id) == id)).first()
    
    def get_by_user_id(self, *, session: Session, user_id: int) -> Student:
        return session.exec(select(Student).where(col(Student.user_id) == user_id)).first()


    
    def create(self, *, session: Session, obj_in: StudentCreate) -> Student:
    

        db_obj = Student(
            index_number= obj_in.index_number,
            programme= obj_in.programme,
            user_id= obj_in.user_id

        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj



    def update(self, *, session: Session, index_number: str, obj_in: StudentUpdate) -> Student:
        db_obj = session.exec(select(Student).where(col(Student.index_number) == index_number)).first()
        if db_obj: 
            obj_data = obj_in.dict(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(db_obj, key, value)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        return db_obj

    def remove(self, *, session: Session, index_number: str) -> Student:
        db_obj = session.exec(select(Student).where(col(Student.index_number) == index_number)).first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Student not found")
        session.delete(db_obj)
        session.commit()
            
        return db_obj

    



student = CRUDStudent(Student)
