from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base_model import BaseModel


class Card(BaseModel):
    __tablename__ = "cards"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    photo_path: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    user: Mapped["User"] = relationship("User", back_populates="cards") # typing: ignore

    def __repr__(self) -> str:
        return f"<Card(id={self.id}, title={self.title})>"