from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_session import get_db
from src.core.service_factory import ServiceFactory
from src.user.schemas import UserInDB
from .schemas import TokenResponse, LoginRequest
from src.user.schemas import UserCreate
from .service import AuthService
from typing import Optional
from .service import oauth2_scheme

async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Зависимость для получения AuthService"""
    return ServiceFactory.get_auth_service(db)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[UserInDB]:
    """Получение текущего пользователя по JWT токену"""
    return await auth_service.get_current_user(token)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.authenticate_user(
        LoginRequest(email=form_data.username, password=form_data.password)
    )

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Регистрация нового пользователя"""
    return await auth_service.register_user(user_data)

@router.get("/test-auth", dependencies=[Depends(get_current_user)])
async def test_auth():
    """Тестовый endpoint для проверки аутентификации"""
    return {"message": "Authenticated successfully"}