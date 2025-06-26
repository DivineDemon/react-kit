from typing import Sequence

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET: str
    DATABASE_URL: str
    VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"
    JWT_ALGORITHM: str = "HS256"
    APP_NAME: str = "React Kit BE"
    CORS_ORIGINS: Sequence[str] = ["*"]
    JWT_EXPIRATION_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() # type: ignore