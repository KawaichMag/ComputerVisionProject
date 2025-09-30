from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CardBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)


class CardCreate(CardBase):
    user_id: int
    photo_path: str

class CardInDB(CardBase):
    id: int
    created_at: datetime
    photo_path: str
    user_id: int
    
    class Config:
        from_attributes = True