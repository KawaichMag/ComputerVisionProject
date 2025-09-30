from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)


class BaseService(ABC, Generic[T, CreateSchema]):
    """
    Абстрактный базовый класс для всех сервисов приложения.
    
    Определяет базовый набор операций CRUD для сущностей.
    """
    def __init__(self, db: AsyncSession):
        """
        Инициализация сервиса
        
        Args:
            db: Асинхронная сессия SQLAlchemy
        """
        self.db = db

    @abstractmethod
    async def create(self, data: CreateSchema) -> T:
        """
        Создает новую сущность.
        
        Args:
            data: Данные для создания сущности
            
        Returns:
            Созданная сущность
        """
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[T]:
        """
        Получает сущность по идентификатору.
        
        Args:
            id: Идентификатор сущности
            
        Returns:
            Сущность или None, если сущность не найдена
        """
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """
        Удаляет сущность по идентификатору.
        
        Args:
            id: Идентификатор сущности
            
        Returns:
            True если сущность удалена, False если сущность не найдена
        """
        pass

    @abstractmethod
    async def _get_all(self) -> List[T]:
        """
        Получает все сущности.
        
        Returns:
            Список всех сущностей
        """
        pass