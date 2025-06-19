from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parents[3] / ".env"
load_dotenv(env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Neon Boilerplate"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str
    API_BASE_URL: str

    class Config:
        env_file = str(env_path)
        env_file_encoding = 'utf-8'


settings = Settings() #type: ignore
