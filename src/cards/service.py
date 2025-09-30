from typing import Optional, List
import io
from fastapi import UploadFile
from src.core.utils import photo_hashed_name
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base_service import BaseService
from src.user.schemas import UserInDB
from .repository import CardRepository
from .schemas import CardCreate, CardInDB, CardBase
from .model import Card
from src.core.utils import save_photo, get_photo_file, create_zip_archive



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
        """Получение записи карточек по ID"""
        card = await self.repository.get_card(id)
        return CardInDB.model_validate(card)
    
    async def get_photo_files_zip(self, user_id: int) -> Optional[io.BytesIO]:
        """Получение ZIP архива с фотографиями для карточек пользователя"""
        cards = await self.get_user_cards(user_id)
        if not cards:
            return None
        
        photo_files = []
        for card in cards:
            file_obj = get_photo_file(card.photo_path)
            if file_obj:
                photo_files.append(file_obj)
        
        if not photo_files:
            return None
        
        # Создаем ZIP архив
        zip_buffer = create_zip_archive(photo_files)
        return zip_buffer

    async def delete(self, id: int) -> bool:
        """Удаление карточки"""
        return await self.repository.delete_card(id)

    async def _get_all(self) -> List[CardInDB]:
        """Получение всех карточек"""
        cards = await self.repository._get_all_cards()
        return [CardInDB.model_validate(card) for card in cards]

    async def get_user_cards(self, user_id: int) -> List[CardInDB]:
        """Получение карточек конкретного пользователя"""
        cards = await self.repository.get_user_cards(user_id)
        return [CardInDB.model_validate(card) for card in cards]