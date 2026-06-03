import time

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


def _async_database_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return database_url


engine = create_async_engine(
    _async_database_url(settings.database_url),
    pool_pre_ping=True,
    future=True,
)


async def check_database() -> dict:
    start_time = time.perf_counter()
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("select 1"))
            result.scalar_one()
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {"connected": True, "latency_ms": latency_ms}
    except Exception as exc:
        return {"connected": False, "error": exc.__class__.__name__}
