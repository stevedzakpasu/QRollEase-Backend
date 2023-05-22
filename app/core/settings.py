
from pydantic import BaseSettings

class Settings(BaseSettings):

    PROJECT_NAME: str = "QRollEase API"
    DATABASE_URL: str = "sqlite:///app/database.db"
    class Config:
        case_sensitive = True
        env_file = ".venv"


settings = Settings()