from fastapi import APIRouter, Depends, UploadFile, File
from src.core.service_factory import ServiceFactory
from .service import CardService
from .schemas import CardBase, CardInDB
from src.user.schemas import UserInDB
from src.auth.dependencies import get_current_user
from fastapi import Form

router = APIRouter(prefix="/cards", tags=["cards"])

# Создаем dependency для CardService

@router.post("/", response_model=CardInDB)
async def create_card(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    file: UploadFile = File(...),
    user: UserInDB = Depends(get_current_user),
    service: CardService = Depends(ServiceFactory.get_dependency(CardService))
):
    """Создание новой карточки с использованием multipart/form-data"""
    card_data = CardBase(title=title, description=description, price=price)
    return await service.create_with_photo(card_data, file, user)

