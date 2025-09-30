from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from src.core.service_factory import ServiceFactory
from .service import CardService
from .schemas import CardBase, CardInDB
from src.user.schemas import UserInDB
from src.auth.dependencies import get_current_user
from fastapi import Form
import os

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

@router.get("/")
async def get_user_photo_files_zip(
    user: UserInDB = Depends(get_current_user),
    service: CardService = Depends(ServiceFactory.get_dependency(CardService))
):
    """Получение ZIP архива со всеми фотографиями текущего пользователя"""
    zip_buffer = await service.get_photo_files_zip(user.id)
    
    if not zip_buffer:
        raise HTTPException(status_code=404, detail="No photos found")
    
    # Возвращаем ZIP архив как файл
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=user_photos.zip"}
    )

