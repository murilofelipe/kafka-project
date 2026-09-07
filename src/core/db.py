"""Conexão assíncrona com o banco relacional (SQLAlchemy)."""

from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

engine = create_async_engine(settings.database_url, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_models() -> None:
    """Cria as tabelas declaradas em Base.metadata (sem migrations — projeto de estudo)."""
    from src.core import models  # noqa: F401 - registra as tabelas em Base.metadata

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def ping() -> bool:
    """Testa a conectividade com o banco (usado no /health)."""
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return True


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
