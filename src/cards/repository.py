from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from .model import Card
from .schemas import CardCreate


class CardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_card(self, card_data: CardCreate) -> Card:
        db_card = Card(**card_data.model_dump())
        self.db.add(db_card)
        await self.db.commit()
        await self.db.refresh(db_card)
        return db_card

    async def get_card(self, card_id: int) -> Optional[Card]:
        result = await self.db.execute(select(Card).where(Card.id == card_id))
        return result.scalar_one_or_none()


    async def delete_card(self, card_id: int) -> bool:
        db_card = await self.get_card(card_id)
        if not db_card:
            return False
            
        await self.db.execute(delete(Card).where(Card.id == card_id))
        await self.db.commit()
        return True

    async def update_card_photo(self, card_id: int, photo_path: str) -> Optional[Card]:
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

    async def get_user_cards(self, user_id: int) -> List[Card]:
        result = await self.db.execute(select(Card).where(Card.user_id == user_id))
        return list(result.scalars().all())