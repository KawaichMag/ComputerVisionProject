from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from jose import jwt, JWTError
from src.auth.utils import verify_password, create_access_token
from src.user.service import UserService
from src.auth.schemas import LoginRequest, TokenResponse
from datetime import timedelta
from typing import Optional
from src.user.schemas import UserInDB, UserCreate
from src.auth.utils import get_password_hash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class AuthService:
    """
    Сервис аутентификации пользователей.
    
    Отвечает за:
    - Аутентификацию пользователей
    - Валидацию JWT токенов
    - Регистрацию новых пользователей
    """
    def __init__(self, db: AsyncSession):
        """
        Инициализация сервиса аутентификации.
        
        Args:
            db: Асинхронная сессия SQLAlchemy
        """
        self.user_service = UserService(db=db)

    async def authenticate_user(self, login_data: LoginRequest) -> TokenResponse:
        """
        Аутентифицирует пользователя по email и паролю.
        
        Args:
            login_data: Данные для входа (email и пароль)
            
        Returns:
            TokenResponse: Объект с access токеном
            
        Raises:
            HTTPException: При неверных учетных данных
        """
        user = await self.user_service.get_user_by_email(login_data.email)
        if not user or not verify_password(login_data.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
            
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return TokenResponse(access_token=access_token)

    async def get_current_user(self, token: str) -> UserInDB:
        """
        Получает текущего пользователя по токену.
        
        Args:
            token: JWT токен аутентификации
            
        Returns:
            UserInDB: Данные пользователя
            
        Raises:
            HTTPException: При невалидном токене или отсутствии пользователя
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await self.user_service.get(int(user_id))
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def register_user(self, user_data: UserCreate) -> dict:
        """
        Регистрирует нового пользователя.
        
        Args:
            user_data: Данные для регистрации
            
        Returns:
            dict: Словарь с результатом регистрации
            
        Raises:
            HTTPException: При попытке регистрации с существующим email
        """
        # Проверяем, существует ли пользователь с таким email
        existing_user = await self.user_service.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )
            
        new_user = await self.user_service.create(UserCreate(
            email=user_data.email,
            password=get_password_hash(user_data.password),
            full_name=user_data.full_name)
            )
        
        return {
            "message": "User registered successfully",
            "user_id": new_user.id,
            "email": new_user.email
        }