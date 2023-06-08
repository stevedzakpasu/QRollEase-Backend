from fastapi import HTTPException
from sqlmodel import Session, col, select
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate, StaffUpdate
from app.crud.base import CRUDBase


class CRUDStaff(CRUDBase[Staff, StaffCreate, StaffUpdate]):


    def get_by_staff_id(self, *, session: Session, staff_id: str) -> Staff:
        return session.exec(select(Staff).where(col(Staff.staff_id) == staff_id)).first()
    
    def get_by_id(self, *, session: Session, id: int) -> Staff:
        return session.exec(select(Staff).where(col(Staff.id) == id)).first()
    
    def get_by_user_id(self, *, session: Session, user_id: int) -> Staff:
        return session.exec(select(Staff).where(col(Staff.user_id) == user_id)).first()


    
    def create(self, *, session: Session, obj_in: StaffCreate) -> Staff:
    

        db_obj = Staff(
            staff_id= obj_in.staff_id,
            department= obj_in.department,
            user_id= obj_in.user_id

        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj



    def update(self, *, session: Session, staff_id: str, obj_in: StaffUpdate) -> Staff:
        db_obj = session.exec(select(Staff).where(col(Staff.staff_id) == staff_id)).first()
        if db_obj: 
            obj_data = obj_in.dict(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(db_obj, key, value)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        return db_obj

    def remove(self, *, session: Session, staff_id: str) -> Staff:
        db_obj = session.exec(select(Staff).where(col(Staff.staff_id) == staff_id)).first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Staff not found")
        session.delete(db_obj)
        session.commit()
            
        return db_obj

    



staff = CRUDStaff(Staff)
