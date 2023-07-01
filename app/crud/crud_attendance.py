from fastapi import HTTPException
from sqlmodel import Session, col, select
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceUpdate
from app.crud.base import CRUDBase


class CRUDAttendance(CRUDBase[Attendance, AttendanceCreate, AttendanceUpdate]):



    def get_by_id(self, *, session: Session, id: int) -> Attendance:
        return session.exec(select(Attendance).where(col(Attendance.id) == id)).first()
    
    def get_by_student_and_lecture_id(self, *, session: Session, student_id: str, lecture_id) -> Attendance:
        return session.exec(select(Attendance).where(Attendance.student_id == student_id and Attendance.lecture_id== lecture_id )).first()


    
    def create(self, *, session: Session, obj_in: AttendanceCreate) -> Attendance:
    

        db_obj = Attendance(
            student_id=obj_in.student_id,
            lecture_id= obj_in.lecture_id

        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj



    def update(self, *, session: Session, attendance_id: int, obj_in: AttendanceUpdate) -> Attendance:
        db_obj = session.exec(select(Attendance).where(col(Attendance.id) == attendance_id)).first()
        if db_obj: 
            obj_data = obj_in.dict(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(db_obj, key, value)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        return db_obj

    def remove(self, *, session: Session, attendance_ld: int) -> Attendance:
        db_obj = session.exec(select(Attendance).where(col(Attendance.id) == attendance_ld)).first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Attendance not found")
        session.delete(db_obj)
        session.commit()
            
        return db_obj

    



attendance = CRUDAttendance(Attendance)
