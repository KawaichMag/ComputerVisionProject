from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from fastapi import Depends
from .config import settings


# Асинхронный движок подключения к БД
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=True
)

# Асинхронная фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессий для FastAPI Depends
    Пример использования:
    async def get_user(db: AsyncSession = Depends(get_db)):
        ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_db_and_tables():
    """Создает таблицы в БД при старте приложения"""
    from src.core.base_model import Base
    from src.user.model import User
    from src.cards.model import Card
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Алиас для удобства
GetDBDependency = Depends(get_db)