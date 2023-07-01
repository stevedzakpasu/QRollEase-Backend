from fastapi import HTTPException
from sqlmodel import Session, col, select
from app.models.lecture import Lecture
from app.schemas.lecture import LectureCreate, LectureUpdate, LectureUpdate
from app.crud.base import CRUDBase


class CRUDLecture(CRUDBase[Lecture, LectureCreate, LectureUpdate]):


    def get_by_lecture_description(self, *, session: Session, lecture_description: str) -> Lecture:
        return session.exec(select(Lecture).where(col(Lecture.lecture_description) == lecture_description)).first()
    
    def get_by_id(self, *, session: Session, id: int) -> Lecture:
        return session.exec(select(Lecture).where(col(Lecture.id) == id)).first()
    
    def get_by_course_code(self, *, session: Session, course_code: str) -> Lecture:
        return session.exec(select(Lecture).where(col(Lecture.course_code) == course_code)).all()
    


    
    def create(self, *, session: Session, obj_in: LectureCreate) -> Lecture:
    

        db_obj = Lecture(
            course_code= obj_in.course_code,
            lecture_description = obj_in.lecture_description,

            lecture_location=obj_in.lecture_location
        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj



    def update(self, *, session: Session, lecture_id: int, obj_in: LectureUpdate) -> Lecture:
        db_obj = session.exec(select(Lecture).where(col(Lecture.id) == lecture_id)).first()
        if db_obj: 
            obj_data = obj_in.dict(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(db_obj, key, value)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        return db_obj

    def remove(self, *, session: Session, lecture_ld: int) -> Lecture:
        db_obj = session.exec(select(Lecture).where(col(Lecture.id) == lecture_ld)).first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Lecture not found")
        session.delete(db_obj)
        session.commit()
            
        return db_obj

    



lecture = CRUDLecture(Lecture)
