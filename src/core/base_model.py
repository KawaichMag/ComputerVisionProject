from datetime import datetime
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""
    
    def __init_subclass__(cls):
        """Автоматически регистрирует все подклассы в метаданных"""
        super().__init_subclass__()
        cls.metadata


class BaseModel(Base):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"
