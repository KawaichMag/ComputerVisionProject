from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)


class BaseService(ABC, Generic[T, CreateSchema]):
    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def create(self, data: CreateSchema) -> T:
        """Создание сущности"""
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[T]:
        """Получение сущности по ID"""
        pass    

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Удаление сущности"""
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        """Получение всех сущностей"""
        pass