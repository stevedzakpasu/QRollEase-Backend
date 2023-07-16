from sqlmodel import create_engine
from app.core.settings import settings


# connect_args = {"check_same_thread": False}
engine = create_engine(settings.DB_URL, echo=False)

