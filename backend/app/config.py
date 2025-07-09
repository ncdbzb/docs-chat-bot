from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Database
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    # Secrets
    SECRET_MANAGER: str
    SECRET_JWT: str

    # SMTP
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_CELERY_DB: int

    @property
    def redis_url(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_CELERY_DB}"

    # Server
    SERVER_DOMAIN: str
    BACKEND_PORT: int

    # Admin
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    
    # Service settings
    SEND_ADMIN_NOTICES: bool = Field(default=False)
    VERIFY_AFTER_REGISTER: bool = Field(default=False)

    class Config:
        env_file = ".env"


settings = Settings()
