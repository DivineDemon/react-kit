from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings #type: ignore

database_url = settings.DATABASE_URL.replace(
    "postgres://", "postgresql+asyncpg://", 1
)

engine = create_async_engine(
    database_url,
    future=True,
    echo=False,
)

async_session = sessionmaker( #type: ignore
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)