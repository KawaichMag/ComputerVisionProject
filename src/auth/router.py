from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from src.core.service_factory import ServiceFactory
from src.user.schemas import UserInDB
from .schemas import TokenResponse, LoginRequest
from src.user.schemas import UserCreate
from .service import AuthService
from typing import Optional
from .service import oauth2_scheme
from src.core.service_factory import ServiceFactory
from src.user.service import UserService
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(ServiceFactory.get_dependency(AuthService))
):
    return await auth_service.authenticate_user(
        LoginRequest(email=form_data.username, password=form_data.password)
    )

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(ServiceFactory.get_dependency(AuthService))
):
    """Регистрация нового пользователя"""
    return await auth_service.register_user(user_data)

@router.get("/test-auth", dependencies=[Depends(ServiceFactory.get_dependency(AuthService))])
async def test_auth():
    """Тестовый endpoint для проверки аутентификации"""
    return {"message": "Authenticated successfully"}