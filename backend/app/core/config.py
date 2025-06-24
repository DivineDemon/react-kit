from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"
    APP_NAME: str = "React Kit BE"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() # type: ignore