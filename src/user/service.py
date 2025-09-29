from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base_service import BaseService
from .repository import UserRepository
from .schemas import UserInDB, UserCreate
from .model import User

class UserService(BaseService[UserInDB, UserCreate]):
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create(self, data: UserCreate) -> UserInDB:
        """Создание пользователя с хешированием пароля"""
        user = await self.repository.create_user(data)
        return UserInDB.model_validate(user)

    async def get(self, id: int) -> Optional[UserInDB]:
        user = await self.repository.get_user(id)
        return UserInDB.model_validate(user) if user else None

    async def get_all(self) -> List[UserInDB]:
        users = await self.repository.get_all_users()
        return [UserInDB.model_validate(user) for user in users]

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        user = await self.repository.get_user_by_email(email)
        return UserInDB.model_validate(user) if user else None

    async def delete(self, id: int) -> bool:
        return await self.repository.delete_user(id)