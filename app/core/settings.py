import os
from pydantic import AnyHttpUrl, BaseSettings, EmailStr
from fastapi_mail import ConnectionConfig
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env
class Settings(BaseSettings):

    DB_URL: str = os.environ.get("DB_URL")
    PROJECT_NAME: str = "QRollEase API"


    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES_WEB: int = 60 * 24 * 2
    ACCESS_TOKEN_EXPIRE_MINUTES_MOBILE: int = 60 * 24 * 3000
    ALGORITHM: str = "HS256"

    SERVER_HOST = AnyHttpUrl

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = ["http://localhost:8000"]

    SUPERUSER_EMAIL: EmailStr = "qrollease@gmail.com"
    SUPERUSER_FIRSTNAME: str = "QRollEase"
    SUPERUSER_LASTNAME: str = "Admin"
    SUPERUSER_PASSWORD: str = "admin"
    SUPERUSER: bool = True
    VERIFIED: bool = True


    CONF = ConnectionConfig(
    MAIL_USERNAME = "qrollease@gmail.com",
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM = "qrollease@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="QRollEase Verification",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
    class Config:
        case_sensitive = True
        env_file = ".venv"


settings = Settings()