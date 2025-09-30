from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from .model import Card
from .schemas import CardCreate


class CardRepository:
    """Репозиторий для операций с карточками (Card) в базе данных"""
    def __init__(self, db: AsyncSession):
        """
        Инициализация репозитория карточек
        
        Args:
            db: Асинхронная сессия SQLAlchemy
        """
        self.db = db

    async def create_card(self, card_data: CardCreate) -> Card:
        """
        Создает новую карточку в базе данных
        
        Args:
            card_data: Данные для создания карточки
            
        Returns:
            Созданный объект карточки
        """
        db_card = Card(**card_data.model_dump())
        self.db.add(db_card)
        await self.db.commit()
        await self.db.refresh(db_card)
        return db_card

    async def get_card(self, card_id: int) -> Optional[Card]:
        """
        Получает карточку по идентификатору
        
        Args:
            card_id: Идентификатор карточки
            
        Returns:
            Экземпляр Card или None, если карточка не найдена
        """
        result = await self.db.execute(select(Card).where(Card.id == card_id))
        return result.scalar_one_or_none()

    async def delete_card(self, card_id: int) -> bool:
        """
        Удаляет карточку по идентификатору
        
        Args:
            card_id: Идентификатор карточки
            
        Returns:
            True если удаление успешно, False если карточка не найдена
        """
        db_card = await self.get_card(card_id)
        if not db_card:
            return False
            
        await self.db.execute(delete(Card).where(Card.id == card_id))
        await self.db.commit()
        return True

    async def update_card_photo(self, card_id: int, photo_path: str) -> Optional[Card]:
        """
        Обновляет путь к фотографии карточки
        
        Args:
            card_id: Идентификатор карточки
            photo_path: Новый путь к фотографии
            
        Returns:
            Обновленный объект Card или None, если карточка не найдена
        """
        db_card = await self.get_card(card_id)
        if not db_card:
            return None
            
        await self.db.execute(
            update(Card)
            .where(Card.id == card_id)
            .values(photo_path=photo_path)
        )
        await self.db.commit()
        await self.db.refresh(db_card)
        return db_card

    async def get_all_cards(self) -> List[Card]:
        """
        Получает все карточки без фильтрации по пользователю
        
        Returns:
            Список всех карточек
        """
        result = await self.db.execute(select(Card))
        return list(result.scalars().all())

    async def get_user_cards(self, user_id: int) -> List[Card]:
        """
        Получает карточки, принадлежащие определенному пользователю
        
        Args:
            user_id: Идентификатор пользователя
            
        Returns:
            Список карточек пользователя
        """
        result = await self.db.execute(select(Card).where(Card.user_id == user_id))
        return list(result.scalars().all())