from fastapi import APIRouter, Depends
from .schemas import UserInDB, UserOut
from src.auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def get_me(
    current_user: UserInDB = Depends(get_current_user)
):
    """Получение информации о текущем аутентифицированном пользователе"""
    current_user_dict = current_user.model_dump()
    # Преобразуем UserInDB в UserOut, исключив пароль
    return UserOut(**current_user_dict)
    