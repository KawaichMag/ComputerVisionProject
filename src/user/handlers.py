from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.core.service_factory import ServiceFactory
from .service import UserService
from .schemas import UserInDB
from src.auth.service import AuthService
from src.auth.service import oauth2_scheme
router = APIRouter(prefix="/users", tags=["users"])

get_user_service = ServiceFactory.get_dependency(UserService)
get_auth_service = ServiceFactory.get_auth_dependency()

@router.get("/me", response_model=UserInDB)
async def get_me(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service)
):
    print(token)
    """Получение информации о текущем аутентифицированном пользователе"""
    current_user = await auth_service.get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=404, detail="Wrong creds")
    user = await user_service.get(current_user.id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    return user