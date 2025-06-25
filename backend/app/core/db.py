import json
from pathlib import Path

from passlib.context import CryptContext
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.future import select

from app.core.base import Base
from app.core.config import settings
from app.core.logger import get_logger
from app.models.item import Item
from app.models.user import User

logger = get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
            conn.run_sync(lambda sync_conn: inspect(
                sync_conn).get_table_names())

    if not existing_tables:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("🛠️ Database created.")

        if seed:
            if not seed_file.exists():
                raise FileNotFoundError(f"Seed file not found: {seed_file}")

            with seed_file.open() as f:
                data = json.load(f)
            users_data = data.get("users", [])
            items_data = data.get("items", [])
            if not isinstance(users_data, list):
                raise ValueError(
                    "`users` key must be a list in seed_data.json")
            if not isinstance(items_data, list):
                raise ValueError(
                    "`items` key must be a list in seed_data.json")

            async with AsyncSessionLocal() as db:
                for user_data in users_data:
                    email = user_data.get("email")
                    result = await db.execute(select(User).where(User.email == email))
                    if result.scalar_one_or_none():
                        continue

                    hashed_password = pwd_context.hash(user_data.get("password"))

                    db.add(User(
                        id=user_data.get("id"),
                        email=email,
                        password=hashed_password,
                        first_name=user_data.get("first_name"),
                        last_name=user_data.get("last_name"),
                        profile_picture=user_data.get("profile_picture", None)
                    ))
                await db.commit()

                for item_data in items_data:
                    name = item_data.get("name")
                    result = await db.execute(select(Item).where(Item.name == name))
                    if result.scalar_one_or_none():
                        continue
                    db.add(Item(
                        name=name,
                        image_url=item_data.get("image_url", ""),
                        description=item_data.get("description", ""),
                        owner_id=item_data.get("owner_id")
                    ))
                await db.commit()
            logger.info("🌱 Seed data loaded.")
    else:
        logger.info("✅ Tables already exist; skipping create/seed.")