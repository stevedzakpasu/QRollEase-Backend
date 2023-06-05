from sqlmodel import Session, col, select
from app.crud.base import CRUDBase
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):
        def create(self, *, session: Session, obj_in: CourseCreate) -> Course:
    

            db_obj = Course(
                code=obj_in.code,
                name=obj_in.name

            )

            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

        def get_by_id(self, *, session: Session, id: int) -> Course:
            return session.exec(select(Course).where(col(Course.id) == id)).first()
        

        def update(self, *, session: Session, id: int, obj_in: CourseUpdate) -> Course:
            db_obj = session.exec(select(Course).where(col(Course.id) == id)).first()
            if db_obj: 
                obj_data = obj_in.dict(exclude_unset=True)
                for key, value in obj_data.items():
                    setattr(db_obj, key, value)
                session.add(db_obj)
                session.commit()
                session.refresh(db_obj)
            return db_obj   
        

        def remove(self, *, session: Session, id: int) -> Course:
            db_obj = session.exec(select(Course).where(col(Course.id) == id)).first()
            if not db_obj:
                raise HTTPException(status_code=404, detail="Course not found")
            session.delete(db_obj)
            session.commit()
                
            return db_obj
course = CRUDCourse(Course)