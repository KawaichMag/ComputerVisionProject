from typing import Optional, List
from fastapi import UploadFile
from src.core.utils import photo_hashed_name
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base_service import BaseService
from src.user.schemas import UserInDB
from .repository import CardRepository
from .schemas import CardCreate, CardInDB, CardBase
from .model import Card
from src.core.utils import save_photo



class CardService(BaseService[CardInDB, CardCreate]):
    def __init__(self, db: AsyncSession):
        self.repository = CardRepository(db)

    async def create(self, data: CardCreate) -> CardInDB:
        """Создание карточки (реализация абстрактного метода)"""
        card = await self.repository.create_card(data)
        return CardInDB.model_validate(card)

    async def create_with_photo(self, card_data: CardBase, file: UploadFile, user:UserInDB) -> CardInDB:
        """Создание карточки с фото"""
        hashed_name = photo_hashed_name(email=user.email)
        photo_path = save_photo(file, hashed_name)
        card_data_in_db = CardCreate(
            **card_data.model_dump(),
            user_id=user.id,
            photo_path=photo_path
        )
        return await self.create(card_data_in_db)

    async def get(self, id: int) -> Optional[CardInDB]:
        """Получение карточки по ID"""
        card = await self.repository.get_card(id)
        return CardInDB.model_validate(card) if card else None

    async def delete(self, id: int) -> bool:
        """Удаление карточки"""
        return await self.repository.delete_card(id)

    async def get_all(self) -> List[CardInDB]:
        """Получение всех карточек"""
        cards = await self.repository.get_all_cards()
        return [CardInDB.model_validate(card) for card in cards]

    async def get_user_cards(self, user_id: int) -> List[CardInDB]:
        """Получение карточек конкретного пользователя"""
        cards = await self.repository.get_user_cards(user_id)
        return [CardInDB.model_validate(card) for card in cards]