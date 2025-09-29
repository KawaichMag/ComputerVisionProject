from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.core.service_factory import ServiceFactory
from .service import CardService
from .schemas import CardCreate, CardInDB

router = APIRouter(prefix="/cards", tags=["cards"])

# Создаем dependency для CardService
get_card_service = ServiceFactory.get_dependency(CardService)

@router.post("/", response_model=CardInDB)
async def create_card(
    card_data: CardCreate,
    file: UploadFile = File(...),
    service: CardService = Depends(get_card_service)
):
    """Создание новой карточки"""
    return await service.create_card(card_data, file)

@router.get("/user/{user_id}", response_model=list[CardInDB])
async def get_user_cards(
    user_id: int,
    service: CardService = Depends(get_card_service)
):
    """Получение всех карточек пользователя"""
    return await service.get_user_cards(user_id)
