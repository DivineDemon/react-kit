from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings #type: ignore
from app.db.session import async_session, engine #type: ignore
from app.models.item import Base, Item #type: ignore
from sqlalchemy import text
from app.routers.item_router import router as item_router #type: ignore
from app.routers.health_router import router as health_router #type: ignore

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        result = await session.execute(text("SELECT count(*) FROM items")) #type: ignore
        count = result.scalar_one()
        if count == 0:
            session.add_all([Item(name="Sample Item 1"), Item(name="Sample Item 2")])
            await session.commit()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(item_router, prefix="/items", tags=["items"])
