from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from .model import User
from typing import List
from .schemas import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        user = User(**user_data.dict(exclude_unset=True))
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_user(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**user_data.dict(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_user(user_id)

    async def delete_user(self, user_id: int) -> bool:
        await self.db.execute(delete(User).where(User.id == user_id))
        await self.db.commit()
        return True

    async def get_all_users(self) -> list[User]:
        result = await self.db.execute(select(User))
        return list(result.scalars().all())