from typing import Optional, List
from fastapi import UploadFile
from src.core.utils import photo_hashed_name
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base_service import BaseService
from .repository import CardRepository
from .schemas import CardCreate, CardInDB
from .model import Card


class CardService(BaseService[CardInDB, CardCreate]):
    def __init__(self, db: AsyncSession):
        self.repository = CardRepository(db)

    async def create_card(self, card_data: CardCreate, file: UploadFile) -> CardInDB:
        """Создание карточки с фото"""
        hashed_name = photo_hashed_name(username="")
        # TODO: здесь будет логика сохранения файла
        card = await self.repository.create_card(card_data)
        return CardInDB.model_validate(card)

    async def get_card(self, card_id: int) -> Optional[CardInDB]:
        """Получение карточки с преобразованием в схему"""
        card = await self.repository.get_card(card_id)
        return CardInDB.model_validate(card) if card else None

    async def delete(self, id: int) -> bool:
        """Удаление карточки"""
        return await self.repository.delete_card(id)

    async def get_user_cards(self, user_id: int) -> List[CardInDB]:
        """Получение всех карточек пользователя"""
        cards = await self.repository.get_user_cards(user_id)
        return [CardInDB.model_validate(card) for card in cards]