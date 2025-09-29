# core/service_factory.py
from typing import Type, TypeVar, Callable
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_session import get_db
from src.user.service import UserService
from src.auth.service import AuthService

T = TypeVar('T')

class ServiceFactory:
    @staticmethod
    def create(
        service_class: Type[T],
        db: AsyncSession
    ) -> T:
        """Фабрика для создания экземпляров сервисов с инъекцией сессии"""
        return service_class(db) # typing: ignore

    @classmethod
    def get_dependency(cls, service_class: Type[T]) -> Callable[..., T]:
        """Создает dependency для FastAPI"""
        async def _get_service(db: AsyncSession = Depends(get_db)) -> T:
            return cls.create(service_class, db)
        return _get_service

    @staticmethod
    def get_user_service(db: AsyncSession) -> UserService:
        """Создает экземпляр UserService"""
        return UserService(db)

    @staticmethod
    def get_auth_service(db: AsyncSession) -> AuthService:
        """Создает экземпляр AuthService"""
        user_service = UserService(db)
        return AuthService(user_service)

    @classmethod
    def get_auth_dependency(cls) -> Callable[..., AuthService]:
        """Создает dependency для AuthService"""
        async def _get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
            return cls.get_auth_service(db)
        return _get_auth_service
