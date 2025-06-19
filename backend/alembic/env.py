from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
import sys
from pathlib import Path
from app.models.item import Base
from app.core.config import settings

current_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(current_dir))

database_url = settings.DATABASE_URL.replace("postgres://", "postgresql://", 1)

config = context.config
config.set_main_option("sqlalchemy.url", database_url)

fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            context.configure,
            target_metadata=target_metadata
        )
        async with connection.begin():
            await connection.run_sync(context.run_migrations)


def main():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        import asyncio
        asyncio.run(run_migrations_online())


if __name__ == "__main__":
    main()
