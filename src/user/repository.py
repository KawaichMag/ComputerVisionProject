from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from .model import User
from .schemas import UserCreate, UserUpdate


class UserRepository:
    """
    Репозиторий для операций с пользователями (User) в базе данных.
    
    Обеспечивает CRUD операции для сущности User.
    """
    def __init__(self, db: AsyncSession):
        """
        Инициализация репозитория пользователей.
        
        Args:
            db: Асинхронная сессия SQLAlchemy
        """
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        """
        Создает нового пользователя.
        
        Args:
            user_data: Данные для создания пользователя
            
        Returns:
            Созданный объект пользователя
        """
        # Используем model_dump() вместо устаревшего dict()
        user = User(**user_data.model_dump(exclude_unset=True))
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Получает пользователя по email.
        
        Args:
            email: Email пользователя
            
        Returns:
            Объект User или None, если пользователь не найден
        """
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_user(self, user_id: int) -> Optional[User]:
        """
        Получает пользователя по идентификатору.
        
        Args:
            user_id: Идентификатор пользователя
            
        Returns:
            Объект User или None, если пользователь не найден
        """
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Обновляет данные пользователя.
        
        Args:
            user_id: Идентификатор пользователя
            user_data: Обновленные данные пользователя
            
        Returns:
            Обновленный объект User или None, если пользователь не найден
        """
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**user_data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_user(user_id)

    async def delete_user(self, user_id: int) -> bool:
        """
        Удаляет пользователя.
        
        Args:
            user_id: Идентификатор пользователя
            
        Returns:
            Всегда True (для сохранения обратной совместимости)
        """
        await self.db.execute(delete(User).where(User.id == user_id))
        await self.db.commit()
        return True

    async def get_all_users(self) -> List[User]:
        """
        Получает всех пользователей.
        
        Returns:
            Список всех пользователей
        """
        result = await self.db.execute(select(User))
        return list(result.scalars().all())