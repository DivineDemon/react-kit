import json
from pathlib import Path

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.future import select

from app.core.base import Base
from app.core.config import settings
from app.core.logger import get_logger
from app.models.item import Item

logger = get_logger(__name__)

connection_string = settings.DATABASE_URL
seed_file = Path(__file__).resolve().parent.parent / \
    "constants" / "seed_data.json"

if not connection_string:
    raise RuntimeError("DATABASE_URL is not set in the environment variables.")

engine = create_async_engine(connection_string, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def init_db(seed: bool = True):
    async with engine.connect() as conn:
        existing_tables = await \
              conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())

    if not existing_tables:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("🛠️ Database created.")

        if seed:
            if not seed_file.exists():
                raise FileNotFoundError(f"Seed file not found: {seed_file}")

            with seed_file.open() as f:
                data = json.load(f)
            items_data = data.get("items", [])
            if not isinstance(items_data, list):
                raise ValueError(
                    "`items` key must be a list in seed_data.json")

            async with AsyncSessionLocal() as db:
                for item_data in items_data:
                    name = item_data.get("name")
                    result = await db.execute(select(Item).where(Item.name == name))
                    if result.scalar_one_or_none():
                        continue
                    db.add(Item(
                        id=item_data.get("id"),
                        name=name,
                        image_url=item_data.get("image_url", ""),
                        description=item_data.get("description", "")
                    ))
                await db.commit()
            logger.info("🌱 Seed data loaded.")
    else:
        logger.info("✅ Tables already exist; skipping create/seed.")
