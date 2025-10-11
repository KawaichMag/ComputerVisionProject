from typing import Type, TypeVar, Callable, Awaitable, Protocol
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_session import get_db
from src.user.service import UserService
from src.auth.service import AuthService

class ServiceProtocol(Protocol):
    """Протокол для сервисов, которые принимают db в конструкторе"""
    def __init__(self, db: AsyncSession) -> None: ...

T = TypeVar('T', bound=ServiceProtocol)

class ServiceFactory:
    
    @staticmethod
    def create(
        service_class: Type[T],
        db: AsyncSession
    ) -> T:
        """Фабрика для создания экземпляров сервисов с инъекцией сессии"""
        return service_class(db=db)

    @classmethod
    def get_dependency(cls, service_class: Type[T]) -> Callable[..., Awaitable[T]]:
        """Создает dependency для FastAPI"""
        async def _get_service(db: AsyncSession = Depends(get_db)) -> T:
            return cls.create(service_class, db)
        return _get_service
