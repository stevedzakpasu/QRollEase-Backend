from typing import List, TypeVar, Generic, Type
from sqlmodel import SQLModel, Session, select


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Initialize class with the model
        """
        self.model = model

    
    def get_multiple(self, *, session: Session, offset: int, limit: int) -> List[ModelType]:
        return session.exec(select(self.model).offset(offset).limit(limit)).all()