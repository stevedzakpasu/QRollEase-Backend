from sqlmodel import Session
from app.core.db import engine
from app.core.security import get_hashed_password
from app.core.settings import settings
from app.crud.crud_user import user
from app.models.user import User


def get_session():
    with Session(engine) as session:
        yield session


def create_superuser():
    with Session(engine) as session:
        super_user = user.get_by_email(
            session=session, email=settings.SUPERUSER_EMAIL)
        if not super_user:
            new_user = User(
                first_name=settings.SUPERUSER_FIRSTNAME,
                last_name=settings.SUPERUSER_LASTNAME,
                email=settings.SUPERUSER_EMAIL,
                hashed_password=get_hashed_password(
                    settings.SUPERUSER_PASSWORD),
                is_superuser=settings.SUPERUSER,
                is_verified=settings.VERIFIED
            )
            session.add(new_user)
            session.commit()


