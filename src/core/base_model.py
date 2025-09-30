from datetime import datetime
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.
    
    Обеспечивает базовую функциональность и автоматическую регистрацию моделей.
    """
    
    def __init_subclass__(cls, **kwargs):
        """
        Автоматически регистрирует все подклассы в метаданных SQLAlchemy.
        
        Этот метод вызывается при создании подкласса и гарантирует,
        что все модели будут зарегистрированы в метаданных.
        """
        super().__init_subclass__(**kwargs)
        # Доступ к metadata вызывает регистрацию модели
        cls.metadata


class BaseModel(Base):
    """
    Абстрактный базовый класс для всех моделей приложения.
    
    Содержит общие поля и методы для всех моделей.
    """
    __abstract__ = True
    
    # Основные поля модели
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        doc="Время создания записи в UTC"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="Время последнего обновления записи в UTC"
    )

    def __repr__(self) -> str:
        """
        Строковое представление объекта модели.
        
        Returns:
            Строка в формате "<ИмяКласса(id=значение_id)>"
        """
        return f"<{self.__class__.__name__}(id={self.id})>"
